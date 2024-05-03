
# Data Pipeline for Terradata Vantage AWS & Data Lake automation

  

Please see [this confluence page](https://confluence.sunvalle.net/display/IM/User+Documentation+for+the+TDV+Superpipeline) for more information on how to use this repo.

  

## Project specific details

  

**Dataset**: OSS

  

**DEV SNS Topic ARN :**  arn:aws:sns:us-east-1:302619437920:data-pipeline-notification

  

**TEST SNS Topic ARN :**  arn:aws:sns:us-east-1:302619437920:data-pipeline-notification

  

**PROD SNS Topic ARN :**  arn:aws:sns:us-east-1:355113922316:data-pipeline-notification

  

**Checkmarx App profile:**  data-pipeline

  

**Glue Execution Role:**  ad-data-services-DATA-PIPELINE-GLUE-ROLE

  

**Jenkins jobs:**  https://orchestrator1.orchestrator-v2.sunvalle.net/job/orchestrators-folders/job/enterprise360/job/360-data-services/job/TDV/job/TDV-SuperPipeline/job/data-pipeline/

  

**Team Email:**  support@sunvalle.net


**AIRFLOW_AWS_CONNECTION:** oss_glue_connection

  

## Branching Strategy
main->feature

feature->test

feature->release

release->main
