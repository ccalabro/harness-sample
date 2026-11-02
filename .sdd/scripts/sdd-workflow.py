"""Evidence-based lifecycle. Review submissions are attestations, not a security boundary."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from sdd_workflow_runtime import (SDDError, atomic_write, change_path, digest, load, now, read_json, repo_lock, require_success, run, safe_path, write_json)

TASK = re.compile(r"^\s*- \[([ xX])\]\s+(T[\w-]+)\s+(.+)$", re.MULTILINE)
REVIEW_KINDS = {"plan", "spec", "code", "security", "final"}


@dataclass(frozen=True)
class ReviewResult:
    verdict: str
    blockers: list[str]
    advisories: list[str]
    evidence: list[str]
    reviewer: str
    model: str
    revision: str

    @classmethod
    def parse(cls, data: dict[str, Any]) -> ReviewResult:
        try:
            result = cls(**data)
        except TypeError as exc:
            raise SDDError(
                "Review needs verdict, blockers, advisories, evidence, reviewer, model, revision"
            ) from exc
        if result.verdict not in ("PASS", "FAIL") or bool(result.blockers) != (
            result.verdict == "FAIL"
        ):
            raise SDDError("PASS must have no blockers; FAIL must have blockers")
        for value in (result.blockers, result.advisories, result.evidence):
            if not isinstance(value, list) or not all(
                isinstance(v, str) and v.strip() for v in value
            ):
                raise SDDError("Review findings and evidence must be lists of non-empty strings")
        if not result.evidence or not all(
            isinstance(v, str) and v.strip()
            for v in (result.reviewer, result.model, result.revision)
        ):
            raise SDDError(
                "Review must identify an independent reviewer session, actual model, and evidence"
            )
        return result


@dataclass(frozen=True)
class WorkflowState:
    change: str
    phase: str
    task: str | None
    reason: str
    revision: str
    spec_revision: str
    plan_revision: str
    required_reviews: list[str]
    brainstorming: str | None = None


def brainstorming_choice(root: Path, change: str) -> str | None:
    """Read a local workflow preference, outside all approval/review revisions."""
    change_path(root, change)
    data = read_json(safe_path(root, f".sdd/runs/{change}-preferences.json"), {})
    if not isinstance(data, dict) or data.get("brainstorming") not in (None, "yes", "no"):
        raise SDDError("Brainstorming preference must be yes or no")
    choice: str | None = data.get("brainstorming")
    return choice


def set_brainstorming(root: Path, change: str, choice: str) -> None:
    """Record an explicit per-change answer without granting workflow approval."""
    if choice not in ("yes", "no"):
        raise SDDError("Brainstorming choice must be yes or no")
    change_path(root, change)
    with repo_lock(root):
        path = safe_path(root, f".sdd/runs/{change}-preferences.json")
        write_json(path, {"brainstorming": choice})


def artifacts(root: Path, change: str) -> tuple[str, str]:
    folder = change_path(root, change)
    spec_paths = [folder / "proposal.md", *sorted((folder / "specs").rglob("*.md"))]
    spec = {
        str(p.relative_to(folder)): p.read_text(encoding="utf-8") for p in spec_paths if p.is_file()
    }
    plan: dict[str, str] = {"spec_revision": digest(str(spec))}
    for name in ("design.md", "tasks.md"):
        path = folder / name
        if path.exists():
            plan[name] = re.sub(r"\[[xX]\]", "[ ]", path.read_text(encoding="utf-8"))
    return digest(str(spec)), digest(str(plan))


def code_files(root: Path) -> dict[str, str]:
    """Tracked and non-ignored untracked content, including deletion markers.

    A symlink is hashed from the bytes it points at when that target stays
    inside the repository and is not ignored. Links outside the repository,
    links to ignored paths, and checked-out submodules are rejected so a
    review cannot stay valid after those bytes change.
    """
    names = require_success(
        run(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], root)
    )
    files: dict[str, str] = {}
    root_resolved = root.resolve()
    for name in sorted(set(names.split("\0"))):
        if not name or name.startswith((".sdd/", "openspec/")):
            continue
        path = root / name
        if path.is_symlink():
            files[name] = _hash_review_symlink(root_resolved, path, name)
        elif path.is_dir() and (path / ".git").exists():
            raise SDDError(f"Review refuses a checked-out submodule: {name}")
        elif path.is_file():
            files[name] = digest(path.read_bytes())
        elif not path.exists():
            files[name] = "deleted"
    return files


def _hash_review_symlink(root: Path, path: Path, name: str) -> str:
    target = path.resolve()
    try:
        relative = target.relative_to(root)
    except ValueError as exc:
        raise SDDError(f"Review refuses a symlink outside the repository: {name}") from exc
    ignored = run(["git", "check-ignore", "-q", "--", relative.as_posix()], root)
    if ignored.code == 0:
        raise SDDError(f"Review refuses a symlink to an ignored path: {name}")
    if not target.is_file():
        raise SDDError(f"Review refuses a symlink that does not point at a file: {name}")
    return digest(target.read_bytes())


def revision(root: Path, change: str) -> str:
    import json

    return digest(
        json.dumps(
            {
                "artifacts": artifacts(root, change),
                "files": code_files(root),
                "checks": load(root)["checks"],
            },
            sort_keys=True,
        )
    )


def record_path(root: Path, change: str) -> Path:
    return change_path(root, change) / ".sdd-review.json"


def records(root: Path, change: str) -> dict[str, Any]:
    data = read_json(
        record_path(root, change),
        {"schema_version": 1, "reviews": {}, "tasks": {}, "rounds": {}, "events": []},
    )
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise SDDError("Unsupported workflow record version")
    return data


def tasks(root: Path, change: str) -> list[tuple[str, bool, str]]:
    file = change_path(root, change) / "tasks.md"
    if not file.exists():
        return []
    text = file.read_text(encoding="utf-8")
    result = [(m[1], m[0].lower() == "x", m[2]) for m in TASK.findall(text)]
    checkboxes = re.findall(r"^\s*- \[[ xX]\]", text, re.MULTILINE)
    if len(checkboxes) != len(result) or len({t[0] for t in result}) != len(result):
        raise SDDError("Every task needs a unique ID: - [ ] T001 Description")
    return result


def passed(data: dict[str, Any], key: str, expected: str) -> bool:
    record = data["reviews"].get(key, {})
    return bool(record.get("verdict") == "PASS" and record.get("revision") == expected)


def status(root: Path, change: str) -> WorkflowState:
    folder = change_path(root, change)
    data = records(root, change)
    spec, plan = artifacts(root, change)
    rev = revision(root, change)
    brainstorming = brainstorming_choice(root, change)

    def state(
        phase: str, reason: str, task: str | None = None, reviews: list[str] | None = None
    ) -> WorkflowState:
        return WorkflowState(
            change, phase, task, reason, rev, spec, plan, reviews or [], brainstorming
        )

    if not (folder / "proposal.md").is_file() or not list((folder / "specs").rglob("*.md")):
        return state(
            "specification",
            "Resolve the brainstorming preference, then produce proposal and delta specs "
            "through OpenSpec.",
        )
    if data.get("approval", {}).get("revision") != spec:
        return state(
            "human-spec-review", "Human approval of this specification revision is required."
        )
    if not (folder / "design.md").is_file() or not tasks(root, change):
        return state("planning", "Create design.md and tasks.md using approved requirements.")
    if not passed(data, "plan", plan):
        if len(data["rounds"].get("plan", [])) > load(root)["workflow"]["max_repairs"]:
            return state("blocked", "Plan repair budget exhausted.")
        return state(
            "plan-review",
            "Independent plan reviewer must pass this plan revision.",
            reviews=["plan"],
        )
    files = code_files(root)
    ordered_tasks = tasks(root, change)
    # An active writer may legitimately modify files from earlier tasks. Finish
    # its review round before revisiting the now-stale earlier task evidence.
    ordered_tasks.sort(key=lambda item: not data["tasks"].get(item[0], {}).get("active", False))
    for task_id, checked, _ in ordered_tasks:
        task = data["tasks"].get(task_id, {})
        signatures = task.get("files", {})
        accepted = (
            task.get("accepted")
            and task.get("plan") == plan
            and all(files.get(p, "deleted") == signature for p, signature in signatures.items())
        )
        if checked and accepted:
            continue
        if accepted:
            return state(
                "task-completion",
                "Accepted task needs its checkbox finalized after interruption.",
                task_id,
            )
        if len(data["rounds"].get(task_id, [])) > load(root)["workflow"]["max_repairs"]:
            return state("blocked", f"Repair budget exhausted for {task_id}.", task_id)
        if task.get("active") and task.get("plan") == plan:
            needed = [k for k in ("spec", "code") if not passed(data, f"{task_id}:{k}", rev)]
            if needed:
                return state(
                    "implementation",
                    "Implement/fix this task, then obtain independent reviews.",
                    task_id,
                    needed,
                )
            return state(
                "task-completion",
                "Reviews pass; complete task evidence, then check its box.",
                task_id,
            )
        return state(
            "implementation",
            "Begin this task before implementation; checkboxes are not review evidence.",
            task_id,
            ["spec", "code"],
        )
    checks = data.get("checks", {})
    if checks.get("revision") != rev or not checks.get("passed"):
        return state("verification", "Run required checks and OpenSpec validation.")
    for kind in ("security", "final"):
        if not passed(data, kind, rev):
            if len(data["rounds"].get(kind, [])) > load(root)["workflow"]["max_repairs"]:
                return state("blocked", f"{kind} repair budget exhausted.")
            return state(f"{kind}-review", f"Independent {kind} review required.", reviews=[kind])
    return state(
        "ready-to-archive", "All gates pass; use OpenSpec sync/archive. No automatic merge or push."
    )


def persist(root: Path, change: str, data: dict[str, Any], event: str) -> None:
    data["events"].append({"at": now(), "event": event})
    write_json(safe_path(root, str(record_path(root, change).relative_to(root))), data)


def approve(root: Path, change: str, reviewer: str, expected: str) -> None:
    with repo_lock(root):
        current = status(root, change)
        if current.phase == "specification" or expected != current.spec_revision:
            raise SDDError("Specification missing or changed since preview; review it again.")
        if not reviewer.strip():
            raise SDDError("Human reviewer identity is required")
        data = records(root, change)
        data["approval"] = {"reviewer": reviewer, "revision": expected, "at": now()}
        persist(root, change, data, "human-spec-approved")


def begin_task(root: Path, change: str, task_id: str, implementer: str) -> None:
    with repo_lock(root):
        current = status(root, change)
        if current.phase != "implementation" or current.task != task_id:
            raise SDDError("This task is not eligible; inspect workflow status")
        if not implementer.strip():
            raise SDDError("Provide the implementer session ID")
        data = records(root, change)
        task = data["tasks"].get(task_id, {})
        if task.get("active") and task.get("plan") == current.plan_revision:
            if task["implementer"] != implementer:
                raise SDDError("Active task already belongs to a different implementer session")
            return
        data["tasks"][task_id] = {
            "active": True,
            "baseline": code_files(root),
            "implementer": implementer,
            "plan": current.plan_revision,
            "previous_files": task.get("files", {}),
        }
        persist(root, change, data, f"task-started:{task_id}")


def submit_review(
    root: Path, change: str, kind: str, review: ReviewResult, task_id: str | None = None
) -> None:
    with repo_lock(root):
        if kind not in REVIEW_KINDS:
            raise SDDError("Unknown review kind")
        current = status(root, change)
        expected = current.plan_revision if kind == "plan" else current.revision
        if review.revision != expected:
            raise SDDError("Review is stale; code or artifacts changed")
        phases = {
            "plan": "plan-review",
            "spec": "implementation",
            "code": "implementation",
            "security": "security-review",
            "final": "final-review",
        }
        if current.phase != phases[kind]:
            raise SDDError(f"Cannot record {kind} review in {current.phase}")
        data = records(root, change)
        key = kind
        round_key = kind
        if kind in ("security", "final") and any(
            t.get("implementer") == review.reviewer for t in data["tasks"].values()
        ):
            raise SDDError("Whole-change reviews must use independent sessions")
        if kind in ("spec", "code"):
            if task_id != current.task or not data["tasks"].get(task_id, {}).get("active"):
                raise SDDError("Begin the eligible task before recording reviews")
            task = data["tasks"][task_id]
            if review.reviewer == task["implementer"]:
                raise SDDError("Review must use an independent session")
            other = "code" if kind == "spec" else "spec"
            peer = data["reviews"].get(f"{task_id}:{other}", {})
            if peer.get("reviewer") == review.reviewer:
                raise SDDError("Spec and code reviews require distinct reviewer sessions")
            key = f"{task_id}:{kind}"
            round_key = str(task_id)
        previous = data["reviews"].get(key)
        if previous and previous["revision"] == expected:
            if previous == asdict(review):
                return
            raise SDDError(
                "A verdict is already recorded for this revision; fix the inputs before retrying"
            )
        data["reviews"][key] = asdict(review)
        if review.verdict == "FAIL":
            rounds = data["rounds"].setdefault(round_key, [])
            if expected not in rounds:
                rounds.append(expected)  # Concurrent reviewers share one repair round.
        persist(root, change, data, f"review:{key}:{review.verdict}")


def complete_task(root: Path, change: str, task_id: str) -> None:
    with repo_lock(root):
        current = status(root, change)
        if current.phase != "task-completion" or current.task != task_id:
            raise SDDError("Both current task reviews must pass before completion")
        data = records(root, change)
        task = data["tasks"][task_id]
        files = code_files(root)
        baseline = task["baseline"]
        task["files"] = {
            p: files.get(p, "deleted")
            for p in set(files) | set(baseline) | set(task.get("previous_files", {}))
            if files.get(p) != baseline.get(p) or p in task.get("previous_files", {})
        }
        task.update({"accepted": True, "active": False, "revision": current.revision})
        persist(root, change, data, f"task-completed:{task_id}")
        task_file = change_path(root, change) / "tasks.md"
        text = task_file.read_text(encoding="utf-8")
        text = re.sub(
            rf"(^\s*- )\[ \](\s+{re.escape(task_id)}\s)", r"\1[x]\2", text, flags=re.MULTILINE
        )
        atomic_write(task_file, text)


def run_checks(root: Path, change: str) -> dict[str, Any]:
    start = status(root, change)
    config = load(root)
    results: list[dict[str, Any]] = []
    commands = [
        *config["checks"],
        {
            "name": "openspec-validate",
            "argv": ["openspec", "validate", change, "--strict"],
            "required": True,
        },
    ]
    for check in commands:
        result = run(check["argv"], root, timeout=check.get("timeout", 300))
        results.append(
            {
                "name": check["name"],
                "required": check.get("required", True),
                "code": result.code,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
        )
    with repo_lock(root):
        if revision(root, change) != start.revision:
            raise SDDError(
                "Checks changed inputs or files changed concurrently; rerun against stable inputs"
            )
        data = records(root, change)
        report = {
            "revision": start.revision,
            "at": now(),
            "passed": all(r["code"] == 0 for r in results if r["required"]),
            "results": [
                {k: v for k, v in r.items() if k not in ("stdout", "stderr")} for r in results
            ],
        }
        data["checks"] = report
        persist(root, change, data, "checks-completed")
        # Output may contain project data; local, ignored log only.
        write_json(safe_path(root, f".sdd/runs/{change}-checks.json"), results)
    return report


def list_changes(root: Path) -> list[WorkflowState]:
    folder = root / "openspec/changes"
    if not folder.exists():
        return []
    return [
        status(root, p.name) for p in sorted(folder.iterdir()) if p.is_dir() and p.name != "archive"
    ]


if __name__ == "__main__":
    import argparse
    import json
    from dataclasses import asdict

    root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["status", "preference", "approve", "begin", "complete", "review", "checks"])
    parser.add_argument("change")
    parser.add_argument("values", nargs="*")
    parser.add_argument("--reviewer", default="")
    parser.add_argument("--revision", default="")
    parser.add_argument("--task", default=None)
    args = parser.parse_args()
    if args.action == "status":
        print(json.dumps(asdict(status(root, args.change)), indent=2))
    elif args.action == "preference":
        if len(args.values) != 1:
            parser.error("preference requires yes or no")
        set_brainstorming(root, args.change, args.values[0])
    elif args.action == "approve":
        approve(root, args.change, args.reviewer, args.revision)
    elif args.action == "begin":
        if len(args.values) != 2:
            parser.error("begin requires task ID and implementer session ID")
        begin_task(root, args.change, args.values[0], args.values[1])
    elif args.action == "complete":
        if len(args.values) != 1:
            parser.error("complete requires a task ID")
        complete_task(root, args.change, args.values[0])
    elif args.action == "review":
        if len(args.values) != 2:
            parser.error("review requires kind and report path")
        report = read_json(Path(args.values[1]), {})
        submit_review(root, args.change, args.values[0], ReviewResult.parse(report), args.task)
    elif args.action == "checks":
        print(json.dumps(run_checks(root, args.change), indent=2))
