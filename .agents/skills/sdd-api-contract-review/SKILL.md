---
name: sdd-api-contract-review
description: Use when an approved change adds or changes a public API, CLI interface, event, schema, or other producer-consumer contract.
---

# API contract review

Make compatibility and failure behavior explicit before implementation.

## Analysis

1. Identify producers, consumers, public schemas, CLI flags/output/exit codes,
   events, and versions affected by the approved criteria.
2. Compare current and proposed contracts, including optionality, defaults,
   validation, serialization, ordering, and backward compatibility.
3. Specify error semantics and applicable authentication, authorization,
   retries, idempotency, pagination, and deprecation/versioning behavior.
4. Add contract tests for old/new consumers, valid and invalid payloads,
   failure responses, and machine-readable output. Cite schema examples and
   consumer evidence; return unresolved breaking changes to the conductor.

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
