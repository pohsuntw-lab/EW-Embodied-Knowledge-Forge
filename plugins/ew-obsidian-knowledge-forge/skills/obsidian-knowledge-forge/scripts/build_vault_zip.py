#!/usr/bin/env python3
"""Build a standard, plugin-free Obsidian Vault ZIP."""

from __future__ import annotations

import argparse
import shutil
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

BLOCKED_PARTS = {".obsidian", "__MACOSX"}
BLOCKED_SUFFIXES = {".exe", ".dll", ".dylib", ".so", ".bat", ".cmd"}

def safe_path(path: Path, root: Path) -> PurePosixPath:
    rel = PurePosixPath(path.relative_to(root).as_posix())
    if rel.is_absolute() or ".." in rel.parts or any(part in BLOCKED_PARTS for part in rel.parts):
        raise ValueError(f"Unsafe Vault path: {rel}")
    if path.suffix.lower() in BLOCKED_SUFFIXES:
        raise ValueError(f"Executable files are not allowed: {rel}")
    return rel

def render_guide(template: Path, vault_name: str) -> str:
    return template.read_text(encoding="utf-8").replace("{{VAULT_NAME}}", vault_name)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("staging", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--vault-name", required=True)
    parser.add_argument("--assets-dir", type=Path, default=Path(__file__).resolve().parent.parent / "assets")
    args = parser.parse_args()
    source, output = args.staging.resolve(), args.output.resolve()
    vault_name = args.vault_name.strip().strip("/\\")
    if not source.is_dir() or not vault_name or output.suffix.lower() != ".zip":
        parser.error("Provide a staging directory, a Vault name, and a .zip output")
    with tempfile.TemporaryDirectory(prefix="ew-vault-") as temporary:
        vault = Path(temporary) / vault_name
        shutil.copytree(source, vault)
        guides = {
            "README-START-HERE.md": args.assets_dir / "README-START-HERE.md",
            "使用說明-請先閱讀.md": args.assets_dir / "使用說明-請先閱讀.md",
        }
        for filename, template in guides.items():
            (vault / filename).write_text(render_guide(template, vault_name), encoding="utf-8")
        output.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(vault.rglob("*")):
                if path.is_file():
                    archive.write(path, PurePosixPath(vault_name) / safe_path(path, vault))
        with zipfile.ZipFile(output) as archive:
            bad, names = archive.testzip(), archive.namelist()
            if bad:
                raise ValueError(f"ZIP integrity check failed: {bad}")
            for guide in guides:
                if not any(name.endswith(guide) for name in names):
                    raise ValueError(f"Required ZIP guide is missing: {guide}")
        print(f"Built {output} with {len(names)} files")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

