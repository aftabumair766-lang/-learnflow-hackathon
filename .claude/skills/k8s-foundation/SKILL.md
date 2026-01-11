---
name: k8s-foundation
description: Setup Kubernetes namespace and foundation resources
---

# Kubernetes Foundation Setup

## When to Use
- Starting new K8s project
- Creating namespace for LearnFlow
- Setting up basic K8s resources

## Instructions
1. Run setup: `bash scripts/setup.sh <namespace>`
2. Verify: `python3 scripts/verify.py <namespace>`
3. Check output for ✓ or ✗

## Validation
- [ ] Namespace created
- [ ] Namespace is Active
- [ ] No errors in kubectl

See [REFERENCE.md](./REFERENCE.md) for details.
