#!/bin/bash
set -e -o pipefail

export MODULE_NAME="${1}"
export ENV="${2}"
export REGION="${3:-us-east-1}"
# export ENV="${1:-local}"
# export REGION="${2:-us-east-1}"
# export TERRAGRUNT_PARALLELISM="${3:-3}"
# export MODULE_NAME="base_infra"

# cd "$(dirname "${0}")/module/aws/commands" || true
# source pre.sh
# cd "../${MODULE_NAME}" || true
cd "$(dirname "${0}")/module/aws/${MODULE_NAME}" || true
source "commands/pre.sh"

# tfenv converts all environment variables to TF_VAR's
# CAUTION: destroy set to interactive to avoiding accidentally destroy resources
source <(tfenv)
terragrunt destroy ${TFTG_CLI_ARGS_DESTROY_MODULE}
