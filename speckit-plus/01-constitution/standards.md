# LearnFlow Technical Standards

## Technology Stack

### Frontend
- **Framework:** Next.js 14.x
- **Language:** TypeScript
- **Port:** 3000
- **Styling:** TailwindCSS (optional)

### Backend Services
- **Language:** Node.js 20
- **Framework:** Express.js
- **Container:** node:20-alpine

### Databases
- **Type:** PostgreSQL
- **Version:** 15
- **Deployment:** Kubernetes StatefulSet or Bitnami Helm

### Event Streaming
- **Platform:** Apache Kafka
- **Version:** 3.6.0
- **Chart:** bitnami/kafka
- **Topics:** student.events, tutor.events, matching.events

### Service Mesh
- **Runtime:** Dapr 1.12+
- **Components:** pub/sub, state management
- **Sidecar:** Auto-injected

### Orchestration
- **Platform:** Kubernetes (Minikube)
- **Namespace:** learnflow
- **Tool:** kubectl + Helm

## Skill Structure Standard

### Required Files
```
.claude/skills/<skill-name>/
├── SKILL.md           # ~100 tokens, YAML frontmatter
├── REFERENCE.md       # Deep docs, loaded on-demand
└── scripts/
    ├── deploy.sh      # Deployment logic
    ├── verify.py      # Verification logic
    └── cleanup.sh     # Cleanup logic
```

### SKILL.md Template
```markdown
---
name: skill-name
description: One-line description
---

# Skill Name

## When to Use
- Trigger condition 1
- Trigger condition 2

## Instructions
1. Run: `./scripts/deploy.sh`
2. Verify: `python3 scripts/verify.py`
3. Check output for ✓ or ✗

## Validation
- [ ] Success criterion 1
- [ ] Success criterion 2

See [REFERENCE.md](./REFERENCE.md) for details.
```

## Naming Conventions

### Services
- Format: `<domain>-api` or `<domain>-service`
- Examples: `student-api`, `tutor-api`, `matching-service`

### Kubernetes Resources
- Namespace: `learnflow`
- Labels: `app=<service-name>`, `component=<type>`

### Kafka Topics
- Format: `<domain>.events`
- Examples: `student.events`, `tutor.events`

### Skills
- Format: `<capability>-<scope>`
- Examples: `kafka-k8s-setup`, `postgres-deploy`, `nextjs-dapr-app`

## Script Standards

### Bash Scripts
```bash
#!/usr/bin/env bash
set -e  # Exit on error

# Minimal output only
echo "✓ Success" or "✗ Failure"
```

### Python Scripts
```python
#!/usr/bin/env python3
import sys

# Return only status
print("✓ Success")
sys.exit(0)  # or sys.exit(1) for failure
```

## Port Assignments
- Frontend: 3000
- Student API: 3001
- Tutor API: 3002
- Matching Service: 3003
- PostgreSQL: 5432
- Kafka: 9092

## Environment Variables
- `DAPR_HTTP_PORT`: 3500
- `KAFKA_BROKER`: `kafka.kafka.svc.cluster.local:9092`
- `DB_HOST`: `<service>-postgres.learnflow.svc.cluster.local`

## Documentation Standards
- All Skills must have REFERENCE.md
- Architecture diagrams in Docusaurus
- Inline comments only for complex logic
- README.md in project root

## Testing Standards
- Verification scripts in all Skills
- Healthcheck endpoints: `/health`
- Readiness probes on all services

## AAIF Compliance
- Skills follow AAIF format
- Compatible with Claude Code + Goose
- No vendor lock-in

**Status:** ACTIVE | **Version:** 1.0
