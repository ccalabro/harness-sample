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

**Applies:** Always. Invoked by reading the generated strategy instructions. Acceptance criteria map to deterministic unit tests:

| Criterion | Level and scenario | Task | Planned command |
|---|---|---|---|
| Greet a named person; preserve capitalization and internal spaces | Unit: `Ada Lovelace` returns `Hello, Ada Lovelace!` | T001 | `uv run --with pytest pytest -q tests/test_greeting.py` |
| Trim surrounding whitespace | Unit: padded name returns normalized greeting | T001 | `uv run --with pytest pytest -q tests/test_greeting.py` |
| Reject empty and whitespace-only names with exact error | Unit: empty and spaces/tabs raise exact `ValueError` | T001 | `uv run --with pytest pytest -q tests/test_greeting.py` |
| Full regression suite | Full suite after implementation | T001 | `uv run --with pytest pytest -q` |

Inspected paths: `.sdd/POLICY.md`, approved proposal and delta spec, generated conductor and test-strategy skill, and repository file inventory. Assumptions: Python and `uv` are available in the demo environment; pytest is fetched ephemerally for checks. Planned commands are not observed results.

### `sdd-threat-model`

**Applies:** Yes, because the function accepts caller-provided text. The only data flow is a name string into formatting; there is no filesystem, process, network, credential, or persistent-data access. Threat: whitespace or unusual text could produce an empty or malformed greeting. Mitigation: trim surrounding whitespace and reject blank results. Negative verification is included in T001 with empty, spaces, and tabs. Residual risk: arbitrary nonblank text is preserved as the approved contract requires.

### `sdd-api-contract-review`

**Applies:** Yes, because `greet_person(name: str) -> str` is a public Python function contract. Compatibility: this is a new function with no existing consumers. Error semantics are `ValueError("name must not be blank")`; contract cases are covered by T001 unit tests for valid, normalized, and invalid inputs. No versioning or migration is needed for this demo.

### `sdd-database-migration-review`

**Not applicable:** The change adds no schema or persistent data.

### `sdd-accessibility-review`

**Not applicable:** The change adds no user interface or interaction behavior.

### `sdd-observability-review`

**Not applicable:** The change adds no service, background job, or operational behavior.
