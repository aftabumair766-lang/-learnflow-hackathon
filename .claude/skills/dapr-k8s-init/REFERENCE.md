# dapr-k8s-init - Reference Documentation

## Overview
Installs Dapr (Distributed Application Runtime) on Kubernetes and creates necessary components for LearnFlow microservices.

## What It Does
1. Installs Dapr control plane in `dapr-system` namespace
2. Waits for all Dapr pods to be Running
3. Creates Kafka pub/sub component for event streaming
4. Prepares cluster for Dapr-enabled services

## Usage

### Install Dapr
```bash
bash scripts/install.sh
```

### Verify Installation
```bash
python3 scripts/verify.py
```

### Create Components
```bash
bash scripts/create-components.sh learnflow
```

### Complete Workflow
```bash
bash scripts/install.sh && \
python3 scripts/verify.py && \
bash scripts/create-components.sh learnflow
```

## Scripts

### install.sh
**Purpose:** Install Dapr runtime on K8s

**Requirements:**
- Dapr CLI installed
- kubectl configured
- Kubernetes cluster running

**What it does:**
- Runs `dapr init -k`
- Waits up to 5 minutes for installation
- Installs: dapr-operator, dapr-sidecar-injector, dapr-placement, dapr-sentry

**Output:**
- `✓ Dapr installed in namespace 'dapr-system'` on success
- `✗ Dapr CLI not found` if CLI missing

### verify.py
**Purpose:** Verify Dapr control plane is healthy

**Checks:**
- Dapr pods exist in dapr-system namespace
- All pods in Running state

**Output:**
- `✓ Dapr ready (X/X control plane pods Running)` on success
- `✗ Dapr not ready (X/Y pods Running)` on failure

**Exit Codes:**
- `0` - Success
- `1` - Failure

### create-components.sh
**Purpose:** Create Dapr components (pub/sub, state)

**Parameters:**
- `$1` - Namespace (default: `learnflow`)

**Components Created:**
- **kafka-pubsub** - Kafka pub/sub component

**Output:**
- `✓ Dapr components created in namespace '<namespace>'`

## Dapr Components

### Kafka Pub/Sub
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
  namespace: learnflow
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    - name: brokers
      value: kafka.kafka.svc.cluster.local:9092
```

Services use this to publish/subscribe to Kafka topics:
```javascript
// Publish event
await fetch('http://localhost:3500/v1.0/publish/kafka-pubsub/student.events', {
  method: 'POST',
  body: JSON.stringify({ student_id: 123, name: 'Ali' })
});

// Subscribe via annotation
app.post('/dapr/subscribe', (req, res) => {
  res.json([{ pubsubname: 'kafka-pubsub', topic: 'student.events', route: '/events' }]);
});
```

## Token Efficiency

| Component | Tokens | In Context? |
|-----------|--------|-------------|
| SKILL.md | ~100 | ✓ Yes (when triggered) |
| REFERENCE.md | ~400 | ✗ No (on-demand only) |
| install.sh | 0 | ✗ No (executed) |
| verify.py | 0 | ✗ No (executed) |
| create-components.sh | 0 | ✗ No (executed) |
| Output | ~15 | ✓ Yes (minimal) |

**Total context cost:** ~115 tokens

## Cross-Agent Compatibility

### Claude Code
```bash
claude "Install Dapr for LearnFlow"
# Triggers dapr-k8s-init skill
```

### Goose
```bash
goose "Install Dapr for LearnFlow"
# Same skill works
```

## Dependencies

### Required Tools
- **Dapr CLI** - Install:
  ```bash
  # macOS/Linux
  curl -fsSL https://raw.githubusercontent.com/dapr/cli/master/install/install.sh | bash

  # Windows (PowerShell)
  iwr -useb https://raw.githubusercontent.com/dapr/cli/master/install/install.ps1 | iex
  ```

- **kubectl** - Kubernetes CLI
- **Kubernetes cluster** - Minikube, K3s, or cloud

### Minimum Resources
- 1 CPU, 1GB RAM for Dapr control plane

## Spec-Kit Plus Integration

Reads configuration from:
- `speckit-plus/03-specifications/infrastructure/dapr.yaml`

## Troubleshooting

### Dapr CLI Not Found
```bash
# Install Dapr CLI
curl -fsSL https://raw.githubusercontent.com/dapr/cli/master/install/install.sh | bash

# Verify
dapr --version
```

### Pods Stuck in Pending
```bash
kubectl describe pod -n dapr-system <pod-name>
# Check Events for resource/image issues
```

**Solution:** Increase cluster resources or pull images manually

### Component Not Found
```bash
# Check components
kubectl get components -n learnflow

# Recreate
bash scripts/create-components.sh learnflow
```

## Advanced Configuration

### Add State Store Component
Edit `create-components.sh`:
```bash
cat <<EOF | kubectl apply -f -
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: postgres-state
  namespace: $NAMESPACE
spec:
  type: state.postgresql
  version: v1
  metadata:
    - name: connectionString
      value: "host=postgres.learnflow.svc.cluster.local user=postgres password=postgres dbname=state_db"
EOF
```

### Enable mTLS
```bash
dapr init -k --enable-mtls=true
```

### Custom Placement Hosts
```bash
dapr init -k --set dapr_placement.cluster.replicas=3
```

## Service Integration

### Enable Dapr Sidecar
Add annotations to deployment:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: student-api
spec:
  template:
    metadata:
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "student-api"
        dapr.io/app-port: "3001"
```

### Environment Variables
Services access Dapr via:
```bash
DAPR_HTTP_PORT=3500
DAPR_GRPC_PORT=50001
```

## Testing

### Test Pub/Sub
```bash
# Publish event
kubectl run -it --rm test-publisher \
  --image=curlimages/curl \
  --restart=Never \
  -- curl -X POST http://dapr-api.dapr-system:80/v1.0/publish/kafka-pubsub/test-topic \
    -H "Content-Type: application/json" \
    -d '{"message":"hello"}'
```

### Check Dapr Dashboard
```bash
dapr dashboard -k
# Opens dashboard at http://localhost:8080
```

## Cleanup

```bash
# Uninstall Dapr
dapr uninstall -k

# Delete components
kubectl delete components -n learnflow --all
```

## Integration with LearnFlow

All 3 microservices use Dapr for:
1. **Pub/Sub** - Kafka event streaming
2. **Service Invocation** - matching-service calls tutor-api
3. **State Management** (optional) - Distributed state

## Reusability

This skill works for:
- ✅ LearnFlow platform
- ✅ Any Dapr-based microservices
- ✅ Event-driven architectures
- ✅ Service mesh deployments

**Generic skill** - no LearnFlow-specific logic in install/verify.

## Monitoring

### Check Dapr Status
```bash
dapr status -k
```

### View Dapr Logs
```bash
# Operator logs
kubectl logs -n dapr-system -l app=dapr-operator -f

# Sidecar injector logs
kubectl logs -n dapr-system -l app=dapr-sidecar-injector -f
```

## Upgrading Dapr

```bash
# Upgrade to specific version
dapr upgrade -k --runtime-version 1.13.0

# Check version
dapr version
```

---

**Version:** 1.0
**Status:** Active
**Maintained By:** Agentic AI
