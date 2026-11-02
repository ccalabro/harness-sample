---
name: sdd-threat-model
description: Use when an approved change touches authentication, authorization, payments, sensitive data, external input, filesystem or process access, or trust boundaries.
---

# Threat model

Turn the approved change's concrete attack surfaces into mitigations and tests.

## Analysis

1. Identify assets, actors, entry points, data flows, privileges, and trust
   boundaries from the specs and inspected architecture.
2. Describe plausible abuse paths: unauthorized access, injection, secret
   exposure, path traversal, unsafe process execution, dependency compromise,
   integrity loss, and resource exhaustion where applicable.
3. For each threat, record preconditions, impact, mitigation, residual risk,
   and the negative/security test and task that verifies it. Mark irrelevant
   categories with a reason; do not treat every category as a new requirement.
4. Identify required scanner commands only where configured or justified by
   the approved scope. Never claim an unavailable or unrun scan passed.
   Unresolved security requirements return to the conductor before plan review.

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
