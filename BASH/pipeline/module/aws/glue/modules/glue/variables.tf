/*
    **************
    GLUE Variables
    **************
*/

variable "name" {
  type    = string
  default = "1"
}

variable "max_capacity" {
  type    = string
  default = "1"
}

variable "glue_version" {
  type = string
}

variable "timeout" {
  type    = string
  default = "300"
}

variable "max_retries" {
  type    = string
  default = "0"
}

variable "python_version" {
  default = 3.9
}

variable "max_concurrent_runs" {
  type    = string
  default = "1"
}

variable "role_arn" {
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

variable "cigna_common_tags" {
  description = "Map of tags required for AWS resources for Cigna compliance purposes"
  type        = map(string)
  default = {
    SecurityReviewID = "RITM4181504"
    AppName          = "EDE-GOV-PRODUCER-COMMISSIONS"
    AssetName        = "gov-solutions-commissions"
    AssetOwner       = "thesprinters@cigna.com"
    BackupOwner      = "sarah.williams@evernorth.com"
    CiId             = "notAssigned"
    ServiceNowBA     = "BA17057"
    CostCenter       = "00790113"
    Purpose          = "Glue Infrastructure"
    Team             = "The Sprinters"
    ServiceNowAS     = "AS040440"
    BusinessEntity   = "evernorth"
    LineOfBusiness   = "government"
  }
}

variable "connections" {
  type        = list(any)
  description = "Connections for jobs"
}

variable "script_location" {
  description = "Location of execution script"
  type        = string
}

variable "job_type" {
  description = "Type of glue job: glueetl/pythonshell/gluestreaming"
  type        = string
}

variable "arguments" {
  description = "Script arguments"
  type        = map(string)
}

/* 
    ********************
    Cloudwatch variables
    ********************
*/

variable "cloudwatch_log_group_name" {
  description = "Cloudwatch log group name"
  type        = string
}

variable "retention_in_days" {
  description = "Cloudwatch log retention period"
  type        = string
}

variable "splunk_destination_arn" {
  description = "String representing the ARN destination to push cloud watch logs to splunk"
  type        = string
}