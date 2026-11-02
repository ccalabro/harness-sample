# Harness Sample

Harness Sample is a small Python project configured to work with several AI coding harnesses (Claude Code, Codex, Gemini CLI, Grok, GitHub Copilot, OpenCode, or a generic setup). It demonstrates a portable, specification-driven workflow for turning an approved feature request into tests, implementation, and reviewable commits.

## Why

When AI agents write most of the code, the rules around them matter as much as the code. This repository carries those rules with it, so every agent follows the same workflow:

- Only a human can approve the specification.
- Tests are written before the implementation.
- Separate reviewer sessions check the plan, each task, security, and the final result, and each review is recorded.
- Agents don't merge, push, or deploy without a separate request from a person (`.sdd/POLICY.md`).

You can clone this repository as a base, use it as-is, or copy the skills and agent roles you prefer into another repository.

## Use it

1. Install OpenSpec 1.13.1 (needs Node.js 20.19 or later):

   ```sh
   npm install -g @fission-ai/openspec@1.13.1
   openspec --version
   ```

2. Install Superpowers for your coding harness. For example:
   - Claude Code: `claude plugin marketplace add obra/superpowers-marketplace`, then `claude plugin install superpowers@superpowers-marketplace`
   - Codex: open `/plugins`, search for Superpowers, and select Install Plugin.

   Steps for Gemini CLI, Grok, Copilot, OpenCode, and other harnesses are in `.sdd/harnesses/`. Restart the harness and confirm its skills load.

3. Open this repository with your coding agent and ask it to implement a feature. `AGENTS.md` routes the request through the `sdd-run` skill, which checks that OpenSpec and Superpowers are available and then guides the agent through specification, approval, planning, implementation, checks, and review.

To run the sample tests, install `uv` and run:

```sh
uv run --with pytest python -m pytest -q
```

## What the commits show

Start with `git log --oneline`. Each step of the workflow is its own commit.

- **Bootstrap project** adds portable repository instructions and harness-specific agent guidance.
- The proposal and specification commits capture the feature intent and its observable behavior before implementation.
- Planning commits record the implementation approach and verification criteria.
- **Write personalized greeting tests** records the test-first step.
- **Implement personalized greeting** adds `greet_person(name)` after the tests were in place.
- **Mark greeting tasks complete** records the completed implementation tasks.
- **Record workflow review evidence** and **Record final review outcome** commit the review record (`.sdd-review.json`): the human spec approval, the spec, code, security, and final reviews, and the OpenSpec validation result.
- **Sync** and **Archive** merge the approved spec into `openspec/specs/` and move the change to `openspec/changes/archive/`.
- **Updated harness files** refreshes the agent workflow files after the run, the way an existing project would receive template updates.

## Demo note

This repository is a demo run on a deliberately small example. I approved the specification myself. Reviews ran as separate agent sessions, recorded in `openspec/changes/archive/2026-11-02-add-personalized-greeting/.sdd-review.json`, and the implementation tasks ran in the main Codex session. Paths inside that record point to the change folder before it was archived. It is not a claim that larger projects or production rollouts have been exercised here.

## Third-party tools

[OpenSpec](https://github.com/Fission-AI/OpenSpec) (MIT) owns the specification and change files. [Superpowers](https://github.com/obra/superpowers) is referenced but not included. See `THIRD_PARTY_NOTICES` for details.

## License

MIT. See `LICENSE`.

## Contact

Cristian Calabro · [ccalabro.dev](https://www.ccalabro.dev) · [cristian@ccalabro.dev](mailto:cristian@ccalabro.dev)