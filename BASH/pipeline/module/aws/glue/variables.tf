/*
    Variable declarations. These default values should not be modified
    To set these vars, update the vpc.auto.tfvars file
*/

variable "profile" {
  description = "The AWS profile to use"
  type        = string
  default     = "saml"
}


variable "required_common_tags" {
  description = "Map of required resource tags for AWS"
  type        = map(string)
  default = {
    CostCenter       = "01567"
    AssetOwner       = "thesprinters@Cigna.com"
    ServiceNowBA     = "BA17057"
    ServiceNowAS     = "AS040440"
    SecurityReviewID = "RITM4181504"
    AsaqId           = "RITM4181504"
    CiId             = "notApplicable"
  }

}

variable "required_data_tags" {
  description = "Map of required data resource tags for AWS"
  type        = map(string)
  default = {
    BusinessEntity         = "usMedical"
    LineOfBusiness         = "None"
    DataClassification     = "None"
    ComplianceDataCategory = "None"
    DataSubjectArea        = "None"
    DataRetention          = "None"
  }
}

variable "additional_data_tags" {
  description = "Additional resource tags"
  type        = map(string)
  default     = {}
}

variable "environment" {
  description = "Environment we're operating, e.g. dev, test, etc."
  type        = string
  default     = "dev"
}

variable "cigna_common_tags" {
  description = "Map of tags required for AWS resources for Cigna compliance purposes"
  type        = map(string)
}

variable "cigna_data_tags" {
  description = "Map of tags required for AWS resources for Cigna compliance purposes"
  type        = map(string)
}

variable "required_tags" {
  description = "Map of tags required for AWS resources for Cigna compliance purposes"
  type        = map(string)
}

#######################################################################
#                         BUCKET AND KEYS
#######################################################################

variable "artifacts_bucket" {
  description = "Artifacts bucket"
  type        = string
}

variable "artifacts_bucket_key" {
  description = "Artifacts bucket Key"
  type        = string
}

variable "artifacts_bucket_library_key" {
  description = "Artifacts bucket Library Key"
  type        = string
}

variable "artifacts_bucket_script_key" {
  description = "Artifacts bucket Scripts Key"
  type        = string
}

variable "vendor_bucket" {
  description = "Vendor bucket"
  type        = string
}

variable "tfstate_bucket" {
  description = "A string with the name of the bucket containing  tfstate files"
  type        = string
}

variable "tfstate_path" {
  description = "A string with the name of the key for VPC tfstate file"
  type        = string
}

variable "kmsaliasname" {
  description = "KMS Alias Name"
  type        = string
}

#######################################################################
#                          GLUE CONFIG
#######################################################################

variable "glue_max_capacity" {
  type    = string
  default = "1"
}

variable "worker_type" {
  type    = string
  default = "G.1X"
}

variable "number_of_workers" {
  type    = string
  default = "4"
}

variable "glue_version" {
  type    = string
  default = "3.0"
}

variable "glueetl_version" {
  type    = string
  default = "3"
}

variable "glue_job_timeout" {
  type    = string
  default = "300"
}

variable "glue_max_retries" {
  type    = string
  default = "0"
}

variable "glue_python_version" {
  default = 3.9
}

variable "glue_max_concurrent_runs" {
  type    = string
  default = "1"
}

variable "glue_role_arn" {
  description = "glue_role_arn created by RAAS for bids rewrite"
  type        = string
}

variable "description" {
  type    = string
  default = "Glue job description"
}

variable "glue_default_arguments" {
  type = map(string)
  default = {
    "--job-bookmark-option"              = "job-bookmark-enable"
    "--enable-metrics"                   = "true"
    "--job-language"                     = "Python"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-continuous-log-filter"     = "true"
  }
}

variable "gov_solutions_commissions_glue_config" {
  description = "Variable for Glue Connection"
  type = object({
    region_name = string
    host        = string
    user        = string
  })
}

variable "aws_glue_connection" {
  type = object({
    broker = string
  })
  description = "Connection for jobs"
}

variable "glue_sql" {
  description = "String representing the name of sql script"
  type        = string
}

#######################################################################
#                       GLUE JOB NAMES
#######################################################################
variable "gov_solutions_commissions_tdv_to_s3_pcs_error_report_job" {
  description = "Unique name to identify your glue job."
  type        = string
}

variable "gov_solutions_commissions_pcs_error_report_job" {
  description = "Unique name to identify your glue job."
  type        = string
}

variable "gov_solutions_commissions_tdv_to_s3_member_dim_job" {
  description = "Unique name to identify your glue job."
  type        = string
}

variable "gov_solutions_commissions_tdv_to_s3_broker_comm_sircon_job" {
  description = "Unique name to identify your glue job for broker commissions sircon."
  type        = string
}

variable "gov_solutions_commissions_data_load_s3_to_tdv_job" {
  description = "Unique name to identify your glue job."
  type        = string
}

variable "gov_solutions_commissions_tdv_to_s3_pcs_member_enrollments_coverage_job" {
  description = "Unique name to identify your glue job."
  type        = string
}

variable "gov_solutions_commissions_tdv_to_s3_pcs_member_enrollments_medicare_job" {
  description = "Unique name to identify your glue job."
  type        = string
}

variable "gov_solutions_commissions_tdv_to_s3_pcs_member_sales_agent_job" {
  description = "Unique name to identify your glue job."
  type        = string
}

variable "gov_solutions_commissions_tdv_to_s3_evolve_memberp_job" {
  description = "Unique name to identify the member P Evolve TDV to S3 Parquet File Extract glue job."
  type        = string
}

variable "gov_solutions_commissions_tdv_to_s3_evolve_membere_job" {
  description = "Unique name to identify the member E Evolve TDV to S3 Parquet File Extract glue job."
  type        = string
}

variable "gov_solutions_commissions_quality_check_evolve_member_enrollments_job" {
  description = "Unique name to identify your glue job."
  type        = string
}

variable "gov_solutions_commissions_quality_check_evolve_member_policies_job" {
  description = "Unique name to identify your glue job."
  type        = string
}

variable "gov_solutions_commissions_quality_check_pcs_agent_enrollments_job" {
  description = "Unique name to identify your glue job."
  type        = string
}

variable "gov_solutions_commissions_gameday_job" {
  description = "Unique name to identify test job for Gameday"
  type        = string
}

variable "gov_solutions_commissions_transform_pcs_weekly_agent_enrollment_transactions_job" {
  description = "Unique name to identify your glue job."
  type        = string
}

variable "gov_solutions_commissions_s3_to_tdv_data_load_job" {
  description = "Unique name to identify your glue job."
  type        = string
}

variable "gov_solutions_commissions_test_conn_job" {
  description = "Unique name to identify your glue job."
  type        = string
}

variable "gov_solutions_commissions_transform_evolve_memberp_membere_enrollment_transactions_job" {
  description = "Glue etl job which creates the memberp and membere files which are sent to Evolve."
  type        = string
}

#######################################################################
#                       GLUE JOB SCRIPT PATHS
#######################################################################
variable "gov_solutions_commissions_tdv_to_s3_pcs_error_report_path" {
  description = "Unique name to identify script path for tdv to s3 member enrollments medicare related data extract script path"
  type        = string
}

variable "gov_solutions_commissions_pcs_error_report_path" {
  description = "Unique name to identify script path for tdv to s3 member enrollments medicare related data extract script path"
  type        = string
}

variable "gov_solutions_commissions_tdv_to_s3_pcs_member_enrollments_medicare_path" {
  description = "Unique name to identify script path for tdv to s3 member enrollments medicare related data extract script path"
  type        = string
}

variable "gov_solutions_commissions_tdv_to_s3_mem_dim_path" {
  description = "Unique name to identify script path for tdv to s3 member dim extract job"
  type        = string
}

variable "gov_solutions_commissions_tdv_to_s3_member_sales_agent_path" {
  description = "Unique name to identify script path for tdv to s3 member sales agent extract job"
  type        = string
}

variable "gov_solutions_commissions_data_load_s3_to_tdv_path" {
  description = "Unique name to identify script path for s3 to tdv load job"
  type        = string
}

variable "gov_solutions_commissions_tdv_to_s3_broker_comm_sircon_path" {
  description = "Unique name to identify script path for tdv to s3 broker commissions sircon job"
  type        = string
  default     = "Glue job description"
}

variable "gov_solutions_commissions_quality_check_evolve_member_enrollments_path" {
  description = "Unique name to identify script path for quality check pcs agent enrollments job"
  type        = string
}

variable "gov_solutions_commissions_quality_check_evolve_member_policies_path" {
  description = "Unique name to identify script path for quality check pcs agent enrollments job"
  type        = string
}

variable "gov_solutions_commissions_quality_check_pcs_agent_enrollments_path" {
  description = "Unique name to identify script path for quality check evolve member enrollments job"
  type        = string
}

variable "gov_solutions_commissions_tdv_to_s3_evolve_memberp_path" {
  description = "Unique name to identify script path for Member P TDV to S3 Parquet File Glue job"
  type        = string
}

variable "gov_solutions_commissions_tdv_to_s3_evolve_membere_path" {
  description = "Unique name to identify script path for Member E TDV to S3 Parquet File Glue job"
  type        = string
}

variable "gov_solutions_commissions_transform_pcs_weekly_agent_enrollment_transactions_path" {
  description = "Unique name to identify script path for Glue Tr"
  type        = string
}

variable "gov_solutions_commissions_tdv_to_s3_pcs_member_enrollments_coverage_path" {
  description = "Unique name to identify script path for tdv to s3 member enrollments coverage extract job"
  type        = string
}

variable "gov_solutions_commissions_gameday_path" {
  description = "Unique name to identify script path for Gameday testing job"
  type        = string
}

variable "gov_solutions_commissions_s3_to_tdv_data_load_path" {
  description = "Unique name to identify script path for S3 To TDV Data load script path"
  type        = string
}

variable "gov_solutions_commissions_test_conn_path" {
  description = "Unique name to identify script path for tdv connection testing script"
  type        = string
}

variable "gov_solutions_commissions_transform_evolve_memberp_membere_enrollment_transactions_path" {
  description = "Unique name to identify script path for the creation of the memberp and membere files for Evolve Glue ETL extract job"
  type        = string
}

#######################################################################
#                     CRAWLERS AND CATALOG DATABASE
#######################################################################

variable "aws_glue_catalog_database" {
  type = object({
    name = string
  })
  description = "Glue Catalog Database"
}

#######################################################################
#                              ALARMS
#######################################################################

variable "alarm_environment" {
  description = "String representing the deployment environment"
  type        = string
}

variable "alarm_arn" {
  description = "The SNS Topic to send alerts to the funnel"
  type        = list(string)
  default     = ["arn:aws:sns:us-east-1:929468956630:cloudwatch-alarm-funnel"]
}

variable "alert_funnel_app_name" {
  description = "A string for the alert funnel app name needed for funnel to operate"
  type        = string
}

#######################################################################
#                              SECRETS
#######################################################################

variable "tdv_ssm" {
  type        = string
  description = "Teradata Vantage Secret in aws ssm"
}

variable "tdv_secretsmanager" {
  type        = string
  description = "Teradata Vantage Secret in aws secrets manager"
}

variable "tdv_secretsmanager_id" {
  type        = string
  description = "Secrets Id for Teradata Vantage Secret in aws secrets manager"
}

#######################################################################
#                          MISCELLANEOUS
#######################################################################

variable "b2b_queue_aws_account" {
  description = "String representing the name of sql script"
  type        = string
}

variable "splunk_destination_arn" {
  description = "String representing the ARN destination to push cloud watch logs to splunk"
  type        = string
}

#######################################################################
#                          SCHEMAS
#######################################################################

variable "schema_trxhub" {
  description = "trxhub core schema in tdv"
  type        = string
}

variable "schema_sales_commission" {
  description = "sales_commission core schema in tdv"
  type        = string
}

variable "schema_datamart_reftable" {
  description = "datamart_reftable core schema in tdv"
  type        = string
}

variable "schema_datamart_member" {
  description = "datamart_member schema in tdv"
  type        = string
}

variable "schema_reporting" {
  description = "reporting schema in tdv"
  type        = string
}