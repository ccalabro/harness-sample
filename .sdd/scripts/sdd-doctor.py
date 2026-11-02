#!/usr/bin/env python3
"""Check project-local workflow prerequisites without installing anything."""
import argparse
import shutil
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--harness", default=None)
parser.add_argument("action", nargs="?")
parser.add_argument("answer", nargs="?")
args = parser.parse_args()
root = Path(__file__).resolve().parents[2]
config = root / ".sdd/config.yaml"
harness = args.harness or "generic"
for line in config.read_text(encoding="utf-8").splitlines():
    if args.harness is None and line.strip().startswith("default_harness:"):
        harness = line.split(":", 1)[1].strip().strip("'\" ")
        break
missing = []
if not shutil.which("openspec"):
    missing.append("OpenSpec is missing. Install Node.js >=20.19, then run: npm install -g @fission-ai/openspec@1.13.1")
if missing:
    print("\n".join(missing))
    raise SystemExit(1)
print("OpenSpec is available.")
print("Before starting, confirm Superpowers loaded in this " + harness + " session.")
print("If not, follow the Superpowers steps in .sdd/harnesses/" + harness + ".md and restart the harness.")
if args.action != "confirm-superpowers" or (args.answer or "").strip().lower() != "yes":
    print("Starting is blocked until you confirm Superpowers is available.")
    raise SystemExit(1)
print("Superpowers confirmed for this session.")
