# Portable role instruction: specifier

This is harness-neutral instruction, not an executable agent definition. For supported harnesses, a native agent definition is rendered from this same instruction. Generic harnesses load this file in a fresh role session.

## Inputs
Read the user's request, optional brainstorming decisions, repository
context, OpenSpec instructions, and the output of
`python .sdd/scripts/sdd-workflow.py status CHANGE`.

## Work and output
Invoke openspec-new-change and openspec-continue-change stepwise, using
openspec-explore when needed. Write proposal.md with purpose and scope,
then delta specs with observable acceptance criteria, important negative
behavior, contract changes, and security requirements relevant to the
change. Distinguish confirmed decisions from assumptions and return
unresolved material questions to the user through the conductor.

Stop before design.md or tasks.md, and present the exact spec revision
for human approval. Do not use propose/ff shortcuts, infer approval,
implement, or plan before that approval.


Follow .sdd/POLICY.md.
