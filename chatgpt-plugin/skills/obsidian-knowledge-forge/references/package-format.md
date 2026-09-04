# EW Knowledge Package format

EW Knowledge Forge v1 uses one UTF-8 JSON file with the `.ewforge` extension. The file is portable, inspectable, and does not contain executable code.

## Top-level object

```json
{
  "format": "ew-knowledge-forge",
  "format_version": "1.0",
  "package_id": "ewf-20260904-example",
  "created_at": "2026-09-04T00:00:00Z",
  "title": "Example knowledge package",
  "target_root": "EW-Knowledge",
  "package_type": "incremental",
  "notes": [],
  "attachments": []
}
```

`package_type` is either `incremental` or `full-import`. Version 1 importers must reject unknown `format` values and unsupported major versions.

## Notes

Each note contains a relative path, complete Markdown content, content hash, and stable knowledge identity:

```json
{
  "path": "Projects/Example/Decision.md",
  "knowledge_id": "example-decision",
  "version": "1.0.0",
  "sha256": "...",
  "content": "---\nknowledge_id: example-decision\n...\n---\n# Decision\n"
}
```

- Paths are relative to `target_root` and must end in `.md`.
- Paths may not be absolute, hidden, contain `..`, or address `.obsidian`.
- Generated notes set `ew_managed: true` in YAML.
- The hash is the lowercase SHA-256 of the UTF-8 content bytes.
- Every note follows the knowledge schema and has at least one valid `up` link.

## Attachments

Attachments are optional and use Base64 data:

```json
{
  "path": "90-Attachments/source.pdf",
  "media_type": "application/pdf",
  "sha256": "...",
  "encoding": "base64",
  "data": "..."
}
```

Keep packages small enough for a mobile device. Prefer Markdown-only packages when original binary files are already available to the user.

## Import behavior

- New paths are created.
- Identical content is skipped.
- A newer note with the same `knowledge_id` may update an EW-managed note after the importer creates a backup.
- A collision with an unmanaged or unrelated note creates a conflict copy; it never overwrites the existing file.
- The importer never writes outside its configured knowledge root and never writes into `.obsidian`.
