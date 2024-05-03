// Temporary solution for creating a key for enc/dec secrets. We should use vault and remove this key and the
// secret from this project. The piple lines should be executed twice. 1st to create the key, 2nd to modify/add the
// encrypted string apps module

resource "aws_kms_key" "secret_key" {
  description         = "Key for decrypt and encrypt TDV secrets"
  policy              = data.aws_iam_policy_document.this.json
  is_enabled          = true
  enable_key_rotation = true

  tags = merge(var.cigna_common_tags,
    {
      "Name" = "alias/${var.kmsaliasname}"
    }
  )
}

resource "aws_kms_alias" "secret_key" {
  name          = "alias/${var.kmsaliasname}"
  target_key_id = aws_kms_key.secret_key.id
}

data "aws_iam_policy_document" "this" {
  statement {
    sid       = "AllowAuthorizedPrincipals"
    resources = ["*"]
    principals {
      identifiers = [
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/ACCOUNTADMIN",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/DEVELOPER",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/Enterprise/GBSBROKERGATEKEEPERJENKINS",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/READONLYACCESS"
      ]
      type = "AWS"
    }
    actions = [
      "kms:Create*",
      "kms:Describe*",
      "kms:Enable*",
      "kms:List*",
      "kms:Put*",
      "kms:Update*",
      "kms:Revoke*",
      "kms:Disable*",
      "kms:Get*",
      "kms:Delete*",
      "kms:ScheduleKeyDeletion",
      "kms:CancelKeyDeletion"
    ]
  }

  statement {
    sid       = "Allow administration of the key"
    resources = ["*"]
    principals {
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"]
      type        = "AWS"
    }
    actions = ["kms:*"]
  }
  statement {
    sid       = "Allow use of the key"
    resources = ["*"]
    principals {
      identifiers = [
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/Enterprise/GBSBROKERGATEKEEPERJENKINS",
        "arn:aws:iam::${var.b2b_queue_aws_account}:role/B2BIONPREMCONNECTOR"
      ]
      type = "AWS"
    }
    actions = [
      "kms:Encrypt",
      "kms:Decrypt",
      "kms:ReEncrypt",
      "kms:GenerateDataKey*",
      "kms:DescribeKey"
    ]
  }
}
