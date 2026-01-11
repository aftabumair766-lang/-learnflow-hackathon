---
name: nodejs-dapr-service
description: Generate Node.js microservice with Dapr from spec
---

# Node.js + Dapr Service Generator

## When to Use
- Need to generate backend microservice from spec
- Building Node.js + Express + Dapr service
- Reading from speckit-plus/03-specifications/services/

## Instructions
1. Generate service: `bash scripts/generate.sh <spec-file> <output-dir>`
2. Verify structure: `python3 scripts/verify.py <output-dir>`
3. Build & deploy: `bash scripts/deploy.sh <output-dir>`

## Validation
- [ ] Service code generated
- [ ] Dockerfile created
- [ ] K8s manifests created
- [ ] Dapr annotations configured

See [REFERENCE.md](./REFERENCE.md) for details.
