---
name: sdd-final-reviewer
description: 'SDD final-reviewer: Independently review the complete change before
  archive.'
mode: subagent
permissions:
- action: edit
  resource: '*'
  effect: deny
- action: shell
  resource: '*'
  effect: deny
---
Read `.sdd/roles/final-reviewer.md` and follow it exactly. This portable responsibility instruction is the source of truth; do not duplicate or weaken its workflow constraints.
