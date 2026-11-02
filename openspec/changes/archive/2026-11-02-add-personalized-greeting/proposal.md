# Proposal

## Why

The starter application always returns the same greeting, so it cannot show how
an input value changes application behavior. A personalized greeting is a small,
useful example that demonstrates a public function and its tests.

## What Changes

- Add `greet_person(name: str) -> str` to return a friendly greeting using the
  supplied name.
- Trim leading and trailing whitespace from a nonblank name before formatting
  the greeting.
- Raise `ValueError` with a clear message when the name is blank or contains
  only whitespace.
- Add tests for a normal name, whitespace trimming, and blank-name rejection.

## Capabilities

### New Capabilities

- `personalized-greetings`: Return a friendly greeting for a named person and
  reject blank names.

### Modified Capabilities

None.

## Impact

- Add the function to the small Python greeting module.
- Add focused tests for its output and invalid input behavior.
- No external dependencies or persistent data changes.
