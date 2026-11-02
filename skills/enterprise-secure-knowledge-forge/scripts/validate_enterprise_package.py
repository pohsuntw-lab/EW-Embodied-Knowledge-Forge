#!/usr/bin/env python3
"""Validate an Enterprise Secure Knowledge Forge staging tree.

This is a conservative structural and secret-pattern check. It is not a
confidentiality guarantee, endpoint DLP control, or compliance certification.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_PATHS = (
    "00-Governance/Security Intake.md",
    "00-Governance/Source Register.md",
    "00-Governance/Approval Register.md",
    "FORGE-MANIFEST.json",
)

FORBIDDEN_SUFFIXES = {
    ".exe", ".dll", ".dylib", ".so", ".bat", ".cmd", ".ps1", ".sh",
    ".p12", ".pfx", ".pem", ".key", ".keystore", ".jks",
}

TEXT_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml", ".csv", ".tsv"}

SECRET_PATTERNS = (
    ("private-key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("openai-style-token", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("aws-access-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    (
        "credential-assignment",
        re.compile(
            r"(?i)\b(?:password|passwd|api[_-]?key|access[_-]?token|client[_-]?secret)"
            r"\s*[:=]\s*[\"']?(?!null\b|none\b|redacted\b|placeholder\b|example\b|unknown\b)"
            r"[^\s\"']{8,}"
        ),
    ),
)


def add_error(errors: list[str], message: str) -> None:
    errors.append(message)


def load_manifest(root: Path, errors: list[str]) -> dict:
    path = root / "FORGE-MANIFEST.json"
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        add_error(errors, f"Invalid FORGE-MANIFEST.json: {exc}")
        return {}
    if not isinstance(data, dict):
        add_error(errors, "FORGE-MANIFEST.json must contain a JSON object")
        return {}
    return data


def validate_manifest(manifest: dict, errors: list[str]) -> None:
    required = (
        "schema_version", "forge_type", "project_id", "enterprise",
        "package_audience", "processing_environment", "created_at",
        "policy_version", "boundary_status", "sources", "notes",
        "approvals", "validation",
    )
    for field in required:
        if field not in manifest:
            add_error(errors, f"Manifest missing required field: {field}")

    if manifest.get("forge_type") != "enterprise-secure":
        add_error(errors, "Manifest forge_type must be enterprise-secure")

    for index, source in enumerate(manifest.get("sources", [])):
        if not isinstance(source, dict):
            add_error(errors, f"Source entry {index} must be an object")
            continue
        classification = source.get("classification")
        route = source.get("processing_route")
        if classification not in {"P0", "P1", "P2", "P3"}:
            add_error(errors, f"Source entry {index} has invalid classification: {classification}")
        if route not in {"cloud-approved", "cloud-sanitized", "local-only", "blocked"}:
            add_error(errors, f"Source entry {index} has invalid processing_route: {route}")
        if classification == "P3" and route != "local-only":
            add_error(errors, f"P3 source {source.get('source_id', index)} must be local-only")
        if classification == "P2" and route == "cloud-approved":
            add_error(errors, f"P2 source {source.get('source_id', index)} cannot use cloud-approved")

    for index, note in enumerate(manifest.get("notes", [])):
        if not isinstance(note, dict):
            add_error(errors, f"Note entry {index} must be an object")
            continue
        status = note.get("approval_status")
        path = str(note.get("path", ""))
        if status == "approved":
            if not note.get("approved_by") or not note.get("approved_at"):
                add_error(errors, f"Approved note {path or index} lacks approver or approval time")
            if not path.startswith("20-Published/"):
                add_error(errors, f"Approved note must be under 20-Published/: {path or index}")
        elif path.startswith("20-Published/"):
            add_error(errors, f"Published path is not approved: {path}")


def scan_tree(root: Path, errors: list[str]) -> None:
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if ".obsidian" in relative.parts:
            add_error(errors, f"Forbidden .obsidian content: {relative}")
            continue
        if not path.is_file():
            continue
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            add_error(errors, f"Forbidden file type: {relative}")
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            add_error(errors, f"Unreadable text file: {relative}")
            continue
        for label, pattern in SECRET_PATTERNS:
            if pattern.search(text):
                add_error(errors, f"Potential {label} detected in {relative}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("vault_root", type=Path)
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args()

    root = args.vault_root.resolve()
    errors: list[str] = []
    if not root.is_dir():
        errors.append(f"Vault root is not a directory: {root}")
    else:
        for required in REQUIRED_PATHS:
            if not (root / required).is_file():
                add_error(errors, f"Missing required path: {required}")
        manifest = load_manifest(root, errors)
        if manifest:
            validate_manifest(manifest, errors)
        scan_tree(root, errors)

    result = {
        "validator": "EW Enterprise Package Validator",
        "result": "fail" if errors else "pass",
        "disclaimer": "Defense-in-depth only; not a confidentiality or compliance certification.",
        "errors": errors,
    }
    if args.json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Enterprise package validation: {result['result'].upper()}")
        for error in errors:
            print(f"- {error}")
        print(result["disclaimer"])
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

