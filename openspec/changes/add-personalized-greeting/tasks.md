# Tasks

## 1. Personalized greeting

- [x] T001 Write unit tests in `tests/test_greeting.py` for `Ada Lovelace`, surrounding whitespace, empty input, and spaces/tabs; run `uv run --with pytest pytest -q tests/test_greeting.py` and confirm failure because `greeting.py` is not implemented, then commit as `Write personalized greeting tests`.
- [ ] T002 Implement `greet_person(name: str) -> str` in `greeting.py` using `strip()` and the specified `ValueError`; run `uv run --with pytest python -m pytest -q` and confirm all tests pass, then commit as `Implement personalized greeting`.
