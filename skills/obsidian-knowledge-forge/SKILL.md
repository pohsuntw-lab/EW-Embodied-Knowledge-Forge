---
name: obsidian-knowledge-forge
description: Turn current ChatGPT conversations, exported chat segments, generated documents, and user-provided sources into a validated, full-fidelity Obsidian Vault ZIP. Guide users through large projects in resumable batches so the whole project can be forged without relying on one oversized conversation.
---

# EW_knowledge_forge

Build durable Obsidian knowledge from ChatGPT conversations and documents while respecting ChatGPT's limited visible context and the possibility of interrupted generations.

## Non-negotiable truth

Never imply access to the user's complete ChatGPT history, every conversation in a Project, phone storage, iCloud, or an existing Obsidian Vault. Process only the current visible conversation, uploaded/exported chat content, supplied files, and previously generated forge checkpoints.

A short user prompt does not mean the available source corpus is small. Do not blame prompt length or context size for a generic network error without evidence.

## First response: guide, do not forge

On first invocation, ask only which path the user wants:

1. **Start a complete project forge** — create a project identity and process the project in resumable batches.
2. **Continue an existing project forge** — ask for `FORGE-CHECKPOINT.md` and the next source batch.
3. **Forge only this conversation or these files** — create one standalone Vault ZIP.

After the user chooses, ask for exactly one compression level:

- **A — Full preservation (recommended), 0–10% reduction**
- **B — Balanced organization, 20–35% reduction**
- **C — High condensation, 50–65% reduction**

Ask one decision at a time. Do not begin reading a large corpus or generating files in the same turn as these choices unless the user explicitly provided the choices and said to proceed without questions.

## Complete-project mode

Use complete-project mode when the user wants an entire project, many historical conversations, or a corpus too large to handle reliably in one pass. Read [staged-project-forging.md](references/staged-project-forging.md) before acting.

Core behavior:

- Create a stable `project_id`, Vault name, source register, volume plan, and `FORGE-CHECKPOINT.md` before substantive forging.
- Guide the user to provide one historical conversation, exported chat segment, or bounded file group at a time.
- Process only the current batch. Do not ask the model to recall or reproduce earlier full text.
- End every completed batch with a validated incremental ZIP and an updated checkpoint.
- Make every volume extract into the same top-level Vault folder, with unique note paths and stable `knowledge_id` values.
- The checkpoint carries state, not knowledge prose. Keep it compact enough to upload into a fresh chat.
- A new chat must be able to continue from the checkpoint without the earlier conversation.
- When all registered sources are complete, create the final index/receipt volume and give exact merge and completion-check instructions.

## Standalone mode

Use standalone mode for one visible conversation or a bounded set of files that can be completed reliably in the current task. If the corpus becomes unsafe for one pass, stop before synthesis, propose complete-project mode, and preserve any finished inventory in a checkpoint.

## Full-fidelity rules

Default to complete knowledge, not outline-only output. Removing noise must not remove definitions, reasoning, procedures, requirements, conditions, exceptions, roles, evidence, examples, metrics, decisions, limitations, disputes, or open questions.

Read [completeness-standard.md](references/completeness-standard.md) whenever sources or long conversations are forged.

- Register every selected source before synthesis.
- Preserve a readable source note or a complete set of substantive notes for every processed source.
- Separate confirmed facts from proposals, assumptions, disputes, preferences, and unresolved questions.
- Do not let a hub, folder tree, or title list substitute for body content.
- Never silently choose B or C.

## Note and package construction

Read [knowledge-schema.md](references/knowledge-schema.md) before creating durable notes. Read [package-format.md](references/package-format.md) before building any ZIP.

Every new Vault must include:

- one clearly named top-level Vault folder;
- linked Markdown notes;
- `00-Home/Project Home.md`;
- `00-Home/Source Register.md`;
- `00-Home/Forge Progress.md`;
- `README-START-HERE.md`;
- `使用說明-請先閱讀.md`.

For every batch:

1. Confirm the batch boundary and source IDs.
2. Extract durable knowledge without importing unrelated material.
3. Add source notes and semantic notes using stable identities.
4. Update progress and source status.
5. Validate the staging tree with `scripts/validate_graph.py`; for Part01 and later, pass the last checkpoint with `--checkpoint` so links to earlier volumes can be verified.
6. Validate the checkpoint with `scripts/validate_checkpoint.py`.
7. Build the ZIP with `scripts/build_vault_zip.py` and run its integrity check.
8. Deliver both the incremental ZIP and updated `FORGE-CHECKPOINT.md`.

Never package `.obsidian`, credentials, temporary files, executable payloads, unrelated source files, or absolute local paths.

## Failure and recovery

If a generation, upload, or ZIP build fails:

- do not claim the batch is complete;
- do not advance `next_volume` or mark sources processed;
- keep the last successfully delivered checkpoint authoritative;
- retry only the failed batch in a fresh chat when necessary;
- never ask the user to restart the whole project if a valid checkpoint exists.

## Delivery receipt

Report:

- project and Vault names;
- selected compression level;
- current volume and expected/unknown total volumes;
- source IDs selected, processed, preserved in full text, deferred, and skipped with reasons;
- notes created, updated, superseded, and proposed;
- graph validation, checkpoint validation, and ZIP integrity results;
- unresolved conflicts or missing sources;
- the exact next action and which files the user must retain.

State clearly that ZIP files are prepared but not yet imported into Obsidian.

For installation instructions, follow [package-format.md](references/package-format.md). Do not claim control of the user's device.
