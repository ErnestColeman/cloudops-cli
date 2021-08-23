import os

# class AwsCredentials:
#     def __init__(self, id: str, key: str, token: str):
#         self.AWS_ACCESS_KEY_ID = id
#         self.AWS_SECRET_ACCESS_KEY = key
#         self.AWS_SESSION_TOKEN = token

def validate_aws_credentials(AWS_SESSION_TOKEN, AWS_SECRET_ACCESS_KEY,AWS_ACCESS_KEY_ID):
    """
    Programmatic Access
    Check if the User provided AWS credentials.
    If not, checks if the environment variables are set.
    If not, raises exception to input credentials.

    """
    if not AWS_SESSION_TOKEN:
        if os.getenv('AWS_SESSION_TOKEN'):
            AWS_SESSION_TOKEN = os.getenv('AWS_SESSION_TOKEN')
        else:
            raise ValueError("You did not enter an AWS_SESSION_TOKEN and there is not environment variable set. Please enter it when running this program or set the environment variable manually")
    if not AWS_SECRET_ACCESS_KEY:
        if os.getenv('AWS_SECRET_ACCESS_KEY'):
            AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
        else:
            raise ValueError("You did not enter an AWS_SECRET_ACCESS_KEY and there is not environment variable set. Please enter it when running this program or set the environment variable manually")
    if not AWS_ACCESS_KEY_ID:
        if os.getenv('AWS_ACCESS_KEY_ID'):
            AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
        else:
            raise ValueError("You did not enter an AWS_ACCESS_KEY_ID and there is not environment variable set. Please enter it when running this program or set the environment variable manually")

def set_environment_variables(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN, **kwargs):
    """
    Setting environment variables
    from the credentials that the User has passed
    to the program.

    """
    os.environ['AWS_ACCESS_KEY_ID'] = AWS_ACCESS_KEY_ID
    os.environ['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY
    os.environ['AWS_SESSION_TOKEN'] = AWS_SESSION_TOKEN
    print(AWS_ACCESS_KEY_ID)
    print(AWS_SECRET_ACCESS_KEY)
    print(AWS_SESSION_TOKEN)

def delete_environment_variables(AWS_SESSION_TOKEN, AWS_SECRET_ACCESS_KEY,AWS_ACCESS_KEY_ID):
    """
    Not needed.
    The environment variables set above will only be available
    for child processes that spawned from this script.
    
    """
    del os.environ["AWS_ACCESS_KEY_ID"]
    del os.environ['AWS_SECRET_ACCESS_KEY']
    del os.environ['AWS_SESSION_TOKEN']