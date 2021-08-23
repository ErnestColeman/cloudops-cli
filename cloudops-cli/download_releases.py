import base64
import boto3
import subprocess
import sys
import os

def download_releases(releases, **kwargs):
    # We use the Operations AWS account for ECR registries
    AWS_PROFILE="operations"

    #  Make sure to export OPERATIONS Creds from AWS
    AWS_ACCESS_KEY_ID=os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY=os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_SESSION_TOKEN=os.getenv('AWS_SESSION_TOKEN')
    # Get a token to authenticate to our ECR registry
    ecr_client = boto3.session.Session(aws_access_key_id = AWS_ACCESS_KEY_ID, aws_secret_access_key = AWS_SECRET_ACCESS_KEY, aws_session_token = AWS_SESSION_TOKEN, profile_name = AWS_PROFILE).client('ecr')
    auth_token_response = ecr_client.get_authorization_token()
    ecr_credentials = base64.b64decode(auth_token_response['authorizationData'][0]['authorizationToken'])
    ecr_endpoint = auth_token_response['authorizationData'][0]['proxyEndpoint'].replace("https://", "")
    for r in releases:
        r = f"docker-repo.prometheusgroup.com/{r}"
        image_and_tag = r[r.find("/") + 1:]
        skopeo_response = subprocess.run([
            'skopeo', 'copy',
            '--dest-creds', ecr_credentials,
            f"docker://{r}",
            f"docker://{ecr_endpoint}/{image_and_tag}"
        ])
        # Don't use "checked=True" with the run function above, it'll spit out the access token in the output
        if skopeo_response.returncode > 0:
            raise Exception("Skopeo returned an error")
