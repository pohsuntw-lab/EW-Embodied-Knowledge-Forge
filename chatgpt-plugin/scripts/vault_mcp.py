#!/usr/bin/env python3
"""Minimal stdio MCP server for safe Markdown access to one Obsidian Vault."""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any


CONFIG_DIR = Path(os.environ.get("EW_KNOWLEDGE_CONFIG_DIR", Path.home() / ".config" / "ew-knowledge-forge"))
CONFIG_FILE = CONFIG_DIR / "config.json"
BLOCKED_PARTS = {".obsidian", ".git", ".trash"}
VALID_MODES = {"guided-auto", "preview", "manual"}


def result(data: Any, error: bool = False) -> dict:
    return {
        "content": [{"type": "text", "text": json.dumps(data, ensure_ascii=False, indent=2)}],
        "isError": error,
    }


def load_config() -> dict:
    if not CONFIG_FILE.exists():
        return {}
    try:
        return json.loads(CONFIG_FILE.read_text("utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def save_config(config: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    temp = CONFIG_FILE.with_suffix(".tmp")
    temp.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", "utf-8")
    os.replace(temp, CONFIG_FILE)


def vault_root() -> Path:
    configured = os.environ.get("EW_OBSIDIAN_VAULT") or load_config().get("vault_path")
    if not configured:
        raise ValueError("Vault is not configured. Call configure_vault with the user's chosen Vault path.")
    root = Path(configured).expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"Configured Vault does not exist: {root}")
    return root


def safe_note(root: Path, relative_path: str) -> Path:
    rel = Path(relative_path)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError("Path must be relative and may not contain '..'.")
    if any(part.startswith(".") or part in BLOCKED_PARTS for part in rel.parts):
        raise ValueError("Hidden and Obsidian settings paths are not writable.")
    if rel.suffix.lower() != ".md":
        raise ValueError("Direct writes are limited to Markdown notes.")
    target = (root / rel).resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise ValueError("Path escapes the configured Vault.") from exc
    return target


def file_hash(path: Path) -> str | None:
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frontmatter_value(text: str, key: str) -> str:
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---\n", 4)
    if end < 0:
        return ""
    match = re.search(rf"(?m)^{re.escape(key)}:\s*[\"']?([^\"'\n]+)", text[4:end])
    return match.group(1).strip() if match else ""


def note_inventory(root: Path) -> list[dict]:
    notes = []
    for path in root.rglob("*.md"):
        rel = path.relative_to(root)
        if any(part.startswith(".") for part in rel.parts):
            continue
        try:
            text = path.read_text("utf-8", errors="replace")
        except OSError:
            continue
        notes.append({
            "path": str(rel),
            "title": frontmatter_value(text, "title") or path.stem,
            "knowledge_id": frontmatter_value(text, "knowledge_id"),
            "project": frontmatter_value(text, "project"),
            "domain": frontmatter_value(text, "domain"),
            "note_type": frontmatter_value(text, "note_type"),
            "status": frontmatter_value(text, "status"),
            "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "_text": text,
        })
    return notes


def configure_vault(arguments: dict) -> dict:
    raw_path = arguments.get("vault_path", "")
    mode = arguments.get("mode", "guided-auto")
    root = Path(raw_path).expanduser().resolve()
    if not root.is_dir():
        raise ValueError("The selected Vault folder does not exist.")
    if not (root / ".obsidian").is_dir():
        raise ValueError("The selected folder is not an Obsidian Vault: .obsidian is missing.")
    if mode not in VALID_MODES:
        raise ValueError(f"mode must be one of {sorted(VALID_MODES)}")
    config = {"vault_path": str(root), "mode": mode}
    save_config(config)
    return {"configured": True, **config}


def vault_status(_: dict) -> dict:
    config = load_config()
    root = vault_root()
    notes = note_inventory(root)
    return {
        "configured": True,
        "vault_path": str(root),
        "mode": config.get("mode", "guided-auto"),
        "markdown_notes": len(notes),
        "topic_hubs": sum(1 for note in notes if note["note_type"] == "project"),
    }


def search_notes(arguments: dict) -> dict:
    root = vault_root()
    query = str(arguments.get("query", "")).strip()
    limit = max(1, min(int(arguments.get("limit", 10)), 50))
    if not query:
        raise ValueError("query is required")
    terms = [term.casefold() for term in re.findall(r"[\w\-]+", query) if len(term) > 1]
    scored = []
    for note in note_inventory(root):
        title_blob = " ".join([
            note["title"], note["knowledge_id"], note["project"], note["domain"], note["note_type"]
        ]).casefold()
        body = note.pop("_text").casefold()
        score = sum(title_blob.count(term) * 8 + body.count(term) for term in terms)
        if score:
            note["score"] = score
            scored.append(note)
    scored.sort(key=lambda item: (-item["score"], item["path"]))
    return {"query": query, "matches": scored[:limit]}


def read_note(arguments: dict) -> dict:
    root = vault_root()
    target = safe_note(root, str(arguments.get("path", "")))
    if not target.is_file():
        raise ValueError("Note not found.")
    content = target.read_text("utf-8", errors="replace")
    return {
        "path": str(target.relative_to(root)),
        "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
        "content": content,
    }


def write_notes(arguments: dict) -> dict:
    root = vault_root()
    actions = arguments.get("actions")
    dry_run = bool(arguments.get("dry_run", False))
    if not isinstance(actions, list) or not actions:
        raise ValueError("actions must be a non-empty list")
    if len(actions) > 50:
        raise ValueError("A transaction may contain at most 50 notes.")

    planned = []
    for action in actions:
        target = safe_note(root, str(action.get("path", "")))
        content = action.get("content")
        if not isinstance(content, str) or not content.strip():
            raise ValueError(f"Non-empty Markdown content is required for {target.name}.")
        current_hash = file_hash(target)
        expected = action.get("expected_sha256")
        operation = action.get("operation", "upsert")
        if operation == "create" and target.exists():
            raise ValueError(f"Create conflict: {target.relative_to(root)} already exists.")
        if operation == "update" and not target.exists():
            raise ValueError(f"Update conflict: {target.relative_to(root)} does not exist.")
        if target.exists() and not expected:
            raise ValueError(f"expected_sha256 is required to update {target.relative_to(root)}.")
        if expected and expected != current_hash:
            raise ValueError(f"Version conflict: {target.relative_to(root)} changed after it was read.")
        planned.append({
            "target": target,
            "content": content,
            "operation": "update" if target.exists() else "create",
            "previous_sha256": current_hash,
        })

    receipt = [{
        "path": str(item["target"].relative_to(root)),
        "operation": item["operation"],
        "previous_sha256": item["previous_sha256"],
        "new_sha256": hashlib.sha256(item["content"].encode("utf-8")).hexdigest(),
    } for item in planned]
    if dry_run:
        return {"dry_run": True, "changes": receipt}

    temporary: list[tuple[Path, Path]] = []
    try:
        for item in planned:
            item["target"].parent.mkdir(parents=True, exist_ok=True)
            fd, temp_name = tempfile.mkstemp(prefix=".ew-forge-", suffix=".tmp", dir=item["target"].parent)
            with os.fdopen(fd, "w", encoding="utf-8") as stream:
                stream.write(item["content"])
                if not item["content"].endswith("\n"):
                    stream.write("\n")
            temporary.append((Path(temp_name), item["target"]))
        for temp, target in temporary:
            os.replace(temp, target)
    finally:
        for temp, _ in temporary:
            if temp.exists():
                temp.unlink()
    return {"dry_run": False, "changes": receipt}


TOOLS = [
    {
        "name": "configure_vault",
        "description": "Configure the user-selected local Obsidian Vault and guided interaction mode. Never guess the path.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "vault_path": {"type": "string"},
                "mode": {"type": "string", "enum": sorted(VALID_MODES)},
            },
            "required": ["vault_path"],
        },
    },
    {
        "name": "vault_status",
        "description": "Check the configured Vault, interaction mode, and note counts.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "search_notes",
        "description": "Search existing Obsidian notes to route a conversation or find related knowledge.",
        "inputSchema": {
            "type": "object",
            "properties": {"query": {"type": "string"}, "limit": {"type": "integer", "minimum": 1, "maximum": 50}},
            "required": ["query"],
        },
    },
    {
        "name": "read_note",
        "description": "Read one Markdown note and return its content hash for conflict-safe updates.",
        "inputSchema": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"],
        },
    },
    {
        "name": "write_notes",
        "description": "Create or conflict-safely update Markdown notes in one batch. Does not delete notes or edit .obsidian.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "dry_run": {"type": "boolean", "default": False},
                "actions": {
                    "type": "array",
                    "minItems": 1,
                    "maxItems": 50,
                    "items": {
                        "type": "object",
                        "properties": {
                            "operation": {"type": "string", "enum": ["create", "update", "upsert"]},
                            "path": {"type": "string"},
                            "content": {"type": "string"},
                            "expected_sha256": {"type": "string"},
                        },
                        "required": ["path", "content"],
                    },
                },
            },
            "required": ["actions"],
        },
    },
]
HANDLERS = {
    "configure_vault": configure_vault,
    "vault_status": vault_status,
    "search_notes": search_notes,
    "read_note": read_note,
    "write_notes": write_notes,
}


def handle(message: dict) -> dict | None:
    method = message.get("method")
    request_id = message.get("id")
    if method == "initialize":
        payload = {
            "protocolVersion": "2025-06-18",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "ew-knowledge-vault", "version": "0.1.0"},
        }
    elif method == "tools/list":
        payload = {"tools": TOOLS}
    elif method == "tools/call":
        params = message.get("params", {})
        name = params.get("name")
        try:
            if name not in HANDLERS:
                raise ValueError(f"Unknown tool: {name}")
            payload = HANDLERS[name](params.get("arguments") or {})
            payload = result(payload)
        except Exception as exc:
            payload = result({"error": str(exc)}, error=True)
    elif method in {"notifications/initialized", "notifications/cancelled"}:
        return None
    elif request_id is None:
        return None
    else:
        return {"jsonrpc": "2.0", "id": request_id, "error": {"code": -32601, "message": f"Method not found: {method}"}}

    return {"jsonrpc": "2.0", "id": request_id, "result": payload}


def main() -> None:
    for line in sys.stdin:
        try:
            message = json.loads(line)
            response = handle(message)
            if response is not None:
                print(json.dumps(response, ensure_ascii=False), flush=True)
        except Exception as exc:
            print(json.dumps({
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32603, "message": str(exc)},
            }, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
