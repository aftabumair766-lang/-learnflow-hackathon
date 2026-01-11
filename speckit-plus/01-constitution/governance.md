# LearnFlow Governance Rules

## Development Rules

### ABSOLUTE RULES (Non-Negotiable)

#### 1. Skills-First Development
- ❌ NO manual application code allowed
- ❌ NO scaffolding outside `.claude/skills/`
- ✅ EVERY capability must be a reusable Skill

#### 2. MCP Usage Policy
- ❌ NO MCP servers loaded directly into agent context
- ✅ MCP servers treated as Code APIs via scripts
- ✅ Scan for existing MCP before creating new ones

#### 3. MCP Code Execution Pattern
- ❌ NO direct MCP tool calls in chat
- ✅ ALL MCP interaction in `.claude/skills/*/scripts/`
- ✅ ONLY minimal output enters context

#### 4. Token Efficiency
- SKILL.md ≤ 100 tokens
- REFERENCE.md never auto-loaded
- Scripts do heavy work, not markdown
- NO logs/JSON/YAML in context
- Return only: ✓/✗, counts, status

#### 5. Spec-Kit Plus Mandatory
```
Specs → Skills → Scripts → Deployment
```
- NO jumping to implementation
- ALL work follows Spec-Kit Plus

#### 6. Reusability
- Skills must work beyond LearnFlow
- Avoid LearnFlow-specific hardcoding
- Generic, composable skills preferred

#### 7. Cross-Agent Compatibility
- MUST work on Claude Code AND Goose
- AAIF-compatible format
- No Claude-only assumptions

## Decision Authority

| Decision Type | Authority | Process |
|--------------|-----------|---------|
| Architecture | AI Agent | Based on specs |
| Skill Design | AI Agent | Following governance |
| Spec Approval | Human Supervisor | Review & approve |
| Deployment | AI Agent (via Skills) | Automated |

## Quality Gates

### Before Creating Any Skill:
- [ ] Is it reusable beyond this project?
- [ ] Does similar Skill already exist?
- [ ] Does it follow MCP Code Execution pattern?
- [ ] Is SKILL.md ≤ 100 tokens?
- [ ] Will it work on Goose too?

### Before Deployment:
- [ ] All specs defined
- [ ] All Skills tested
- [ ] Token efficiency verified
- [ ] Cross-agent compatibility checked

## Change Management
- Specs can evolve
- Skills must remain backward compatible
- All changes documented in REFERENCE.md

**Status:** ACTIVE | **Version:** 1.0
