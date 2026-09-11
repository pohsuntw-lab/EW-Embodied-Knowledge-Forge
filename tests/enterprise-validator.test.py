#!/usr/bin/env python3

import json
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "plugins/ew-obsidian-knowledge-forge/skills/enterprise-secure-knowledge-forge/scripts/validate_enterprise_package.py"


def make_vault(base: Path) -> Path:
    vault = base / "Enterprise-Vault"
    governance = vault / "00-Governance"
    governance.mkdir(parents=True)
    for name in ("Security Intake.md", "Source Register.md", "Approval Register.md"):
        (governance / name).write_text("# Synthetic test record\n", encoding="utf-8")
    (vault / "20-Published").mkdir()
    manifest = {
        "schema_version": "1.0",
        "forge_type": "enterprise-secure",
        "project_id": "test-project",
        "enterprise": "Example Enterprise",
        "package_audience": ["operations"],
        "processing_environment": "approved-test-environment",
        "created_at": "2026-09-11T00:00:00Z",
        "policy_version": "EW-default-1.0",
        "boundary_status": "not-yet-visible",
        "sources": [{
            "source_id": "SRC-001",
            "classification": "P1",
            "processing_route": "cloud-approved"
        }],
        "notes": [{
            "path": "20-Published/Example.md",
            "approval_status": "approved",
            "approved_by": "Synthetic Approver",
            "approved_at": "2026-09-11T00:00:00Z"
        }],
        "approvals": [],
        "validation": {}
    }
    (vault / "FORGE-MANIFEST.json").write_text(json.dumps(manifest), encoding="utf-8")
    (vault / "20-Published/Example.md").write_text("# Synthetic approved note\n", encoding="utf-8")
    return vault


def run(vault: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["python3", str(VALIDATOR), str(vault), "--json"],
        check=False,
        capture_output=True,
        text=True,
    )


with tempfile.TemporaryDirectory() as temp:
    root = Path(temp)
    clean = make_vault(root / "clean")
    clean_result = run(clean)
    assert clean_result.returncode == 0, clean_result.stdout + clean_result.stderr

    secret = make_vault(root / "secret")
    (secret / "20-Published/Leak.md").write_text(
        "client_secret = super-secret-value-123", encoding="utf-8"
    )
    secret_result = run(secret)
    assert secret_result.returncode != 0
    assert "credential-assignment" in secret_result.stdout

    p3 = make_vault(root / "p3")
    manifest_path = p3 / "FORGE-MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["sources"][0]["classification"] = "P3"
    manifest["sources"][0]["processing_route"] = "cloud-approved"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    p3_result = run(p3)
    assert p3_result.returncode != 0
    assert "must be local-only" in p3_result.stdout

print("Validated enterprise package positive and negative cases.")

