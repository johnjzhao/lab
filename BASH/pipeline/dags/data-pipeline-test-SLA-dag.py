#-----PLEASE NOTE: The SLA Notifications via SNS in this DAG are NOT functional.------
# There are currently architectural issues with Airflow's "sla_miss_callback" parameter.
# Teams are welcome to try to make it work, however please note at this time, SNS notifications for SLAs
# are not supported. 
# SLA Miss logs can be viewed in the MWAA Console (Browse > SLA Misses). 

# This DAG tests the ability to trigger SNS notifications if one or more tasks exceed the specified SLA.
# The AWS_CONN_ID must be configured in MWAA. The role specified within it must have sns:Publish permissions for the TARGET_SNS_TOPIC. 

import time
from datetime import datetime, timedelta
from airflow import DAG
from airflow.models import SlaMiss
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.providers.amazon.aws.operators.sns import SnsPublishOperator


AWS_CONN_ID = "oss_glue_connection"
TARGET_SNS_TOPIC = "arn:aws:sns:us-east-1:302619437920:tdv-oss-demo-notification" # in your repo, use a terraform variable

def sla_miss_notification(dag, task_list, blocking_task_list, slas, blocking_tis): #(*args, **kwargs): #, context):
    print("missed SLA")
    # op = SnsPublishOperator(
    #         task_id='send_sla_sns',
    #         target_arn=TARGET_SNS_TOPIC, 
    #         message='DAG exceeded SLA. See Airflow logs for details.',
    #         aws_conn_id=AWS_CONN_ID
    #     )
    # op.execute(context)


def exceed_sla():
    """Function that takes 40 seconds to complete. For testing purposes only."""
    print("task is sleeping")
    time.sleep(35)
    print("task done sleeping")


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022, 1, 30),
    'sla': timedelta(seconds=20)
    }
with DAG('tdv-oss-demo-test-SLA-dag',
    default_args=default_args,
    schedule_interval='25 12 * * *',
    sla_miss_callback=sla_miss_notification,
    catchup=False) as dag:

    test_task = PythonOperator(
                    task_id='test_task',
                    python_callable=exceed_sla
                )

    test_task
