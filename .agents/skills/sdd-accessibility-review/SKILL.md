---
name: sdd-accessibility-review
description: Use when an approved change affects user interfaces, navigation, controls, content presentation, or assistive-technology behavior.
---

# Accessibility review

Translate accessible use of the changed interface into concrete checks.

## Analysis

1. Map affected user journeys to keyboard operation, focus order, visible
   focus, focus restoration, and freedom from keyboard traps.
2. Inspect semantic elements, accessible names, roles/states, instructions,
   validation/errors, status announcements, and screen-reader behavior.
3. Check contrast, non-color cues, zoom/reflow, reduced motion, and target
   sizes as relevant to the approved scope and platform.
4. Add automated checks and manual keyboard/screen-reader steps with expected
   results, platform/browser/tool versions, and responsible task IDs. Record
   limitations; automation alone does not establish accessible behavior.
   Return ambiguous acceptance criteria or missing user journeys to the conductor.

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
