# Tasks

## 1. README documentation

- [x] T001 Append the approved `## Running agents remotely` section and its exact two sentences to `README.md`, preserving existing content; first run the targeted assertion below and confirm it fails against the unmodified README, then make the edit and confirm it passes. Also run the documented full suite `uv run --with pytest python -m pytest -q`; if `uv` is unavailable, use an isolated pytest environment and run `PYTHONDONTWRITEBYTECODE=1 /tmp/readme-remote-agents-test-venv/bin/python -m pytest -q`. Run `git diff --check`, inspect `git diff -- README.md` and `git diff --name-only` to confirm the product diff is only the specified append, then run `PYTHONDONTWRITEBYTECODE=1 python3 .sdd/scripts/sdd-workflow.py checks readme-remote-agents`.

  Targeted assertion command:

  ```sh
  python3 - <<'PY'
  import subprocess
  from pathlib import Path

  original = subprocess.check_output(["git", "show", "HEAD:README.md"], text=True)
  addition = (
      "\n\n## Running agents remotely\n\n"
      "Plans and builds can run headlessly on a dedicated machine. "
      "The resulting changes can be opened as draft pull requests for human review.\n"
  )
  actual = Path("README.md").read_text()
  assert actual == original + addition, "README differs from HEAD by more than the approved final section"
  print("PASS: README preserves HEAD content and ends with the exact approved section")
  PY
  ```
