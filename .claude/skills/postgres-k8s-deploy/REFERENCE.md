# postgres-k8s-deploy - Reference Documentation

## Overview
Deploys multiple PostgreSQL database instances on Kubernetes using Bitnami Helm chart for LearnFlow microservices.

## What It Does
1. Adds Bitnami Helm repository
2. Creates namespace for databases
3. Deploys 3 PostgreSQL instances:
   - `postgres-students` → `students_db`
   - `postgres-tutors` → `tutors_db`
   - `postgres-matching` → `matching_db`
4. Configures ephemeral storage (dev environment)
5. Sets default credentials (postgres/postgres)

## Usage

### Deploy All Databases
```bash
bash scripts/deploy.sh learnflow
```

### Verify Deployment
```bash
python3 scripts/verify.py learnflow
```

### Complete Workflow
```bash
bash scripts/deploy.sh learnflow && \
python3 scripts/verify.py learnflow
```

## Scripts

### deploy.sh
**Purpose:** Deploy PostgreSQL instances

**Parameters:**
- `$1` - Namespace (default: `learnflow`)

**Databases Deployed:**
| Instance | Database Name | Service DNS |
|----------|--------------|-------------|
| postgres-students | students_db | postgres-students.learnflow.svc.cluster.local |
| postgres-tutors | tutors_db | postgres-tutors.learnflow.svc.cluster.local |
| postgres-matching | matching_db | postgres-matching.learnflow.svc.cluster.local |

**Configuration:**
- Persistence: disabled (ephemeral)
- Memory: 256Mi request
- CPU: 100m request
- Password: `postgres` (dev only)

**Output:**
- `✓ PostgreSQL databases deployed to namespace '<namespace>'`

### verify.py
**Purpose:** Verify all PostgreSQL instances are healthy

**Parameters:**
- `sys.argv[1]` - Namespace (default: `learnflow`)

**Checks:**
- All 3 PostgreSQL instances exist
- All pods in Running state

**Output:**
- `✓ All PostgreSQL databases ready in namespace '<namespace>'` on success
- `✗ Some PostgreSQL databases not ready` on failure

**Exit Codes:**
- `0` - Success
- `1` - Failure

## Database Access

### Connection Strings

**student-api:**
```
host=postgres-students.learnflow.svc.cluster.local
port=5432
database=students_db
user=postgres
password=postgres
```

**tutor-api:**
```
host=postgres-tutors.learnflow.svc.cluster.local
port=5432
database=tutors_db
user=postgres
password=postgres
```

**matching-service:**
```
host=postgres-matching.learnflow.svc.cluster.local
port=5432
database=matching_db
user=postgres
password=postgres
```

### Connect from Pod
```bash
# Port-forward to access locally
kubectl port-forward -n learnflow svc/postgres-students 5432:5432

# Connect via psql
psql -h localhost -U postgres -d students_db
# Password: postgres

# Or exec into pod
kubectl exec -it -n learnflow postgres-students-0 -- psql -U postgres -d students_db
```

## Token Efficiency

| Component | Tokens | In Context? |
|-----------|--------|-------------|
| SKILL.md | ~100 | ✓ Yes (when triggered) |
| REFERENCE.md | ~500 | ✗ No (on-demand only) |
| deploy.sh | 0 | ✗ No (executed) |
| verify.py | 0 | ✗ No (executed) |
| Output | ~15 | ✓ Yes (minimal) |

**Total context cost:** ~115 tokens

## Cross-Agent Compatibility

### Claude Code
```bash
claude "Deploy PostgreSQL databases for LearnFlow"
# Triggers postgres-k8s-deploy skill
```

### Goose
```bash
goose "Deploy PostgreSQL databases for LearnFlow"
# Same skill works
```

## Dependencies

### Required Tools
- `kubectl` - Kubernetes CLI
- `helm` - Helm package manager
- Kubernetes cluster running

### Minimum Resources
- 1 CPU, 1GB RAM for all 3 databases

## Spec-Kit Plus Integration

Reads configuration from:
- `speckit-plus/03-specifications/infrastructure/postgresql.yaml`
- `speckit-plus/03-specifications/services/student-api.yaml` (database: students_db)
- `speckit-plus/03-specifications/services/tutor-api.yaml` (database: tutors_db)
- `speckit-plus/03-specifications/services/matching-service.yaml` (database: matching_db)

## Troubleshooting

### Pods Stuck in Pending
```bash
kubectl describe pod -n learnflow postgres-students-0
# Check Events for resource issues
```

**Solution:** Increase Minikube resources

### Cannot Connect to Database
```bash
# Check service exists
kubectl get svc -n learnflow | grep postgres

# Check pod logs
kubectl logs -n learnflow postgres-students-0

# Test connection from within cluster
kubectl run -it --rm psql-client \
  --image=postgres:15 \
  --restart=Never \
  -- psql -h postgres-students.learnflow.svc.cluster.local -U postgres -d students_db
```

### Helm Install Fails
```bash
# Check existing releases
helm list -n learnflow

# Uninstall and retry
helm uninstall postgres-students -n learnflow
bash scripts/deploy.sh learnflow
```

## Advanced Configuration

### Enable Persistence (Production)
Edit `deploy.sh`:
```bash
helm upgrade --install postgres-$DB bitnami/postgresql \
  --namespace $NAMESPACE \
  --set auth.postgresPassword=postgres \
  --set auth.database=${DB}_db \
  --set primary.persistence.enabled=true \
  --set primary.persistence.size=10Gi \
  --set primary.persistence.storageClass=standard
```

### Increase Resources
```bash
--set primary.resources.requests.memory=1Gi \
--set primary.resources.requests.cpu=500m \
--set primary.resources.limits.memory=2Gi \
--set primary.resources.limits.cpu=1000m
```

### Use Secrets for Passwords
```bash
# Create secret
kubectl create secret generic postgres-secret \
  -n learnflow \
  --from-literal=postgres-password=<strong-password>

# Reference in Helm
--set auth.existingSecret=postgres-secret
```

## Database Initialization

### Create Tables
```bash
# Connect to database
kubectl exec -it -n learnflow postgres-students-0 -- psql -U postgres -d students_db

# Create schema
CREATE TABLE students (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  grade VARCHAR(50),
  subjects TEXT[],
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Run Migrations (from service)
Services should handle migrations on startup using tools like:
- **Node.js**: `knex`, `sequelize`, `typeorm`
- **Python**: `alembic`, `django migrations`

## Testing

### Test Database Connection
```bash
# Run test pod
kubectl run -it --rm test-postgres \
  --image=postgres:15 \
  --restart=Never \
  -- psql -h postgres-students.learnflow.svc.cluster.local -U postgres -d students_db -c "SELECT 1"
```

### Insert Test Data
```sql
INSERT INTO students (name, email, grade, subjects)
VALUES ('Ali Khan', 'ali@example.com', '10', ARRAY['Math', 'Science']);
```

## Cleanup

```bash
# Delete all PostgreSQL instances
for DB in students tutors matching; do
  helm uninstall postgres-$DB -n learnflow
done

# Delete PVCs (if persistence enabled)
kubectl delete pvc -n learnflow -l app.kubernetes.io/name=postgresql
```

## Integration with LearnFlow Services

### student-api (Node.js example)
```javascript
const { Pool } = require('pg');

const pool = new Pool({
  host: process.env.DB_HOST || 'postgres-students.learnflow.svc.cluster.local',
  port: 5432,
  database: 'students_db',
  user: 'postgres',
  password: 'postgres'
});

// Use pool for queries
const result = await pool.query('SELECT * FROM students');
```

### Environment Variables
```yaml
env:
  - name: DB_HOST
    value: postgres-students.learnflow.svc.cluster.local
  - name: DB_PORT
    value: "5432"
  - name: DB_NAME
    value: students_db
  - name: DB_USER
    value: postgres
  - name: DB_PASSWORD
    value: postgres
```

## Monitoring

### Check Database Size
```bash
kubectl exec -n learnflow postgres-students-0 -- \
  psql -U postgres -d students_db -c "\l+"
```

### View Active Connections
```sql
SELECT * FROM pg_stat_activity;
```

### Database Logs
```bash
kubectl logs -n learnflow postgres-students-0 -f
```

## Reusability

This skill works for:
- ✅ LearnFlow platform
- ✅ Any microservices needing PostgreSQL
- ✅ Development databases
- ✅ Multi-database architectures

**Configurable** - Change database names in `deploy.sh` for other projects.

## Upgrading PostgreSQL

```bash
# Upgrade chart
helm repo update
helm upgrade postgres-students bitnami/postgresql -n learnflow

# Upgrade PostgreSQL version
--set image.tag=16
```

## Backup & Restore

### Backup
```bash
kubectl exec -n learnflow postgres-students-0 -- \
  pg_dump -U postgres students_db > backup.sql
```

### Restore
```bash
cat backup.sql | kubectl exec -i -n learnflow postgres-students-0 -- \
  psql -U postgres students_db
```

---

**Version:** 1.0
**Status:** Active
**Maintained By:** Agentic AI
