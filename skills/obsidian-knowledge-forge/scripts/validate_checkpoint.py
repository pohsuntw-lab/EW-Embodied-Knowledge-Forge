#!/usr/bin/env python3
"""Validate a portable EW Knowledge Forge checkpoint."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

REQUIRED = {
    "checkpoint_schema", "forge_id", "checkpoint_revision", "project_id",
    "project_name", "vault_name", "language", "compression_level", "mode",
    "status", "last_completed_volume", "next_volume", "updated",
}


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("Checkpoint must start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("Checkpoint frontmatter is not closed")
    values: dict[str, str] = {}
    for line in text[4:end].splitlines():
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
        if match:
            values[match.group(1)] = match.group(2).strip().strip('"').strip("'")
    return values


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("checkpoint", type=Path)
    args = parser.parse_args()
    values = parse_frontmatter(args.checkpoint.read_text(encoding="utf-8"))
    missing = sorted(REQUIRED - set(values))
    if missing:
        raise ValueError(f"Missing checkpoint fields: {', '.join(missing)}")
    if values["checkpoint_schema"] != "ew-forge-checkpoint-v1":
        raise ValueError("Unsupported checkpoint schema")
    if values["compression_level"] not in {"A", "B", "C"}:
        raise ValueError("compression_level must be A, B, or C")
    if values["mode"] != "complete-project":
        raise ValueError("mode must be complete-project")
    if values["status"] not in {"active", "complete", "paused", "blocked"}:
        raise ValueError("Unsupported checkpoint status")
    for key in ("checkpoint_revision", "last_completed_volume", "next_volume"):
        try:
            number = int(values[key])
        except ValueError as exc:
            raise ValueError(f"{key} must be an integer") from exc
        if number < 0:
            raise ValueError(f"{key} must not be negative")
    if int(values["next_volume"]) <= int(values["last_completed_volume"]):
        raise ValueError("next_volume must be greater than last_completed_volume")
    print(f"Valid checkpoint: {args.checkpoint}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
