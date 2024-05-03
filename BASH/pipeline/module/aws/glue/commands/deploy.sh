#!/bin/bash
set -e -o pipefail

export ENV="${1:-local}"
export REGION="${2:-us-east-1}"
export TERRAGRUNT_PARALLELISM="${3:-3}"
export MODULE_NAME="glue"

pwd
cd "$(dirname "${0}")/module/aws/${MODULE_NAME}" || true
pwd
source "commands/pre.sh"
# cd ".."

# Run Terragrunt to apply all infrastructure
echo "Terragrunt parallelism set to ${TERRAGRUNT_PARALLELISM}"
echo "Running Terragrunt for environment: ${ENV}"

# tfenv converts all environment variables to TF_VAR's
source <(tfenv)
terragrunt run-all apply ${TFTG_CLI_ARGS_DEPLOY}


# add copy to s3 script
source "commands/copyToS3.sh"

