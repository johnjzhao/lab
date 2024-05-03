
module "test_conn_glue_job" {
  source = "./modules/glue"

  cloudwatch_log_group_name = "/aws-glue/jobs/${var.gov_solutions_commissions_test_conn_job}"
  retention_in_days         = 14

  name                = var.gov_solutions_commissions_test_conn_job
  description         = "Commissions TDV Connection Test Job"
  role_arn            = var.glue_role_arn
  max_capacity        = var.glue_max_capacity
  glue_version        = var.glue_version
  connections         = [var.aws_glue_connection.broker]
  timeout             = var.glue_job_timeout
  max_retries         = var.glue_max_retries
  script_location     = "s3://${var.artifacts_bucket}/${var.artifacts_bucket_script_key}/${var.gov_solutions_commissions_test_conn_path}"
  python_version      = var.glue_python_version
  job_type            = "pythonshell"
  max_concurrent_runs = var.glue_max_concurrent_runs

  splunk_destination_arn = var.splunk_destination_arn

  arguments = tomap(
    {
      "--scriptLocation"     = "s3://${var.artifacts_bucket}/${var.artifacts_bucket_script_key}/${var.gov_solutions_commissions_test_conn_path}"
      "--extra-py-files"     = "s3://${var.artifacts_bucket}/${var.artifacts_bucket_library_key}/teradatasql-17.10.0.1-py3-none-any.whl, s3://${var.artifacts_bucket}/${var.artifacts_bucket_library_key}/s3fs-2022.8.2-py3-none-any.whl, s3://${var.artifacts_bucket}/${var.artifacts_bucket_script_key}/connector.py,s3://${var.artifacts_bucket}/${var.artifacts_bucket_script_key}/logger.py"
      "--region_name"        = var.gov_solutions_commissions_glue_config.region_name
      "--host"               = var.gov_solutions_commissions_glue_config.host
      "--user"               = var.gov_solutions_commissions_glue_config.user
      "--tdv_env"            = var.environment
      "--tdv_secretsmanager" = var.tdv_secretsmanager_id
    }
  )

}