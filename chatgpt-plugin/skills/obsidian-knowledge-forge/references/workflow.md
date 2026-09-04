# Knowledge-forging workflow

## 1. Define the corpus

Supported sources include the visible conversation, user-selected chats, exported chat files, uploaded documents, connected files, and a supplied Obsidian vault. State what was not available.

## 2. Build an inventory

Record filename, format, size, modified date, content hash when available, apparent subject, language, and explicit version. Group exact duplicates before semantic analysis.

## 3. Distill conversation

Extract:

- claims and concepts;
- decisions and their rationale;
- requirements and acceptance conditions;
- workflows and responsibilities;
- evidence and source documents;
- unresolved questions;
- tasks and deadlines;
- named projects, products, people, and organizations.

Treat brainstorming as proposed unless the user confirmed it. Treat corrections as authoritative over the corrected statement.

## 4. Match existing knowledge

For each candidate note, decide:

- create a new durable identity;
- update an existing note;
- supersede an old version;
- merge an exact or semantic duplicate;
- keep separate because claims conflict;
- skip because it is transient or irrelevant.

Prefer title, knowledge_id, explicit aliases, links, and content evidence over filename similarity alone.

## 5. Construct the graph

Create small hub notes for projects and major domains. Every durable note needs a route back to one hub through up links. Add lateral related links sparingly. A graph with many weak links is worse than a smaller graph with explained relationships.

Backlinks make a new-to-old relationship visible without rewriting every old note. Update the old note only when its meaning, status, or forward navigation must change.

## 6. Preserve source artifacts

- Markdown: keep as the main reading surface.
- DOCX and PDF: convert their text when possible; preserve the original in attachments.
- Images: keep in attachments and embed only where they improve understanding.
- ZIP or code packages: preserve the archive and safely extract searchable documentation.
- Chat transcript: keep one source note when auditability is needed.

Do not flatten source and interpretation together. Label summaries and inferences.

## 7. Deliver incrementally

An incremental package mirrors vault-relative paths and contains only additions or replacements. Include a change manifest. Exclude .obsidian, caches, temporary transfers, and unrelated source files.

When the existing vault is unavailable, create a self-contained import folder. Do not claim that links to unseen notes were validated.

## 8. Validate

Run the graph validator. Resolve missing internal links, duplicate knowledge IDs, missing required properties, empty notes, and unsafe settings content. Review warnings for orphan notes and unversioned material.
