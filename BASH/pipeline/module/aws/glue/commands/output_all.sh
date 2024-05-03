#!/bin/bash
set -e -o pipefail

export ENV="${1:-local}"
export REGION="${2:-us-east-1}"
export TERRAGRUNT_PARALLELISM="${3:-3}"

cd "$(dirname "${0}")/module/aws/commands" || true
source pre.sh
cd ".."

# Run Terragrunt to output all infrastructure
echo "Terragrunt parallelism set to ${TERRAGRUNT_PARALLELISM}"
echo "Running Terragrunt for environment: ${ENV}"

# tfenv converts all environment variables to TF_VAR's
source <(tfenv)
terragrunt run-all output ${TFTG_CLI_ARGS_OUTPUT_ALL}
