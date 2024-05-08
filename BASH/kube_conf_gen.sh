#!/usr/bin/env bash

NS="$1"
CLUSTER=$2
SA=$3


if [ -z "$NS" ] || [ -z "${CLUSTER}" ] || [ -z "$SA" ]
then
  echo "Usage :"
  echo "$0 <namespace> <cluster name> <service_account>"
  exit 1
fi

readonly CONTEXT=$(kubectl config current-context)

echo "Please be sure that your kubectl context is the good one !"
echo "********"
echo "Context : $CONTEXT"
echo "SA: $SA"
echo "Server : $CLUSTER"
echo "********"
echo "sure ? (<ENTER>/<CTRL+C>)"
read -r

KUBERNETES_API_ENDPOINT=$(kubectl config view -o jsonpath="{.clusters[?(@.name == \"${CLUSTER}\")].cluster.server}")

SECRET_NAME=$(kubectl describe sa "$SA" -n "$NS" | grep Tokens | awk '{ print $2 }')
USER_TOKEN=$(kubectl get secret "$SECRET_NAME" -n "$NS" -o "jsonpath={.data.token}" | base64 --decode)
CA=$(kubectl get secret "$SECRET_NAME" -n "$NS" -o "jsonpath={.data['ca\.crt']}")

echo "SECRET_NAME=$SECRET_NAME"
echo "USER_TOKEN=$USER_TOKEN"
echo "CA=$CA"
echo -e "\n\n\n*************************************************\n\n\n"

cat > "kubeconfig_${SA}-${NS}_${CLUSTER}" <<EOF
apiVersion: v1
kind: Config
preferences: {}

# Define the cluster
clusters:
- cluster:
    certificate-authority-data: $CA
    server: ${KUBERNETES_API_ENDPOINT}
  name: ${CLUSTER}

# Define the user
users:
- name: $SA
  user:
    token: $USER_TOKEN

# Define the context: linking a user to a cluster
contexts:
- context:
    cluster: ${CLUSTER}
    namespace: $NS
    user: $SA
  name: $NS@${CLUSTER}

# Define current context
current-context: $NS@${CLUSTER}
EOF

echo "kubeconfig has been generated : kubeconfig_${NS}_${CLUSTER}"
