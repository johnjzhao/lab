# This DAG tests the ability to trigger SNS notifications upon failure of a DAG (or specific task).
# The AWS_CONN_ID must be configured in MWAA. The role specified within it must have sns:Publish permissions for the TARGET_SNS_TOPIC. 

from datetime import datetime
from airflow import DAG
from airflow import AirflowException
from airflow.operators.python_operator import PythonOperator
from airflow.providers.amazon.aws.operators.sns import SnsPublishOperator

AWS_CONN_ID = "oss_glue_connection"
TARGET_SNS_TOPIC = "arn:aws:sns:us-east-1:302619437920:tdv-oss-demo-notification" # in your repo, use a terraform variable

def send_failure_notification(context):
    op = SnsPublishOperator(
            task_id='send_failure_sns',
            target_arn=TARGET_SNS_TOPIC, 
            message='DAG failed. See Airflow logs for details.',
            aws_conn_id=AWS_CONN_ID
        )
    op.execute(context)

def fail_task():
    """Raise exception to cause task to fail. For testing purposes only."""
    raise AirflowException("Task Failure")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022, 1, 30),
    'on_failure_callback': send_failure_notification # sends notification if ANY of the tasks fail
    }
with DAG('tdv-oss-demo-test-SNS-dag',
    default_args=default_args,
    schedule_interval='0 0 * * *',
    catchup=False) as dag:

    test_task = PythonOperator(
                    task_id='test_task',
                    on_failure_callback=send_failure_notification, # sends notification if THIS task fails
                    python_callable=fail_task
                )

    test_task