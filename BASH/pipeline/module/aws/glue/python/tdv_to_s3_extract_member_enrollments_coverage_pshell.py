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
# from watchtower import CloudWatchLogHandler
# from glue_utilities import GlueUtilities
import time
import numpy as np
import pandas as pd
from connector import TdvConnector
from logger import ScriptLogger
import site
import importlib
from setuptools.command import easy_install
import subprocess
from io import StringIO, BytesIO
import shutil
from logger import ScriptLogger
install_path = os.environ['GLUE_INSTALLATION']
from pyarrow import *
ACTION = "extract"

logger = ScriptLogger("tdv_to_s3_extract_member_enrollments_coverage_pshell").get_logger(action = ACTION)
pd.set_option('display.max_rows', 1000, 'display.max_columns', 200, 'display.max_colwidth', 100)

#############################
#                           #
#                           #
#############################

args = getResolvedOptions(sys.argv, ['region_name', 'host', 'artifacts_bucket', 'tdv_env', 'sqlfile', 'artifacts_bucket_key', 'username', 'tdv_secretsmanager', 'custom_log_group', 'schema_trxhub', 'schema_datamart_reftable', 'schema_datamart_member'])

schema_trxhub = args['schema_trxhub']
schema_datamart_reftable = args['schema_datamart_reftable']
schema_datamart_member = args['schema_datamart_member']
region_name = args['region_name']
tdv_user = args['username']
tdv_secretsmanager = args['tdv_secretsmanager']
# tdv_pass = ssm_client.get_parameter(Name=tdv_secrets, WithDecryption=True) ['Parameter']['Value']
tdv_host = "awstddev.sys.cigna.com"
oss_env = args['tdv_env']
sql = args['sqlfile']
s3_bucket = args['artifacts_bucket']
artifacts_bucket_key = args['artifacts_bucket_key']

#######################

sql_props_location = artifacts_bucket_key + '/sql'
print("s3_bucket", s3_bucket)
print("artifacts_bucket_key", artifacts_bucket_key)
print("OSS env", oss_env)

mem_enroll_cvrg_fileloc = sql_props_location + '/tdv_extracts/mem_enroll_coverage_sql.properties'

#######################

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install("jproperties")


from jproperties import Properties

#######################
props = Properties()
s3_client = boto3.client('s3')

#######################
response = s3_client.get_object(Bucket=s3_bucket, Key=mem_enroll_cvrg_fileloc)
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

q_CREATE_VT_ENR1 = props.get("q_CREATE_VT_ENR1").data
#print(f"q_CREATE_VT_BROKER_HIER: {q_CREATE_VT_BROKER_HIER}")
q_COLLECT_STATS_VT_ENR1 = props.get("q_COLLECT_STATS_VT_ENR1").data.format(TRXHUB_CORE=schema_trxhub, DATAMART_MEMBER=schema_datamart_member, DATAMART_REFDATA=schema_datamart_reftable)

q_CREATE_VT_CSB_MBR_ENRLMT_CVRG_BASE_GET = props.get("q_CREATE_VT_CSB_MBR_ENRLMT_CVRG_BASE_GET").data
q_COLLECT_STATS_VT_CSB_MBR_ENRLMT_CVRG_BASE_GET = props.get("q_COLLECT_STATS_VT_CSB_MBR_ENRLMT_CVRG_BASE_GET").data

q_UPDATE_CSB_MEM_ENROLL_CVRG_GET_01 = props.get("q_UPDATE_CSB_MEM_ENROLL_CVRG_GET_01").data

q_CREATE_VT_ENR2 = props.get("q_CREATE_VT_ENR2").data
q_COLLECT_STATS_VT_ENR2 = props.get("q_COLLECT_STATS_VT_ENR2").data

q_CREATE_VT_PRD1 = props.get("q_CREATE_VT_PRD1").data
q_COLLECT_STATS_VT_PRD1 = props.get("q_COLLECT_STATS_VT_PRD1").data

q_CREATE_VT_PRD3 = props.get("q_CREATE_VT_PRD3").data
q_COLLECT_STATS_VT_PRD3 = props.get("q_COLLECT_STATS_VT_PRD3").data

q_UPDATE_CSB_MEM_ENROLL_CVRG_GET_02 = props.get("q_UPDATE_CSB_MEM_ENROLL_CVRG_GET_02").data

q_CREATE_VT_PAY1 = props.get("q_CREATE_VT_PAY1").data
q_COLLECT_STATS_VT_PAY1 = props.get("q_COLLECT_STATS_VT_PAY1").data

q_CREATE_VT_PAY3 = props.get("q_CREATE_VT_PAY3").data
q_COLLECT_STATS_VT_PAY3 = props.get("q_COLLECT_STATS_VT_PAY3").data

q_UPDATE_CSB_MEM_ENROLL_CVRG_GET_03 = props.get("q_UPDATE_CSB_MEM_ENROLL_CVRG_GET_03").data

q_SELECT_VT_CSB_MBR_ENRLMT_CVRG_BASE_GET = props.get("q_SELECT_VT_CSB_MBR_ENRLMT_CVRG_BASE_GET").data
print(f"q_SELECT_VT_CSB_MBR_ENRLMT_CVRG_BASE_GET: {q_SELECT_VT_CSB_MBR_ENRLMT_CVRG_BASE_GET}")

write_path = props.get("s3_writePath").data
print(f"s3_write_path: {write_path}")
        
#############################
#                           #
#                           #
#############################

def retry(func, *func_args, **kwargs):
    count = kwargs.pop("count", 5)
    delay = kwargs.pop("delay", 5)
    return any(func(*func_args, **kwargs)
            or logging.debug("Waiting for %s seconds before retrying again" % delay)
            or time.sleep(delay)
            for _ in range (count))
            
            
def get_logger():
    logger  = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[%(asctime)s - %(levelname)s - %(name)s:%(lineno)s - %(funcName)s ] - %(message)s')

    dt = int(time.time() * 10000 )
    log_stream_name = f"gov_solutions_commissions_{dt}"
    cw_handler = CloudWatchLogHandler(log_group=args['custom_log_group'], stream_name=log_stream_name)
    # cw_handler.setFormatter(formatter)
    logger.addHandler(cw_handler)
    logger.addHandler(handler)
    handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    return logger

#############################
#                           #
#                           #
#############################
# Adding error logging for all functions in this file. Try & Except w/ error messages.
def get_connection(tdv_host):
    try:
        session = boto3.session.Session()
        tdvconn_obj = TdvConnector(tdv_host, tdv_user, region_name, session, logger, tdv_secretsmanager)
        return tdvconn_obj.connect()
    except Exception as error:
        logger.exception("Error in TDV connection")
        raise error
        
#############################
#                           #
#                           #
#############################

def write_dataframe_to_parquet_on_s3(dataframe, filepath):
    """ Write a dataframe to a Parquet on S3 """
    try:
        logger.info("Writing {} records to {}".format(len(dataframe), filepath))
        return dataframe.to_parquet(filepath)
    except Exception as error:
        logger.error("Error in writng dataframe to Parquet on S3")
        raise error 



#############################
#                           #
#                           #
#############################    
def drop_table(vt_table_name):
    
    db_drop_table =  db_drop_table(f"{vt_table_name}")
    try:
        db_drop_table(f"{vt_table_name}")
        print(f"{vt_table_name} has been dropped")
        logger.info('Table has been dropped.:) {} - {}.format'(drop_table))
        return print(f"{vt_table_name} has been dropped")
    except:
        logger.info(f"Not able to drop the Volatile Table -> {vt_table_name}")


#############################
#                           #
#                           #
#############################

def executeStmtOnTDV():
    logger.info('Executed Statement on TDV')
    conn = get_connection(tdv_host)
    cur = conn.cursor()
    try:
        ##################   {Start} creating volatile table    ######################
        print("##################   start creating volatile table    ###################### \n")
        
        print("Creating Volatile Table and Collect Stats for --> VT_ENR1")
        cur.execute(q_CREATE_VT_ENR1)
        cur.execute(q_COLLECT_STATS_VT_ENR1)
        
        print("Creating Volatile Table and Collect Stats for --> VT_CSB_MBR_ENRLMT_CVRG_BASE_GET")
        cur.execute(q_CREATE_VT_CSB_MBR_ENRLMT_CVRG_BASE_GET)
        cur.execute(q_COLLECT_STATS_VT_CSB_MBR_ENRLMT_CVRG_BASE_GET)
  
        print("Creating Volatile Table and Collect Stats for --> VT_ENR2")
        cur.execute(q_CREATE_VT_ENR2)
        cur.execute(q_COLLECT_STATS_VT_ENR2)
        
        print("Update 01 : Volatile Table --> VT_CSB_MBR_ENRLMT_CVRG_BASE_GET")
        cur.execute(q_UPDATE_CSB_MEM_ENROLL_CVRG_GET_01)
        
        print("Creating Volatile Table and Collect Stats for --> VT_PRD1")
        cur.execute(q_CREATE_VT_PRD1)
        cur.execute(q_COLLECT_STATS_VT_PRD1)
        
        print("Creating Volatile Table and Collect Stats for --> VT_PRD3")
        cur.execute(q_CREATE_VT_PRD3)
        cur.execute(q_COLLECT_STATS_VT_PRD3)
        
        print("Update 02 : Volatile Table --> VT_CSB_MBR_ENRLMT_CVRG_BASE_GET")
        cur.execute(q_UPDATE_CSB_MEM_ENROLL_CVRG_GET_02)
        
        print("Creating Volatile Table and Collect Stats for --> VT_PAY1")
        cur.execute(q_CREATE_VT_PAY1)
        cur.execute(q_COLLECT_STATS_VT_PAY1)
        
        print("Creating Volatile Table and Collect Stats for --> VT_PAY3")
        cur.execute(q_CREATE_VT_PAY3)
        cur.execute(q_COLLECT_STATS_VT_PAY3)
        
        print("Update 03 : Volatile Table --> VT_CSB_MBR_ENRLMT_CVRG_BASE_GET")
        cur.execute(q_UPDATE_CSB_MEM_ENROLL_CVRG_GET_03)
        
        print("Feteching final Data extract from TDV to S3 as a parquet file")
        final_df = pd.read_sql(q_SELECT_VT_CSB_MBR_ENRLMT_CVRG_BASE_GET, conn)
        
        #########Drop all volatile tables##################
        print("Dropping all the volatile tables")
        cur.execute("DROP TABLE VT_PRD1;")
        cur.execute("DROP TABLE VT_PRD3;")
        cur.execute("DROP TABLE VT_ENR1;")
        cur.execute("DROP TABLE VT_ENR2;")
        cur.execute("DROP TABLE VT_PAY1;")
        cur.execute("DROP TABLE VT_PAY3;")
        cur.execute("DROP TABLE VT_CSB_MBR_ENRLMT_CVRG_BASE_GET;")
        
        print("Closing TDV Connection")
        conn.close()
        return final_df
    except Exception as error:
        logger.error("Error in executeStmtOnTDV()")
        raise error

#############################
#                           #
#                           #
#############################
def extractFromTDVToS3():
    try:
        logger.info("Read from TDV:")
        
        df = executeStmtOnTDV()
       
        # Fetch current date and time
        now = datetime.now()
        curr_datetime = now.strftime("%d%m%Y %H%M%S")
        
        s3_write_path = write_path + curr_datetime + '.parquet'
        
        write_dataframe_to_parquet_on_s3(df,s3_write_path)
    except Exception as error:
        logger.error("Could not extract data from TDV: %s" % error)
        raise error

#############################
#                           #
#                           #
#############################    
def main():
    
    try:
        print("Main execution ...")
        extractFromTDVToS3() 
        logger.info("Starting extraction: PCS Member Enrollments Coverage")
    except Exception as error:
        logging.exception("Error in Main Execution (extract from TDVToS3)") 

if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        raise err