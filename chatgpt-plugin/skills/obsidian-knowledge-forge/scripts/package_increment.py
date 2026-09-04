#!/usr/bin/env python3
"""Create a safe Obsidian incremental-update ZIP with a hash manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path


TEMP_MARKERS = (".openai-download-", ".tmp", ".lock", "~$", ".DS_Store")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collect(root: Path) -> list[Path]:
    files = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if ".obsidian" in rel.parts:
            continue
        if any(marker in path.name for marker in TEMP_MARKERS):
            continue
        files.append(path)
    return files


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("staging", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--package-type", choices=("incremental", "full-import"), default="incremental")
    args = parser.parse_args()

    root = args.staging.resolve()
    output = args.output.resolve()
    if not root.is_dir():
        print(f"Staging directory not found: {root}", file=sys.stderr)
        return 2
    if output == root or root in output.parents:
        print("Output ZIP must be outside the staging directory.", file=sys.stderr)
        return 2

    files = collect(root)
    manifest = {
        "format": "ew-obsidian-knowledge-forge",
        "format_version": "1.0",
        "package_type": args.package_type,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "root_folder": root.name,
        "file_count": len(files),
        "files": [
            {
                "path": str(path.relative_to(root)),
                "size_bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in files
        ],
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            archive.write(path, arcname=str(Path(root.name) / path.relative_to(root)))
        archive.writestr(
            str(Path(root.name) / "UPDATE_MANIFEST.json"),
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        )

    print(json.dumps({
        "output": str(output),
        "package_type": args.package_type,
        "file_count": len(files),
        "size_bytes": output.stat().st_size,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
