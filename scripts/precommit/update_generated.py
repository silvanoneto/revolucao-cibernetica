#!/usr/bin/env python3
"""
Hook script for pre-commit: regenerate generated artifacts (rizoma) and ensure they're up-to-date.

Behavior:
- Runs: python3 scripts/export_file.py rizoma
- If generated files changed, stages them and exits with code 1 so the commit can be retried with updated files staged.
- If no changes, exits 0 and commit proceeds.

This pattern prevents commits from proceeding when generated files are stale.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parents[2]

# Files that the export should produce/update
GENERATED = [
    # Rizoma outputs
    "docs/rizoma-revolucao-cibernetica.json",
    "docs/rizoma-revolucao-cibernetica.graphml",
    "docs/rizoma-revolucao-cibernetica.md",
    "docs/rizoma-nodes.csv",
    "docs/rizoma-edges.csv",
    # Main exports
    "docs/revolucao_cibernetica.epub",
    "docs/revolucao_cibernetica.pdf",
    "docs/revolucao_cibernetica.min.xml",
    "docs/revolucao_cibernetica.xml",
    "docs/revolucao_cibernetica.jsonl",
]


def run_export() -> int:
    # Run full export to keep all generated artifacts in sync before commit.
    # Note: this may require dependencies from scripts/requirements.txt
    cmd = [sys.executable, "scripts/export_file.py", "all"]
    print("Running:", " ".join(cmd))
    proc = subprocess.run(cmd, cwd=ROOT)
    return proc.returncode


def git_status_contains_generated() -> list[str]:
    """Return list of generated files that appear as changed/untracked in git status --porcelain."""
    try:
        out = subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True)
    except subprocess.CalledProcessError as e:
        print("Failed to run git status:", e)
        return []

    changed = []
    for line in out.splitlines():
        # porcelain lines: XY PATH or ?? PATH
        parts = line.strip().split()
        if not parts:
            continue
        path = parts[-1]
        if path in GENERATED:
            changed.append(path)
    return changed


def git_add(paths: list[str]) -> bool:
    try:
        subprocess.check_call(["git", "add", *paths], cwd=ROOT)
        return True
    except subprocess.CalledProcessError as e:
        print("git add failed:", e)
        return False


def main() -> int:
    rc = run_export()
    if rc != 0:
        print("Export script failed (non-zero exit). Aborting commit.")
        return 1

    changed = git_status_contains_generated()
    if not changed:
        print("No generated rizoma files changed. OK.")
        return 0

    print("Generated files were updated:")
    for p in changed:
        print("  -", p)

    # Stage them so the user can commit the updated files.
    ok = git_add(changed)
    if not ok:
        print("Failed to stage updated files. Aborting commit.")
        return 1

    # Auto-commit the generated files so history contains the evolution logs.
    try:
        timestamp = datetime.now(timezone.utc).isoformat()
        # Author (from git config) and statistics
        try:
            author = subprocess.check_output(["git", "config", "user.name"], cwd=ROOT, text=True).strip()
        except subprocess.CalledProcessError:
            author = "unknown"

        total_bytes = 0
        for p in changed:
            fp = ROOT / p
            if fp.exists():
                try:
                    total_bytes += fp.stat().st_size
                except Exception:
                    pass

        total_kb = total_bytes // 1024
        file_count = len(changed)

        # Build concise title + detailed body (option 1)
        title = "chore: update generated files [ci skip]"

        files_list = "\n".join([f"- {p.split('/')[-1]}" for p in changed])
        body_lines = [
            "Files:",
            files_list,
            "",
            f"Count: {file_count}",
            f"Size: {total_kb} KB",
            f"Timestamp: {timestamp}",
            f"Author: {author}",
        ]
        body = "\n".join(body_lines)

        # Commit with a short title and a detailed body (use two -m args)
        subprocess.check_call(["git", "commit", "-m", title, "-m", body, "--no-verify"], cwd=ROOT)
        print("Auto-committed generated files:")
        print("  ", title)
        print(body)
        return 0
    except subprocess.CalledProcessError as e:
        print("Failed to auto-commit generated files:", e)
        print("Staged updated generated files. Please re-run commit to include them.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
