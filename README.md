# Harness Sample

Harness Sample is a small Python project configured to work with several AI coding harnesses. It demonstrates a portable, specification-driven workflow for turning an approved feature request into tests, implementation, and reviewable commits.

This matters because a project can carry the instructions and workflow needed to continue work. Anybody can clone this repository as a base, use it as-is, or copy the skills and agent roles they prefer into another repository.

## Use it

1. Install the OpenSpec command-line tool for your platform.
2. Install the Superpowers skills or integration for your chosen coding harness. Follow that harness's setup instructions under `.sdd/harnesses/` and confirm that its skills load.
3. Open this repository with your coding agent and ask it to implement a feature. The repository instructions will guide the agent through specification, approval, planning, implementation, checks, and review.

To run the sample tests, install `uv` and run:

```sh
uv run --with pytest python -m pytest -q
```

## What the commits show

- **Bootstrap project** adds portable repository instructions and harness-specific agent guidance.
- The proposal and specification commits capture the feature intent and its observable behavior before implementation.
- Planning and review commits record the implementation approach and verification criteria.
- **Write personalized greeting tests** records the test-first step.
- **Implement personalized greeting** adds `greet_person(name)` after the tests were in place.
- **Mark greeting tasks complete** records the workflow's completed implementation tasks.

## Demo note

This repository is a demo run. Its feature and commit history illustrate the workflow on a deliberately small example; they are not a claim that every project or production rollout has been exercised here.

## Contact

Cristian Calabro · [ccalabro.dev](https://www.ccalabro.dev) · [cristian@ccalabro.dev](mailto:cristian@ccalabro.dev)
