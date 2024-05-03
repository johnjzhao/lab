
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
# pip3 install psycopg2 --user
# pip3 install psycopg2-binary --user
# pip3 install boto3 --user
# pip3 install pandasql --user
import os
import datetime
import difflib

import boto3
import pyarrow.parquet as pq
import glob
import configparser
import getpass
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql.functions import *
import numpy as np
import pandas as pd
pd.set_option('display.max_rows', 1000, 'display.max_columns', 200, 'display.max_colwidth', 100)
from pyspark.context import SparkContext


spark = SparkSession.builder.master("local").appName("app name") .config("spark.some.config.option").getOrCreate()


########################################################################
conf = pyspark.SparkConf()
sc = pyspark.SparkContext.getOrCreate(conf=conf)
sqlContext = SQLContext(sc)

#df = sqlcontext.read.json('random.json')

########################################################################

# spark = SparkContext.getOrCreate()
# sc = SparkContext()
# sqlContext = SQLContext(sc)

########################################################################
# sc = SparkContext()
# sqlContext = SQLContext(sc)

########################################################################
s3 = boto3.client('s3')
#s3 = boto3.Session(profile_name="default").client("s3")
PCS_Enroll_Transactions= 'gov-solutions-commissions-artifacts-dev'
ARTIFACTORY='artifactory/glue/extracts'

#Print the S3 objects:
# objects = s3.list_objects_v2(Bucket='gov-solutions-commissions-artifacts-dev',Prefix=ARTIFACTORY)
# for obj in objects['Contents']:
#     print(obj['Key'])

s3_ReadPath_PCS_Enroll_Transactions='artifactory/glue/transform/pcs/pcs_weekly_agent_enrollment_transactions_report/*'
s3_ReadPath_PCS_Enroll_Transactions_Rel = 's3://'+PCS_Enroll_Transactions+'/'+s3_ReadPath_PCS_Enroll_Transactions
Files_DF1= spark.read.csv(s3_ReadPath_PCS_Enroll_Transactions_Rel)
#Files_DF1= sqlContext.read.parquet('s3_ReadPath_PCS_Enroll_Transactions_Rel')
Files_DF1.registerTempTable('pcs_weekly_agent_enrollment_transactions_report')
#Files_DF1.show()

# s3_ReadPath_PCS_Enroll_Transactions_Hist='artifactory/glue/extracts/pcs_member_enrollments_coverage_hist/*'
# s3_ReadPath_PCS_Enroll_Transactions_Hist_Rel = 's3://'+PCS_Enroll_Transactions+'/'+s3_ReadPath_PCS_Enroll_Transactions_Hist
# Files_DF2= spark.read.parquet(s3_ReadPath_PCS_Enroll_Transactions_Hist_Rel)
# Files_DF2.registerTempTable('pcs_member_enrollments_coverage_hist')


s3_ReadPath_SRC_DATA_DIM='artifactory/glue/extracts/src_data_dim/*'
s3_ReadPath_SRC_DATA_DIM_Rel = 's3://'+PCS_Enroll_Transactions+'/'+s3_ReadPath_SRC_DATA_DIM
Files_DF3= spark.read.parquet(s3_ReadPath_SRC_DATA_DIM_Rel)
Files_DF3.registerTempTable('src_data_dim')

pcs_error_final_Df = spark.sql("""select AGT.SRC_MBR_KEY,AGT.MBR_ID,AGT.MEDCR_ID,AGT.ENRLMT_START_DT,AGT.ENRLMT_SIG_DT,AGT.SALES_AGT_ID,AGT.AGT_ERR_REASON,AGT.RCD_TY_CD
                 ,AGT.SRC_DATA_KEY,AGT.SRC_DATA_DESC,V_CURR_TIMESTAMP AS ETL_LOAD_DT_TM ,V_CURR_TIMESTAMP AS ETL_LAST_UPDT_DT_TM,AGT.ETL_NK_HASH_VAL
                 ,AGT.ETL_HASH_VAL,DIM.SRC_DATA_DESC
				,CASE WHEN SALES_AGT_ID = 'UNKNOWN' THEN 'NO Agent in QNXT'
							WHEN BROKER_AGT_ID  = 'UNKNOWN' THEN 'Agent Not in Broker'
							WHEN  AGT_TY_CD = 'DUMMY' THEN 'Agent Type Not Found'
							ELSE 'No Error'
						   END AS AGT_ERR_REASON
				,MD5(MBR_ID||ENRLMT_START_DT||RCD_TY_CD||SALES_AGT_ID) AS ETL_NK_HASH_VAL
				,MD5(COALESCE(MEDCR_ID,' ')||COALESCE(SRC_MBR_KEY,' ')||COALESCE(ENRLMT_SIG_DT,DATE '1900-01-01')||COALESCE(AGT_ERR_REASON,' ')) AS ETL_HASH_VAL

				FROM pcs_weekly_agent_enrollment_transactions_report  AGT
				LEFT JOIN src_data_dim DIM
				ON AGT.SRC_DATA_KEY = DIM.SRC_DATA_KEY 
				AND to_date(cast(ENRLMT_SIG_DT AS string), 'YYYYMMDD' )>='20201007' """)

pcs_error_final_Df.show()





