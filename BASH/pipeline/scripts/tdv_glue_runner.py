# This script pulls your sql files from s3, connects to Teradata Vantage, and executes the queries in each sql file.
# You must have your TDV credentials set up in AWS Secrets Manager so you can pass in the secret_name. 
# You are free to modify this script for your own use cases or keep as is.

import time
import boto3
import sys
from awsglue.utils import getResolvedOptions
import teradatasql
import logging
import json


logger = logging.getLogger(__name__)

class TdvGlueRunner:
    def __init__(self, host, secret_name,  logmech="LDAP"):
        self.host = host
        self.tdv_secret = secret_name
        self.logmech = logmech


    def get_secret(self):
        """
        Input @param: tdv environment, secret_name, logger-type-variable
        Get the teradata vantage credential information from secret manager
        @return: TDV username/password from AWS-Secrets-Manager
        """
       
        logger.info(self.tdv_secret)
        client = boto3.client("secretsmanager", region_name="us-east-1", verify=False)
        try:
            get_secret_value_response = client.get_secret_value(SecretId=self.tdv_secret)
        except Exception as e:
            logger.error(f"Failed with exception {e}")
            raise e

        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = json.loads(get_secret_value_response['SecretString'])
            logger.info("Got the secret manager password")
            return secret['username'], secret['password']
        else:
            logger.info(f"Error retrieving secret from AWS-Secrets-Manager")
            return '', ''

    def read_file_s3(self, bucket, key):
        """
        Connects to s3, retrieves file and extracts the sql from the file.
        """
        s3 = boto3.client('s3', region_name='us-east-1')
        logger.info(f"Retriveing sql query from s3 bucket {bucket} {key}")
        response = s3.get_object(Bucket=bucket, Key=key)
        response_body = response['Body'].read().decode('utf-8')
        return response_body

    def replace_sql_params(self, sql_query, sql_params):
        """Passes the given params into the SQL queries where necessary and returns the query."""
        for key,val in sql_params.items():
            sql_query = sql_query.replace(key, val)
        return sql_query

    def execute_sql_files(self, sql_files, bucket, sql_params={}):
        """Connects to TDV and executes each sql query from the specified s3 bucket."""
        username,password= self.get_secret()
        print("__sqlfiles", self.host, self.logmech)
        with teradatasql.connect(host=self.host,  user=username, 
        password=password, LOGMECH=self.logmech, encryptdata="true") as conn:
            for sql in sql_files.split(","):
                sql_queries = self.read_file_s3(bucket, sql)
                for sql_query in sql_queries.split(";"):
                    if not sql_query:
                        continue
                    sql_query = self.replace_sql_params(sql_query, sql_params)
                    tdcursor = conn.cursor()
                    logger.info(f"Executing {sql_query}")
                    tdcursor.execute(sql_query)


if __name__ == "__main__":
    command_line_options = ['s3_bucket', # The name of the bucket containing the sql files
                            's3_sql_files', # String of all sql file names to be read separated by commas, i.e. "tdv-oss-demo/dml/project1/1.sql,tdv-oss-demo/dml/project1/2.sql"
                            'host', # TDV Hostname 
                            'secret_name', # Name of secret stored in AWS Secrets Manager that contains the TDV user/password creds
                            'logmech', # i.e. "LDAP"
                            'sql_params' # Variables to use in SQL queries, i.e. {'database': 'HSETL_WORK_DEV2'}
                            ]
    args = getResolvedOptions(sys.argv, command_line_options)
    s3_bucket = args["s3_bucket"]
    s3_sql_files = args["s3_sql_files"]
    host = args["host"]
    secret_name = args["secret_name"]
    logmech = args["logmech"]
    sql_params = json.loads(args["sql_params"])
    tdv = TdvGlueRunner(host, secret_name,  logmech=logmech)
    tdv.execute_sql_files(s3_sql_files, s3_bucket, sql_params)
    
