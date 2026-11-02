# MCP server import and retrieval contract

The package does not include a running server. Inspect an actual server before claiming import compatibility. Translate this EW contract into its accepted schema with an explicit adapter and integration test.

1. Validate the whole JSON before import. Enforce a unique `(knowledge_base_id, knowledge_id, version)` key and transactional import; reject conflicting content for an existing revision. Recompute hashes from received bytes; hashes prove integrity, not truth or approval.
2. Keep all revisions and source provenance. Update the active revision atomically; remove superseded, withdrawn and revoked content from active indexes and caches immediately.
3. Build exact indexes on knowledge ID, category, status, jurisdiction, law/article and validity dates. Use a suitable full-text index for title, summary, keywords, synonyms and questions. SQLite FTS5 needs an appropriate tokenizer strategy for Chinese; benchmark real queries instead of promising a search speed. Do not treat a JSON array as a database index.
4. Establish caller identity on the server. Enforce classification, audience, approval, processing route, effective dates and revocation before ranking, pagination, counts, snippets or content. Never accept caller-supplied roles as proof of authority. The generated retrieval index contains access metadata but is not safe to publish as a public download.
5. Suggested application tools (names are proposals, not MCP requirements):

| Tool | Input | Output |
| --- | --- | --- |
| search_knowledge | query, allowed filters, bounded limit, cursor | Authorized ID/version/title/summary, relevance and source locations; no full body |
| get_knowledge | knowledge_id, optional version | Authorized full body, content kind, provenance, validity, approval and relations |

6. Check authorization again for full-text retrieval, including when a user knows a restricted record ID. Return no restricted metadata on denial. Use an authorized separate workflow for history or candidates.
7. Acceptance cases: exact ID, colloquial Chinese query, synonyms, empty results, revoked access, unknown/expired/future legal dates, conflicting versions, malformed packages, candidate exclusion and blocked sources. Do not claim this integration passed without an actual server test.
