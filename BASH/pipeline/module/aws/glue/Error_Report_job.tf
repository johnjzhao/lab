module "pcs_error_report_glue_job" {
  source = "./modules/glue"

  cloudwatch_log_group_name = "/aws-glue/jobs/${var.gov_solutions_commissions_pcs_error_report_job}"
  retention_in_days         = 14

  name                = var.gov_solutions_commissions_pcs_error_report_job
  description         = "PCS Error Report Job"
  role_arn            = var.glue_role_arn
  max_capacity        = var.glue_max_capacity
  glue_version        = var.glue_version
  connections         = [var.aws_glue_connection.broker]
  timeout             = var.glue_job_timeout
  max_retries         = var.glue_max_retries
  job_type            = "glueetl"
  max_concurrent_runs = var.glue_max_concurrent_runs
  script_location     = "s3://${var.artifacts_bucket}/${var.artifacts_bucket_script_key}/${var.gov_solutions_commissions_pcs_error_report_path}"
  python_version      = 3

  splunk_destination_arn = var.splunk_destination_arn

  arguments = tomap(
    {
      "--scriptLocation"       = "s3://${var.artifacts_bucket}/${var.artifacts_bucket_script_key}/${var.gov_solutions_commissions_pcs_error_report_path}"
      "--extra-py-files"       = "s3://${var.artifacts_bucket}/${var.artifacts_bucket_library_key}/teradatasql-17.10.0.1-py3-none-any.whl,s3://${var.artifacts_bucket}/${var.artifacts_bucket_library_key}/s3fs-2022.8.2-py3-none-any.whl,s3://${var.artifacts_bucket}/${var.artifacts_bucket_script_key}/connector.py,s3://${var.artifacts_bucket}/${var.artifacts_bucket_script_key}/logger.py"
      "--region_name"          = var.gov_solutions_commissions_glue_config.region_name
      "--host"                 = var.gov_solutions_commissions_glue_config.host
      "--sqlfile"              = var.glue_sql
      "--artifacts_bucket"     = var.artifacts_bucket
      "--artifacts_bucket_key" = var.artifacts_bucket_key
      "--user"                 = var.gov_solutions_commissions_glue_config.user
      "--tdv_env"              = var.environment
      "--tdv_secretsmanager"   = var.tdv_secretsmanager_id
      "--custom_log_group"     = "/aws-glue/jobs/${var.gov_solutions_commissions_pcs_error_report_job}"
      "--run_job_name"         = "pcs_error_report_spark"
    }
  )

}