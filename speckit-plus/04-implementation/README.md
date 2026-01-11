# Implementation Directory

## Purpose
This directory is where **AI agents generate code** based on specifications.

## How It Works

### Spec-Kit Plus Workflow
```
01-constitution → 02-tasks → 03-specifications → 04-implementation
    (Rules)        (What)         (How)              (Generated Code)
```

### Implementation Process

1. **AI reads specifications** from `03-specifications/`
2. **AI loads appropriate Skill** from `.claude/skills/`
3. **Skill generates code** and places it here
4. **Code is deployed** to Kubernetes

## Directory Structure (After Generation)

```
04-implementation/
├── services/
│   ├── student-api/
│   │   ├── src/
│   │   ├── Dockerfile
│   │   ├── package.json
│   │   └── k8s/
│   ├── tutor-api/
│   │   ├── src/
│   │   ├── Dockerfile
│   │   ├── package.json
│   │   └── k8s/
│   └── matching-service/
│       ├── src/
│       ├── Dockerfile
│       ├── package.json
│       └── k8s/
├── frontend/
│   └── learnflow-web/
│       ├── src/
│       ├── pages/
│       ├── Dockerfile
│       ├── package.json
│       └── k8s/
└── infrastructure/
    ├── kafka/
    ├── dapr/
    └── postgresql/
```

## ⚠️ Important Rules

### DO NOT manually write code here!
- ❌ NO manual scaffolding
- ❌ NO copy-paste from templates
- ❌ NO editing generated code (unless debugging)

### Instead:
- ✅ Let Skills generate everything
- ✅ Modify specifications if changes needed
- ✅ Re-run Skills to regenerate code

## Skills That Generate Code

| Skill | Generates | Location |
|-------|-----------|----------|
| nodejs-dapr-service | Backend services | services/ |
| nextjs-dapr-app | Frontend app | frontend/ |
| kafka-k8s-setup | Kafka manifests | infrastructure/kafka/ |
| dapr-k8s-init | Dapr config | infrastructure/dapr/ |
| postgres-k8s-deploy | PostgreSQL manifests | infrastructure/postgresql/ |

## Verification

After generation, verify:
```bash
# Check structure
ls -la 04-implementation/services/
ls -la 04-implementation/frontend/
ls -la 04-implementation/infrastructure/

# Verify Dockerfiles exist
find 04-implementation -name Dockerfile

# Verify K8s manifests exist
find 04-implementation -name "*.yaml" -o -name "*.yml"
```

## Next Steps

Once code is generated:
1. Build Docker images
2. Deploy to Kubernetes
3. Verify all pods Running
4. Test end-to-end workflow

**Status:** READY for code generation
