#!/usr/bin/env python3
"""Build a single-file EW Knowledge Package from validated Markdown notes."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath


FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def scalar(frontmatter: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", frontmatter)
    if not match:
        return None
    return match.group(1).strip().strip('"\'')


def safe_relative(path: Path, root: Path) -> str:
    rel = PurePosixPath(path.relative_to(root).as_posix())
    if rel.is_absolute() or ".." in rel.parts or any(part.startswith(".") for part in rel.parts):
        raise ValueError(f"Unsafe package path: {rel}")
    return str(rel)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("staging", type=Path, help="Directory containing Obsidian-ready Markdown")
    parser.add_argument("output", type=Path, help="Output .ewforge file")
    parser.add_argument("--title", required=True)
    parser.add_argument("--target-root", default="EW-Knowledge")
    parser.add_argument("--package-type", choices=("incremental", "full-import"), default="incremental")
    args = parser.parse_args()

    root = args.staging.resolve()
    output = args.output.resolve()
    if not root.is_dir():
        print(f"Staging directory not found: {root}", file=sys.stderr)
        return 2
    if output.suffix != ".ewforge":
        print("Output filename must end in .ewforge", file=sys.stderr)
        return 2
    if output == root or root in output.parents:
        print("Output must be outside the staging directory", file=sys.stderr)
        return 2

    notes = []
    for path in sorted(root.rglob("*.md")):
        rel = safe_relative(path, root)
        data = path.read_bytes()
        text = data.decode("utf-8")
        match = FRONTMATTER.match(text)
        if not match:
            print(f"Missing YAML frontmatter: {rel}", file=sys.stderr)
            return 2
        fm = match.group(1)
        knowledge_id = scalar(fm, "knowledge_id")
        version = scalar(fm, "version")
        managed = scalar(fm, "ew_managed")
        if not knowledge_id or not version:
            print(f"Missing knowledge_id or version: {rel}", file=sys.stderr)
            return 2
        if (managed or "").lower() != "true":
            print(f"ew_managed must be true: {rel}", file=sys.stderr)
            return 2
        notes.append({
            "path": rel,
            "knowledge_id": knowledge_id,
            "version": version,
            "sha256": sha256_bytes(data),
            "content": text,
        })

    if not notes:
        print("No Markdown notes found", file=sys.stderr)
        return 2

    now = datetime.now(timezone.utc)
    package = {
        "format": "ew-knowledge-forge",
        "format_version": "1.0",
        "package_id": f"ewf-{now.strftime('%Y%m%dT%H%M%SZ')}-{sha256_bytes(args.title.encode())[:8]}",
        "created_at": now.isoformat(),
        "title": args.title,
        "target_root": args.target_root.strip("/"),
        "package_type": args.package_type,
        "notes": notes,
        "attachments": [],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output),
        "package_id": package["package_id"],
        "note_count": len(notes),
        "size_bytes": output.stat().st_size,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
