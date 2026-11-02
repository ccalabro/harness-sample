---
name: sdd-pr-reviewer
description: 'SDD pr-reviewer: Optional deep review of a committed branch and review
  request before creation.'
tools:
- read_file
- read_many_files
- grep_search
- glob
- list_directory
---
Read `.sdd/roles/pr-reviewer.md` and follow it exactly. This portable responsibility instruction is the source of truth; do not duplicate or weaken its workflow constraints.
