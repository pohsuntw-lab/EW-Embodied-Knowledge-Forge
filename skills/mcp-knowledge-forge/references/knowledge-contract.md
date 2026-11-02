# EW retrieval contract 1.0.0

This is an EW interchange contract, not an MCP standard. The machine-readable schema is `../assets/knowledge.schema.json`. Preserve Unicode and use UTF-8. Unknown dates/positions are null or explicitly unlocated, not fabricated.

| Field | Meaning |
| --- | --- |
| format / schema_version | `ew-mcp-knowledge` / `1.0.0` |
| knowledge_base_id | Stable identity of the knowledge base |
| sources | IDs, titles, filenames, media types, extraction status, warnings and optional SHA-256 of source bytes |
| records[].knowledge_id | Stable concept identity; not a title or file path |
| version / status | Positive revision number; candidate, approved, rejected, superseded, withdrawn |
| summary / body | Short retrieval summary and complete substantive content |
| content_kind | source_text, expert_interpretation, fact, proposal, unresolved |
| keywords / synonyms / questions | Separate discovery fields; may be empty when not justified |
| source_refs | source_id plus locator kind and value, or explicit unlocated |
| relations | up, related, replaces: arrays of knowledge IDs; resolve within this cumulative package |
| validity | effective_from and effective_until dates; null when unknown |
| legal | null for nonlegal records; otherwise law_name, article, jurisdiction, effective_from, effective_until, verified_at |
| access | P0–P3 or unknown classification, allowed audiences, processing route |
| approval | pending/approved/rejected, reviewer, reviewed_at, evidence |
| created_at / updated_at | ISO 8601 timestamps with timezone; not legal effective dates |

Every approved record requires complete source extraction, located references, resolved classification/route, explicit audience, no source warnings, no unresolved content, and genuine approval evidence. These are structural gates only: the validator cannot authenticate a reviewer, certify OCR, or judge legal correctness.

Legal metadata applies to source text and interpretations of legal material. Known dates must be chronological. Unknown legal validity emits a warning; the server must avoid calling that record currently valid. Superseded/withdrawn/rejected/candidate records must never enter the normal retrieval index. Replacements cannot point to themselves or form cycles. Relations may refer to withdrawn records for provenance, but the server must not return their content without a separate authorized history workflow.

Keep a readable review document alongside JSON, preserving source excerpts and interpretation labels. The Markdown is an audit view; changing it does not update JSON automatically. Reforge and revalidate both after edits.
