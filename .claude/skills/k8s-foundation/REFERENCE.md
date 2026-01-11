# k8s-foundation - Reference Documentation

## Overview
Creates and verifies Kubernetes namespaces and foundation resources for projects.

## What It Does
1. Creates namespace (idempotent via `--dry-run=client`)
2. Applies labels for organization
3. Verifies namespace is Active

## Usage

### Basic Usage
```bash
bash scripts/setup.sh learnflow
python3 scripts/verify.py learnflow
```

### Custom Namespace
```bash
bash scripts/setup.sh my-custom-namespace
python3 scripts/verify.py my-custom-namespace
```

## Scripts

### setup.sh
**Purpose:** Create and label namespace

**Parameters:**
- `$1` - Namespace name (default: `learnflow`)

**Output:**
- `✓ Namespace '<name>' ready` on success

**Idempotency:** Safe to run multiple times

### verify.py
**Purpose:** Verify namespace status

**Parameters:**
- `sys.argv[1]` - Namespace name (default: `learnflow`)

**Output:**
- `✓ Namespace '<name>' is Active` on success
- `✗ Namespace '<name>' not found` on failure

**Exit Codes:**
- `0` - Success
- `1` - Failure

## Token Efficiency

| Component | Tokens | In Context? |
|-----------|--------|-------------|
| SKILL.md | ~100 | ✓ Yes (when triggered) |
| REFERENCE.md | ~200 | ✗ No (on-demand only) |
| setup.sh | 0 | ✗ No (executed) |
| verify.py | 0 | ✗ No (executed) |
| Output | ~10 | ✓ Yes (minimal) |

**Total context cost:** ~110 tokens (vs 10,000+ for direct MCP)

## Cross-Agent Compatibility

### Claude Code
```bash
claude "Setup Kubernetes namespace for LearnFlow"
# Triggers k8s-foundation skill automatically
```

### Goose
```bash
goose "Setup Kubernetes namespace for LearnFlow"
# Same skill works without modification
```

## Dependencies
- `kubectl` installed and configured
- Valid kubeconfig (Minikube, cloud, etc.)
- Python 3.6+ for verification script

## Error Handling

### Common Errors

**Error:** `kubectl: command not found`
**Solution:** Install kubectl: `brew install kubectl` (macOS) or see https://kubernetes.io/docs/tasks/tools/

**Error:** `The connection to the server localhost:8080 was refused`
**Solution:** Start Minikube: `minikube start`

**Error:** `✗ Namespace 'learnflow' not found`
**Solution:** Run setup.sh first before verify.py

## Advanced Usage

### Create Multiple Namespaces
```bash
for ns in dev staging prod; do
  bash scripts/setup.sh $ns
  python3 scripts/verify.py $ns
done
```

### With Additional Labels
Modify `setup.sh`:
```bash
kubectl label namespace "$NAMESPACE" \
  app=learnflow \
  environment=dev \
  team=platform \
  --overwrite
```

## Integration with Other Skills

This skill is typically the **first step** in deployment:

```
1. k8s-foundation → Create namespace
2. kafka-k8s-setup → Deploy Kafka
3. dapr-k8s-init → Install Dapr
4. postgres-k8s-deploy → Deploy databases
5. nodejs-dapr-service → Deploy services
```

## Spec-Kit Plus Integration

Reads from:
- `speckit-plus/03-specifications/architecture.yaml`
  - `deployment.namespace: learnflow`

## Testing

### Manual Test
```bash
# Setup
bash .claude/skills/k8s-foundation/scripts/setup.sh test-namespace

# Verify
python3 .claude/skills/k8s-foundation/scripts/verify.py test-namespace

# Cleanup
kubectl delete namespace test-namespace
```

### Automated Test
```bash
#!/bin/bash
NAMESPACE="test-$(date +%s)"

bash scripts/setup.sh $NAMESPACE
if python3 scripts/verify.py $NAMESPACE; then
  echo "✓ Test passed"
  kubectl delete namespace $NAMESPACE
else
  echo "✗ Test failed"
  exit 1
fi
```

## Maintenance

### Updating the Skill
1. Modify scripts (not SKILL.md)
2. Test locally
3. Update REFERENCE.md if behavior changes
4. Keep SKILL.md concise (~100 tokens)

### Versioning
- Track in git
- Document breaking changes in REFERENCE.md

## Reusability

This skill is **generic** and works for:
- ✅ LearnFlow platform
- ✅ Any microservices project
- ✅ Any K8s deployment
- ✅ Development, staging, production

**No LearnFlow-specific logic** - pure K8s foundation.

## Contributing

If enhancing this skill:
1. Keep SKILL.md ≤ 100 tokens
2. Put complexity in scripts
3. Return only ✓/✗ status
4. Maintain cross-agent compatibility
5. Update REFERENCE.md

---

**Version:** 1.0
**Status:** Active
**Maintained By:** Agentic AI
