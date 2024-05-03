# libs
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
import boto3
import sys
import logging
from datetime import datetime
from logger import ScriptLogger
from quality_methods import QualityMethods

#################
#
#################

args = getResolvedOptions(sys.argv, [
    'region_name',
    'host',
    'artifacts_bucket',
    'tdv_env',
    'sqlfile',
    'artifacts_bucket_key',
    'tdv_secretsmanager',
    'custom_log_group',
    'run_job_name'
])

########################
# Create Spark Session
########################

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

########################
#                      #
#                      #
########################

ACTION = "QA"
region_name = args['region_name']
run_job_name = args['run_job_name']
sql = args['sqlfile']
s3_bucket = args['artifacts_bucket']
artifacts_bucket_key = args['artifacts_bucket_key']
logger = ScriptLogger(run_job_name).get_logger(action=ACTION)
s3_client = boto3.client('s3')

def write_dataframe_to_parquet_on_s3(dataframe, filepath, partition):
    """ Write a dataframe to a Parquet on S3 """
    dataframe.write.partitionBy(partition).parquet(filepath)

#######################
#
#######################
def main():
    try:
        print("Main execution ...")
        read_filepath = "s3://gov-solutions-commissions-artifacts-dev/artifactory/glue/extracts/evolve/" \
                        "membere_evolve/meme_test.txt"
        print(f"s3_readPath for 'evolve_member_enrollment' : {read_filepath}")
        write_filepath = "s3://gov-solutions-commissions-artifacts-dev/artifactory/glue/quality_results/evolve"
        print(f"s3_writePath for 'evolve_member_enrollment' : {write_filepath}")

        # read file
        evolve_meme_df = spark.read.option("delimiter", "|").option("header", True).csv(read_filepath)

        # set the test date
        now = datetime.now()
        curr_datetime = now.strftime("%d%m%Y %H%M%S")
        print(f"curr_datetime : {curr_datetime}")

        # perform general evaluations
        general_stats_df = QualityMethods.quality_general_stats(evolve_meme_df, curr_datetime)
        print(f"general_stats eval complete")

        # write dataframes to s3
        write_dataframe_to_parquet_on_s3(general_stats_df, write_filepath + "/evolve_meme_quality_general_stats"
                                         + "/" + curr_datetime, "test_date")
        print(f"general_stats_f written")

        # specify expected column datatypes in a list []
        # Options are "date", "string", "number", "number and letter"
        col_datatypes = ["number_letter", "number_letter", "number_letter", "date_evolve", "date_evolve", "number",
                         "number", "number", "number", "number_letter", "date_evolve", "date_evolve", "number",
                         "date_evolve", "number", "number_letter", "number", "number_letter", "number", "number_letter"]

        #preview dataframe for troubleshooting.
        print(evolve_meme_df.show(1))

        # perform format evaluations
        formats_df = QualityMethods.quality_formats(evolve_meme_df, col_datatypes,  curr_datetime)
        print(f"formats eval complete")

        # write dataframes to s3
        write_dataframe_to_parquet_on_s3(formats_df, write_filepath + "/evolve_meme_quality_formats" + "/"
                                         + curr_datetime, "test_date")
        print(f"formats_df written")
        print("main_executed")

    except Exception as error:
        logging.exception("Error in Main Execution (quality_check_pcs_enrollment)")

if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        raise err

# stop spark instance
spark.stop()