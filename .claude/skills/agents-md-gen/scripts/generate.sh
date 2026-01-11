#!/usr/bin/env bash
set -e

echo "🔍 Analyzing repository..."

PROJECT_NAME=$(basename "$(pwd)")
DATE=$(date +"%Y-%m-%d")

cat <<EOF > AGENTS.md
# AGENTS.md

## Project
$PROJECT_NAME

## Generated On
$DATE

## Purpose
This file defines AI agents, their roles, responsibilities, and boundaries
for working in this repository.

---

## Agent: Architect
**Responsibilities**
- Design system architecture
- Make high-level technical decisions
- Ensure scalability and maintainability

**Restrictions**
- Does not write production code
- Does not modify business logic

---

## Agent: Developer
**Responsibilities**
- Implement features
- Fix bugs
- Write clean, maintainable code

**Restrictions**
- Must follow architectural decisions
- No breaking changes without approval

---

## Agent: Reviewer
**Responsibilities**
- Review code for quality and security
- Suggest improvements
- Enforce standards

**Restrictions**
- Does not merge code
- Does not introduce new features

---

## Usage Rules
- One agent per task
- No overlapping responsibilities
- All actions must align with project goals
EOF

echo "✅ AGENTS.md generated successfully"

