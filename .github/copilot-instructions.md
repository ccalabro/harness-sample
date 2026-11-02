<!-- sdd-managed:start -->
# Mandatory SDD routing

When the user asks to add, implement, change, fix, refactor, or otherwise do
feature work, invoke this repository's `sdd-run` skill immediately, before
exploring, planning, or editing. Do not implement directly outside that skill.
Use the harness's native skill invocation mechanism; if it cannot invoke a
project skill, read `.agents/skills/sdd-run/SKILL.md` and follow it exactly.

OpenSpec owns specifications and change artifacts; Superpowers provides
optional brainstorming, `writing-plans`, `test-driven-development`, and
`subagent-driven-development` or `executing-plans` for fresh-session handoffs.
The conductor asks yes/no before proposal/specs, saves the per-change answer,
and preserves it on resume. It invokes applicable project skills and records
their outputs in the OpenSpec plan/task evidence. Run
`python .sdd/scripts/sdd-workflow.py status CHANGE` before each phase. Only a human can approve
the specification. Model and harness guidance is under `.sdd/harnesses/`.
<!-- sdd-managed:end -->
