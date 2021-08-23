import datetime
#import sys
import time
import boto3
import os
from util.ssm import get_parameters
from util.sqlserver import get_connection, execute_sql

def get_rds_task_status(conn, task_id):
    return execute_sql(conn, 'exec msdb.dbo.rds_task_status @task_id=?', task_id)[0]

def backup_epas_db(conn, db_name, s3_path):
    sql = """exec msdb.dbo.rds_backup_database 
        @source_db_name=?,
        @s3_arn_to_backup_to=?,
        @overwrite_S3_backup_file=0,
        @type='FULL';"""
    task_id = execute_sql(conn, sql, db_name, s3_path)[0]['task_id']
    
    status = get_rds_task_status(conn, task_id)
    while(status['lifecycle'] in ['CREATED', 'IN_PROGRESS']):
        time.sleep(5)
        status = get_rds_task_status(conn, task_id)
    
    if(status['lifecycle'] != 'SUCCESS'):
        raise Exception(status['task_info'])

def backup_epas(account, region, customer, environment, **kwargs):
    #Import AWS Exported Credentials
    AWS_ACCESS_KEY_ID=os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY=os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_SESSION_TOKEN=os.getenv('AWS_SESSION_TOKEN')

    #Updated Authentication
    s3_client = boto3.session.Session(profile_name=account, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, aws_session_token=AWS_SESSION_TOKEN).client('s3')

    current_datetime = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    s3_bucket = f"pg-saas-operations-{region}"
    # We have to remove the colon characters so that the ARN will be properly formed
    s3_object_key = f"sql-server/{customer}-{environment}-epas_{current_datetime}.bak".replace(':', '')

    credentials = get_parameters(account, region, customer, environment)

    with get_connection(credentials['epas/db_host'], credentials['epas/db_admin_username'], credentials['epas/db_admin_password']) as conn:
        backup_epas_db(conn, credentials['epas/db_name'], f"arn:aws:s3:::{s3_bucket}/{s3_object_key}")

    # By default, the object will be owned by the account that created it (development, staging, production)
    # The bucket is owned by the Operations account, and we want Operations to have full control over the object
    s3_client.put_object_acl(
        ACL = 'bucket-owner-full-control',
        Bucket = s3_bucket,
        Key = s3_object_key)

    print(s3_client.generate_presigned_url('get_object',
        Params={'Bucket': s3_bucket,
                'Key': s3_object_key},
        ExpiresIn=3600))



