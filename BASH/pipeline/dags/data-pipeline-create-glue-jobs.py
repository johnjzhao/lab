from airflow.providers.amazon.aws.operators.glue import AwsGlueJobOperator
from datetime import datetime, timedelta
from airflow import DAG
from dependencies.glue_plugin import CustomGlueJobOperator
import json
from airflow.models import Variable
from airflow.providers.amazon.aws.operators.sns import SnsPublishOperator

REPO_NAME = 'tdv-oss-demo' # put repo name here
AWS_CONN_ID = "oss_glue_connection" # Provided in your readme.md file
TARGET_SNS_TOPIC = "arn:aws:sns:us-east-1:302619437920:tdv-oss-demo-notification" # Provided in your readme.md file
TDV_GLOBAL_CONFIG = Variable.get("tdv_global_config", deserialize_json=True) # imported from Airflow (see Admin > Variables in the console).
# Value:  	
#       { "env":"dev", 
#         "host":"awstddev.sunvalle.net", 
#         "logmech": "LDAP", 
#         "glue_s3_bucket": "da-ent360-tdv-gluescript-dev", 
#         "teradatasql_library_path": "s3://da-ent360-config-scripts-dev/python-libraries-3/teradatasql-17.10.0.2-py3-none-any.whl", 
#         "glue_connections": ["da-ent360-Redshift-Connection-5","da-ent360-Redshift-Connection-4","da-ent360-Redshift-Connection-3","da-ent360-Redshift-Connection-2","da-ent360-Redshift-Connection-1"] }

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
    'on_failure_callback': send_failure_notification # sends notification if ANY of the tasks fail
}

dag_id = f'{REPO_NAME}-create-glue-jobs' # ALL DAG_IDs MUST begin with the REPO NAME, i.e. if repo name is 'tdv-oss-demo', dag_id = 'tdv-oss-demo-create-glue-jobs'
glue_job_name = f'{REPO_NAME}' # ALL GLUE JOBS MUST begin with the REPO NAME
region_name = "us-east-1" # keep as is
glue_iam_role = "ad-data-services-TDV-OSS-DEMO-GLUE-ROLE" # Provided in your readme.md file.

script_path = f"s3://{TDV_GLOBAL_CONFIG['glue_s3_bucket']}/{REPO_NAME}/scripts/tdv_glue_runner.py" # If you wish to use our pre-made script, keep this as is. 
# Or create your own script and put it under 'scripts/' in your repo, then update this path.

# Change the tags accordingly for your project
tags = {
    "AsaqId": "ASAQ-377943",
    "AssetOwner": "Bob.Krass@sunvalle.net",
    "CiId": "Enterprise 360-AWS",
    "CostCenter": "00079729",
    "DataSubjectArea": "claim:client:clinical:customer:producer:provider:pharmacy",
    "Frequency": "adhoc",
    "JobType": "Hist",
    "Module": "tdv",
    "Project": "common",
    "SecurityReviewID": "ASAQ-377943",
    "ServiceNowAS": "AS017902",
    "ServiceNowBA": "BA12353"
}

with DAG(dag_id = dag_id, default_args = default_args, schedule_interval = None) as dag:
    create_glue_job1 = CustomGlueJobOperator(
            task_id = "create_glue_job",
            job_name = glue_job_name,
            job_desc = f"glue job {glue_job_name}",
            iam_role_name = glue_iam_role,
            dag = dag,
            aws_conn_id=AWS_CONN_ID,
            s3_logs_bucket=TDV_GLOBAL_CONFIG["glue_s3_bucket"],
            command = {
                    'Name': 'pythonshell',
                    'ScriptLocation': script_path,
                    'PythonVersion': '3'
            },
            tags = tags,
            create_job = True, # This creates the glue job. Do not change
            connections=TDV_GLOBAL_CONFIG["glue_connections"]
    )


   

