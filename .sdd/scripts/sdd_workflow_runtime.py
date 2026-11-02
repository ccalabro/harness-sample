"""Standard-library support for the generated project workflow engine."""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast


class SDDError(Exception):
    pass


@dataclass(frozen=True)
class CommandResult:
    argv: list[str]
    code: int
    stdout: str
    stderr: str


def launch_argv(executable: str, args: list[str]) -> list[str]:
    if executable.lower().endswith((".cmd", ".bat")):
        return ["cmd.exe", "/c", subprocess.list2cmdline([executable, *args])]
    return [executable, *args]


def run(argv: list[str], cwd: Path | None = None, *, timeout: int = 120, env: dict[str, str] | None = None) -> CommandResult:
    executable = shutil.which(argv[0])
    if not executable:
        return CommandResult(argv, 127, "", f"Not installed or not on PATH: {argv[0]}")
    try:
        result = subprocess.run(launch_argv(executable, argv[1:]), cwd=cwd, env=env, text=True, encoding="utf-8", errors="replace", capture_output=True, stdin=subprocess.DEVNULL, timeout=timeout, check=False, shell=False)
        return CommandResult(argv, result.returncode, result.stdout, result.stderr)
    except subprocess.TimeoutExpired:
        return CommandResult(argv, 124, "", f"Command timed out after {timeout}s")
    except OSError as exc:
        return CommandResult(argv, 126, "", str(exc))


def require_success(result: CommandResult) -> str:
    if result.code:
        raise SDDError(f"{result.argv[0]} failed ({result.code}): {result.stderr.strip()}")
    return result.stdout.strip()


def safe_path(root: Path, relative: str) -> Path:
    candidate = root / relative
    try:
        candidate.resolve().relative_to(root.resolve())
    except ValueError as exc:
        raise SDDError(f"Path escapes repository: {relative}") from exc
    cursor = candidate
    while cursor != root and cursor != cursor.parent:
        if cursor.is_symlink():
            raise SDDError(f"Refusing managed symlink: {relative}")
        cursor = cursor.parent
    return candidate


def change_path(root: Path, change: str) -> Path:
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,99}", change) or change == "archive":
        raise SDDError("Change IDs must contain only letters, digits, underscores, and hyphens.")
    return safe_path(root, f"openspec/changes/{change}")


def digest(data: str | bytes) -> str:
    return hashlib.sha256(data.encode() if isinstance(data, str) else data).hexdigest()


def now() -> str:
    return datetime.now(UTC).isoformat()


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        raise SDDError(f"Cannot read JSON: {path}") from exc


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".sdd-write-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def write_json(path: Path, data: Any) -> None:
    atomic_write(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


@contextmanager
def repo_lock(root: Path) -> Iterator[None]:
    folder = safe_path(root, ".sdd/runs")
    folder.mkdir(parents=True, exist_ok=True)
    lock_path = folder / "project-workflow.lock"
    deadline = time.monotonic() + 10
    descriptor = None
    while descriptor is None:
        try:
            descriptor = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
            if time.monotonic() >= deadline:
                raise SDDError("Timed out waiting for another workflow update") from None
            time.sleep(0.05)
    try:
        yield
    finally:
        os.close(descriptor)
        lock_path.unlink(missing_ok=True)


def load(root: Path) -> dict[str, Any]:
    return cast(
        dict[str, Any],
        read_json(
            safe_path(root, ".sdd/runtime-config.json"),
            {"workflow": {"max_repairs": 2}, "checks": []},
        ),
    )
