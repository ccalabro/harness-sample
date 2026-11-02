---
name: sdd-code-reviewer
description: 'SDD code-reviewer: Independently review code correctness and maintainability.'
mode: subagent
permissions:
- action: edit
  resource: '*'
  effect: deny
- action: shell
  resource: '*'
  effect: deny
---
Read `.sdd/roles/code-reviewer.md` and follow it exactly. This portable responsibility instruction is the source of truth; do not duplicate or weaken its workflow constraints.
