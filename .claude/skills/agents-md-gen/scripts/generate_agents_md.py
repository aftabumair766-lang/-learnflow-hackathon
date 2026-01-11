#!/usr/bin/env python3
from pathlib import Path
import datetime

root = Path("..")  # skill folder ke ek level upar repo root

# Scan repo folders (ignore hidden)
folders = [p.name for p in root.iterdir() if p.is_dir() and not p.name.startswith(".")]

date = datetime.date.today().isoformat()
project_name = root.name

content = f"""# AGENTS.md

## Project
{project_name}

## Generated On
{date}

## Purpose
This file defines AI agents, their roles, responsibilities, and boundaries
for working in this repository.

---

## Repository Structure
{chr(10).join([f"- {f}/" for f in folders])}

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
"""

# Write AGENTS.md in repo root
root.joinpath("AGENTS.md").write_text(content)
print("✓ AGENTS.md generated dynamically with repo structure")

