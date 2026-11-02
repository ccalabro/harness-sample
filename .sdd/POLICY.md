# Repository SDD policy

Requirements and acceptance criteria live in OpenSpec. A human approves the
specification before planning. Planning, task spec/code, security, and final
reviews are performed by independent agents. Read the conductor skill to run
the workflow; use the generated project scripts to determine the next eligible step.

Implement under TDD with failing tests before implementation; confirm tests
actually ran, and run the full suite before submitting a task for review.
Define machine-readable contracts when a change crosses a system boundary.
Cover authentication, authorization, sensitive data, and dependency risks in
specifications and security reviews as relevant to the change.

Reviews cite evidence and distinguish blockers from advisories. Failed required
checks and exhausted repair budgets block the change. Agents cannot invent or
assume specification approval or grant themselves new execution permissions.
After the conductor has presented the specification and explicitly asked, a
human may reply `approved` in that active harness conversation; the conductor
may then record that attestation. The sole routine human review is specification
approval; uncertainty may still require a question.

Do not merge, push, or deploy without a separate user request. Never place keys
in repository configuration. This policy is generic; adapt it for this project
or reference an existing constitution here.
