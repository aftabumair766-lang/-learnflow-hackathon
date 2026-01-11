# LearnFlow Task Breakdown

## Task Hierarchy

### Phase 1: Foundation (Spec-Kit Plus)
- [x] Create constitution (charter, governance, standards)
- [ ] Define task breakdown
- [ ] Create complete specifications
- [ ] Setup implementation structure

### Phase 2: Infrastructure Skills
- [ ] **Task 2.1:** Kubernetes Foundation Skill
  - Namespace creation
  - Basic resource setup
  - Verification

- [ ] **Task 2.2:** Kafka Deployment Skill
  - Helm chart installation
  - Topic creation
  - Producer/consumer verification

- [ ] **Task 2.3:** Dapr Installation Skill
  - Dapr CLI setup
  - Dapr init on K8s
  - Component configuration

- [ ] **Task 2.4:** PostgreSQL Deployment Skill
  - Helm chart installation
  - Database creation
  - Connection verification

### Phase 3: Service Generation Skills
- [ ] **Task 3.1:** Node.js + Dapr Service Generator Skill
  - Express.js boilerplate
  - Dapr sidecar integration
  - Dockerfile generation
  - K8s manifests generation

- [ ] **Task 3.2:** Next.js + Dapr Frontend Generator Skill
  - Next.js 14 setup
  - TypeScript configuration
  - Dapr client integration
  - Dockerfile + manifests

### Phase 4: LearnFlow Services (Generated via Skills)
- [ ] **Task 4.1:** Student API Service
  - Endpoints: POST /register, GET /students, POST /request-tutor
  - Events: student.registered, tutor.requested
  - Database: students_db

- [ ] **Task 4.2:** Tutor API Service
  - Endpoints: POST /register, GET /tutors, PUT /availability
  - Events: tutor.registered, tutor.available
  - Database: tutors_db

- [ ] **Task 4.3:** Matching Service
  - Consumes: tutor.requested events
  - Logic: Match student with available tutor
  - Publishes: match.created events
  - Database: matching_db

- [ ] **Task 4.4:** LearnFlow Frontend
  - Student dashboard
  - Tutor dashboard
  - Matching status display
  - Real-time updates

### Phase 5: Deployment & Integration
- [ ] **Task 5.1:** Deploy all infrastructure
  - Kafka cluster running
  - Dapr installed
  - PostgreSQL instances running

- [ ] **Task 5.2:** Deploy all services
  - All pods in Running state
  - All databases connected
  - All Dapr sidecars healthy

- [ ] **Task 5.3:** End-to-End Verification
  - Student registration works
  - Tutor registration works
  - Matching logic executes
  - Events flow through Kafka
  - Frontend displays data

### Phase 6: Documentation & Polish
- [ ] **Task 6.1:** REFERENCE.md for all Skills
- [ ] **Task 6.2:** Docusaurus site setup
- [ ] **Task 6.3:** Architecture diagrams
- [ ] **Task 6.4:** Demo preparation

## Task Dependencies

```
Phase 1 (Specs) → Phase 2 (Infrastructure Skills)
                                ↓
                Phase 3 (Service Generator Skills)
                                ↓
                Phase 4 (LearnFlow Services)
                                ↓
                Phase 5 (Deployment)
                                ↓
                Phase 6 (Documentation)
```

## Skill Inventory (To Be Created)

| Skill Name | Purpose | Phase |
|------------|---------|-------|
| k8s-foundation | K8s namespace & basics | 2 |
| kafka-k8s-setup | Deploy Kafka on K8s | 2 |
| dapr-k8s-init | Install Dapr runtime | 2 |
| postgres-k8s-deploy | Deploy PostgreSQL | 2 |
| nodejs-dapr-service | Generate Node.js service | 3 |
| nextjs-dapr-app | Generate Next.js app | 3 |
| learnflow-deploy-all | Orchestrate full deployment | 5 |
| service-verify | Verify service health | 5 |
| docusaurus-setup | Setup docs site | 6 |

## Estimated Skill Count
- Infrastructure: 4 Skills
- Generators: 2 Skills
- Deployment: 2 Skills
- Documentation: 1 Skill
- **Total: ~9 reusable Skills**

(Plus 2 existing: agents-md-gen, kafka-k8s-setup)

**Status:** ACTIVE | **Version:** 1.0
