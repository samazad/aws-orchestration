import boto3


class ClientLocator:
    def __init__(self, client):
        session = boto3.session.Session(profile_name='sazad', region_name='us-east-1')
        self._client = session.client(client)

    def get_client(self):
        return self._client


class EC2Client(ClientLocator):
    def __init__(self):
        super().__init__('ec2')
