resource "aws_cloudwatch_log_group" "gov_solutions_commissions_log_group" {
  name              = var.cloudwatch_log_group_name
  retention_in_days = var.retention_in_days
}

//--- Centralized Logging Splunk Subscription for Glue Log Group
resource "aws_cloudwatch_log_subscription_filter" "splunk_subscription_gov_sol_commissions" {
  count           = var.splunk_destination_arn == null ? 0 : 1
  name            = "gov_solutions_commissions_glue_splunk_subscription"
  log_group_name  = "/aws-glue/jobs/${var.name}"
  filter_pattern  = ""
  destination_arn = var.splunk_destination_arn
  depends_on      = [aws_cloudwatch_log_group.gov_solutions_commissions_log_group]
}

resource "aws_glue_job" "this" {
  name         = var.name
  description  = var.description
  role_arn     = var.role_arn
  max_capacity = var.max_capacity
  glue_version = var.glue_version
  connections  = var.connections
  timeout      = var.timeout
  max_retries  = var.max_retries
  depends_on   = [aws_cloudwatch_log_group.gov_solutions_commissions_log_group]
  command {
    script_location = var.script_location
    python_version  = var.python_version
    name            = var.job_type
  }
  execution_property {
    max_concurrent_runs = var.max_concurrent_runs
  }
  default_arguments = merge(var.glue_default_arguments, var.arguments, tomap({ "--continous-log-group" = aws_cloudwatch_log_group.gov_solutions_commissions_log_group.name }))
  tags              = merge(var.cigna_common_tags, tomap({ "Name" = var.name, "resourceName" = var.name }))
}
