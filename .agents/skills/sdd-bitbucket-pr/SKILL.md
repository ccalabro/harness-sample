---
name: sdd-bitbucket-pr
description: Use when the user explicitly requests a Bitbucket Cloud or Data Center pull request for a completed SDD change.
---

# Bitbucket pull request

## Authorization and inputs

Require an explicit user request to open this provider's review request after
the local SDD workflow and OpenSpec sync/archive are complete. Availability or
`ready-to-archive` alone never triggers publication. That request authorizes
the push needed to publish the intended branch; commit, approval, merge, and
deployment remain separate actions. Read `.sdd/POLICY.md`, completion/review
and check evidence, approved criteria, intended commits, and repository templates.

Inspect the current branch, Git status, staged and working diffs, remote URL,
source and target repositories/branches, and outgoing commits. Stop on an
ambiguous or mismatched remote, unrelated outgoing work, stale/incomplete gates,
or uncommitted intended changes. Use `sdd-commit` only if a commit is authorized;
never sweep up unrelated staged files. Do not rewrite history or force-push.
Missing CLI/authentication is an operator setup issue: report the required
setup, do not install tools, authenticate, or store credentials in the repo.

## Publication contract

Before preparing the request, ask: “Would you like the optional deep PR review?
It uses an extra model/session and may take longer and consume additional model
usage.” Do not dispatch the reviewer until the user opts in. If they
decline, proceed after the required final review without a second publication
review. If no suitably deeper model is available or its tier cannot be verified,
tell the user and offer to continue without this optional review; do not block
publication on it.

When the user opts in, after the duplicate lookup and verified branch push,
prepare the exact title/body and dispatch the generated `sdd-pr-reviewer` agent
in a fresh read-only session immediately before creating the request. Give it
the complete branch diff against the base branch, approved OpenSpec criteria
and archived artifacts, check/CI results, earlier review evidence, proposed
request text, and fixed head/base SHAs. Resolve model bindings from the `models`
section of `.sdd/config.yaml` (`profiles`, `roles`, `candidates`); if empty, use
the harness default and record it. Verify the actual model used. Require a
different actual
model from every implementer, a distinct reviewer session, and evidence from
provider model documentation or an explicit operator mapping that it has a
deeper reasoning tier. Different IDs alone do not establish a different model
level. Never silently use the harness default as proof of a different model
level.

For an opted-in review, require a recorded PASS with no blockers, concrete
evidence, reviewer session ID, actual model, all implementer models,
model_tier_evidence, and matching head/base SHAs before creating the request.
The reviewer returns request_title and request_body with its summary already
included. Save the report under ignored `.sdd/runs/` and use those exact final
fields without editing. A FAIL, missing evidence, or changed head/base requires
repair and a fresh review. The reviewer is independent of the implementer and
prior final reviewer; it cannot approve, publish, or merge.

Before pushing or creating, query open requests for the exact project repository,
source branch, and target branch. If one exists, report its URL/state; do not
create a duplicate. If lookup fails, stop rather than treating failure as an
empty result. Check again before retrying after a create timeout.

Prepare a title and description from the approved criteria, implementation,
observed tests/checks, migration/rollout notes, and repository template. Pass
explicit command arguments through an argument array or safe quoting, preserving
real newlines. Never interpolate description text as shell code. Push only the
intended source branch to the verified remote, verify its remote commit matches
the intended local commit, then run the independent review above and create the
request with explicit source/target.
Never approve, merge, enable automatic merge, deploy, or delete branches.

## Output and evidence

Inspect the resulting request and return its URL, state, source/target branches,
commit, and check summary to the user. Retain the sanitized commands/results in
task evidence. Report a partial push/create failure accurately and re-query
before retrying. Do not claim a remote request exists without observing it.

## Bitbucket CLI

Use the operator-installed `avivsinai/bitbucket-cli` binary `bkt`; do not build
a REST adapter or copy/install its agent skill. Check `bkt --version`,
`bkt auth status`, and the selected context/host against the Git remote. Inspect
installed help for context selection and use explicit `--context` where needed.
Cloud uses workspace/repository identity; Data Center uses project/repository
and may need explicit fork source identity.

Use `bkt pr list` with `--json` where supported and compare the exact open source
and target identities before creating. Prepare `bkt pr create` with explicit
repository/context, `--source`, `--target`, `--title`, and `--description` as one
argument; inspect installed help for platform-specific flags. Preserve real
newlines using structured arguments. Inspect the returned PR with `bkt pr view`.

Draft requests require Cloud or Data Center 8.18+. Check platform/version before
using `--draft`; if unsupported or unknown, stop and report the limitation.
Do not silently create a non-draft request. Keep credentials operator-managed.

References: [CLI setup](https://github.com/avivsinai/bitbucket-cli#installation)
and [PR commands](https://github.com/avivsinai/bitbucket-cli/blob/master/skills/bkt/rules/pr.md).
