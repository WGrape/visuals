#!/usr/bin/env python3
"""Check that active historical relocations resolve to existing repository paths."""
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
ACTIVE = {
    "lesson_moves": "file",
    "deduplicated_articles": "file",
    "retired_indices": "file",
    "directory_renames": "directory",
}


def audit(root=ROOT, ledger=None):
    root = Path(root).resolve()
    ledger = Path(ledger) if ledger is not None else root / "docs/knowledge-relocations.json"
    data = json.loads(ledger.read_text(encoding="utf-8"))
    errors = []
    counts = {}
    active_sources = set()
    for section, kind in ACTIVE.items():
        entries = data[section]
        counts[section] = len(entries)
        for source, destination in entries.items():
            active_sources.add(source)
            path = (root / destination).resolve()
            if source == destination:
                errors.append(f"自指映射：{section}: {source}")
            if not path.is_relative_to(root):
                errors.append(f"目标越出仓库：{section}: {source} -> {destination}")
            elif kind == "file" and not path.is_file():
                errors.append(f"课程/索引目标不存在：{section}: {source} -> {destination}")
            elif kind == "directory" and not path.is_dir():
                errors.append(f"目录目标不存在：{section}: {source} -> {destination}")
    unavailable = data.get("unavailable_legacy_entries", {})
    archived = 0
    for source, entry in unavailable.items():
        if source in active_sources:
            errors.append(f"未确认旧路径仍列为活跃映射：{source}")
        commit = entry.get("archive_commit")
        archive_path = entry.get("archive_path")
        if bool(commit) != bool(archive_path):
            errors.append(f"Git 归档记录不完整：{source}")
        elif commit and archive_path:
            if (not re.fullmatch(r"[0-9a-f]{40}", commit) or
                    archive_path.startswith("/") or
                    ".." in archive_path.split("/")):
                errors.append(f"Git 归档引用无效：{source}")
            else:
                archived += 1
                if (root / ".git").exists() and not (root / ".git/shallow").exists():
                    result = subprocess.run(
                        ["git", "cat-file", "-e", f"{commit}:{archive_path}"],
                        cwd=root, capture_output=True)
                    if result.returncode:
                        errors.append(f"Git 归档对象不存在：{source}")
    for error in errors:
        print(error, file=sys.stderr)
    print("活跃映射 " + ", ".join(f"{name}={counts[name]}" for name in ACTIVE) +
          f"；未确认旧路径={len(unavailable)}（可从 Git 恢复 {archived}）；错误={len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(audit())
