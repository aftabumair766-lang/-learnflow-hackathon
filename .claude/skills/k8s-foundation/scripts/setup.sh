#!/usr/bin/env bash
set -e

NAMESPACE=${1:-learnflow}

echo "Setting up Kubernetes foundation..."

# Create namespace
kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

# Label namespace
kubectl label namespace "$NAMESPACE" app=learnflow --overwrite

# Only minimal output enters context
echo "✓ Namespace '$NAMESPACE' ready"
