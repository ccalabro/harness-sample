---
name: sdd-security-reviewer
description: 'SDD security-reviewer: Independently review whole-change security.'
mode: subagent
permissions:
- action: edit
  resource: '*'
  effect: deny
- action: shell
  resource: '*'
  effect: deny
---
Read `.sdd/roles/security-reviewer.md` and follow it exactly. This portable responsibility instruction is the source of truth; do not duplicate or weaken its workflow constraints.
