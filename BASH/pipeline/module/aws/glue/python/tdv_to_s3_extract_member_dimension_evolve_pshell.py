from distutils.debug import DEBUG
import re
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
from watchtower import CloudWatchLogHandler
from glue_utilities import GlueUtilities
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

logger = ScriptLogger("tdv_to_s3_dataextract_memberp_evolve").get_logger(action = ACTION)
pd.set_option('display.max_rows', 1000, 'display.max_columns', 200, 'display.max_colwidth', 100)
TDV_CONN_WAIT_TIMES = [2**i for i in range(5, 9)]

#############################
#                           #
#                           #
#############################

args = getResolvedOptions(sys.argv, ['region_name', 'host', 'artifacts_bucket', 'tdv_env', 'sqlfile', 'artifacts_bucket_key', 'username', 'tdv_secretsmanager', 'custom_log_group', 'schema_datamart_member', 'schema_reporting', 'schema_trxhub'])

trxhub_core= args['schema_trxhub']
schema_datamart_member = args['schema_datamart_member']
schema_reporting = args['schema_reporting']
region_name = args['region_name']
tdv_user = args['username']
tdv_secretsmanager = args['tdv_secretsmanager']
# tdv_pass = ssm_client.get_parameter(Name=tdv_secrets, WithDecryption=True) ['Parameter']['Value']
tdv_host = args['host']
oss_env = args['tdv_env']
sql = args['sqlfile']
s3_bucket = args['artifacts_bucket']
artifacts_bucket_key = args['artifacts_bucket_key']

#######################

sql_props_location = artifacts_bucket_key + '/sql'
logger.info("tdv host: %s" % tdv_host)
logger.info("s3_bucket: %s" % s3_bucket)
logger.info("artifacts_bucket_key: %s" % artifacts_bucket_key)
logger.info("OSS env: %s" % oss_env)

mem_dim_fileloc = sql_props_location + '/tdv_extracts/evolve_memberp_tdv_to_s3.properties'

#######################
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install("jproperties")

from jproperties import Properties

#######################
props = Properties()
s3_client = boto3.client('s3')

#######################
response = s3_client.get_object(Bucket=s3_bucket, Key=mem_dim_fileloc)
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

q_CREATE_VT_CURRENT_DATETIME = props.get("q_CREATE_VT_CURRENT_DATETIME").data
logger.info(f"q_CREATE_VT_CURRENT_DATETIME: {q_CREATE_VT_CURRENT_DATETIME}")

q_SELECT_VT_MEMP_DATA = props.get("q_SELECT_VT_MEMP_DATA").data.format(DATAMART_MEMBER=schema_datamart_member,REPORTING=schema_reporting, TRXHUB_CORE=trxhub_core )
logger.info(f"q_SELECT_VT_MEMP_DATA: {q_SELECT_VT_MEMP_DATA}")

write_file_name_pattern_pf = props.get("write_file_name_pattern_pf").data
logger.info(f"write_file_name_pattern_pf: {write_file_name_pattern_pf}")

write_path = props.get("s3_writePath").data
logger.info(f"s3_write_path: {write_path}")

write_path_w_filename_pf = props.get("s3_writePath").data + write_file_name_pattern_pf
logger.info(f"s3_write_path_w_filename_pf: {write_path_w_filename_pf}")

write_path_archive = props.get("s3_writePath_archive").data
logger.info(f"s3_write_path_archive: {write_path_archive}")

write_path_archive_w_filename_pf = props.get("s3_writePath_archive").data + write_file_name_pattern_pf
logger.info(f"s3_write_path_archive_w_filename_pf: {write_path_archive_w_filename_pf}")

archive_file_flag = props.get("archive_file_flag").data
logger.info(f"archive_file_flag: {archive_file_flag}")

delete_previous_files_flag = props.get("delete_previous_files_flag").data
logger.info(f"delete_previous_files_flag: {delete_previous_files_flag}")


#############################
#                           #
#                           #
#############################
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
def write_dataframe_to_parquet_on_s3(dataframe, filepath):
    """ Write a dataframe to a Parquet on S3 """
    
    try:
        logger.info("Writing {} records to {}".format(len(dataframe), filepath))
        return dataframe.to_parquet(filepath)
    except Exception as error:
        logger.error("Error in writing dataframe to Parquet on S3")
        raise error 


#############################
#                           #
#                           #
#############################    
def drop_table(vt_table_name):
    
    db_drop_table =  db_drop_table(f"{vt_table_name}")
    try:
        db_drop_table(f"{vt_table_name}")
        logger.info(f"{vt_table_name} has been dropped")
        logger.info('Table has been dropped.:) {} - {}.format'(drop_table))
        return logger.info(f"{vt_table_name} has been dropped")
    except:
        logger.info(f"Not able to drop the Volatile Table -> {vt_table_name}")


#############################
#                           #
#                           #
#############################
def executeStmtOnTDV():
    logger.info('Executed Statement on TDV')#: {} - {}.format'(vt_table_name))
    conn = get_connection()
    cur = conn.cursor()
    try:
        #cur.execute(f'DROP TABLE {table_name}')
        cur.execute(q_CREATE_VT_CURRENT_DATETIME)
        src_df = pd.read_sql(q_SELECT_VT_MEMP_DATA, conn)
        conn.close()
        return src_df
    except:
        # cur.execute(q_CREATE_VT_MEMP_DATA)
        logger.info(f"Failed execution of the queries to generate the parquet file.")


#############################
#                           #
#                           #
#############################
def deleteObjectsFromS3Folder(s3_bucket_name_var, s3_bucket_prefix_var, regex_filename_pattern_var):

    s3_client = boto3.client("s3")
    
    # First we list all files in folder
    response = s3_client.list_objects_v2(Bucket=s3_bucket_name_var, Prefix=s3_bucket_prefix_var)

    files_in_folder = response["Contents"]
    files_to_delete = []

    # We will create Key array to pass to delete_objects function
    for f in files_in_folder:
        if re.search(regex_filename_pattern_var, f["Key"]):
            files_to_delete.append({"Key": f["Key"]})
            print ('File will be deleted: ' + f["Key"]) 
        else:
            print ('File will not be deleted: ' + f["Key"])

    # All files in this list will be deleted: files_to_delete
    if response['KeyCount'] > 0:
        print (files_to_delete)
        
        response = s3_client.delete_objects(
            Bucket=s3_bucket_name_var, Delete={"Objects": files_to_delete}
        )

        logger.info("Deleted the following file(s): ")
        print (response)
        logger.info(response)


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

        # Delete any files from the active folder which match the file pattern if delete_previous_files_flag in ('Y', 'y').
        if (delete_previous_files_flag in ('Y', 'y')):
            s3_write_path = f"{write_path}"
            s3_bucket, s3_key = s3_write_path.replace("s3://", "").split('/', 1)
            print ('s3_bucket: ' + s3_bucket)
            print ('s3_key: ' + s3_key)
            
            regex_filename_pattern =  re.escape(write_file_name_pattern_pf) + r'[\w*]+[ ][\w*]+\.(parquet)$'
            deleteObjectsFromS3Folder(s3_bucket, s3_key, regex_filename_pattern)

        #Write the current file
        s3_write_path_w_filename_pf = f"{write_path_w_filename_pf}{curr_datetime}.parquet"
        write_dataframe_to_parquet_on_s3(df,s3_write_path_w_filename_pf)

        #Write the current file to the archive folder as well if archive_file_flag in ('Y', 'y').
        if (archive_file_flag in ('Y', 'y')):
            s3_write_path_archive_w_filename_pf = f"{write_path_archive_w_filename_pf}{curr_datetime}.parquet"
            write_dataframe_to_parquet_on_s3(df,s3_write_path_archive_w_filename_pf)

    except Exception as error:
        logger.error("Could not extract data from TDV: %s" % error)
        raise error

#############################
#                           #
#                           #
#############################    
def main():
    
    try:
        logger.info("Main execution ...")
        extractFromTDVToS3() 
        logger.info("Starting extraction")
    except Exception as error:
        logging.exception("Error in Main Execution (extract from TDVToS3)") 

if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        raise err
