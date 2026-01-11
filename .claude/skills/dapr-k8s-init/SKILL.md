---
name: dapr-k8s-init
description: Install Dapr runtime on Kubernetes cluster
---

# Dapr Kubernetes Initialization

## When to Use
- Setting up service mesh for microservices
- Need pub/sub, state management, service invocation
- Before deploying Dapr-enabled services

## Instructions
1. Install Dapr: `bash scripts/install.sh`
2. Verify: `python3 scripts/verify.py`
3. Create components: `bash scripts/create-components.sh`

## Validation
- [ ] Dapr control plane Running
- [ ] Kafka pub/sub component created
- [ ] Ready for service deployment

See [REFERENCE.md](./REFERENCE.md) for details.
