---
name: sdd-observability-review
description: Use when an approved change affects service operations, background jobs, failure handling, telemetry, alerts, or operational diagnosis.
---

# Observability review

Specify how operators detect, explain, and respond to the changed behavior.

## Analysis

1. Identify success/failure signals and diagnostic questions for the affected
   journeys. Inspect existing logs, metrics, traces, dashboards, and alerts.
2. Define structured log events, metric units/labels, trace propagation, and
   correlation needed by the approved scope. Limit cardinality and overhead.
3. Keep telemetry privacy-safe: redact secrets and sensitive data, minimize
   identifiers, and specify retention/access requirements where applicable.
4. Map actionable alerts to thresholds, response/runbook, and operational
   ownership. Include instrumentation failure behavior and sampling limits.
5. Add tests for emitted signals, redaction, failure paths, and alert behavior;
   distinguish a planned dashboard from one observed working. Return missing
   operational requirements or unsafe telemetry to the conductor.

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
