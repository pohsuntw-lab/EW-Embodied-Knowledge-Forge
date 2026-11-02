# Living Wiki / 持續累積的 Wiki

## Scope and ownership

The forging agent reads the admitted sources and writes source-backed topic drafts during the same forge batch. The user supplies sources and direction; authorized reviewers approve enterprise publication. Upload is receipt, not approval. This skills-only plugin generates a portable package and update plan; it does not install a watcher, deploy Enterprise Brain, write through MCP, or automatically merge a user's local Vault.

## Required operations on every batch

1. After existing intake gates, register each admitted source with a stable source_id. Read existing topic bodies, source records and checkpoint before synthesizing. If unavailable, request the prior bounded package or checkpoint and record unresolved dependencies; do not invent previous knowledge.
2. Preserve substantive source notes as required by the existing fidelity rules. Restricted sources must follow the existing route; never package original P2/P3 contents. A sanitized derivative is a distinct admitted source, with its own identity/hash and permitted lineage metadata.
3. Assess EVERY registered source: `create`, `update`, `duplicate`, `no_change`, `deferred` or `blocked`, with a concrete reason and impacted topic IDs. Not every source needs a new page. Blocked/local-only sources in cloud mode receive metadata-only decisions, never invented summaries.
4. Synthesize linked concept, decision, SOP or comparison pages across available sources. Cite every factual conclusion with source ID plus a locator (heading, page, paragraph or line). Preserve conditions, exceptions, disagreements and uncertainties. Clearly distinguish fact, inference, proposal and unresolved conflict. Do not let an index replace substantive notes.
5. Use stable knowledge_id values, increment topic versions, preserve prior approved versions and record changes. New dates alone do not establish authority. Source changes invalidate dependent conclusions for review; withdrawal or reduced authorization requires reevaluating every dependent topic. Never silently erase contrary evidence.
6. Enterprise topic drafts live in `10-Candidates/Wiki/`; published topics belong in `20-Published/Wiki/` only after existing named authorization checks. Personal topics live in `30-Wiki/` and remain draft unless actually reviewed. Maintain `00-Home/Wiki Index.md`, `00-Home/Wiki Change Log.md`, `00-Home/Wiki Review Queue.md` and `WIKI-MANIFEST.json`. Link these from Project Home.
7. Query the index then relevant topics and sources. Useful answers may become new draft revisions during the authorized batch. Re-run graph, checkpoint, enterprise (when applicable), wiki and ZIP checks. Report stale sources, contradictions, pending approvals and deferred dependencies explicitly.

## Portable WIKI-MANIFEST.json (schema 1.0)

```json
{
  "schema_version": "1.0",
  "sources": [{"source_id":"SRC-001","path":"01-Sources/Source.md","sha256":"SHA256_OF_PACKAGED_SOURCE_NOTE"}],
  "decisions": [{"source_id":"SRC-001","action":"create","reason":"New supported concept","topic_ids":["topic-001"]}],
  "topics": [{"knowledge_id":"topic-001","path":"30-Wiki/Topic.md","version":"1.0.0","status":"draft","sha256":"SHA256_OF_TOPIC_BYTES","source_ids":["SRC-001"],"evidence":[{"source_id":"SRC-001","locator":"Summary, paragraph 2"}]}]
}
```

Use actual 64-character lowercase SHA256 digests, never the example placeholders. Paths are relative to the Vault. Include all sources listed in the existing Source Register or FORGE-MANIFEST, including blocked/deferred metadata records. A source without packaged content uses `path: null, sha256: null`; its decision must be `blocked` or `deferred` and no topic may cite it. Hashes describe packaged source notes, not an inaccessible original. Only include source body content permitted for this package's single audience.

Every topic must also use the existing note frontmatter schema. Its `source_refs` must link the source notes; body citations include precise locators. Track source-to-topic dependencies in the manifest. Enterprise source IDs, audience and classification must agree with FORGE-MANIFEST; synthesis cannot broaden source access. Mixed audiences require separate packages. Formal publication continues through the existing enterprise gate; WIKI-MANIFEST never grants approval.

## Incremental updates and merge boundary

Record each proposed file change with stable ID, previous version/hash, new version/hash, source changes and approval state in Wiki Change Log. Keep prior approved content in the previous delivery or retained history. If the prior target hash differs from the base, emit a separate proposed revision and a merge-conflict entry; do not overwrite user edits. Checkpoint includes topic identities/paths/versions, unresolved source dependencies and review queue so future sessions can resume. Final packages validate all local links; incremental batches use the existing checkpoint link resolution.

## Lint and receipt

The deterministic wiki validator checks manifest structure, packaged hashes, source coverage, citation locator presence, candidate location and dependency references. It cannot judge semantic support, real reviewer authority or actual runtime permissions. The agent must review semantic contradictions and cite the evidence; don't label those checks passed merely because hashes pass. Existing enterprise validator remains mandatory and authoritative for governance fields. Report what was actually generated, validated, deferred, approved and manually awaiting import. No automatic refresh or MCP publication is claimed.
