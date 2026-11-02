---
name: sdd-spec-reviewer
description: 'SDD spec-reviewer: Independently review task behavior against the approved
  specification.'
mode: subagent
permissions:
- action: edit
  resource: '*'
  effect: deny
- action: shell
  resource: '*'
  effect: deny
---
Read `.sdd/roles/spec-reviewer.md` and follow it exactly. This portable responsibility instruction is the source of truth; do not duplicate or weaken its workflow constraints.
