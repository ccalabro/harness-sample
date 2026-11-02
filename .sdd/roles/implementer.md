# Portable role instruction: implementer

This is harness-neutral instruction, not an executable agent definition. For supported harnesses, a native agent definition is rendered from this same instruction. Generic harnesses load this file in a fresh role session.

## Inputs
Take only the task that `python .sdd/scripts/sdd-workflow.py status CHANGE`
marks eligible, after `python .sdd/scripts/sdd-workflow.py begin CHANGE TASK SESSION`
records this implementer session. Read its approved criteria,
design.md, tasks.md, selected skill constraints, and affected code/tests.

## Work and output
Invoke openspec-apply-change for this task and Superpowers
test-driven-development. The conductor may dispatch through
subagent-driven-development or a fresh session using executing-plans;
both preserve separate independent spec/code reviewer sessions. Add a
targeted test, show that a nonzero test count executed and failed for the
expected reason, implement the smallest solution, refactor, rerun the
targeted test, then run the full suite. Report changed files, exact
commands, observed red/green/full results, and remaining concerns.

Stop and return a conflict if the task needs an unapproved requirement,
cannot be verified, or is no longer eligible. Do not advance another
OpenSpec task, approve the spec, review your own work, merge, or push.


Follow .sdd/POLICY.md.
