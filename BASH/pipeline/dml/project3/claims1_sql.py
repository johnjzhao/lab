import teradatasql
import boto3
import logging
import json

logger = logging.getLogger(__name__)

def get_secret(secret):
        """
        Input @param: tdv environment, secret_name, logger-type-variable
        Get the teradata vantage credential information from secret manager
        @return: TDV username/password from AWS-Secrets-Manager
        """
       
        print(secret)
        client = boto3.client("secretsmanager", region_name="us-east-1", verify=False)
        try:
            get_secret_value_response = client.get_secret_value(SecretId=secret)
        except Exception as e:
            logger.error(f"Failed with exception {e}")
            raise e

        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = json.loads(get_secret_value_response['SecretString'])
            print("Got the secret manager password")
            return secret['username'], secret['password']
        else:
            print(f"Error retrieving secret from AWS-Secrets-Manager")
            return '', ''

def replace_sql_params(sql_query, sql_params):
        """Passes the given params into the SQL queries where necessary and returns the query."""
        for key,val in sql_params.items():
            sql_query = sql_query.replace(key, val)
        return sql_query

def execute_query(query, host, secret_name, logmech, sql_params={}):
        """Connects to TDV and executes each sql query from the specified s3 bucket."""
        username,password= get_secret(secret_name)
        print("__host", host, logmech)
        with teradatasql.connect(host=host,  user=username, 
        password=password, LOGMECH=logmech, encryptdata="true") as conn:     
            sql_query = replace_sql_params(query, sql_params)
            tdcursor = conn.cursor()
            print(f"Executing {sql_query}")
            tdcursor.execute(sql_query)

def main(host, secret_name, logmech, sql_params):
    sql1 = "SELECT * FROM <database>.LANG_DIM_T13 ldt"
    sql2 = "SELECT * FROM <database>.LANG_DIM_T13 ldt "
    execute_query(sql1, host, secret_name, logmech, sql_params)
    execute_query(sql2, host, secret_name, logmech, sql_params)
    

