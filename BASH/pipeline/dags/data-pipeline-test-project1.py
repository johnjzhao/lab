# This DAG will trigger the Glue job created in tdv-oss-demo-create-glue-jobs.py

from airflow.providers.amazon.aws.operators.glue import AwsGlueJobOperator
from datetime import datetime, timedelta
from airflow import DAG
from dependencies.glue_plugin import CustomGlueJobOperator
import json
from airflow.models import Variable
from airflow.providers.amazon.aws.operators.sns import SnsPublishOperator

TDV_GLOBAL_CONFIG = Variable.get("tdv_global_config", deserialize_json=True) # imported from Airflow (see Admin > Variables in the console).
REPO_NAME = 'tdv-oss-demo' # put repo name here
OSS_PROJECT = True # indicate if project is OSS (True) or CCW (False)
AWS_CONN_ID = "oss_glue_connection"  # provided in your readme.md file
TARGET_SNS_TOPIC = "arn:aws:sns:us-east-1:302619437920:tdv-oss-demo-notification" # Provided in your readme.md file
def send_failure_notification(context):
    op = SnsPublishOperator(
            task_id='send_failure_sns',
            target_arn=TARGET_SNS_TOPIC, 
            message='DAG failed. See Airflow logs for details.',
            aws_conn_id=AWS_CONN_ID
        )
    op.execute(context)

default_args = {
    'owner': 'me',
    'start_date': datetime(2020, 1, 1),
    'retry_delay': timedelta(minutes=5),
    'on_failure_callback': send_failure_notification
}

dag_id = f'{REPO_NAME}-oss-test-project1' # ALL DAG_IDs MUST begin with the REPO NAME, i.e. if repo name is 'tdv-oss-demo', dag_id = 'tdv-oss-demo-create-glue-jobs'
glue_job_name = f'{REPO_NAME}' # ALL GLUE JOBS MUST begin with the REPO NAME


def get_glue_params(merge_dict = {}):
        """"Get parameters needed for the glue job."""
        glue_params = {
                "--host": TDV_GLOBAL_CONFIG["host"],
                "--secret_name": "dev/Ent360-Secret-TDV-SVT-AUTOCHG-User", # Contact Admin team to set up your TDV Creds in secrets manager. Replace with your secret name
                "--logmech": TDV_GLOBAL_CONFIG["logmech"],
                "--s3_bucket": TDV_GLOBAL_CONFIG["glue_s3_bucket"],
                "--extra-py-files": TDV_GLOBAL_CONFIG["teradatasql_library_path"]
                
        }

        # modify secret name and SQL variables for each environment
        if TDV_GLOBAL_CONFIG["env"] == "dev":
                secret_name = "dev/Ent360-Secret-TDV-SVT-AUTOCHG-User"
                sql_param_database = "HSETL_WORK_DEV2"

        if TDV_GLOBAL_CONFIG["env"] == "test":
                secret_name = "dev/Ent360-Secret-TDV-SVT-AUTOCHG-User"
                sql_param_database = "HSETL_WORK_TEST"

        if TDV_GLOBAL_CONFIG["env"] == "prod":
                secret_name = "dev/Ent360-Secret-TDV-SVT-AUTOCHG-User"
                sql_param_database = "HSETL_WORK_PROD"
        
        
        glue_params["--secret_name"] = secret_name
        glue_params["--sql_params"] = json.dumps( # pass in the values for variables used in your .sql files
                {
                        "<database>": sql_param_database 
                }
        )
        glue_params.update(merge_dict)
        print("glue params", glue_params)
        return glue_params

with DAG(dag_id = dag_id, default_args = default_args, schedule_interval = None) as dag:
   
    sql1_sql2 = CustomGlueJobOperator(
            task_id = "sql1_sql2",
            dag=dag,
            job_name = glue_job_name,
            aws_conn_id=AWS_CONN_ID,
            script_args = get_glue_params( 
                {
                        "--s3_sql_files": "tdv-oss-demo/dml/project1/1.sql,tdv-oss-demo/dml/project1/2.sql", # String of sql file name(s) to be read, separated by commas
                }
            ),
            run_job = True, # This triggers the glue job. Do not change
            
    )
   
    sql3 = CustomGlueJobOperator(
            task_id = "sql3",
            job_name = glue_job_name,
            dag = dag,
            aws_conn_id=AWS_CONN_ID,
            script_args = get_glue_params(
                {"--s3_sql_files": "tdv-oss-demo/dml/project1/3.sql"}
            ),
            run_job = True,
    )
    sql4 = CustomGlueJobOperator(
            task_id = "sql4",
            job_name = glue_job_name,
            dag = dag,
            aws_conn_id=AWS_CONN_ID,
            script_args = get_glue_params(
                {"--s3_sql_files": "tdv-oss-demo/dml/project1/4.sql"}
            ),
            run_job = True,
    )
    demo_table_2 = CustomGlueJobOperator(
            task_id = "demo_table_2",
            job_name = glue_job_name,
            dag = dag,
            aws_conn_id=AWS_CONN_ID,
            script_args = get_glue_params(
                {"--s3_sql_files": "tdv-oss-demo/dml/project1/demo_table_2.sql"}
            ),
            run_job = True,
    )

    
    sql1_sql2 >> sql3
    sql4
    demo_table_2
