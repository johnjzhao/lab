# ################################################## Gov Solutions Digital #################################################
#------------------------ Cloudwatch EVENT RULE for Gov Solutions Digital glue job(FAILURE) ---------------------------------------
resource "aws_cloudwatch_event_rule" "failed_rule" {
  name        = var.failed_rule_name
  description = var.failed_rule_description

  event_pattern = <<PATTERN
{
  "source": [ "aws.glue" ],
  "detail-type": [ "Glue Job State Change" ],
  "detail": {
    "jobName": [ "${var.jobName}" ],
    "state": ["FAILED"]
  }
}
PATTERN
}

#------------------------ Cloudwatch EVENT RULE for Gov Solutions Digital glue job(SUCCESS) ---------------------------------------
resource "aws_cloudwatch_event_rule" "success_rule" {
  name        = var.success_rule_name
  description = var.success_rule_description

  event_pattern = <<PATTERN
{
  "source": [ "aws.glue" ],
  "detail-type": [ "Glue Job State Change" ],
  "detail": {
    "jobName": [ "${var.jobName}" ],
    "state": ["SUCCEEDED"]
  }
}
PATTERN
}

#------------------------CLOUDWATCH METRIC ALARM for Gov Solutions Digital glue failure---------------------------#
# Description Pattern:  Environment | Log Level | App Name | Alarm Description
resource "aws_cloudwatch_metric_alarm" "failed_alarm" {
  alarm_name          = var.failed_alarm_name
  comparison_operator = var.comparison_operator
  namespace           = var.namespace
  metric_name         = var.metric_name
  statistic           = var.statistic
  period              = var.period
  threshold           = var.threshold
  evaluation_periods  = var.evaluation_periods
  dimensions = {
    RuleName = "${aws_cloudwatch_event_rule.failed_rule.name}"
  }
  alarm_description         = "${var.alarm_environment}|CRITICAL|${var.alert_funnel_app_name}|Errors >= 0."
  alarm_actions             = var.alarm_actions
  insufficient_data_actions = var.insufficient_data_actions
  ok_actions                = var.ok_actions
  tags                      = var.tags

}

#------------------------CLOUDWATCH METRIC ALARM for Gov Solutions Digital glue success---------------------------#
# Description Pattern:  Environment | Log Level | App Name | Alarm Description
resource "aws_cloudwatch_metric_alarm" "success_alarm" {
  alarm_name          = var.success_alarm_name
  comparison_operator = var.comparison_operator
  namespace           = var.namespace
  metric_name         = var.metric_name
  statistic           = var.statistic
  period              = var.period
  threshold           = var.threshold
  evaluation_periods  = var.evaluation_periods
  dimensions = {
    RuleName = "${aws_cloudwatch_event_rule.success_rule.name}"
  }
  alarm_description         = "${var.alarm_environment}|INFO|${var.alert_funnel_app_name}|Success"
  alarm_actions             = var.alarm_actions
  insufficient_data_actions = var.insufficient_data_actions
  ok_actions                = var.ok_actions
  tags                      = var.tags

}