module "pcs_mem_dim_crawler_alarm" {
  source = "./modules/glue-crawler-alarms"

  failed_rule_name        = "commissions_pcs_mem_dim_crawler-failed-rule"
  failed_rule_description = "Capture Glue crawler failed event"
  depends_on              = [aws_glue_crawler.pcs_mem_dim_crawler]
  crawlerName             = aws_glue_crawler.pcs_mem_dim_crawler.name

  failed_alarm_name         = "${aws_glue_crawler.pcs_mem_dim_crawler.name}-failed-alarm"
  cloudwatch_log_group_name = "${aws_glue_crawler.pcs_mem_dim_crawler.name}-log"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  namespace                 = "AWS/Events"
  metric_name               = "TriggeredRules"
  statistic                 = "Sum"
  period                    = "120"
  threshold                 = "1"
  evaluation_periods        = "1"
  alarm_actions             = var.alarm_arn
  insufficient_data_actions = []
  ok_actions                = var.alarm_arn
  alarm_environment         = var.alarm_environment
  alert_funnel_app_name     = var.alert_funnel_app_name
  tags = merge(var.cigna_common_tags,
    {
      "Name" = "gov_solutions_commissions_glue_crawler_alarm"
    }
  )
}

module "pcs_broker_comm_sircon_crawler_alarm" {
  source = "./modules/glue-crawler-alarms"

  failed_rule_name        = "commissions_pcs_broker_comm_sircon_crawler-failed-rule"
  failed_rule_description = "Capture Glue crawler failed event"
  depends_on              = [aws_glue_crawler.pcs_broker_comm_sircon_crawler]
  crawlerName             = aws_glue_crawler.pcs_broker_comm_sircon_crawler.name

  failed_alarm_name         = "${aws_glue_crawler.pcs_broker_comm_sircon_crawler.name}-failed-alarm"
  cloudwatch_log_group_name = "${aws_glue_crawler.pcs_broker_comm_sircon_crawler.name}-log"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  namespace                 = "AWS/Events"
  metric_name               = "TriggeredRules"
  statistic                 = "Sum"
  period                    = "120"
  threshold                 = "1"
  evaluation_periods        = "1"
  alarm_actions             = var.alarm_arn
  insufficient_data_actions = []
  ok_actions                = var.alarm_arn
  alarm_environment         = var.alarm_environment
  alert_funnel_app_name     = var.alert_funnel_app_name
  tags = merge(var.cigna_common_tags,
    {
      "Name" = "gov_solutions_commissions_glue_crawler_alarm"
    }
  )
}

module "evolve_membere_crawler_alarm" {
  source = "./modules/glue-crawler-alarms"

  failed_rule_name        = "commissions_evolve_membere_crawler-failed-rule"
  failed_rule_description = "Capture Glue crawler failed event"
  depends_on              = [aws_glue_crawler.evolve_membere_crawler]
  crawlerName             = aws_glue_crawler.evolve_membere_crawler.name

  failed_alarm_name         = "${aws_glue_crawler.evolve_membere_crawler.name}-failed-alarm"
  cloudwatch_log_group_name = "${aws_glue_crawler.evolve_membere_crawler.name}-log"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  namespace                 = "AWS/Events"
  metric_name               = "TriggeredRules"
  statistic                 = "Sum"
  period                    = "120"
  threshold                 = "1"
  evaluation_periods        = "1"
  alarm_actions             = var.alarm_arn
  insufficient_data_actions = []
  ok_actions                = var.alarm_arn
  alarm_environment         = var.alarm_environment
  alert_funnel_app_name     = var.alert_funnel_app_name
  tags = merge(var.cigna_common_tags,
    {
      "Name" = "gov_solutions_commissions_glue_crawler_alarm"
    }
  )
}

module "evolve_memberp_crawler_alarm" {
  source = "./modules/glue-crawler-alarms"

  failed_rule_name        = "commissions_evolve_memberp_crawler-failed-rule"
  failed_rule_description = "Capture Glue crawler failed event"
  depends_on              = [aws_glue_crawler.evolve_memberp_crawler]
  crawlerName             = aws_glue_crawler.evolve_memberp_crawler.name

  failed_alarm_name         = "${aws_glue_crawler.evolve_memberp_crawler.name}-failed-alarm"
  cloudwatch_log_group_name = "${aws_glue_crawler.evolve_memberp_crawler.name}-log"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  namespace                 = "AWS/Events"
  metric_name               = "TriggeredRules"
  statistic                 = "Sum"
  period                    = "120"
  threshold                 = "1"
  evaluation_periods        = "1"
  alarm_actions             = var.alarm_arn
  insufficient_data_actions = []
  ok_actions                = var.alarm_arn
  alarm_environment         = var.alarm_environment
  alert_funnel_app_name     = var.alert_funnel_app_name
  tags = merge(var.cigna_common_tags,
    {
      "Name" = "gov_solutions_commissions_glue_crawler_alarm"
    }
  )
}

module "pcs_member_enrollments_coverage_crawler_alarm" {
  source = "./modules/glue-crawler-alarms"

  failed_rule_name        = "commissions_pcs_mem_enrollments_coverage_crawler-failed-rule"
  failed_rule_description = "Capture Glue crawler failed event"
  depends_on              = [aws_glue_crawler.pcs_member_enrollments_coverage_crawler]
  crawlerName             = aws_glue_crawler.pcs_member_enrollments_coverage_crawler.name

  failed_alarm_name         = "${aws_glue_crawler.pcs_member_enrollments_coverage_crawler.name}-failed-alarm"
  cloudwatch_log_group_name = "${aws_glue_crawler.pcs_member_enrollments_coverage_crawler.name}-log"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  namespace                 = "AWS/Events"
  metric_name               = "TriggeredRules"
  statistic                 = "Sum"
  period                    = "120"
  threshold                 = "1"
  evaluation_periods        = "1"
  alarm_actions             = var.alarm_arn
  insufficient_data_actions = []
  ok_actions                = var.alarm_arn
  alarm_environment         = var.alarm_environment
  alert_funnel_app_name     = var.alert_funnel_app_name
  tags = merge(var.cigna_common_tags,
    {
      "Name" = "gov_solutions_commissions_glue_crawler_alarm"
    }
  )
}

module "pcs_member_sales_agent_dim_crawler_alarm" {
  source = "./modules/glue-crawler-alarms"

  failed_rule_name        = "commissions_pcs_member_sales_agent_dim_crawler-failed-rule"
  failed_rule_description = "Capture Glue crawler failed event"
  depends_on              = [aws_glue_crawler.pcs_member_sales_agent_dim_crawler]
  crawlerName             = aws_glue_crawler.pcs_member_sales_agent_dim_crawler.name

  failed_alarm_name         = "${aws_glue_crawler.pcs_member_sales_agent_dim_crawler.name}-failed-alarm"
  cloudwatch_log_group_name = "${aws_glue_crawler.pcs_member_sales_agent_dim_crawler.name}-log"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  namespace                 = "AWS/Events"
  metric_name               = "TriggeredRules"
  statistic                 = "Sum"
  period                    = "120"
  threshold                 = "1"
  evaluation_periods        = "1"
  alarm_actions             = var.alarm_arn
  insufficient_data_actions = []
  ok_actions                = var.alarm_arn
  alarm_environment         = var.alarm_environment
  alert_funnel_app_name     = var.alert_funnel_app_name
  tags = merge(var.cigna_common_tags,
    {
      "Name" = "gov_solutions_commissions_glue_crawler_alarm"
    }
  )
}

module "pcs_member_enrollments_medicare_cdo_mbr_demg_crawler_alarm" {
  source = "./modules/glue-crawler-alarms"

  failed_rule_name        = "commissions_pcs_mem_enrll_medicare_cdo_crawler-failed-rule"
  failed_rule_description = "Capture Glue crawler failed event"
  depends_on              = [aws_glue_crawler.pcs_member_enrollments_medicare_cdo_mbr_demg_crawler]
  crawlerName             = aws_glue_crawler.pcs_member_enrollments_medicare_cdo_mbr_demg_crawler.name

  failed_alarm_name         = "${aws_glue_crawler.pcs_member_enrollments_medicare_cdo_mbr_demg_crawler.name}-failed-alarm"
  cloudwatch_log_group_name = "${aws_glue_crawler.pcs_member_enrollments_medicare_cdo_mbr_demg_crawler.name}-log"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  namespace                 = "AWS/Events"
  metric_name               = "TriggeredRules"
  statistic                 = "Sum"
  period                    = "120"
  threshold                 = "1"
  evaluation_periods        = "1"
  alarm_actions             = var.alarm_arn
  insufficient_data_actions = []
  ok_actions                = var.alarm_arn
  alarm_environment         = var.alarm_environment
  alert_funnel_app_name     = var.alert_funnel_app_name
  tags = merge(var.cigna_common_tags,
    {
      "Name" = "gov_solutions_commissions_glue_crawler_alarm"
    }
  )
}

module "pcs_member_medicare_dim_crawler_alarm" {
  source = "./modules/glue-crawler-alarms"

  failed_rule_name        = "commissions_pcs_mem_medicare_dim-crawler-failed-rule"
  failed_rule_description = "Capture Glue crawler failed event"
  depends_on              = [aws_glue_crawler.pcs_member_medicare_dim_crawler]
  crawlerName             = aws_glue_crawler.pcs_member_medicare_dim_crawler.name

  failed_alarm_name         = "${aws_glue_crawler.pcs_member_medicare_dim_crawler.name}-failed-alarm"
  cloudwatch_log_group_name = "${aws_glue_crawler.pcs_member_medicare_dim_crawler.name}-log"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  namespace                 = "AWS/Events"
  metric_name               = "TriggeredRules"
  statistic                 = "Sum"
  period                    = "120"
  threshold                 = "1"
  evaluation_periods        = "1"
  alarm_actions             = var.alarm_arn
  insufficient_data_actions = []
  ok_actions                = var.alarm_arn
  alarm_environment         = var.alarm_environment
  alert_funnel_app_name     = var.alert_funnel_app_name
  tags = merge(var.cigna_common_tags,
    {
      "Name" = "gov_solutions_commissions_glue_crawler_alarm"
    }
  )
}



############################################################################
#                CRAWLER  and CRAWLER ALARM FOR GAMEDAY PREP
############################################################################

resource "aws_glue_crawler" "gameday_crawler" {
  database_name = var.aws_glue_catalog_database.name
  name          = "gov_solutions_commissions_gameday"
  role          = var.glue_role_arn
  s3_target {
    path = "s3://does-not-exist/"
  }
  tags = merge(var.cigna_common_tags,
    {
      "Name" = "gov_solutions_commissions_crawler"
    }
  )
}


module "gameday_crawler_alarm" {
  source = "./modules/glue-crawler-alarms"

  failed_rule_name        = "gov_solutions_commissions_gameday-crawler-failed-rule"
  failed_rule_description = "Capture Glue crawler failed event"
  depends_on              = [aws_glue_crawler.gameday_crawler]
  crawlerName             = aws_glue_crawler.gameday_crawler.name

  failed_alarm_name         = "gov_solutions_commissions_gameday-crawler-failed-alarm"
  cloudwatch_log_group_name = "gov_solutions_commissions_gameday-crawler-log"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  namespace                 = "AWS/Events"
  metric_name               = "TriggeredRules"
  statistic                 = "Sum"
  period                    = "120"
  threshold                 = "1"
  evaluation_periods        = "1"
  alarm_actions             = var.alarm_arn
  insufficient_data_actions = []
  ok_actions                = var.alarm_arn
  alarm_environment         = var.alarm_environment
  alert_funnel_app_name     = var.alert_funnel_app_name
  tags = merge(var.cigna_common_tags,
    {
      "Name" = "gov_solutions_commissions_glue_crawler_alarm"
    }
  )
}