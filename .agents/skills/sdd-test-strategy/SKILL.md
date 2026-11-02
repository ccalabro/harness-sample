---
name: sdd-test-strategy
description: Use when preparing the implementation plan for an approved OpenSpec change or revising its acceptance criteria or task scope.
---

# Test strategy

Map every acceptance criterion to observable verification before plan review.

## Analysis

1. Inventory existing tests, fixtures, contracts, commands, and CI constraints.
2. For each criterion, choose unit, integration, end-to-end, or contract tests;
   explain the boundary exercised and the production failure each test catches.
3. Include negative cases, permissions, malformed inputs, failures, and relevant
   regression cases. Identify deterministic fixtures and external dependencies.
4. Record a criterion → test level → scenario → task ID → command mapping in
   the design. Add red/green evidence requirements to implementation tasks and
   include the full-suite command. Manual checks need explicit steps and an
   expected result. Flag untestable or ambiguous criteria for resolution.

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
