---
name: sdd-database-migration-review
description: Use when an approved change modifies persistent schemas, indexes, data formats, backfills, or database migration behavior.
---

# Database migration review

Plan a verifiable transition for data and mixed application versions.

## Analysis

1. Inspect schema, migration tooling, data scale assumptions, and deployment
   ordering. Record constraints and affected readers/writers.
2. Describe the expand/migrate/contract sequence, backfill batching,
   resumability, idempotency, lock duration, and transaction boundaries.
3. Check old/new code compatibility during rollout. Define rollback and data
   recovery steps; name irreversible operations and their prerequisites.
4. Add tests for fresh installation, upgrade with representative existing
   data, interruption/retry, mixed versions, and rollback where supported.
   Specify data verification queries/invariants and the operational owner.
5. Return unknown destructive effects or missing recovery requirements to the
   conductor. Planning this skill does not authorize running a migration.

## Inputs and boundaries

Read `.sdd/POLICY.md`, the approved proposal and delta specs, current
`python .sdd/scripts/sdd-workflow.py status CHANGE`, and existing design/tasks. Run after approval
and before independent plan review; re-evaluate when approved scope changes.
Stop if approval is absent or stale, requirements conflict, or evidence needed
for a decision is unavailable. Return the gap to the conductor; never invent
approval or broaden the specification.

## Output and evidence

Write the analysis in `openspec/changes/CHANGE/design.md` and corresponding
uniquely identified verification tasks in `tasks.md`. Include the skill name,
applicability and reason, criterion references, inspected paths, assumptions,
and planned commands. Distinguish planned checks from observed results. These
artifacts are covered by `plan_revision`; do not create competing task lists
or rely on separate ungated analysis files. Report blockers and advisories to
the conductor. Changes invalidate stale plan review. Implementation remains
inside the eligible OpenSpec `apply` task and independent SDD reviews.
