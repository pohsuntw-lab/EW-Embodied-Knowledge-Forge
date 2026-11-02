# Enterprise Brain runtime integration

The skills-only plugin and Enterprise Brain runtime are separate deliverables. Installing this plugin creates instructions and packaging tools; it does not install a server, connect MCP automatically, or gain local Vault access.

When the separately installed Enterprise Brain living-wiki runtime is available:

- Confirmed Vault imports enqueue Markdown sources into the durable Knowledge Forge organizer queue. Source classification is explicit; unspecified classification defaults to restricted. Import does not approve source content or AI synthesis.
- The local model incrementally creates source-bound topic drafts, grouped by registered project where available. Large topic contexts use resumable segment checkpoints. Generation failures stay visible for review.
- Source documents and Wiki synthesis have separate approval/publication gates. Wiki publication requires every source to be published, effective, unchanged and authorized. The model never grants approval.
- `search_wiki` and `get_wiki_topic` are read-only MCP tools. Every response rechecks dependencies; changed, withdrawn, expired or unauthorized sources immediately remove the old topic from formal results. Revised synthesis requires review again.
- The configured owner's dedicated Published-Wiki directory receives only published synthesis from public/internal sources. Confidential/restricted sources remain controlled. Manual-edit conflicts stop overwrites. Background refresh removes untouched stale managed exports; offline or manually edited copies cannot be retroactively revoked.
- Use the existing authenticated Document Organizer Wiki panel for evidence review, approval, publication and withdrawal. Product permissions still apply.

Administrative API prefix: `/api/admin/knowledge-forge/organizer`. Routes include `GET /wiki/topics`, `POST /wiki/refresh`, and `POST /wiki/topics/{id}/{approve|publish|withdraw}` with expected_revision and decision reason. Never fabricate credentials or call private APIs without authorization.

If the runtime or tools are unavailable, follow the portable living-wiki workflow, deliver drafts and proposed updates, and report manual import/server integration as pending. This reference does not prove the customer's server is installed or connected.
