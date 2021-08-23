import boto3
import os

AWS_ACCESS_KEY_ID=os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY=os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_SESSION_TOKEN=os.getenv('AWS_SESSION_TOKEN')

def get_parameters(account, region, customer, environment, next_token=None):
    ssm_client = boto3.session.Session(profile_name=account, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, aws_session_token=AWS_SESSION_TOKEN).client('ssm', region_name=region)

    if(next_token):
        parameters = ssm_client.get_parameters_by_path(
            Path=f"/customers/{customer}/{environment}/",
            Recursive=True,
            WithDecryption=True,
            NextToken=next_token)
    else:
        parameters = ssm_client.get_parameters_by_path(
            Path=f"/customers/{customer}/{environment}/",
            Recursive=True,
            WithDecryption=True)
    
    credentials = {}
    for p in parameters['Parameters']:
        credentials[p['Name'].replace(f"/customers/{customer}/{environment}/", "")] = p['Value']

    # Get the next page of results
    if('NextToken' in parameters):
        credentials.update(get_parameters(account, region, customer, environment, parameters['NextToken']))

    return credentials