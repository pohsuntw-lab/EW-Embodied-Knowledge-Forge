# `.ewforge` 1.0 package specification

An EW Knowledge Package is UTF-8 JSON. It contains no executable code.

```json
{
  "format": "ew-knowledge-forge",
  "format_version": "1.0",
  "package_id": "ewf-20260904-example",
  "created_at": "2026-09-04T00:00:00Z",
  "title": "Example",
  "target_root": "EW-Knowledge",
  "package_type": "incremental",
  "notes": [
    {
      "path": "Projects/Example/Overview.md",
      "knowledge_id": "example-overview",
      "version": "1.0.0",
      "sha256": "lowercase SHA-256 of UTF-8 content",
      "content": "complete Markdown"
    }
  ],
  "attachments": []
}
```

Notes must have safe relative `.md` paths and YAML properties including `knowledge_id`, `version`, and `ew_managed: true`. Attachments are optional Base64 entries. Importers reject absolute/hidden/traversal paths, unsupported extensions, duplicate identities, excessive entry counts, and checksum mismatches.

The Vault destination is chosen by the importer settings. `target_root` is informational in v1 so a package cannot redirect writes to an unexpected Vault location.
