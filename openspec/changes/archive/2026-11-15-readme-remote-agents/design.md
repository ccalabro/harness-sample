# Design

## Context

See `proposal.md` for motivation and `specs/remote-agent-documentation/spec.md` for the approved behavior. `README.md` currently ends with `## Contact` and its existing contact paragraph. The repository includes `tests/test_greeting.py`, and README documents its pytest command as `uv run --with pytest python -m pytest -q`.

## Goals / Non-Goals

**Goals:** Append only the approved section and exact sentences, preserving all existing README content.

**Non-Goals:** Implement remote execution, automation, pull request creation, or any runtime behavior.

## Decisions

- Append the exact approved Markdown after the Contact paragraph, separated by a blank line. This follows the spec's final-section requirement; no alternatives change the specified result.
- Verify the exact result with a targeted Python assertion against the HEAD version of `README.md`, run the documented full pytest suite, then inspect `git diff --check` and the product diff. No persistent test file is needed for the documentation-only change.
- The model configuration has empty profiles, role bindings, and candidates. Use the active Codex harness default model, record its actual identifier in run/review evidence, and verify its availability when each session starts.

## Risks / Trade-offs

- [Copy or placement drift] → An exact-content assertion checks the heading, sentence wording, final placement, and preservation of the HEAD README.
- [Unrelated product edits] → Inspect the product diff and require README.md to be the only product file changed.

## Migration Plan

No migration or deployment is applicable. Rollback consists of reverting the README addition.

## Skill Routing and Test Strategy

Analysis is based on the approved proposal and spec, `.sdd/POLICY.md`, current workflow status, `README.md`, tracked-file inventory (`git ls-files`), `tests/test_greeting.py`, and the documented pytest command. The initial inventory missed the tracked test file; final review caught that omission and this revision corrects the test plan.

| Skill | Applies? / approved scope reason | Invocation and output evidence | Criteria and tasks |
|---|---|---|---|
| `sdd-test-strategy` | Yes; required for every change. The spec defines two observable documentation criteria. | Invoked after approval and re-evaluated after final review found a missed tracked test file. Repository suite is documented in README and implemented in `tests/test_greeting.py`. Plan a targeted exact-content/preservation assertion, the full pytest suite, `git diff --check`, product diff inspection, strict OpenSpec validation, and workflow checks. | R1 → targeted documentation contract assertion, exact text + placement + preservation, T001; inline Python assertion in T001. R2 → product-scope diff inspection, T001; `git diff --check` and `git diff -- README.md`. Negative/regression cases: changed sentence, displaced heading, modified prior README content, or unrelated product-file changes must fail the assertion or scope check. Full-suite command: `uv run --with pytest python -m pytest -q` (documented in README); when `uv` is unavailable, run the suite with an isolated environment using `PYTHONDONTWRITEBYTECODE=1 /tmp/readme-remote-agents-test-venv/bin/python -m pytest -q`. Configured SDD checks are separately run with `PYTHONDONTWRITEBYTECODE=1 python3 .sdd/scripts/sdd-workflow.py checks readme-remote-agents`. |
| `sdd-threat-model` | Not applicable: no authentication, authorization, sensitive data, external input, filesystem/process behavior, or trust boundary changes. | Skill reviewed; not invoked because the approved scope is static README text only. | None. |
| `sdd-api-contract-review` | Not applicable: no public API, CLI, schema, event, or producer-consumer contract changes. | Skill reviewed; not invoked because only reader-facing README prose changes. | None. |
| `sdd-database-migration-review` | Not applicable: no persistent schema, data format, backfill, or migration behavior changes. | Skill reviewed; not invoked because no data is changed. | None. |
| `sdd-accessibility-review` | Not applicable: no interface, navigation, controls, interaction, or assistive-technology behavior changes. | Skill reviewed; not invoked because this is static repository documentation and adds no UI behavior. | None. |
| `sdd-observability-review` | Not applicable: no runtime service, job, failure handling, telemetry, alert, or operational diagnosis changes. | Skill reviewed; not invoked because the approved scope has no runtime effects. | None. |
| `superpowers:writing-plans` | Yes; implementation requires a bounded, reviewable plan. | Invoked. Output is this OpenSpec design and the single implementation task in `tasks.md`; OpenSpec remains the source of truth. | Implementation and verification are T001. |

## Test Mapping

| Criterion | Level and failure caught | Task | Verification |
|---|---|---|---|
| R1: final heading and exact two sentences after Contact | Targeted documentation contract assertion catches wording, order, or placement drift. | T001 | Inline `python3` assertion specified in T001; run before edit for a red result and after edit for green. |
| R2: only the approved append, preserving existing README | Targeted preservation assertion and manual diff inspection catch content loss or unrelated product changes. | T001 | Inline `python3` assertion, `git diff --check`, and inspect `git diff -- README.md` plus `git diff --name-only`. |

The full repository regression suite is `uv run --with pytest python -m pytest -q`, as documented in README. The command could not start in this environment because `uv` is unavailable. Installing pytest into the isolated temporary environment and running `PYTHONDONTWRITEBYTECODE=1 /tmp/readme-remote-agents-test-venv/bin/python -m pytest -q` executed the same repository suite: 4 passed.

## Review Focus

- Exact heading and capitalization: T001 assertion checks `## Running agents remotely`.
- Exact punctuation and wording of both sentences: T001 assertion compares the required literal ending.
- Final placement after Contact: T001 assertion checks the complete expected README ending.
- Existing contact content remains byte-for-byte intact: T001 assertion compares the current file with `git show HEAD:README.md` plus the addition.
- No unrelated product files changed: T001 scope check inspects `git diff --name-only`; workflow artifacts are separately allowed by R2.

## Open Questions

None.
