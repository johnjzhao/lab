# This script pulls your python files from s3 and trigger your python script.
# You must have your main() function in your python script. 
# You are free to modify this script for your own use cases or keep as is.

import time
import boto3
import sys
from awsglue.utils import getResolvedOptions
import teradatasql
import logging
import json
import importlib

logger = logging.getLogger(__name__)

# To execute a script, add the filename to this list 
priv_files = ['example_script.py', 'example_script2.py']

if __name__ == "__main__":
    command_line_options = [
                            'py_file_name', # python file name to import and execute 
                            'host', # TDV Hostname 
                            'secret_name', # Name of secret stored in AWS Secrets Manager that contains the TDV user/password creds
                            'logmech', # i.e. "LDAP"
                            'sql_params' # Variables to use in SQL queries, i.e. {'database': 'HSETL_WORK_DEV2'}
                            ]


    
    args = getResolvedOptions(sys.argv, command_line_options)
    py_file_name = args["py_file_name"]
    host = args["host"]
    secret_name = args["secret_name"]
    logmech = args["logmech"]
    sql_params = json.loads(args["sql_params"])
    if py_file_name in priv_files:
        idx = priv_files.index(py_file_name) # get index in list of privileged files
        file_to_run = priv_files[idx] # get name of desired file
        i = importlib.import_module(file_to_run)
        i.main(host, secret_name, logmech, sql_params)


    
