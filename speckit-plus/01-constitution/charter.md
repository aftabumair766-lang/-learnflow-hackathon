# LearnFlow Project Charter

## Project Identity
- **Name:** LearnFlow
- **Type:** AI-Powered Learning Platform
- **Approach:** Spec-Driven, Skills-First, Agentic Development
- **Architecture:** Event-Driven Microservices

## Vision
Build a cloud-native platform connecting students with tutors, demonstrating Reusable Intelligence via AI agents.

## Core Principles
1. **Skills are the Product** - Not the application
2. **Spec-Driven** - Specs → Skills → Code
3. **Maximum Autonomy** - AI generates, humans guide
4. **Token Efficiency** - MCP Code Execution pattern
5. **Cross-Agent Compatible** - Claude Code + Goose

## Scope

### Included ✅
- Next.js frontend (student/tutor interfaces)
- 3 microservices (student-api, tutor-api, matching-service)
- Kafka event streaming
- Dapr service mesh
- PostgreSQL databases
- Kubernetes deployment
- Docusaurus documentation

### Excluded ❌
- Payment processing
- Video conferencing
- Mobile apps
- Production security (OAuth/JWT)
- Multi-tenancy

## Success Criteria
- [ ] Single prompt → full deployment works
- [ ] All Skills work on Claude Code AND Goose
- [ ] 80-98% token reduction achieved
- [ ] All services communicate via Kafka
- [ ] Complete documentation site

## Constraints
- Minikube (single-node K8s)
- Bitnami Helm charts only
- No manual code - Skills generate everything
- AAIF standards compliance

**Status:** ACTIVE | **Version:** 1.0
