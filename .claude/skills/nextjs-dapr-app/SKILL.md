---
name: nextjs-dapr-app
description: Generate Next.js frontend application with Dapr integration from YAML specification
type: generator
version: 1.0.0
---

# nextjs-dapr-app

Generates complete Next.js + TypeScript + Tailwind CSS frontend application with Dapr service invocation.

## Usage

```bash
bash scripts/generate.sh <spec-file> <output-dir>
```

## Example

```bash
bash scripts/generate.sh \
  speckit-plus/03-specifications/frontend/learnflow-web.yaml \
  speckit-plus/04-implementation/frontend/learnflow-web
```

## Output

- Next.js app structure
- TypeScript components
- Tailwind CSS styling
- Dockerfile
- k8s/deployment.yaml with Dapr

## Verification

```bash
python3 scripts/verify.py <output-dir>
```
