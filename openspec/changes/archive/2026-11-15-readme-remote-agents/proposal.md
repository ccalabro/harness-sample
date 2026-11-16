## Why

The README should briefly explain that agent plans and builds can run remotely and produce draft pull requests for human review.

## What Changes

- Append a final section titled `## Running agents remotely` after the existing Contact section.
- Add two short sentences in American English explaining headless planning and builds on a dedicated machine and draft pull requests for human review.
- Preserve the existing README content.

## Capabilities

### New Capabilities

- `remote-agent-documentation`: Document remote, headless planning and builds and the human review handoff.

### Modified Capabilities

None.

## Impact

The product change affects only README.md. It does not implement remote execution, automation, or pull request creation, and makes no code, dependency, configuration, or runtime behavior changes. OpenSpec workflow artifacts are administrative documentation.
