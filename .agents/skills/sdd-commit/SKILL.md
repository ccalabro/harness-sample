---
name: sdd-commit
description: Use when the user explicitly requests a local commit of a completed SDD change after specification sync and archive.
---

# Commit a completed change

Create only the local commit requested by the user. Skill availability and
`ready-to-archive` alone do not authorize invoking this skill.

## Inputs and stop conditions

Read `.sdd/POLICY.md`, the explicit request, workflow completion evidence,
archived OpenSpec artifacts, and the intended file list. Inspect workflow status
before archive or its retained completion evidence afterward. Stop if required
gates are incomplete/stale or intended changes cannot be distinguished from
unrelated edits. A local commit does not authorize push or review-request creation.

## Procedure

1. Inspect the branch, `git status --short`, working diff, and
   `git diff --cached`. Include intended sync/archive changes in the scope.
2. Before modifying the index, inspect existing partial staging. Preserve its
   selected hunks: do not reset, unstage, or overwrite them. If staged changes
   are unrelated or a partially staged file mixes intended/unrelated work,
   stop and ask how to separate it. If the existing index contains only
   intended changes, preserve it and add only reviewed missing paths/hunks.
3. Stage explicit paths using `git add -- PATH...`; use selective hunks when
   necessary. Never use broad `git add .` or `git add -A`. Exclude unrelated
   local files such as `PLAN.md` and `BUGS.md` unless explicitly in scope.
4. Inspect the final staged diff and file list against the completed change,
   run required checks, and create a descriptive local commit. If hooks fail
   or alter files, inspect the result; do not bypass hooks or amend unrelated
   commits. Do not self-approve, merge, push, or deploy.

## Output and evidence

Return the commit hash, included files, check results, and remaining local
changes to the user. Keep the intended scope and observed commands/results in
the task evidence; do not claim success before inspecting the resulting commit.
