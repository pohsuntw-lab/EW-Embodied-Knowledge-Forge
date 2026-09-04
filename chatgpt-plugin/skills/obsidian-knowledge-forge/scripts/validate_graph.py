#!/usr/bin/env python3
"""Validate an Obsidian knowledge-graph staging directory."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path


REQUIRED = {
    "knowledge_id",
    "title",
    "project",
    "domain",
    "note_type",
    "version",
    "status",
    "created",
    "updated",
    "up",
    "related",
    "replaces",
    "source_refs",
    "tags",
}
TEMP_MARKERS = (".openai-download-", ".tmp", ".lock", "~$")
WIKILINK = re.compile(r"!?\x5b\x5b([^\x5d|#]+)")


def frontmatter(text: str) -> tuple[dict[str, str], bool]:
    if not text.startswith("---\n"):
        return {}, False
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, False
    props: dict[str, str] = {}
    for line in text[4:end].splitlines():
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:\s*(.*))?$", line)
        if match:
            props[match.group(1)] = (match.group(2) or "").strip()
    return props, True


def resolve_link(root: Path, target: str) -> bool:
    target = target.strip()
    if not target or "://" in target:
        return True
    direct = root / target
    if direct.exists() or Path(str(direct) + ".md").exists():
        return True
    name = Path(target).name
    return any(root.rglob(name)) or any(root.rglob(name + ".md"))


def validate(root: Path) -> dict:
    errors: list[dict] = []
    warnings: list[dict] = []
    notes = sorted(root.rglob("*.md"))
    identities: defaultdict[str, list[str]] = defaultdict(list)
    managed = 0

    if (root / ".obsidian").exists():
        errors.append({"code": "unsafe_settings", "path": ".obsidian"})

    for path in root.rglob("*"):
        if path.is_file() and any(marker in path.name for marker in TEMP_MARKERS):
            errors.append({"code": "temporary_file", "path": str(path.relative_to(root))})

    for note in notes:
        rel = str(note.relative_to(root))
        text = note.read_text(encoding="utf-8", errors="replace")
        if not text.strip():
            errors.append({"code": "empty_note", "path": rel})
            continue

        props, has_frontmatter = frontmatter(text)
        if "knowledge_id" in props:
            managed += 1
            missing = sorted(REQUIRED - set(props))
            if missing:
                errors.append({"code": "missing_properties", "path": rel, "properties": missing})
            identities[props["knowledge_id"]].append(rel)
            if props.get("status") == "current" and props.get("up") == "[]":
                warnings.append({"code": "current_note_without_parent", "path": rel})
        elif not rel.startswith(("90-", "attachments/", "sources/", "projects/")):
            warnings.append({
                "code": "unmanaged_markdown",
                "path": rel,
                "message": "Markdown has no knowledge_id and is not validated as a durable note.",
            })
        elif has_frontmatter:
            warnings.append({"code": "frontmatter_without_identity", "path": rel})

        for target in WIKILINK.findall(text):
            if not resolve_link(root, target):
                errors.append({"code": "broken_wikilink", "path": rel, "target": target})

    for knowledge_id, paths in identities.items():
        if len(paths) > 1:
            errors.append({"code": "duplicate_knowledge_id", "knowledge_id": knowledge_id, "paths": paths})

    return {
        "root": str(root.resolve()),
        "files": sum(1 for p in root.rglob("*") if p.is_file()),
        "markdown_notes": len(notes),
        "managed_notes": managed,
        "errors": errors,
        "warnings": warnings,
        "passed": not errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("vault", type=Path)
    parser.add_argument("--json-output", type=Path)
    args = parser.parse_args()

    if not args.vault.is_dir():
        print(f"Vault directory not found: {args.vault}", file=sys.stderr)
        return 2

    result = validate(args.vault)
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.json_output:
        args.json_output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
