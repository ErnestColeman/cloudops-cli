#!/usr/bin/env python
import argparse
from todo.auth import set_environment_variables, validate_aws_credentials, delete_environment_variables
from download_releases import download_releases
from update_deployment import update_deployment
from backup_epas_db import backup_epas

######################## ARGPARSE SECTION BEGIN #####################
parser = argparse.ArgumentParser(
    description="CLI tool to make it easy for Cloudops team to resolve issues and deploy new features")
subparser = parser.add_subparsers(dest="action")

######################## CLOUDOPS ARGUMENTS ######################
auth_parser = subparser.add_parser('auth', help="Authenticate to AWS account")
auth_parser.add_argument('-i', '--AWS_ACCESS_KEY_ID', required=True, help='AWS_ACCESS_KEY_ID')
auth_parser.add_argument('-k', '--AWS_SECRET_ACCESS_KEY', required=True, help='AWS_ACCESS_KEY')
auth_parser.add_argument('-t', '--AWS_SESSION_TOKEN', required=True, help='AWS_ACCESS_TOKEN')
auth_parser.set_defaults(func=set_environment_variables)

######################## UPDATE ARGUMENTS #####################
update_parser = subparser.add_parser('update', help='To update deployments.')
update_parser.add_argument('-r', '--release',  nargs= '+', help='Takes multiple arguments for releases. Example: janus:release-4.8.9.0-1 epas-connector:release-4.12.3.3-2 ')
update_parser.add_argument('-n', '--namespace', required=True, type=str, help='Provide the namespace to connect to.')
update_parser.add_argument('-d', '--deployment', nargs= '+', required=True, type=str, help='Takes multiple arguments for  deployments to edit. Example: janus epas-connector')
update_parser.set_defaults(func=update_deployment)

######################## DOWNLOAD ARGUMENTS #####################
download_parser = subparser.add_parser('download', help='Downloads releases needed')
download_parser.add_argument('-r', '--releases', nargs='+', required=True, help='Takes multiple arguments for downloading releases. Example: janus:release-4.8.9.0-1 epas-connector:release-4.12.3.3-2')
download_parser.set_defaults(func=download_releases)
args = parser.parse_args()

######################## BACKUP ARGUMENTS #####################
backup_parser =  subparser.add_parser('backup', help='Backup epas database. Example: main.py backup staging us-east-1 oneok development')
backup_parser.add_argument('-a', '--account', help='Choose an AWS account. eg: "staging", "production", or "development"')
backup_parser.add_argument('-r', '--region', help='Choose an AWS region. eg: "us-east-1", "us-east-2", "us-west-1", or "us-west-2" ')
backup_parser.add_argument('-c', '--customer', help='Choose a customer. eg: "oneok", "phillips66", or "merck".')
backup_parser.add_argument('-e', '--environment', help='Choose an AWS environment. eg: "staging", "production", or "development"'))
backup_parser.set_defaults(func=backup_epas)

# print(args.func)
args.func(**vars(args))
######################## ARGPARSE SECTION END #######################
