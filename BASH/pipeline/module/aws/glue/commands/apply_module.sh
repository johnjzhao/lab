#!/bin/bash
set -e -o pipefail

export MODULE_NAME="${1}"
echo $MODULE_NAME
export ENV="${2}"
export REGION="${3:-us-east-1}"

pwd
# cd "$(dirname "${0}")/module/aws/commands" || true
cd $(dirname "${0}")
pwd
ls -R
source commands/pre.sh
# cd "../${MODULE_NAME}" || true

# tfenv converts all environment variables to TF_VAR's
source <(tfenv)
terragrunt apply ${TFTG_CLI_ARGS_APPLY_MODULE}
