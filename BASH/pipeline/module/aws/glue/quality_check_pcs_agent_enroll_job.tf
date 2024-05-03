module "pcs_agent_enrollments_quality_check_glue_job" {
  source = "./modules/glue"

  cloudwatch_log_group_name = "/aws-glue/jobs/${var.gov_solutions_commissions_quality_check_pcs_agent_enrollments_job}"
  retention_in_days         = 14

  name                = var.gov_solutions_commissions_quality_check_pcs_agent_enrollments_job
  description         = "PCS Agent Enrollments Quality Check Job"
  role_arn            = var.glue_role_arn
  max_capacity        = 2
  glue_version        = var.glue_version
  connections         = [var.aws_glue_connection.broker]
  timeout             = var.glue_job_timeout
  max_retries         = var.glue_max_retries
  script_location     = "s3://${var.artifacts_bucket}/${var.artifacts_bucket_script_key}/${var.gov_solutions_commissions_quality_check_pcs_agent_enrollments_path}"
  python_version      = 3
  job_type            = "glueetl"
  max_concurrent_runs = var.glue_max_concurrent_runs

  splunk_destination_arn = var.splunk_destination_arn

  arguments = tomap(
    {
      "--scriptLocation"       = "s3://${var.artifacts_bucket}/${var.artifacts_bucket_script_key}/${var.gov_solutions_commissions_quality_check_pcs_agent_enrollments_path}"
      "--extra-py-files"       = "s3://${var.artifacts_bucket}/${var.artifacts_bucket_library_key}/teradatasql-17.10.0.1-py3-none-any.whl,s3://${var.artifacts_bucket}/${var.artifacts_bucket_library_key}/s3fs-2022.8.2-py3-none-any.whl,s3://${var.artifacts_bucket}/${var.artifacts_bucket_script_key}/connector.py,s3://${var.artifacts_bucket}/${var.artifacts_bucket_script_key}/logger.py"
      "--region_name"          = var.gov_solutions_commissions_glue_config.region_name
      "--host"                 = var.gov_solutions_commissions_glue_config.host
      "--sqlfile"              = var.glue_sql
      "--artifacts_bucket"     = var.artifacts_bucket
      "--artifacts_bucket_key" = var.artifacts_bucket_key
      "--user"                 = var.gov_solutions_commissions_glue_config.user
      "--tdv_env"              = var.environment
      "--tdv_secretsmanager"   = var.tdv_secretsmanager_id
      "--custom_log_group"     = "/aws-glue/jobs/${var.gov_solutions_commissions_quality_check_pcs_agent_enrollments_job}"
      "--run_job_name"         = "quality_check_pcs_agent_enrollments_spark"
    }
  )

}

resource "aws_glue_crawler" "pcs_quality_results_general_crawler" {
  database_name = var.aws_glue_catalog_database.name
  name          = "gov_solutions_commissions_pcs_quality_results_general"
  role          = var.glue_role_arn
  recrawl_policy {
    recrawl_behavior = "CRAWL_NEW_FOLDERS_ONLY"
  }
  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "LOG"
  }

  s3_target {
    path = "s3://${var.artifacts_bucket}/${var.artifacts_bucket_key}/quality_results/pcs/pcs_weekly_enr_quality_general_stats"
  }
  tags = merge(var.cigna_common_tags,
    {
      "Name" = "gov_solutions_commissions_crawler"
    }
  )
}

resource "aws_glue_crawler" "pcs_quality_results_formats_crawler" {
  database_name = var.aws_glue_catalog_database.name
  name          = "gov_solutions_commissions_pcs_quality_results_formats"
  role          = var.glue_role_arn
  recrawl_policy {
    recrawl_behavior = "CRAWL_NEW_FOLDERS_ONLY"
  }
  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "LOG"
  }

  s3_target {
    path = "s3://${var.artifacts_bucket}/${var.artifacts_bucket_key}/quality_results/pcs/pcs_weekly_enr_quality_formats"
  }
  tags = merge(var.cigna_common_tags,
    {
      "Name" = "gov_solutions_commissions_crawler"
    }
  )
}

