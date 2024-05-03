#libs
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

from distutils.debug import DEBUG
import os
import io
import glob
import configparser
import difflib
import boto3
import sys
import logging
from datetime import datetime
import time
import numpy as np
import pandas as pd
import site
import importlib
from setuptools.command import easy_install
import subprocess
from io import StringIO, BytesIO
import shutil
from logger import ScriptLogger
from pyarrow import *

#################
#
#
#################

args = getResolvedOptions(sys.argv, [
    'region_name',
    'host',
    'artifacts_bucket',
    'tdv_env',
    'sqlfile',
    'artifacts_bucket_key',
    'username',
    'tdv_secretsmanager',
    'custom_log_group',
    'run_job_name',
    'glue_catalog_database'
    ])

########################
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
    
########################
#                      #
#                      #
########################

ACTION = "transform"
region_name = args['region_name']
tdv_user = args['username']
tdv_secretsmanager = args['tdv_secretsmanager']

# tdv_pass = ssm_client.get_parameter(Name=tdv_secrets, WithDecryption=True) ['Parameter']['Value']

tdv_host = args['host']
oss_env = args['tdv_env']
run_job_name = args['run_job_name']
sql = args['sqlfile']
s3_bucket = args['artifacts_bucket']
artifacts_bucket_key = args['artifacts_bucket_key']
logger = ScriptLogger(run_job_name).get_logger(action=ACTION)

## Glue ###########

glue_catalog_database = args['glue_catalog_database']

#######################

sql_props_location = artifacts_bucket_key + '/sql'
print ('s3_bucket', s3_bucket)
print ('artifacts_bucket_key', artifacts_bucket_key)
print ('OSS env', oss_env)

sql_props_file_loc = sql_props_location \
    + '/transform/transform_pcs_weekly_enrollment_transactions_sql.properties'


#############################
#                           #
#                           #
#############################
def install_package(package_name):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',package_name])


#############################
#                           #
#                           #
#############################

def getProps(s3_bucket, file_loc):
    install_package('jproperties')
    from jproperties import Properties

    # ######################

    props = Properties()
    s3_client = boto3.client('s3')

    # ######################

    response = s3_client.get_object(Bucket=s3_bucket, Key=file_loc)
    sql_str_body = response['Body'].read()
    sql_str = io.BytesIO(sql_str_body)
    props_file = 'input.properties'

    # ############################

    with open(props_file, mode='wb') as f:
        sql_str.seek(0)
        shutil.copyfileobj(sql_str, f)
    with open(props_file, 'rb') as f:
        props.load(f)
        return props
    
########################
#                      #
#                      #
########################

def readFromGlueCataLog(glue_catalog_database, glue_table_name):
    """
        Load Table/data-set to data frame
        Returns:
        DataFrame: Object of Spark DataFrame class for given input args
    """

    readDF = glueContext.create_dynamic_frame.from_catalog(database=glue_catalog_database,
            table_name=glue_table_name, transformation_ctx='readDF')
    return readDF.toDF()


########################
#                      #
#                      #
########################

def writeDataFrameToS3(
    writeDF,
    file_format,
    file_cnt,
    write_mode,
    out_file_path,
    ):
    """
    """

    writeDF.coalesce(file_cnt).write.mode(write_mode).format(file_format).option('header'
            , 'true').save(out_file_path)


########################
#                      #
#                      #
########################

def applyTransform(spark):
    """
        Apply above said transformations
        Parameters:
        arg1 (spark): Object of Spark Sesiion
        arg2 (inp_query): Query String to execute
        Returns:
        DataFrame: Object of Spark DataFrame class for pcs_weekly_enrollment_transactions
    """

    broker_comm_sircon_df = readFromGlueCataLog(glue_catalog_database,'broker_comm_sircon')
    broker_comm_sircon_df.createOrReplaceTempView('vw_broker_comm_sircon')

    member_sales_agent_dim_df = readFromGlueCataLog(glue_catalog_database,'mbr_sales_agt_dim')
    member_sales_agent_dim_df.createOrReplaceTempView('vw_member_sales_agent_dim')
    
    member_sales_agent_df = spark.read.parquet(s3_member_sales_agent_path)
    member_sales_agent_df.createOrReplaceTempView('vw_member_sales_agent')

    member_enrollments_coverage_df = readFromGlueCataLog(glue_catalog_database,'pcs_member_enrollments_coverage')
    member_enrollments_coverage_df.createOrReplaceTempView('vw_member_enrollments_coverage')

    member_enrollments_medicare_cdo_mbr_demg_df = readFromGlueCataLog(glue_catalog_database,'cdo_mbr_demg')
    member_enrollments_medicare_cdo_mbr_demg_df.createOrReplaceTempView('vw_cdo_mbr_demg')

    member_medicare_dim_df = readFromGlueCataLog(glue_catalog_database,'mbr_medcr_dim')
    member_medicare_dim_df.createOrReplaceTempView('vw_member_medicare_dim')

    member_dim_df = readFromGlueCataLog(glue_catalog_database,'member_dimension')
    member_dim_df.createOrReplaceTempView('vw_member_dim')
    
    cms_trans_reply_dim_df = readFromGlueCataLog(glue_catalog_database,'cms_trans_reply_dim')
    cms_trans_reply_dim_df.createOrReplaceTempView('vw_cms_trans_reply_dim')
    
    ######################  q_SELECT_MEM_ENROLL_CVRG_WITH_MEDICARE
    mem_enroll_cvrg_with_medicare_df = spark.sql(q_SELECT_MEM_ENROLL_CVRG_WITH_MEDICARE)
    mem_enroll_cvrg_with_medicare_df.createOrReplaceTempView('vw_mem_enroll_cvrg_with_medicare')
    
    ######################  q_SELECT_AGT_TY_CD
    broker_comm_agt_ty_cd_df = spark.sql(q_SELECT_AGT_TY_CD)
    broker_comm_agt_ty_cd_df.createOrReplaceTempView('vw_agt_ty_cd')
    
    ######################  q_SELECT_MEM_SALES_AGENT_DISENROLL_REINSTATE
    mem_sales_agent_disenroll_reinstate_df = spark.sql(q_SELECT_MEM_SALES_AGENT_DISENROLL_REINSTATE)
    mem_sales_agent_disenroll_reinstate_df.createOrReplaceTempView('vw_mem_sales_agent_disenroll_reinstate')
    
    ######################  q_SELECT_MBR_ENRLMT_CVRG_AGT
    mbr_enrlmt_cvrg_agt_df = spark.sql(q_SELECT_MBR_ENRLMT_CVRG_AGT)
    mbr_enrlmt_cvrg_agt_df.createOrReplaceTempView('vw_mbr_enrlmt_cvrg_agt')
    
    ######################  q_SELECT_BROKER_AGT_ID
    broker_agt_id_df = spark.sql(q_SELECT_BROKER_AGT_ID)
    broker_agt_id_df.createOrReplaceTempView('vw_broker_agt_id')
    
    ######################  q_SELECT_MBR_ENRLMT_CVRG_AGT_BRK
    mbr_enrlmt_cvrg_agt_brk_df = spark.sql(q_SELECT_MBR_ENRLMT_CVRG_AGT_BRK)
    mbr_enrlmt_cvrg_agt_brk_df.createOrReplaceTempView('vw_mbr_enrlmt_cvrg_agt_brk')
    
    ######################  q_SELECT_MBR_ENRLMT_CVRG_AGT_BRK_COMM_AND_NONCOMM
    mbr_enrlmt_cvrg_agt_brk_comm_noncomm_df = spark.sql(q_SELECT_MBR_ENRLMT_CVRG_AGT_BRK_COMM_AND_NONCOMM)
    mbr_enrlmt_cvrg_agt_brk_comm_noncomm_df.createOrReplaceTempView('vw_mbr_enrlmt_cvrg_agt_brk_comm_noncomm')
    
    ######################
    final_df = spark.sql(q_SELECT_PCS_WEEKLY_ENROLL_TRANSACTIONS)
    return final_df


########################
#                      #
#                      #
########################

# def spark_session():
    # glueContext = GlueContext(SparkContext.getOrCreate())
    # spark_session = glueContext.spark_session
    # return spark_session


########################
#                      #
#                      #
########################

def pcsDriver(spark):
    """
    PCS Transform Main/Driver Function
    """
    # ##########
    writeDF = applyTransform(spark)
    writeDataFrameToS3(writeDF, 'csv', 1, 'append',writePath_pcs_weekly)


# #########
props = getProps(s3_bucket, sql_props_file_loc)

# #########
q_SELECT_MEM_ENROLL_CVRG_WITH_MEDICARE = props.get('q_SELECT_MEM_ENROLL_CVRG_WITH_MEDICARE').data
print(f"q_SELECT_MEM_ENROLL_CVRG_WITH_MEDICARE: {q_SELECT_MEM_ENROLL_CVRG_WITH_MEDICARE}")

# #########
q_SELECT_MEM_SALES_AGENT_DISENROLL_REINSTATE = props.get('q_SELECT_MEM_SALES_AGENT_DISENROLL_REINSTATE').data
print(f"q_SELECT_MEM_SALES_AGENT_DISENROLL_REINSTATE: {q_SELECT_MEM_SALES_AGENT_DISENROLL_REINSTATE}")

# #########
q_SELECT_AGT_TY_CD = props.get('q_SELECT_AGT_TY_CD').data
print(f"q_SELECT_AGT_TY_CD: {q_SELECT_AGT_TY_CD}")

# #########
q_SELECT_MBR_ENRLMT_CVRG_AGT = props.get('q_SELECT_MBR_ENRLMT_CVRG_AGT').data
print(f"q_SELECT_MBR_ENRLMT_CVRG_AGT: {q_SELECT_MBR_ENRLMT_CVRG_AGT}")

# #########
q_SELECT_BROKER_AGT_ID = props.get('q_SELECT_BROKER_AGT_ID').data
print(f"q_SELECT_BROKER_AGT_ID: {q_SELECT_BROKER_AGT_ID}")

# #########
q_SELECT_MBR_ENRLMT_CVRG_AGT_BRK = props.get('q_SELECT_MBR_ENRLMT_CVRG_AGT_BRK').data
print(f"q_SELECT_MBR_ENRLMT_CVRG_AGT_BRK: {q_SELECT_MBR_ENRLMT_CVRG_AGT_BRK}")

# #########
q_SELECT_MBR_ENRLMT_CVRG_AGT_BRK_COMM_AND_NONCOMM = props.get('q_SELECT_MBR_ENRLMT_CVRG_AGT_BRK_COMM_AND_NONCOMM').data
print(f"q_SELECT_MBR_ENRLMT_CVRG_AGT_BRK_COMM_AND_NONCOMM: {q_SELECT_MBR_ENRLMT_CVRG_AGT_BRK_COMM_AND_NONCOMM}")

# #########
q_SELECT_PCS_WEEKLY_ENROLL_TRANSACTIONS = props.get('q_SELECT_PCS_WEEKLY_ENROLL_TRANSACTIONS').data
print(f"q_SELECT_PCS_WEEKLY_ENROLL_TRANSACTIONS: {q_SELECT_PCS_WEEKLY_ENROLL_TRANSACTIONS}")

# #########
s3_read_member_sales_agent = props.get('s3_read_member_sales_agent').data
print(f"S3 Read path for 'member sales agent' : {s3_read_member_sales_agent}")

# #########
writePath_pcs_weekly = props.get('s3_weekly_file_write_path').data
print(f"s3_writePath for 'pcs_weekly_enrollment_transactions' : {writePath_pcs_weekly}")


#############################
#                           #
#                           #
#############################

if __name__ == '__main__':
    try:
        #spark = spark_session()
        pcsDriver(spark)
    except Exception as err:
        raise err

spark.stop()