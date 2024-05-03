locals {
  tdv_secrets = var.tdv_secretsmanager
}

resource "aws_secretsmanager_secret" "tdv_secret" {
  depends_on              = [aws_kms_alias.secret_key]
  name                    = "gov-solutions-commissions-tdv-secret-${var.environment}"
  description             = "TDV service account secret"
  kms_key_id              = aws_kms_key.secret_key.id
  recovery_window_in_days = 0
}

resource "aws_secretsmanager_secret_version" "tdv_secret_values" {
  secret_id     = aws_secretsmanager_secret.tdv_secret.id
  secret_string = local.tdv_secrets
}