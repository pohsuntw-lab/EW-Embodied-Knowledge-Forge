# Forge Manifest schema

`FORGE-MANIFEST.json` is UTF-8 JSON with no comments. It records governance state, not protected source bodies.

## Required top-level fields

```json
{
  "schema_version": "1.0",
  "forge_type": "enterprise-secure",
  "project_id": "project-stable-id",
  "enterprise": "Enterprise name",
  "package_audience": ["operations"],
  "processing_environment": "approved-enterprise-chatgpt",
  "created_at": "2026-09-11T00:00:00Z",
  "policy_version": "customer-policy-or-EW-default-1.0",
  "boundary_status": "not-yet-visible",
  "sources": [],
  "notes": [],
  "approvals": [],
  "validation": {}
}
```

## Source entry

Required fields: `source_id`, `title`, `type`, `owner`, `classification`, `audience`, `boundary_status`, `processing_route`, `redaction_status`, `authorization_status`, and `status`.

Do not include source body, credentials, personal identifiers, original P2/P3 paths, token maps, or secret-manager values.

## Note entry

Required fields: `path`, `knowledge_id`, `source_ids`, `classification`, `audience`, `approval_status`, `approved_by`, `approved_at`, and `content_hash` when available.

An approved note requires non-empty `approved_by` and `approved_at`. A candidate must use null values for both unless it records a separate review that is not publication approval.

## Validation entry

Record each validator name, version when known, result, time, and report hash when available. A passing report is not a confidentiality or compliance certification.

