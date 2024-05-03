import os
import io
import glob
import configparser
import difflib
import boto3
import sys, logging
import json
import teradatasql
from datetime import datetime
from awsglue.utils import getResolvedOptions
import numpy as np
import pandas as pd
from connector import TdvConnector
from logger import ScriptLogger
import site
import time
import importlib
from setuptools.command import easy_install
import subprocess
from io import StringIO, BytesIO
import shutil
from pyarrow import *
import psycopg2

ACTION = "dataload-from-s3-to-TDV"
logger = ScriptLogger("s3_to_tdv_data_load").get_logger(action = ACTION)
pd.set_option('display.max_rows', 1000, 'display.max_columns', 200, 'display.max_colwidth', 100)
TDV_CONN_WAIT_TIMES = [2**i for i in range(5, 9)]

#############################
#                           #
#                           #
#############################

args = getResolvedOptions(sys.argv, ['region_name', 'host', 'artifacts_bucket', 'tdv_env', 'sqlfile', 'artifacts_bucket_key', 'username', 'tdv_secretsmanager'])
print("Retrieval of data required for connection string")

region_name = args['region_name']
tdv_user = args['username']
tdv_secretsmanager = args['tdv_secretsmanager']
#tdv_pass = ssm_client.get_parameter(Name=tdv_secrets, WithDecryption=True) ['Parameter']['Value']
tdv_host = args['host']
oss_env = args['tdv_env']
sql = args['sqlfile']
s3_bucket = args['artifacts_bucket']
artifacts_bucket_key = args['artifacts_bucket_key']
sql_props_location = artifacts_bucket_key + '/sql'
logger.info("tdv host: %s" % tdv_host)
logger.info("s3_bucket: %s" % s3_bucket)
logger.info("artifacts_bucket_key: %s" % artifacts_bucket_key)
logger.info("OSS env: %s" % oss_env)

#######################

props_filename = "csb_prodt"
props_fileloc = sql_props_location + '/tdv_extracts/' + props_filename +'.properties'

#######################

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install("jproperties")
#install("sqlalchemy")
install("teradatasqlalchemy")
install("sqlalchemy-teradata")

import sqlalchemy_teradata
import sqlalchemy
from sqlalchemy import *
import teradatasqlalchemy
from jproperties import Properties
#from teradatasqlalchemy.types import *
#from teradataml.dataframe.fastload import fastload

#######################
props = Properties()
s3_client = boto3.client('s3')
#
# secret_name = "gov-solutions-commissions-tdv-secret-dev"
# secret_arn="arn:aws:secretsmanager:us-east-1:215132885729:secret:gov-solutions-commissions-tdv-secret-dev-Nvdsnw"
# region_name = "us-east-1"
#
# secret_client = boto3.client('secretsmanager')
# tdv_pass = secret_client.get_secret_value(SecretId=secret_arn).get('SecretString')

#test_tdv_conn = teradatasql.connect(host=tdv_host, user=tdv_user, password=tdv_pass, logmech='LDAP') #host= 'teradatasql://'+tdv_host+':1025'
#tdv_engine = sqlalchemy.create_engine('teradatasql://'+tdv_host+':1025/?user='+tdv_user+'&password='+tdv_pass+'/'+'?authentication=LDAP')
session = boto3.session.Session()
client = session.client(service_name="secretsmanager", region_name="us-east-1")
get_secret_value_response = client.get_secret_value(SecretId="gov-solutions-commissions-tdv-secret-dev")
secret = get_secret_value_response['SecretString']

engine_str = f'teradatasql://{tdv_user}:{secret}@{tdv_host}:22/'

tdv_engine = sqlalchemy.create_engine(engine_str)

#print (f'tdv_engine --> {tdv_engine}')

#############################
#                           #
#                           #
#############################

response = s3_client.get_object(Bucket=s3_bucket, Key=props_fileloc)
sql_str_body = response['Body'].read()
sql_str = io.BytesIO(sql_str_body)
props_file = 'input.properties'

#############################
#                           #
#                           #
#############################
with open(props_file, mode='wb') as f:
    sql_str.seek(0)
    shutil.copyfileobj(sql_str, f)
    #print(sql_str.getvalue(), file=f)

#############################
#                           #
#                           #
#############################   
with open(props_file, 'rb') as f:
    props.load(f)

read_path = props.get("s3_read_path").data
logger.info(f"s3_read_path: {read_path}")

tdv_write_tablename = props.get("tdv_write_tablename").data
logger.info(f"TDV Table Name: {tdv_write_tablename}")
        
#############################
#                           #
#                           #
#############################
def initialize_connection():
    session = boto3.session.Session()
    logger.info("Client session established")
    tdvconn_obj = TdvConnector(tdv_host, tdv_user, region_name, session, logger, tdv_secretsmanager)
    logger.info("TDV connector object instantiated")

    return tdvconn_obj.connect()

#############################
#                           #
#                           #
#############################
def retry_connection():
    tdv_conn = None

    for delay in TDV_CONN_WAIT_TIMES:
        try:
            logger.info(f"Waiting for {delay} seconds before attempting another connection")
            time.sleep(delay)
            tdv_conn = initialize_connection()
        except Exception as error:
            logger.error(f"Error in TDV connection retry: {error}")
        else:
            break

    return tdv_conn

#############################
#                           #
#                           #
#############################
def get_connection():

    tdv_conn = None
    try:
        tdv_conn = initialize_connection()
    except Exception as error:
        logger.error(f"Error in TDV connection: {error}. Retrying connection...")
        tdv_conn = retry_connection()
    if tdv_conn is None:
        raise Exception("TDV connection not established")
    return tdv_conn

#############################
#                           #
#                           #
#############################
def read_csv_from_s3(read_path):
    """ Write a dataframe to a CSV on S3 """
    readDF = pd.read_csv(read_path, engine='pyarrow')
    logger.info("Count of records from dataframe --> {}".format(len(readDF)))
    return readDF


#############################
#                           #
#                           #
#############################    
# def drop_table(vt_table_name):
#     try:
#         db_drop_table(f"{vt_table_name}")
#         logger.info(f"{table_name} has been dropped")
#     except:
#         logger.info(f"Not able to drop the Volatile Table -> {vt_table_name}")

#############################
#                           #
#                           #
#############################
def writeDataToTDV(inputDF, tablename):
    try:
        writeDF = pd.DataFrame(inputDF)
        print("Start writing to TDV Table")
        writeDF.to_sql(name='TRXHUB_CORE_INT_T.CSB_PRODT', con = tdv_engine, if_exists='append')
    except Exception as error:
        logger.exception("Error in writeDataToTDV")
        raise error

#############################
#                           #
#                           #
#############################
def dataLoadFromS3ToTDV():
    try:
        logger.info("Read from S3:")
        inputDF = read_csv_from_s3(read_path)
        
        logger.info("Write To TDV Table:")
        writeDataToTDV(inputDF, tdv_write_tablename)
    except Exception as error:
        logger.exception("Error in dataLoadFromS3ToTDV")
        raise error

#############################
#                           #
#                           #
#############################    
def main():
    logger.info("Main execution ...")
    dataLoadFromS3ToTDV()   

if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        raise err