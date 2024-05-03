# ################################################## Gov Solutions Digital #################################################
#------------------------ Cloudwatch EVENT RULE for Gov Solutions Digital glue crawler(FAILURE) ---------------------------------------
resource "aws_cloudwatch_event_rule" "crawler_failed_rule" {
  name        = var.failed_rule_name
  description = var.failed_rule_description

  event_pattern = <<PATTERN
{
  "source": ["aws.glue"],
  "detail-type": ["Glue Crawler State Change"],
  "detail": {
    "crawlerName": ["${var.crawlerName}"],
    "state": ["Failed"]
  }
}
PATTERN
}

resource "aws_cloudwatch_log_group" "gov_solutions_commissions_crawler_log_group" {
  name              = var.cloudwatch_log_group_name
  retention_in_days = 14
}

resource "aws_cloudwatch_event_target" "log_group" {
  rule       = aws_cloudwatch_event_rule.crawler_failed_rule.name
  depends_on = [aws_cloudwatch_log_group.gov_solutions_commissions_crawler_log_group]
  target_id  = "SendToCloudwatchLog"
  arn        = aws_cloudwatch_log_group.gov_solutions_commissions_crawler_log_group.arn
}

#------------------------CLOUDWATCH METRIC ALARM for Gov Solutions Digital glue crawler failure---------------------------#
# Description Pattern:  Environment | Log Level | App Name | Alarm Description
resource "aws_cloudwatch_metric_alarm" "crawler_failed_alarm" {
  alarm_name          = var.failed_alarm_name
  comparison_operator = var.comparison_operator
  namespace           = var.namespace
  metric_name         = var.metric_name
  statistic           = var.statistic
  period              = var.period
  threshold           = var.threshold
  evaluation_periods  = var.evaluation_periods
  depends_on          = [aws_cloudwatch_event_rule.crawler_failed_rule]
  dimensions = {
    RuleName = "${aws_cloudwatch_event_rule.crawler_failed_rule.name}"
  }
  alarm_description         = "${var.alarm_environment}|CRITICAL|${var.alert_funnel_app_name}|Errors >= 0."
  alarm_actions             = var.alarm_actions
  insufficient_data_actions = var.insufficient_data_actions
  ok_actions                = var.ok_actions
  tags                      = var.tags

}