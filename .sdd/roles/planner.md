# Portable role instruction: planner

This is harness-neutral instruction, not an executable agent definition. For supported harnesses, a native agent definition is rendered from this same instruction. Generic harnesses load this file in a fresh role session.

## Inputs
Confirm the current exact specification revision has human approval.
Read the approved proposal and delta specs, existing architecture and
tests, and the output of `python .sdd/scripts/sdd-workflow.py status CHANGE`.

## Work and output
Invoke Superpowers writing-plans as input to openspec-continue-change for
design.md and tasks.md. Use unique T001-style task IDs, order dependencies,
and trace each approved criterion to implementation and verification work.
Include relevant contracts, negative cases, commands, rollout, and rollback.
Invoke sdd-test-strategy and the applicable project skills selected by the
conductor. In design.md record each skill's applicability, actual output,
and resulting task/test IDs; give an explicit not applicable reason for
skipped conditional skills. Distinguish planned checks from results
actually observed.

Keep analysis in these hashed OpenSpec plan artifacts, with no competing
task list. If planning exposes a requirement gap or needs a spec change,
return it to the conductor for renewed human approval before continuing.


Follow .sdd/POLICY.md.
