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
AWS_CONN_ID = "oss_glue_connection" # Provided in your readme.md file
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

dag_id = f'{REPO_NAME}-pvs-testing' # ALL DAG_IDs MUST begin with the REPO NAME, i.e. if repo name is 'tdv-oss-demo', dag_id = 'tdv-oss-demo-create-glue-jobs'
glue_job_name = f'{REPO_NAME}-ccw' # ALL GLUE JOBS MUST begin with the REPO NAME


def get_glue_params(merge_dict = {}):
        """"Get parameters needed for the glue job."""
        glue_params = {
                "--host": TDV_GLOBAL_CONFIG["host"],
                "--secret_name": "dev/Ent360-Secret-TDV-SVT-AUTOCHG-User", # Contact Admin team to set up your TDV Creds in secrets manager. Replace with your secret name
                "--logmech": TDV_GLOBAL_CONFIG["logmech"],
                "--s3_bucket": TDV_GLOBAL_CONFIG["glue_s3_bucket"],
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
        glue_params["--extra-py-files"] = f"{glue_params['--extra-py-files']},{TDV_GLOBAL_CONFIG['teradatasql_library_path']}"
        print("glue params", glue_params)
        return glue_params

with DAG(dag_id = dag_id, default_args = default_args, schedule_interval = None) as dag:
   
    claims1_sql = CustomGlueJobOperator(
            task_id = "claims1_sql",
            dag=dag,
            job_name = glue_job_name,
            aws_conn_id=AWS_CONN_ID,
            script_args = get_glue_params( 
                {
                        "--extra-py-files": f"s3://{TDV_GLOBAL_CONFIG['glue_s3_bucket']}/{REPO_NAME}/dml/pvs-testing/claims1_sql.py", # python file name
                        "--py_file_name": "claims1_sql" # python file name without .py extension
                }
            ),
            run_job = True, # This triggers the glue job. Do not change
            
    )
    claims2_sql = CustomGlueJobOperator(
            task_id = "claims2_sql",
            dag=dag,
            job_name = glue_job_name,
            aws_conn_id=AWS_CONN_ID,
            script_args = get_glue_params( 
                {
                        "--extra-py-files": f"s3://{TDV_GLOBAL_CONFIG['glue_s3_bucket']}/{REPO_NAME}/dml/pvs-testing/claims2_sql.py", # python file name
                        "--py_file_name": "claims2_sql" # python file name without .py extension
                }
            ),
            run_job = True, # This triggers the glue job. Do not change
            
    )
    claims3_sql = CustomGlueJobOperator(
            task_id = "claims3_sql",
            dag=dag,
            job_name = glue_job_name,
            aws_conn_id=AWS_CONN_ID,
            script_args = get_glue_params( 
                {
                        "--extra-py-files": f"s3://{TDV_GLOBAL_CONFIG['glue_s3_bucket']}/{REPO_NAME}/dml/pvs-testing/claims3_sql.py", # python file name
                        "--py_file_name": "claims3_sql" # python file name without .py extension
                }
            ),
            run_job = True, # This triggers the glue job. Do not change
            
    )
   
    

    
    claims1_sql >> claims2_sql
    claims3_sql
