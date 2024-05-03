from distutils.debug import DEBUG
import os
import io
import glob
import configparser
import difflib
import boto3
import sys
import logging
import teradatasql
from datetime import datetime
from awsglue.utils import getResolvedOptions
#from watchtower import CloudWatchLogHandler
#from glue_utilities import GlueUtilities
import time
import numpy as np
import pandas as pd
from connector import TdvConnector
from logger import ScriptLogger
import site
import importlib
import time
from setuptools.command import easy_install
import subprocess
from io import StringIO, BytesIO
import shutil
from logger import ScriptLogger
install_path = os.environ['GLUE_INSTALLATION']
from pyarrow import *
ACTION = "extract"

logger = ScriptLogger("tdv_to_s3_extract_broker_commissions_sircon_pshell").get_logger(action = ACTION)
pd.set_option('display.max_rows', 1000, 'display.max_columns', 200, 'display.max_colwidth', 100)
TDV_CONN_WAIT_TIMES = [2**i for i in range(5, 9)]

#############################
#                           #
#                           #
#############################

args = getResolvedOptions(sys.argv, ['region_name',
                                     'host',
                                     'artifacts_bucket',
                                     'tdv_env',
                                     'sqlfile',
                                     'artifacts_bucket_key',
                                     'username',
                                     'tdv_secretsmanager',
                                     'schema_trxhub',
                                     'schema_sales_commission',
                                     'schema_datamart_reftable'
                                     ])

print("Retrieval of data required for connection string")

schema_datamart_reftable = args['schema_datamart_reftable']
schema_sales_commission = args['schema_sales_commission']
schema_trxhub = args['schema_trxhub']
region_name = args['region_name']
tdv_user = args['username']
tdv_secretsmanager = args['tdv_secretsmanager']
# tdv_pass = ssm_client.get_parameter(Name=tdv_secrets, WithDecryption=True) ['Parameter']['Value']
tdv_host = args['host']
oss_env = args['tdv_env']
sql = args['sqlfile']
s3_bucket = args['artifacts_bucket']
artifacts_bucket_key = args['artifacts_bucket_key']
sql_location = artifacts_bucket_key + '/sql/' + sql
logger.info("tdv host: %s" % tdv_host)
logger.info("s3_bucket: %s" % s3_bucket)
logger.info("artifacts_bucket_key: %s" % artifacts_bucket_key)
logger.info("OSS env: %s" % oss_env)

#######################

sql_props_location = artifacts_bucket_key + '/sql'
print("s3_bucket", s3_bucket)
print("artifacts_bucket_key", artifacts_bucket_key)
print("OSS env", oss_env)

broker_hier_sircon_fileloc = sql_props_location + '/tdv_extracts/broker_hier_sircon_sql.properties'


#######################

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install("jproperties")


from jproperties import Properties

#######################
props = Properties()
s3_client = boto3.client('s3')

#######################
response = s3_client.get_object(Bucket=s3_bucket, Key=broker_hier_sircon_fileloc)
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

#############################
#                           #
#                           #
#############################   
with open(props_file, 'rb') as f:
    props.load(f)

q_CREATE_VT_BROKER_HIER = props.get("q_CREATE_VT_BROKER_HIER").data.format(TRXHUB_CORE=schema_trxhub)
print(f"q_CREATE_VT_BROKER_HIER: {q_CREATE_VT_BROKER_HIER}")
q_COLLECT_STATS_VT_BROKER_HIER = props.get("q_COLLECT_STATS_VT_BROKER_HIER").data

q_CREATE_VT_BROKER_DEMG = props.get("q_CREATE_VT_BROKER_DEMG").data.format(TRXHUB_CORE=schema_trxhub)
print(f"q_CREATE_VT_BROKER_DEMG: {q_CREATE_VT_BROKER_DEMG}")
q_COLLECT_STATS_VT_BROKER_DEMG = props.get("q_COLLECT_STATS_VT_BROKER_DEMG").data

q_CREATE_VT_BROKER_FULL_HD = props.get("q_CREATE_VT_BROKER_FULL_HD").data
q_COLLECT_STATS_VT_BROKER_FULL_HD = props.get("q_COLLECT_STATS_VT_BROKER_FULL_HD").data

q_CREATE_VT_BROKER_NEW_CDO = props.get("q_CREATE_VT_BROKER_NEW_CDO").data
q_CREATE_VT_BROKER_NEW_CDO = q_CREATE_VT_BROKER_NEW_CDO.format(SALES_COMMISSION_CORE=schema_sales_commission, DATAMART_REFTABLE=schema_datamart_reftable)
print(f"q_CREATE_VT_BROKER_NEW_CDO: {q_CREATE_VT_BROKER_NEW_CDO}")
q_COLLECT_STATS_VT_BROKER_NEW_CDO = props.get("q_COLLECT_STATS_VT_BROKER_NEW_CDO").data

q_CREATE_VT_BROKER_NEW_CDO_FINAL = props.get("q_CREATE_VT_BROKER_NEW_CDO_FINAL").data
print(f"q_CREATE_VT_BROKER_NEW_CDO_FINAL: {q_CREATE_VT_BROKER_NEW_CDO_FINAL}")
q_COLLECT_STATS_VT_BROKER_NEW_CDO_FINAL = props.get("q_COLLECT_STATS_VT_BROKER_NEW_CDO_FINAL").data

q_SELECT_BROKER_HIER_DEMG = props.get("q_SELECT_BROKER_HIER_DEMG").data

write_path = props.get("s3_writePath").data
print(f"s3_write_path: {write_path}")

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
def write_dataframe_to_parquet_on_s3(dataframe, filepath):
    """ Write a dataframe to a Parquet on S3 """
    logger.info("Writing {} records to {}".format(len(dataframe), filepath))
    dataframe.to_parquet(filepath)


#############################
#                           #
#                           #
#############################    
def drop_table(vt_table_name):
    try:
        db_drop_table(f"{vt_table_name}")
        logger.info(f"{table_name} has been dropped")
    except:
        logger.info(f"Not able to drop the Volatile Table -> {vt_table_name}")

#############################
#                           #
#                           #
#############################
def executeStmtOnTDV():
    conn = get_connection()
    cur = conn.cursor()
    try:
        ##################   start cretaing volatile table    ######################
        logger.info("##################   start cretaing volatile table    ###################### \n")
        
        logger.info("Creating Volatile Table and Collect Stats for --> VT_BROKER_HIER")
        cur.execute(q_CREATE_VT_BROKER_HIER)
        cur.execute(q_COLLECT_STATS_VT_BROKER_HIER)
        
        logger.info("Creating Volatile Table and Collect Stats for --> VT_BROKER_DEMG")
        cur.execute(q_CREATE_VT_BROKER_DEMG)
        cur.execute(q_COLLECT_STATS_VT_BROKER_DEMG)
        
        logger.info("Creating Volatile Table and Collect Stats for --> VT_BROKER_FULL_HD")
        cur.execute(q_CREATE_VT_BROKER_FULL_HD)
        cur.execute(q_COLLECT_STATS_VT_BROKER_FULL_HD)
        
        logger.info("Creating Volatile Table and Collect Stats for --> VT_BROKER_NEW_CDO")
        cur.execute(q_CREATE_VT_BROKER_NEW_CDO)
        cur.execute(q_COLLECT_STATS_VT_BROKER_NEW_CDO)
        
        logger.info("Creating Volatile Table and Collect Stats for --> VT_BROKER_NEW_CDO_FINAL")
        cur.execute(q_CREATE_VT_BROKER_NEW_CDO_FINAL)
        cur.execute(q_COLLECT_STATS_VT_BROKER_NEW_CDO_FINAL)
        
        logger.info("Feteching final Data extract from TDV to S3 as a parquet file")
        final_df = pd.read_sql(q_SELECT_BROKER_HIER_DEMG, conn)
        
        #########Drop all volatile tables##################
        logger.info("Dropping all the volatile tables")
        cur.execute("DROP TABLE VT_BROKER_HIER;")
        cur.execute("DROP TABLE VT_BROKER_DEMG;")
        cur.execute("DROP TABLE VT_BROKER_FULL_HD;")
        cur.execute("DROP TABLE VT_BROKER_NEW_CDO;")
        cur.execute("DROP TABLE VT_BROKER_NEW_CDO_FINAL;")
        
        logger.info("Closing TDV Connection")
        conn.close()
        return final_df
    except:
        logger.info("ERROR: !!!!!!")
        cur.execute(q_SELECT_BROKER_HIER_DEMG)

#############################
#                           #
#                           #
#############################
def extractFromTDVToS3():
    try:
        print("Read from TDV:")
        broker_hier_df = executeStmtOnTDV()
       
        # Fetch current date and time
        now = datetime.now()
        curr_datetime = now.strftime("%d%m%Y %H%M%S")

        ########
        s3_write_path = write_path + curr_datetime + '.parquet'
        write_dataframe_to_parquet_on_s3(broker_hier_df,s3_write_path)
    except Exception as error:
        logger.exception("[Error] in extractFromTDVToS3: Broker Hier")
        raise error

#############################
#                           #
#                           #
#############################    
def main():
    logger.info("Main execution ...")
    extractFromTDVToS3()   

if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        raise err