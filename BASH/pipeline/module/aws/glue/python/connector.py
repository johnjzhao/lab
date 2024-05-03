import teradatasql
import sys, logging
import boto3
import base64
from botocore.exceptions import ClientError

class TdvConnector(object):
    def __init__(self, host, user, region_name, session, logger, tdv_secretsmanager=None):
        self.class_name = __name__
        self.conn = None
        self.host = host
        self.user = user
        self.region_name = region_name
        self.tdv_secretsmanager = tdv_secretsmanager
        self.session = session
        self.logger = logger

    def connect(self):
        """
        Connect to tdv
        """
        secretsmanager_client = self.session.client(
            service_name = 'secretsmanager',
            region_name = self.region_name
        )
        self.logger.info("SM client instantiated")
        try:
            get_secret_value_response = secretsmanager_client.get_secret_value(
                SecretId=self.tdv_secretsmanager
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'DecryptionFailureException':
                # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'InternalServiceErrorException':
                # An error occurred on the server side.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                # You provided an invalid value for a parameter.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                # You provided a parameter value that is not valid for the current state of the resource.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'ResourceNotFoundException':
                # We can't find the resource that you asked for.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
        else:
            # Decrypts secret using the associated KMS key.
            # Depending on whether the secret is a string or binary, one of these fields will be populated.
            if 'SecretString' in get_secret_value_response:
                tdv_pass = get_secret_value_response['SecretString']
            else:
                decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])

        self.logger.info(f"Host: {self.host}, User: {self.user}")
        self.logger.info("Connecting to TDV")
        try:
            conn = teradatasql.connect(host=self.host, user=self.user, password=tdv_pass,logmech="LDAP",encryptdata="true")
            self.logger.info("Connection established")
            return conn
        except Exception as error:
            self.logger.error("Error in TDV connection")
            raise error
