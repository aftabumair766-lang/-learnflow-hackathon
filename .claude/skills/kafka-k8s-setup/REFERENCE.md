# kafka-k8s-setup - Reference Documentation

## Overview
Deploys Apache Kafka on Kubernetes using Bitnami Helm chart and creates required topics for LearnFlow.

## What It Does
1. Adds Bitnami Helm repository
2. Creates `kafka` namespace
3. Deploys Kafka with ZooKeeper (single replica for dev)
4. Waits for pods to be Running
5. Creates topics: student.events, tutor.events, matching.events

## Usage

### Deploy Kafka
```bash
bash scripts/deploy.sh
```

### Verify Deployment
```bash
python3 scripts/verify.py
```

### Create Topics
```bash
bash scripts/create-topics.sh
```

### Complete Workflow
```bash
bash scripts/deploy.sh && \
python3 scripts/verify.py && \
bash scripts/create-topics.sh
```

## Scripts

### deploy.sh
**Purpose:** Deploy Kafka cluster

**What it does:**
- Adds Bitnami Helm repo
- Creates namespace
- Installs Kafka chart with ephemeral storage
- Waits up to 5 minutes for deployment

**Output:**
- `✓ Kafka deployed to namespace 'kafka'` on success

**Configuration:**
- Replicas: 1
- ZooKeeper replicas: 1
- Persistence: disabled (ephemeral for dev)

### verify.py
**Purpose:** Verify Kafka is healthy

**Checks:**
- Kafka pods exist
- All pods in Running state
- Kafka service exists

**Output:**
- `✓ Kafka ready (X/X pods Running)` on success
- `✗ Kafka not ready (X/Y pods Running)` on failure

**Exit Codes:**
- `0` - Success
- `1` - Failure

### create-topics.sh
**Purpose:** Create Kafka topics for LearnFlow

**Topics Created:**
- `student.events` (3 partitions, replication: 1)
- `tutor.events` (3 partitions, replication: 1)
- `matching.events` (3 partitions, replication: 1)

**Output:**
- `✓ Topics created: student.events, tutor.events, matching.events`

**Idempotency:** Safe to run multiple times (`--if-not-exists`)

## Kafka Configuration

### Service Endpoint
```
kafka.kafka.svc.cluster.local:9092
```

### From Within Cluster
```bash
# Connect from any pod
kubectl run -it --rm kafka-client \
  --image=bitnami/kafka:latest \
  --restart=Never \
  -- kafka-topics.sh --list --bootstrap-server kafka.kafka.svc.cluster.local:9092
```

### Port Forward (External Access)
```bash
kubectl port-forward -n kafka svc/kafka 9092:9092
# Now accessible at localhost:9092
```

## Token Efficiency

| Component | Tokens | In Context? |
|-----------|--------|-------------|
| SKILL.md | ~100 | ✓ Yes (when triggered) |
| REFERENCE.md | ~400 | ✗ No (on-demand only) |
| deploy.sh | 0 | ✗ No (executed) |
| verify.py | 0 | ✗ No (executed) |
| create-topics.sh | 0 | ✗ No (executed) |
| Output | ~15 | ✓ Yes (minimal) |

**Total context cost:** ~115 tokens

## Cross-Agent Compatibility

### Claude Code
```bash
claude "Deploy Kafka for LearnFlow"
# Triggers kafka-k8s-setup skill
```

### Goose
```bash
goose "Deploy Kafka for LearnFlow"
# Same skill works
```

## Dependencies

### Required Tools
- `kubectl` - Kubernetes CLI
- `helm` - Helm package manager
- Python 3.6+ for verification

### Kubernetes Cluster
- Minikube, K3s, or any K8s cluster
- Minimum resources: 2 CPU, 2GB RAM for Kafka

## Spec-Kit Plus Integration

Reads configuration from:
- `speckit-plus/03-specifications/infrastructure/kafka.yaml`

## Troubleshooting

### Pods Stuck in Pending
```bash
kubectl describe pod -n kafka <pod-name>
# Check Events section for resource issues
```

**Solution:** Increase Minikube resources:
```bash
minikube stop
minikube start --cpus=4 --memory=8192
```

### Helm Install Fails
```bash
# Check Helm version
helm version

# Reinstall chart
helm uninstall kafka -n kafka
bash scripts/deploy.sh
```

### Topics Not Created
```bash
# Manual topic creation
kubectl exec -n kafka kafka-0 -- kafka-topics.sh \
  --create --topic test-topic \
  --partitions 1 --replication-factor 1 \
  --bootstrap-server localhost:9092
```

## Advanced Configuration

### Production Settings
Edit `deploy.sh`:
```bash
helm upgrade --install kafka bitnami/kafka \
  --namespace kafka \
  --set replicaCount=3 \
  --set zookeeper.replicaCount=3 \
  --set persistence.enabled=true \
  --set persistence.size=10Gi \
  --set resources.requests.memory=2Gi \
  --set resources.requests.cpu=1000m
```

### Custom Topics
Edit `create-topics.sh`:
```bash
# Add more topics
TOPICS="student.events tutor.events matching.events custom.events"
```

### Authentication (Optional)
```bash
helm upgrade --install kafka bitnami/kafka \
  --set auth.enabled=true \
  --set auth.username=user \
  --set auth.password=password
```

## Testing

### Test Kafka Deployment
```bash
# Producer test
kubectl run -it --rm kafka-producer \
  --image=bitnami/kafka:latest \
  --restart=Never \
  -- kafka-console-producer.sh \
    --broker-list kafka.kafka.svc.cluster.local:9092 \
    --topic test-topic

# Consumer test (separate terminal)
kubectl run -it --rm kafka-consumer \
  --image=bitnami/kafka:latest \
  --restart=Never \
  -- kafka-console-consumer.sh \
    --bootstrap-server kafka.kafka.svc.cluster.local:9092 \
    --topic test-topic \
    --from-beginning
```

## Cleanup

```bash
# Delete Kafka deployment
helm uninstall kafka -n kafka

# Delete namespace
kubectl delete namespace kafka
```

## Integration with LearnFlow

Services connect to Kafka via Dapr pub/sub component:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  metadata:
    - name: brokers
      value: kafka.kafka.svc.cluster.local:9092
```

## Reusability

This skill works for:
- ✅ LearnFlow platform
- ✅ Any event-driven microservices
- ✅ Kafka development environments
- ✅ Message broker infrastructure

**Generic skill** - no LearnFlow-specific logic.

## Maintenance

### Upgrading Kafka
```bash
helm repo update
helm upgrade kafka bitnami/kafka -n kafka
```

### Monitoring
```bash
# Check Kafka logs
kubectl logs -n kafka kafka-0 -f

# Check ZooKeeper logs
kubectl logs -n kafka kafka-zookeeper-0 -f
```

---

**Version:** 2.0 (Upgraded with MCP Code Execution pattern)
**Status:** Active
**Maintained By:** Agentic AI
