
module "broker_comm_sircon_extract_glue_job" {
  source = "./modules/glue"

  cloudwatch_log_group_name = "/aws-glue/jobs/${var.gov_solutions_commissions_tdv_to_s3_broker_comm_sircon_job}"
  retention_in_days         = 14

  name                = var.gov_solutions_commissions_tdv_to_s3_broker_comm_sircon_job
  description         = "Broker Commissions Sircon Job"
  role_arn            = var.glue_role_arn
  max_capacity        = var.glue_max_capacity
  glue_version        = var.glue_version
  connections         = [var.aws_glue_connection.broker]
  timeout             = var.glue_job_timeout
  max_retries         = var.glue_max_retries
  script_location     = "s3://${var.artifacts_bucket}/${var.artifacts_bucket_script_key}/${var.gov_solutions_commissions_tdv_to_s3_broker_comm_sircon_path}"
  python_version      = var.glue_python_version
  job_type            = "pythonshell"
  max_concurrent_runs = var.glue_max_concurrent_runs

  splunk_destination_arn = var.splunk_destination_arn

  arguments = tomap(
    {
      "--scriptLocation"           = "s3://${var.artifacts_bucket}/${var.artifacts_bucket_script_key}/${var.gov_solutions_commissions_tdv_to_s3_broker_comm_sircon_path}"
      "--extra-py-files"           = "s3://${var.artifacts_bucket}/${var.artifacts_bucket_library_key}/teradatasql-17.10.0.1-py3-none-any.whl, s3://${var.artifacts_bucket}/${var.artifacts_bucket_library_key}/s3fs-2022.8.2-py3-none-any.whl, s3://${var.artifacts_bucket}/${var.artifacts_bucket_script_key}/connector.py,s3://${var.artifacts_bucket}/${var.artifacts_bucket_script_key}/logger.py"
      "--region_name"              = var.gov_solutions_commissions_glue_config.region_name
      "--host"                     = var.gov_solutions_commissions_glue_config.host
      "--sqlfile"                  = var.glue_sql
      "--artifacts_bucket"         = var.artifacts_bucket
      "--artifacts_bucket_key"     = var.artifacts_bucket_key
      "--user"                     = var.gov_solutions_commissions_glue_config.user
      "--tdv_env"                  = var.environment
      "--tdv_secretsmanager"       = var.tdv_secretsmanager_id
      "--custom_log_group"         = "/aws-glue/jobs/${var.gov_solutions_commissions_tdv_to_s3_broker_comm_sircon_job}"
      "--schema_trxhub"            = var.schema_trxhub
      "--schema_sales_commission"  = var.schema_sales_commission
      "--schema_datamart_reftable" = var.schema_datamart_reftable
    }
  )

}

resource "aws_glue_crawler" "pcs_broker_comm_sircon_crawler" {
  database_name = var.aws_glue_catalog_database.name
  name          = "gov_solutions_commissions_pcs_broker_comm_sircon"
  role          = var.glue_role_arn
  s3_target {
    path = "s3://${var.artifacts_bucket}/${var.artifacts_bucket_key}/extracts/broker_comm_sircon/"
  }
  tags = merge(var.cigna_common_tags,
    {
      "Name" = "gov_solutions_commissions_crawler"
    }
  )
}