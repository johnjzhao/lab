/*-------------------ALARMS-----------------------*/
variable "failed_rule_name" {
  type    = string
  default = "failed_rule"
}

variable "failed_rule_description" {
  type    = string
  default = "failed_rule_description"
}

variable "success_rule_name" {
  type    = string
  default = "success_rule"
}

variable "success_rule_description" {
  type    = string
  default = "success_rule_description"
}

variable "jobName" {
  type    = string
  default = "job"
}

variable "failed_alarm_name" {
  type    = string
  default = "failed_alarm"
}

variable "success_alarm_name" {
  type    = string
  default = "success_alarm"
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