# nodejs-dapr-service - Reference Documentation

## Overview
Generates complete Node.js + Express + Dapr microservice from YAML specification files.

## What It Does
1. Reads service spec from `speckit-plus/03-specifications/services/`
2. Generates:
   - `package.json` with dependencies
   - `src/index.js` with Express server
   - `Dockerfile` for containerization
   - `k8s/deployment.yaml` with Dapr annotations
3. Verifies generated structure
4. Ready for Docker build and K8s deployment

## Usage

### Generate Service from Spec
```bash
bash scripts/generate.sh \
  speckit-plus/03-specifications/services/student-api.yaml \
  speckit-plus/04-implementation/services/student-api
```

### Verify Generated Service
```bash
python3 scripts/verify.py speckit-plus/04-implementation/services/student-api
```

### Complete Workflow
```bash
SPEC="speckit-plus/03-specifications/services/student-api.yaml"
OUT="speckit-plus/04-implementation/services/student-api"

bash scripts/generate.sh $SPEC $OUT && \
python3 scripts/verify.py $OUT
```

## Generated Structure

```
output-dir/
├── package.json          # Node.js dependencies
├── src/
│   └── index.js         # Express server with health endpoint
├── Dockerfile           # Multi-stage build
└── k8s/
    └── deployment.yaml  # K8s Deployment + Service with Dapr
```

## Scripts

### generate.sh
**Purpose:** Generate service from spec

**Parameters:**
- `$1` - Path to spec YAML file
- `$2` - Output directory path

**Output:**
```
✓ Service generated at '<output-dir>'
```

### generator.py
**Purpose:** Core generation logic

**Reads from spec:**
- `service` - Service name
- `metadata.port` - Service port
- `endpoints` - API endpoints (TODO: full implementation)
- `events` - Pub/sub events (TODO)
- `database` - Database config (TODO)

**Generates:**
1. **package.json** - Express dependency
2. **src/index.js** - Basic server with `/health`
3. **Dockerfile** - node:20-alpine based
4. **k8s/deployment.yaml** - With Dapr sidecar annotations

### verify.py
**Purpose:** Verify generated service

**Checks:**
- package.json exists
- src/index.js exists
- Dockerfile exists
- k8s/deployment.yaml exists

**Output:**
- `✓ Service structure valid (4 files)` on success
- `✗ Missing files: ...` on failure

## Token Efficiency

| Component | Tokens | In Context? |
|-----------|--------|-------------|
| SKILL.md | ~100 | ✓ Yes (when triggered) |
| REFERENCE.md | ~600 | ✗ No (on-demand) |
| generate.sh | 0 | ✗ No (executed) |
| generator.py | 0 | ✗ No (executed) |
| verify.py | 0 | ✗ No (executed) |
| Output | ~20 | ✓ Yes (minimal) |

**Total context cost:** ~120 tokens

## Example: Generate student-api

```bash
bash scripts/generate.sh \
  speckit-plus/03-specifications/services/student-api.yaml \
  speckit-plus/04-implementation/services/student-api
```

**Output:**
```
Generating Node.js + Dapr service from spec...
✓ Generated student-api
  - package.json
  - src/index.js
  - Dockerfile
  - k8s/deployment.yaml
✓ Service generated at 'speckit-plus/04-implementation/services/student-api'
```

**Verify:**
```bash
python3 scripts/verify.py speckit-plus/04-implementation/services/student-api
# ✓ Service structure valid (4 files)
```

## Deployment

### Build Docker Image
```bash
cd speckit-plus/04-implementation/services/student-api
docker build -t student-api:latest .
```

### Load into Minikube
```bash
minikube image load student-api:latest
```

### Deploy to Kubernetes
```bash
kubectl apply -f k8s/deployment.yaml
```

### Verify Dapr Sidecar
```bash
kubectl get pods -n learnflow
# Should show 2/2 containers (app + dapr)
```

## Dapr Integration

### Annotations
```yaml
annotations:
  dapr.io/enabled: "true"
  dapr.io/app-id: "student-api"
  dapr.io/app-port: "3001"
```

### Dapr Sidecar
- Injected automatically
- Port 3500 for HTTP
- Port 50001 for gRPC

### Using Dapr in Code (TODO)
```javascript
// Publish event
await fetch('http://localhost:3500/v1.0/publish/kafka-pubsub/student.events', {
  method: 'POST',
  body: JSON.stringify({ student_id: 123 })
});

// Service invocation
const response = await fetch('http://localhost:3500/v1.0/invoke/tutor-api/method/api/tutors');
```

## Future Enhancements (TODO)

### Full Endpoint Generation
Currently generates only `/health`. Need to add:
- Parse `spec.endpoints`
- Generate routes for each endpoint
- Add request/response handling

### Event Handling
- Parse `spec.events.publishes`
- Add Dapr pub/sub publish calls
- Parse `spec.events.consumes`
- Add subscription routes

### Database Integration
- Parse `spec.database`
- Generate DB connection code
- Add query functions

### Complete Example
See `student-api.yaml` spec for full requirements.

## Cross-Agent Compatibility

### Claude Code
```bash
claude "Generate student-api service from spec"
# Triggers nodejs-dapr-service skill
```

### Goose
```bash
goose "Generate student-api service from spec"
# Same skill works
```

## Reusability

This skill works for:
- ✅ LearnFlow microservices
- ✅ Any Node.js + Dapr service
- ✅ Express-based APIs
- ✅ Event-driven microservices

**Generic generator** - customizable via spec files.

## Testing Generated Service

### Local Test
```bash
cd speckit-plus/04-implementation/services/student-api
npm install
npm start
# Server runs on port 3001

# Test health
curl http://localhost:3001/health
# {"status":"healthy"}
```

### Kubernetes Test
```bash
kubectl port-forward -n learnflow svc/student-api 3001:3001
curl http://localhost:3001/health
```

---

**Version:** 1.0
**Status:** Active (Basic generator - full implementation TODO)
**Maintained By:** Agentic AI
