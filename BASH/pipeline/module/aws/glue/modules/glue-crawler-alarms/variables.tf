/*-------------------ALARMS-----------------------*/
variable "failed_rule_name" {
  type    = string
  default = "failed_rule"
}

variable "failed_rule_description" {
  type    = string
  default = "failed_rule_description"
}

variable "crawlerName" {
  type    = string
  default = "crawler"
}

variable "failed_alarm_name" {
  type    = string
  default = "failed_alarm"
}

variable "comparison_operator" {
  type    = string
  default = "GreaterThanOrEqualToThreshold"
}

variable "namespace" {
  type    = string
  default = "AWS/Events"
}

variable "metric_name" {
  type    = string
  default = "TriggeredRules"
}

variable "statistic" {
  type    = string
  default = "Sum"
}

variable "period" {
  type    = string
  default = "120"
}

variable "threshold" {
  type    = string
  default = "1"
}

variable "evaluation_periods" {
  type    = string
  default = "1"
}

variable "alarm_environment" {
  type = string
}

variable "alert_funnel_app_name" {
  type = string
}

variable "alarm_actions" {
  type = list(string)
}

variable "insufficient_data_actions" {
  type    = list(string)
  default = []
}

variable "ok_actions" {
  type = list(string)
}

variable "tags" {
  type = map(string)
  default = {
    "Name" = "gov_solutions_digital_glue_tdv_extract_job"
  }
}

variable "cloudwatch_log_group_name" {
  type    = string
  default = "commissions_crawler_log_group"
}

variable "retention_in_days" {
  type    = string
  default = "14"
}