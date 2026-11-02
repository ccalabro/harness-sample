---
name: sdd-release-readiness
description: Use when an OpenSpec change has passed independent final review and is ready to archive, before specification sync and archival.
---

# Release readiness

Check the completed change's handover needs before OpenSpec archival. This is
an evidence-based skill check, not an additional state-machine approval gate.

## Inputs

Read `.sdd/POLICY.md`, `python .sdd/scripts/sdd-workflow.py status CHANGE`, approved criteria,
design/tasks, check results, independent reviews, and unresolved advisories.
Require `ready-to-archive`; stop and return unmet gates to the conductor.

## Check and output

Return a readiness report to the conductor's change evidence with criterion
references and inspected paths. For each item record evidence or an explicit
not-applicable reason: user/operator documentation, migration notes, feature
flags and rollout, rollback/recovery procedure, operational owner, and
unresolved review advisories. Distinguish advisories from approved requirements.
Do not claim unavailable checks or tools ran.

If required work is missing, return the change to the appropriate OpenSpec
update/apply action. Re-run reviews invalidated by edits, then repeat this
check. Do not silently promote advisories to requirements or waive blockers.
The conductor may then invoke `openspec-sync-specs` as appropriate and
`openspec-archive-change`. This skill does not authorize release, commit, push,
PR/MR creation, approval, merge, or deployment. Publication needs a separate
user request after the local workflow.
