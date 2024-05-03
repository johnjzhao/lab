####################################################################################
#                                 GLUE JOB ALARMS
####################################################################################

module "extract_mem_enroll_cvrg_job_alarm" {
  source = "./modules/glue-job-alarms"

  failed_rule_name         = "commissions_extract_mem_enroll_cvrg_job-failed-rule"
  failed_rule_description  = "Capture Glue failed event"
  success_rule_name        = "commissions_extract_mem_enroll_cvrg_job-success-rule"
  success_rule_description = "Capture Glue success event"
  depends_on               = [module.pcs_member_enrollments_coverage_extract_glue_job]
  jobName                  = module.pcs_member_enrollments_coverage_extract_glue_job.glue_job_id

  failed_alarm_name         = "${module.pcs_member_enrollments_coverage_extract_glue_job.glue_job_id}-failed-alarm"
  success_alarm_name        = "${module.pcs_member_enrollments_coverage_extract_glue_job.glue_job_id}-success-alarm"
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
      "Name" = "gov_solutions_commissions_glue_tdv_extract_job_alarm"
    }
  )
}

module "extract_broker_comm_sircon_job_alarm" {
  source = "./modules/glue-job-alarms"

  failed_rule_name         = "commissions_extract_broker_comm_sircon_job-failed-rule"
  failed_rule_description  = "Capture Glue failed event"
  success_rule_name        = "commissions_extract_broker_comm_sircon_job-success-rule"
  success_rule_description = "Capture Glue success event"
  depends_on               = [module.broker_comm_sircon_extract_glue_job]
  jobName                  = module.broker_comm_sircon_extract_glue_job.glue_job_id

  failed_alarm_name         = "${module.broker_comm_sircon_extract_glue_job.glue_job_id}-failed-alarm"
  success_alarm_name        = "${module.broker_comm_sircon_extract_glue_job.glue_job_id}-success-alarm"
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
      "Name" = "gov_solutions_commissions_glue_tdv_extract_job_alarm"
    }
  )
}

module "extract_evolve_membere_job_alarm" {
  source = "./modules/glue-job-alarms"

  failed_rule_name         = "commissions_extract_evolve_membere_job-failed-rule"
  failed_rule_description  = "Capture Glue failed event"
  success_rule_name        = "commissions_extract_evolve_membere_job-success-rule"
  success_rule_description = "Capture Glue success event"
  depends_on               = [module.evolve_membere_extract_tdv_to_s3_glue_job]
  jobName                  = module.evolve_membere_extract_tdv_to_s3_glue_job.glue_job_id

  failed_alarm_name         = "${module.evolve_membere_extract_tdv_to_s3_glue_job.glue_job_id}-failed-alarm"
  success_alarm_name        = "${module.evolve_membere_extract_tdv_to_s3_glue_job.glue_job_id}-success-alarm"
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
      "Name" = "gov_solutions_commissions_glue_tdv_extract_job_alarm"
    }
  )
}

module "extract_evolve_memberp_job_alarm" {
  source = "./modules/glue-job-alarms"

  failed_rule_name         = "commissions_extract_evolve_memberp_job-failed-rule"
  failed_rule_description  = "Capture Glue failed event"
  success_rule_name        = "commissions_extract_evolve_memberp_job-success-rule"
  success_rule_description = "Capture Glue success event"
  depends_on               = [module.evolve_memberp_extract_tdv_to_s3_glue_job]
  jobName                  = module.evolve_memberp_extract_tdv_to_s3_glue_job.glue_job_id

  failed_alarm_name         = "${module.evolve_memberp_extract_tdv_to_s3_glue_job.glue_job_id}-failed-alarm"
  success_alarm_name        = "${module.evolve_memberp_extract_tdv_to_s3_glue_job.glue_job_id}-success-alarm"
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
      "Name" = "gov_solutions_commissions_glue_tdv_extract_job_alarm"
    }
  )
}

module "extract_mem_dim_job_alarm" {
  source = "./modules/glue-job-alarms"

  failed_rule_name         = "commissions_extract_mem_dim_job-failed-rule"
  failed_rule_description  = "Capture Glue failed event"
  success_rule_name        = "commissions_extract_mem_dim_job-success-rule"
  success_rule_description = "Capture Glue success event"
  depends_on               = [module.mem_dim_extract_glue_job]
  jobName                  = module.mem_dim_extract_glue_job.glue_job_id

  failed_alarm_name         = "${module.mem_dim_extract_glue_job.glue_job_id}-failed-alarm"
  success_alarm_name        = "${module.mem_dim_extract_glue_job.glue_job_id}-success-alarm"
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
      "Name" = "gov_solutions_commissions_glue_tdv_extract_job_alarm"
    }
  )
}

module "extract_mem_enroll_medicare_job_alarm" {
  source = "./modules/glue-job-alarms"

  failed_rule_name         = "commissions_extract_mem_enroll_medicare_job-failed-rule"
  failed_rule_description  = "Capture Glue failed event"
  success_rule_name        = "commissions_extract_mem_enroll_medicare_job-success-rule"
  success_rule_description = "Capture Glue success event"
  depends_on               = [module.pcs_member_enrollments_medicare_extract_glue_job]
  jobName                  = module.pcs_member_enrollments_medicare_extract_glue_job.glue_job_id

  failed_alarm_name         = "${module.pcs_member_enrollments_medicare_extract_glue_job.glue_job_id}-failed-alarm"
  success_alarm_name        = "${module.pcs_member_enrollments_medicare_extract_glue_job.glue_job_id}-success-alarm"
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
      "Name" = "gov_solutions_commissions_glue_tdv_extract_job_alarm"
    }
  )
}

module "gameday_job_alarm" {
  source = "./modules/glue-job-alarms"

  failed_rule_name         = "commissions_gameday_job-failed-rule"
  failed_rule_description  = "Capture Glue failed event"
  success_rule_name        = "commissions_gameday_job-success-rule"
  success_rule_description = "Capture Glue success event"
  depends_on               = [module.gameday_glue_job]
  jobName                  = module.gameday_glue_job.glue_job_id

  failed_alarm_name         = "${module.gameday_glue_job.glue_job_id}-failed-alarm"
  success_alarm_name        = "${module.gameday_glue_job.glue_job_id}-success-alarm"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  namespace                 = "AWS/Events"
  metric_name               = "TriggeredRules"
  statistic                 = "Sum"
  period                    = "120"
  threshold                 = "1"
  evaluation_periods        = "1"
  alarm_actions             = var.alarm_arn
  insufficient_data_actions = []
  ok_actions                = []
  alarm_environment         = var.alarm_environment
  alert_funnel_app_name     = var.alert_funnel_app_name
  tags = merge(var.cigna_common_tags,
    {
      "Name" = "gov_solutions_commissions_glue_gameday_job_alarm"
    }
  )
}



######################################################################################
#                                   S3 ALARMS
######################################################################################

resource "aws_cloudwatch_metric_alarm" "gov_solutions_commissions_artifictory_failed_s3_alarm" {
  alarm_name          = "${var.artifacts_bucket}-alarm-s3"
  alarm_description   = "${var.alarm_environment}|CRITICAL|${var.alert_funnel_app_name}|Errors >= 0."
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = "4xxErrors"
  period              = 60
  threshold           = 1
  namespace           = "AWS/S3"
  statistic           = "Sum"
  unit                = "Count"
  alarm_actions       = var.alarm_arn
  tags                = merge(var.cigna_common_tags, var.cigna_data_tags, var.required_tags)
  dimensions = {
    BucketName = var.artifacts_bucket
    FilterId   = "GlueArtifactory"
  }
}