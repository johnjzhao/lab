
module "pcs_weekly_agent_enrollment_transactions_transform_glue_job" {
  source = "./modules/glue"

  cloudwatch_log_group_name = "/aws-glue/jobs/${var.gov_solutions_commissions_transform_pcs_weekly_agent_enrollment_transactions_job}"
  retention_in_days         = 14

  name                = var.gov_solutions_commissions_transform_pcs_weekly_agent_enrollment_transactions_job
  description         = "PCS Weekly Sales Agent Enrollments Transaction Transformation Job"
  role_arn            = var.glue_role_arn
  max_capacity        = "4"
  glue_version        = var.glue_version
  connections         = [var.aws_glue_connection.broker]
  timeout             = var.glue_job_timeout
  max_retries         = var.glue_max_retries
  job_type            = "glueetl"
  max_concurrent_runs = var.glue_max_concurrent_runs
  script_location     = "s3://${var.artifacts_bucket}/${var.artifacts_bucket_script_key}/${var.gov_solutions_commissions_transform_pcs_weekly_agent_enrollment_transactions_path}"
  python_version      = "3"

  splunk_destination_arn = var.splunk_destination_arn

  arguments = tomap(
    {
      "--scriptLocation"        = "s3://${var.artifacts_bucket}/${var.artifacts_bucket_script_key}/${var.gov_solutions_commissions_transform_pcs_weekly_agent_enrollment_transactions_path}"
      "--extra-py-files"        = "s3://${var.artifacts_bucket}/${var.artifacts_bucket_library_key}/teradatasql-17.10.0.1-py3-none-any.whl,s3://${var.artifacts_bucket}/${var.artifacts_bucket_library_key}/s3fs-2022.8.2-py3-none-any.whl,s3://${var.artifacts_bucket}/${var.artifacts_bucket_script_key}/connector.py,s3://${var.artifacts_bucket}/${var.artifacts_bucket_script_key}/logger.py"
      "--region_name"           = var.gov_solutions_commissions_glue_config.region_name
      "--host"                  = var.gov_solutions_commissions_glue_config.host
      "--sqlfile"               = var.glue_sql
      "--artifacts_bucket"      = var.artifacts_bucket
      "--artifacts_bucket_key"  = var.artifacts_bucket_key
      "--user"                  = var.gov_solutions_commissions_glue_config.user
      "--tdv_env"               = var.environment
      "--tdv_secretsmanager"    = var.tdv_secretsmanager_id
      "--custom_log_group"      = "/aws-glue/jobs/${var.gov_solutions_commissions_transform_pcs_weekly_agent_enrollment_transactions_job}"
      "--run_job_name"          = "transform_pcs_weekly_enrollment_transactions_spark"
      "--glue_catalog_database" = var.aws_glue_catalog_database.name
    }
  )
}

resource "aws_glue_crawler" "pcs_weekly_agent_enrollment_transactions_report_crawler" {
  database_name = var.aws_glue_catalog_database.name
  name          = "gov_solutions_commissions_pcs_weekly_agent_enrollment_transactions_report"
  role          = var.glue_role_arn
  s3_target {
    path = "s3://gov-solutions-commissions-artifacts-dev/artifactory/glue/transform/pcs/pcs_weekly_agent_enrollment_transactions_report/"
  }
  tags = merge(var.cigna_common_tags,
    {
      "Name" = "gov_solutions_commissions_crawler"
    }
  )
}

resource "aws_glue_crawler" "pcs_weekly_enrollment_transactions_reporting_t_cdo_mbr_demg_crawler" {
  database_name = var.aws_glue_catalog_database.name
  name          = "gov_solutions_commissions_pcs_weekly_enrollment_transactions_reporting_t_cdo_mbr_demg"
  role          = var.glue_role_arn
  s3_target {
    path = "s3://gov-solutions-commissions-artifacts-dev/artifactory/glue/test_data/report_t_cdo_mbr_demg/"
  }
  tags = merge(var.cigna_common_tags,
    {
      "Name" = "gov_solutions_commissions_crawler"
    }
  )
}

resource "aws_glue_crawler" "pcs_report_t_member_enrollments_coverage_crawler" {
  database_name = var.aws_glue_catalog_database.name
  name          = "gov_solutions_commissions_pcs_report_t_member_enrollments_coverage"
  role          = var.glue_role_arn
  s3_target {
    path = "s3://gov-solutions-commissions-artifacts-dev/artifactory/glue/test_data/pcs_report_t_member_enrollments_coverage/"
  }
  tags = merge(var.cigna_common_tags,
    {
      "Name" = "gov_solutions_commissions_crawler"
    }
  )
}

resource "aws_glue_crawler" "pcs_weekly_enrollment_transactions_intrnl_hlth_pln_chng_crawler" {
  database_name = var.aws_glue_catalog_database.name
  name          = "gov_solutions_commissions_pcs_weekly_enrollment_transactions_intrnl_hlth_pln_chng"
  role          = var.glue_role_arn
  s3_target {
    path = "s3://gov-solutions-commissions-artifacts-dev/artifactory/glue/test_data/intrnl_hlth_pln_chng/"
  }
  tags = merge(var.cigna_common_tags,
    {
      "Name" = "gov_solutions_commissions_crawler"
    }
  )
}

resource "aws_glue_crawler" "pcs_cms_trans_reply_dim_crawler" {
  database_name = var.aws_glue_catalog_database.name
  name          = "gov_solutions_commissions_pcs_cms_trans_reply_dim"
  role          = var.glue_role_arn
  s3_target {
    path = "s3://gov-solutions-commissions-artifacts-dev/artifactory/glue/test_data/cms_trans_reply_dim/"
  }
  tags = merge(var.cigna_common_tags,
    {
      "Name" = "gov_solutions_commissions_crawler"
    }
  )
}
