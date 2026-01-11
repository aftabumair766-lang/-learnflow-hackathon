#!/usr/bin/env bash
set -e

NAMESPACE=${1:-learnflow}

echo "Creating Dapr components..."

# Create namespace if it doesn't exist
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f - > /dev/null 2>&1

# Create Kafka pub/sub component
cat <<EOF | kubectl apply -f - > /dev/null 2>&1
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
  namespace: $NAMESPACE
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    - name: brokers
      value: kafka.kafka.svc.cluster.local:9092
    - name: authType
      value: none
    - name: consumerGroup
      value: learnflow-group
EOF

echo "✓ Dapr components created in namespace '$NAMESPACE'"
