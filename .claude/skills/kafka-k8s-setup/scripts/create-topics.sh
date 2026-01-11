#!/usr/bin/env bash
set -e

NAMESPACE="kafka"

# Wait for Kafka to be ready
echo "Creating Kafka topics..."

# Get Kafka pod name
KAFKA_POD=$(kubectl get pods -n $NAMESPACE -l app.kubernetes.io/name=kafka -o jsonpath='{.items[0].metadata.name}')

if [ -z "$KAFKA_POD" ]; then
  echo "✗ Kafka pod not found"
  exit 1
fi

# Create topics
for TOPIC in student.events tutor.events matching.events; do
  kubectl exec -n $NAMESPACE $KAFKA_POD -- kafka-topics.sh \
    --create \
    --if-not-exists \
    --topic $TOPIC \
    --partitions 3 \
    --replication-factor 1 \
    --bootstrap-server localhost:9092 > /dev/null 2>&1 || true
done

echo "✓ Topics created: student.events, tutor.events, matching.events"
