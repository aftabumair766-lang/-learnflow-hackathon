#!/usr/bin/env bash
set -e

echo "Deploying Kafka using Strimzi..."

# Create namespace
kubectl create namespace kafka --dry-run=client -o yaml | kubectl apply -f - > /dev/null 2>&1

# Deploy Kafka using Strimzi operator
cat <<EOF | kubectl apply -f - > /dev/null 2>&1
apiVersion: kafka.strimzi.io/v1
kind: Kafka
metadata:
  name: my-kafka
  namespace: kafka
spec:
  kafka:
    version: 3.6.1
    replicas: 1
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
    storage:
      type: ephemeral
    config:
      offsets.topic.replication.factor: 1
      transaction.state.log.replication.factor: 1
      transaction.state.log.min.isr: 1
  zookeeper:
    replicas: 1
    storage:
      type: ephemeral
  entityOperator:
    topicOperator: {}
    userOperator: {}
EOF

echo "✓ Kafka CR created in namespace 'kafka'"

