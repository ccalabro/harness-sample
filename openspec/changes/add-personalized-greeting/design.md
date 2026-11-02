# Design

## Context

The repository currently contains only the harness setup and OpenSpec change. The approved behavior is defined in `specs/personalized-greetings/spec.md`. The implementation can use Python's standard library and needs no runtime dependency.

## Goals / Non-Goals

**Goals:** Implement the specified name trimming, greeting format, and blank-name error with a small unit-testable function.

**Non-Goals:** Add a command-line interface, localization, or external packages.

## Decisions

- Put `greet_person(name: str) -> str` in `greeting.py`; this keeps the public function easy to import and avoids unnecessary package structure.
- Use `str.strip()` to normalize surrounding whitespace and reject an empty result with the exact specified `ValueError` message. This preserves capitalization and internal spacing.
- Use pytest for focused and full-suite tests, invoked with `uv run --with pytest` so the demo repository does not need a runtime dependency or committed environment.

## Risks / Trade-offs

- [Callers pass a non-string value] → The approved contract specifies names as text; no extra type coercion or behavior is introduced.
- [Whitespace behavior follows Python's Unicode-aware `strip()`] → Tests pin the required spaces and tabs; broader normalization is outside the approved contract.

## Test Strategy

### `sdd-test-strategy`

**Applies:** Always. Invoked by reading and applying `.agents/skills/sdd-test-strategy/SKILL.md`. Analysis output: all four scenario assertions are deterministic unit tests; no external service or fixture is required; the negative cases are the empty string and a string containing spaces and tabs. A full-suite invocation follows implementation. This catches output formatting, whitespace normalization, and blank rejection regressions.

| Criterion | Level and scenario | Task | Planned command |
|---|---|---|---|
| Greet a named person; preserve capitalization and internal spaces | Unit: `Ada Lovelace` returns `Hello, Ada Lovelace!` | T001 | `uv run --with pytest pytest -q tests/test_greeting.py` |
| Trim surrounding whitespace | Unit: padded name returns normalized greeting | T001 | `uv run --with pytest pytest -q tests/test_greeting.py` |
| Reject empty and whitespace-only names with exact error | Unit: empty and spaces/tabs raise exact `ValueError` | T001 | `uv run --with pytest pytest -q tests/test_greeting.py` |
| Full regression suite | Full suite after implementation | T001 | `uv run --with pytest pytest -q` |

Inspected paths: `.sdd/POLICY.md`, approved proposal and delta spec, generated conductor and test-strategy skill, and repository file inventory. Environment evidence: `command -v uv` resolved to `/Users/cristiancalabro/.local/bin/uv`; Python will be invoked by `uv`. Pytest is fetched ephemerally for checks. Planned commands are not observed results.

### `sdd-threat-model`

**Applies:** Yes, because the function accepts caller-provided text. Invoked by reading and applying `.agents/skills/sdd-threat-model/SKILL.md`. Analysis output: asset is the returned greeting; actor is any caller; entry point is the `name` argument; flow is argument → trim/blank validation → formatted return. No privilege, filesystem, process, network, credential, or persistent-data boundary exists. Threat: whitespace-only input could yield an empty greeting; mitigation is trim then reject, with exact-message negative tests in T001. Threat: unusual nonblank text could change presentation; the approved behavior preserves internal content, so this is intentional. Residual risk: no escaping or display policy exists because the function returns plain text and has no rendering sink.

### `sdd-api-contract-review`

**Applies:** Yes, because `greet_person(name: str) -> str` is a public Python function contract. Invoked by reading and applying `.agents/skills/sdd-api-contract-review/SKILL.md`. Analysis output: this is a newly added producer with no existing consumers, so there is no compatibility break or version migration. Success returns a string in the specified format after edge trimming; failure raises `ValueError("name must not be blank")`. T001 and T002 cover the contract with named, whitespace-normalized, empty, and whitespace-only inputs. There are no serialization, ordering, authentication, retry, or idempotency concerns for this local function.

### `sdd-database-migration-review`

**Not applicable:** The change adds no schema or persistent data.

### `sdd-accessibility-review`

**Not applicable:** The change adds no user interface or interaction behavior.

### `sdd-observability-review`

**Not applicable:** The change adds no service, background job, or operational behavior.
