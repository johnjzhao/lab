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
# sc = SparkContext()
# glueContext = GlueContext(sc)
# spark = glueContext.spark_session
    
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
glue_catalog_database = args['glue_catalog_database'] #"gov-solutions-commissions-evolve-dev"
#glue_catalog_connection_name = args['glue_catalog_connection_name']

#######################

sql_props_location = artifacts_bucket_key + '/sql'
print ('s3_bucket', s3_bucket)
print ('artifacts_bucket_key', artifacts_bucket_key)
print ('OSS env', oss_env)

sql_props_file_loc = sql_props_location \
    + '/transform/transform_evolve_memberp_membere_enrollment_transactions_sql.properties'


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
    return readDF.toDF().fillna('')


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
    out_file_name
    ):
    """
    """

    # Write the file and for empty and null values do not write with ""
    writeDF.coalesce(file_cnt).write.mode(write_mode).format(file_format).option('nullValue'
            , '\u0000').option('emptyValue', '\u0000').option('delimiter', '|').option('header', 'true').save(out_file_path)

    # Generate as a function.  Convert to Pandas dataframe.
    s3_client = boto3.client('s3')
    s3_bucket_temp, s3_key_temp = out_file_path.replace("s3://", "").split('/', 1)
    paginator = s3_client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=s3_bucket_temp, Prefix=s3_key_temp)

    for page in pages:

        if page['KeyCount'] > 0:
            for obj in page['Contents']:
                #print (obj['Key'])
                
                copy_source = {'Bucket': s3_bucket_temp, 'Key': obj['Key']}
                
                if ('/part-' in obj['Key']) and (s3_key_temp in obj['Key']):
                    s3_client.copy_object(CopySource = copy_source, Bucket = s3_bucket_temp, Key = s3_key_temp + out_file_name)
                    s3_client.delete_object(Bucket = s3_bucket_temp, Key = obj['Key'])
                    logger.info("Writing data to Filename: " + out_file_path + out_file_name)



########################
#                      #
#                      #
########################

def applyTransform(spark, inp_query, table_name, vw_version_of_table_name):
#def applyTransform(spark, inp_query, table_name):
    """
        Apply above said transformations
        Parameters:
        arg1 (spark): Object of Spark Sesiion
        arg2 (inp_query): Query String to execute
        Returns:
        DataFrame: Object of Spark DataFrame class for pcs_weekly_enrollment_transactions
    """

    final_df = readFromGlueCataLog(glue_catalog_database, table_name)
    final_df.createOrReplaceTempView(vw_version_of_table_name)
    final_df = spark.sql(inp_query)
    return final_df


########################
#                      #
#                      #
########################

def spark_session():
    # glueContext = GlueContext(SparkContext.getOrCreate())
    # spark_session = glueContext.spark_session
    # return spark_session
    sc = SparkContext()
    glueContext = GlueContext(sc)
    spark = glueContext.spark_session
    return spark, glueContext


########################
#                      #
#                      #
########################

def evolveDriver(spark):
    """
    Code Transform Main/Driver Function
    """
    now = datetime.now()
    curr_datetime = now.strftime("%d%m%Y %H%M%S")

    # #########
    props = getProps(s3_bucket, sql_props_file_loc)

    # #########
    q_SELECT_EVOLVE_MEMBERP_ENROLL_TRANSACTIONS = props.get('q_SELECT_EVOLVE_MEMBERP_ENROLL_TRANSACTIONS').data
    print(f"q_SELECT_EVOLVE_MEMBERP_ENROLL_TRANSACTIONS: {q_SELECT_EVOLVE_MEMBERP_ENROLL_TRANSACTIONS}")

    q_SELECT_EVOLVE_MEMBERE_ENROLL_TRANSACTIONS = props.get('q_SELECT_EVOLVE_MEMBERE_ENROLL_TRANSACTIONS').data
    print(f"q_SELECT_EVOLVE_MEMBERE_ENROLL_TRANSACTIONS: {q_SELECT_EVOLVE_MEMBERE_ENROLL_TRANSACTIONS}")

    q_SELECT_EVOLVE_MEMBERE_ENROLL_TRANSACTIONS_MISSING_MEMBERP_REC = props.get('q_SELECT_EVOLVE_MEMBERE_ENROLL_TRANSACTIONS_MISSING_MEMBERP_REC').data
    print(f"q_SELECT_EVOLVE_MEMBERE_ENROLL_TRANSACTIONS_MISSING_MEMBERP_REC: {q_SELECT_EVOLVE_MEMBERE_ENROLL_TRANSACTIONS_MISSING_MEMBERP_REC}")

    writePath_file_memberp = f"{props.get('s3_memberp_file_write_path').data}"
    print(f"s3_memberp_file_write_path for 'evolve_memberp_membere_enrollment_transactions' : {writePath_file_memberp}")

    writePath_file_membere = f"{props.get('s3_membere_file_write_path').data}"
    print(f"s3_membere_file_write_path for 'evolve_memberp_membere_enrollment_transactions' : {writePath_file_membere}")

    # ##########
    writeDF_membere = applyTransform(spark, q_SELECT_EVOLVE_MEMBERE_ENROLL_TRANSACTIONS, 'membere_evolve', 'vw_membere_evolve')
    #print (writeDF_membere)

    writeDF_memberp = applyTransform(spark, q_SELECT_EVOLVE_MEMBERP_ENROLL_TRANSACTIONS, 'memberp_evolve', 'vw_memberp_evolve')
    #print (writeDF_memberp)

    check_membere_member_id_exists_in_memberp_df = spark.sql(q_SELECT_EVOLVE_MEMBERE_ENROLL_TRANSACTIONS_MISSING_MEMBERP_REC)
    if (check_membere_member_id_exists_in_memberp_df.first()['missing_memberp_rec_count']) == 0:

        logger.info("Record count for MemberE File: " + str(writeDF_membere.count()))
        logger.info("Record count for MemberP File: " + str(writeDF_memberp.count()))

        writeDataFrameToS3(writeDF_memberp, 'csv', 1, 'append', writePath_file_memberp, 'memberp_' + curr_datetime + '.txt')
        writeDataFrameToS3(writeDF_membere, 'csv', 1, 'append', writePath_file_membere, 'membere_' + curr_datetime + '.txt')

    else:

        logger.info("Error - Missing MemberP record(s) for available MemberE transactions.  Missing member count from MemberP table: " + str(check_membere_member_id_exists_in_memberp_df.first()['missing_memberp_rec_count']))
        raise Exception("Error - Missing MemberP records for MemberE transactions!!!")


#############################
#                           #
#                           #
#############################
def main():
    try:
        print("Main execution ...")
        logger.info("Starting extraction: Evolve Member Enrollment Coverage")
        evolveDriver(spark)
        logger.info("Completed extraction: Evolve Member Enrollment Coverage")
    except Exception as error:
        logging.exception("Error in Main Execution (Evolve extract from Glue Catalog To S3)")


#############################
#                           #
#                           #
#############################

if __name__ == '__main__':
    try:
        spark, glueContext = spark_session()
        main()
        spark.stop()        
    except Exception as err:
        raise err
