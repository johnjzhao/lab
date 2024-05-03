# include {
#   path = find_in_parent_folders()
# }


generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
  provider "aws" {
    region = "us-east-1"
    profile = "saml"
  }
  EOF
}


terraform {
  extra_arguments "publish_vars" {
    # commands = get_terraform_commands_that_need_vars()
    commands = [
      "apply",
      "plan",
      "import",
      "push",
      "refresh",
      "destroy"
    ]

    arguments = [
      "-var", "environment=${get_env("TF_VAR_env")}",
      "-var", "artifacts_bucket=gov-solutions-commissions-artifacts-${get_env("TF_VAR_env")}",
      "-var", "tfstate_bucket=cigna-tf-state-${get_env("TF_VAR_account_number", "<DEFAULT_ACCOUNT_NUMBER>")}",
      "-var", "tfstate_path=terraform/gov-solutions-commissions/${basename(get_terragrunt_dir())}/${get_env("TF_VAR_env")}/tfstate"

    ]

    required_var_files = [
      "${get_terragrunt_dir()}/env-config/common.tfvars",
      "${get_terragrunt_dir()}/env-config/${get_env("TF_VAR_env")}.tfvars"
    ]
  }
}

remote_state {
  backend = "s3"
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
  config = {
    bucket         = "cigna-tf-state-${get_env("TF_VAR_account_number", "<DEFAULT_ACCOUNT_NUMBER>")}"
    dynamodb_table = "cigna-tf-lock-${get_env("TF_VAR_account_number", "<DEFAULT_ACCOUNT_NUMBER>")}"
    key            = "terraform/gov-solutions-commissions/${basename(get_terragrunt_dir())}/${get_env("TF_VAR_env")}/tfstate"
    profile        = "saml"
    region         = "us-east-1"
  }
}