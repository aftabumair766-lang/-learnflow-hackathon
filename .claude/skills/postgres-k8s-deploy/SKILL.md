---
name: postgres-k8s-deploy
description: Deploy PostgreSQL databases on Kubernetes
---

# PostgreSQL Kubernetes Deployment

## When to Use
- Need PostgreSQL for microservices
- Setting up databases for LearnFlow services
- Development database infrastructure

## Instructions
1. Deploy databases: `bash scripts/deploy.sh <namespace>`
2. Verify: `python3 scripts/verify.py <namespace>`
3. Check all databases Running

## Validation
- [ ] PostgreSQL pods Running
- [ ] Databases accessible
- [ ] Services created

See [REFERENCE.md](./REFERENCE.md) for details.
