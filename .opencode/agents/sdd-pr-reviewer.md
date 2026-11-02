---
name: sdd-pr-reviewer
description: 'SDD pr-reviewer: Optional deep review of a committed branch and review
  request before creation.'
mode: subagent
permissions:
- action: edit
  resource: '*'
  effect: deny
- action: shell
  resource: '*'
  effect: deny
---
Read `.sdd/roles/pr-reviewer.md` and follow it exactly. This portable responsibility instruction is the source of truth; do not duplicate or weaken its workflow constraints.
