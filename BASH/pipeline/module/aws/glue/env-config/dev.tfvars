#AWS CLI Profile to use for Terraform. SAML by default.
profile           = "saml"
alarm_environment = "dev"
environment       = "dev"

glue_role_arn = "arn:aws:iam::215132885729:role/Enterprise/GBSBROKERGLUE"

# GLUE JOB NAMES
gov_solutions_commissions_tdv_to_s3_member_dim_job                                     = "job_gov_solutions_commissions_tdv_to_s3_member_dim"
gov_solutions_commissions_data_load_s3_to_tdv_job                                      = "gov_solutions_commissions_data_load_s3_to_tdv_job"
gov_solutions_commissions_tdv_to_s3_broker_comm_sircon_job                             = "gov_solutions_commissions_tdv_to_s3_broker_comm_sircon_job"
gov_solutions_commissions_tdv_to_s3_pcs_member_enrollments_coverage_job                = "gov_solutions_commissions_tdv_to_s3_pcs_member_enrollments_coverage_job"
gov_solutions_commissions_tdv_to_s3_pcs_member_enrollments_medicare_job                = "gov_solutions_commissions_tdv_to_s3_pcs_member_enrollments_medicare_job"
gov_solutions_commissions_quality_check_evolve_member_enrollments_job                  = "gov_solutions_commissions_quality_check_evolve_member_enrollments_job"
gov_solutions_commissions_tdv_to_s3_evolve_memberp_job                                 = "gov_solutions_commissions_tdv_to_s3_evolve_memberp_job"
gov_solutions_commissions_tdv_to_s3_evolve_membere_job                                 = "gov_solutions_commissions_tdv_to_s3_evolve_membere_job"
gov_solutions_commissions_gameday_job                                                  = "gov_solutions_commissions_gameday_job"
gov_solutions_commissions_transform_pcs_weekly_agent_enrollment_transactions_job       = "gov_solutions_commissions_transform_pcs_weekly_agent_enrollment_transactions_job"
gov_solutions_commissions_s3_to_tdv_data_load_job                                      = "gov_solutions_commissions_s3_to_tdv_data_load_job"
gov_solutions_commissions_pcs_error_report_job                                         = "gov_solutions_commissions_pcs_error_report_job"
gov_solutions_commissions_quality_check_pcs_agent_enrollments_job                      = "gov_solutions_commissions_quality_check_pcs_agent_enrollments_job"
gov_solutions_commissions_test_conn_job                                                = "gov_solutions_commissions_test_conn_job"
gov_solutions_commissions_tdv_to_s3_pcs_error_report_job                               = "gov_solutions_commissions_tdv_to_s3_pcs_error_report_job"
gov_solutions_commissions_transform_evolve_memberp_membere_enrollment_transactions_job = "gov_solutions_commissions_transform_evolve_memberp_membere_enrollment_transactions_job"
gov_solutions_commissions_tdv_to_s3_pcs_member_sales_agent_job                         = "gov_solutions_commissions_tdv_to_s3_pcs_member_sales_agent_job"
gov_solutions_commissions_quality_check_evolve_member_policies_job                     = "gov_solutions_commissions_quality_check_evolve_member_policies_job"

# SCRIPT PATHS
gov_solutions_commissions_tdv_to_s3_pcs_error_report_path                               = "tdv_to_s3_extract_pcs_error_report_pshell.py"
gov_solutions_commissions_pcs_error_report_path                                         = "Error_Report.py"
gov_solutions_commissions_tdv_to_s3_mem_dim_path                                        = "tdv_to_s3_extract_member_dimension_pshell.py"
gov_solutions_commissions_data_load_s3_to_tdv_path                                      = "s3_to_tdv_data_load_pshell.py"
gov_solutions_commissions_tdv_to_s3_broker_comm_sircon_path                             = "tdv_to_s3_extract_broker_commissions_sircon_pshell.py"
gov_solutions_commissions_tdv_to_s3_pcs_member_enrollments_coverage_path                = "tdv_to_s3_extract_member_enrollments_coverage_pshell.py"
gov_solutions_commissions_tdv_to_s3_pcs_member_enrollments_medicare_path                = "tdv_to_s3_extract_member_enrollments_medicare_pshell.py"
gov_solutions_commissions_quality_check_evolve_member_enrollments_path                  = "quality_check_evolve_member_enrollments.py"
gov_solutions_commissions_tdv_to_s3_evolve_memberp_path                                 = "tdv_to_s3_extract_member_dimension_evolve_pshell.py"
gov_solutions_commissions_tdv_to_s3_evolve_membere_path                                 = "tdv_to_s3_extract_member_enrollment_evolve_pshell.py"
gov_solutions_commissions_gameday_path                                                  = "gameday.py"
gov_solutions_commissions_transform_pcs_weekly_agent_enrollment_transactions_path       = "transform/transform_pcs_weekly_enrollment_transactions_spark.py"
gov_solutions_commissions_s3_to_tdv_data_load_path                                      = "s3_to_tdv_data_load_pshell.py"
gov_solutions_commissions_quality_check_pcs_agent_enrollments_path                      = "quality_check_pcs_agent_enrollments.py"
gov_solutions_commissions_test_conn_path                                                = "test_wrapper.py"
gov_solutions_commissions_transform_evolve_memberp_membere_enrollment_transactions_path = "transform/transform_evolve_memberp_membere_enrollment_transactions_spark.py"
gov_solutions_commissions_tdv_to_s3_member_sales_agent_path                             = "tdv_to_s3_extract_member_sales_agent_pshell.py"
gov_solutions_commissions_quality_check_evolve_member_policies_path                     = "quality_check_evolve_member_policies.py"

# BUCKET NAMES AND KEYS
artifacts_bucket             = "gov-solutions-commissions-artifacts-dev"
artifacts_bucket_key         = "artifactory/glue"
artifacts_bucket_script_key  = "artifactory/glue/python"
artifacts_bucket_library_key = "artifactory/glue/library"

vendor_bucket = "evolve-commissions-bucket-dev"


# KMS Alias
kmsaliasname = "gov-solutions-commissions-tdv"

# CONFIG
gov_solutions_commissions_glue_config = {
  region_name = "us-east-1"
  host        = "awstddev.sys.cigna.com"
  user        = "SVTGOVPRODUCERDEV"
}

aws_glue_connection = {
  broker = "gov_solutions_commissions_glue_tdv_connection"
}

aws_glue_catalog_database = {
  name = "gov-solutions-commissions-evolve-dev"
}

glue_sql = "test_sql.sql"

# SECRETS
tdv_ssm = "gov-solutions-commissions-tdv-secret-dev"

tdv_secretsmanager_id = "gov-solutions-commissions-tdv-secret-dev"

# ALARMS
alarm_arn = ["arn:aws:sns:us-east-1:929468956630:cloudwatch-alarm-funnel"]

alert_funnel_app_name = "Gov-Solutions-Commissions"

# EXTRAS
b2b_queue_aws_account = "250022877901"

splunk_destination_arn = "arn:aws:logs:us-east-1:746770431074:destination:CentralizedLogging-v2-Destination"

# SCHEMAS
schema_trxhub = "TRXHUB_CORE_INT_V"

schema_sales_commission = "SALES_COMMISSION_CORE_INT_V"

schema_datamart_reftable = "DATAMART_REFTABLE_INT_V"

schema_datamart_member = "DATAMART_REFTABLE_INT_V"

schema_reporting = "REPORTING_INT_V"