#!/usr/bin/env bash
set -e

NAMESPACE=${1:-learnflow}

echo "Deploying PostgreSQL databases..."

# Add Bitnami repo
helm repo add bitnami https://charts.bitnami.com/bitnami 2>/dev/null || true
helm repo update > /dev/null 2>&1

# Create namespace
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f - > /dev/null 2>&1

# Deploy 3 PostgreSQL instances for LearnFlow services
for DB in students tutors matching; do
  helm upgrade --install postgres-$DB bitnami/postgresql \
    --namespace $NAMESPACE \
    --set auth.postgresPassword=postgres \
    --set auth.database=${DB}_db \
    --set primary.persistence.enabled=false \
    --set primary.resources.requests.memory=256Mi \
    --set primary.resources.requests.cpu=100m \
    --wait --timeout=5m > /dev/null 2>&1
done

echo "✓ PostgreSQL databases deployed to namespace '$NAMESPACE'"
