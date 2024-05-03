
module "pcs_member_enrollments_medicare_extract_glue_job" {
  source = "./modules/glue"

  cloudwatch_log_group_name = "/aws-glue/jobs/${var.gov_solutions_commissions_tdv_to_s3_pcs_member_enrollments_medicare_job}"
  retention_in_days         = 14

  name                = var.gov_solutions_commissions_tdv_to_s3_pcs_member_enrollments_medicare_job
  description         = "PCS Member Enrollments Coverage Data Extract Job"
  role_arn            = var.glue_role_arn
  max_capacity        = var.glue_max_capacity
  glue_version        = var.glue_version
  connections         = [var.aws_glue_connection.broker]
  timeout             = var.glue_job_timeout
  max_retries         = var.glue_max_retries
  script_location     = "s3://${var.artifacts_bucket}/${var.artifacts_bucket_script_key}/${var.gov_solutions_commissions_tdv_to_s3_pcs_member_enrollments_medicare_path}"
  python_version      = var.glue_python_version
  job_type            = "pythonshell"
  max_concurrent_runs = var.glue_max_concurrent_runs

  splunk_destination_arn = var.splunk_destination_arn

  arguments = tomap(
    {
      "--scriptLocation"       = "s3://${var.artifacts_bucket}/${var.artifacts_bucket_script_key}/${var.gov_solutions_commissions_tdv_to_s3_pcs_member_enrollments_medicare_path}"
      "--extra-py-files"       = "s3://${var.artifacts_bucket}/${var.artifacts_bucket_library_key}/teradatasql-17.10.0.1-py3-none-any.whl, s3://${var.artifacts_bucket}/${var.artifacts_bucket_library_key}/s3fs-2022.8.2-py3-none-any.whl, s3://${var.artifacts_bucket}/${var.artifacts_bucket_script_key}/connector.py,s3://${var.artifacts_bucket}/${var.artifacts_bucket_script_key}/logger.py"
      "--region_name"          = var.gov_solutions_commissions_glue_config.region_name
      "--host"                 = var.gov_solutions_commissions_glue_config.host
      "--sqlfile"              = var.glue_sql
      "--artifacts_bucket"     = var.artifacts_bucket
      "--artifacts_bucket_key" = var.artifacts_bucket_key
      "--user"                 = var.gov_solutions_commissions_glue_config.user
      "--tdv_env"              = var.environment
      "--tdv_secretsmanager"   = var.tdv_secretsmanager_id
      "--custom_log_group"     = "/aws-glue/jobs/${var.gov_solutions_commissions_tdv_to_s3_pcs_member_enrollments_medicare_job}"
      "--run_job_name"         = "tdv_to_s3_extract_member_enrollments_medicare_pshell"
      "--schema_reporting"     = var.schema_reporting
    }
  )

}

resource "aws_glue_crawler" "pcs_member_enrollments_medicare_cdo_mbr_demg_crawler" {
  database_name = var.aws_glue_catalog_database.name
  name          = "gov_solutions_commissions_pcs_member_enrollments_medicare_cdo_mbr_demg"
  role          = var.glue_role_arn
  s3_target {
    path = "s3://${var.artifacts_bucket}/${var.artifacts_bucket_key}/extracts/cdo_mbr_demg/"
  }
  tags = merge(var.cigna_common_tags,
    {
      "Name" = "gov_solutions_commissions_crawler"
    }
  )
}

resource "aws_glue_crawler" "pcs_member_medicare_dim_crawler" {
  database_name = var.aws_glue_catalog_database.name
  name          = "gov_solutions_commissions_pcs_member_medicare_dim"
  role          = var.glue_role_arn
  s3_target {
    #path = "s3://gov-solutions-commissions-artifacts-dev/artifactory/glue/extracts/pcs_member_medicare_dim/"
    path = "s3://${var.artifacts_bucket}/${var.artifacts_bucket_key}/test_data/MBR_MEDCR_DIM/"
  }
  tags = merge(var.cigna_common_tags,
    {
      "Name" = "gov_solutions_commissions_crawler"
    }
  )
}