---
name: obsidian-knowledge-forge
description: Organize scattered ChatGPT conversations, uploaded files, and generated documents into a structured Obsidian knowledge graph with atomic notes, metadata, version lineage, bidirectional links, indexes, attachments, and incremental import packages. Use when a user asks to summarize chats into a knowledge base, organize files for Obsidian, connect new material to existing notes, deduplicate versions, or audit an Obsidian vault. Do not claim direct access to a local or mobile vault unless it is actually attached or connected.
---

# EW Embodied Knowledge Forge / 具象知識鍛造器

Transform every meaningful conversation into reusable knowledge, not merely a folder of files.

## Language behavior

- Detect whether the user prefers Traditional Chinese or English and conduct the workflow in that language.
- Accept Simplified Chinese input, but default branded Chinese output to Traditional Chinese unless the user asks otherwise.
- Keep schema keys, IDs, filenames where practical, and package fields in stable ASCII/English form.
- When the user requests a bilingual package, create equivalent Traditional Chinese and English notes, add a `language` property, and connect each pair with `translation_of` plus a `related` wikilink. Do not make one mixed-language paragraph-by-paragraph note unless requested.
- Every delivery receipt uses the user's current language; bilingual deliveries include a compact receipt in both languages.

## Default experience: one-click knowledge package

For general users, default to the shortest understandable flow:

> Chat in ChatGPT → receive one `.ewforge` file → choose it in the EW Knowledge Forge Obsidian plugin → confirm import.

Do not ask the user to configure an API key, YAML, folders, or graph rules for this flow. ChatGPT performs classification, formatting, metadata, linking, and validation before delivery. The mobile Obsidian plugin performs only local validation and safe import; it makes no network request.

Read [package-format.md](references/package-format.md) before producing a package. After staging and validating the Markdown notes, build the deliverable with [build_ewforge.py](scripts/build_ewforge.py). Use ZIP delivery only when the user explicitly needs a conventional folder/archive workflow.

## Optional connected-vault flow

When a configured vault is available, start a meaningful new topic by calling the vault status and searching topic hubs with the user's actual subject.

- If one existing topic is a strong match, briefly tell the user where the conversation will be filed and continue.
- If two or more topics are plausible, ask one short choice question.
- If no topic matches, ask whether to create a new topic, relate it to a suggested existing topic, or keep the conversation temporary.
- Do not interrupt casual remarks, emotional processing, or trivial one-turn questions with filing prompts.
- After a durable decision, requirement, method, evidence item, or reusable explanation forms, forge or update the relevant note. Do not wait for the user to manually request a summary when guided-auto mode is active.
- At the end of the exchange, report what was written and where.

Read [guided-dialogue.md](references/guided-dialogue.md) before running the guided flow.

## Select the operating mode

- **Conversation forge:** Extract durable knowledge from the visible conversation or user-provided chat export.
- **Document forge:** Convert selected documents into linked Markdown notes while preserving originals.
- **Incremental update:** Connect new notes to an existing vault without repackaging the entire vault.
- **Vault audit:** Check metadata, broken links, duplicate identities, orphan notes, and unsafe overwrite risks.

Unless the user explicitly requests direct vault access, Conversation forge and Document forge deliver a one-click `.ewforge` package.

Only use information actually available in the conversation, attached files, connected sources, or a configured vault. Never imply access to the user's complete ChatGPT history, phone storage, iCloud, or Obsidian installation.

## Direct-write boundary

- Use the ew-knowledge-vault tools when they are available and configured.
- Ask the user to choose a local Vault folder during first-time setup. Do not guess a path.
- When the vault is unconfigured or unreachable, read [setup.md](references/setup.md) and explain the applicable connection mode.
- Before the first write in a conversation, state the target topic and whether guided-auto or preview mode is active.
- Guided-auto authorizes routine create/update writes for the selected topic during that conversation. It never authorizes deletion, moving unrelated notes, editing .obsidian, or resolving a factual conflict without the user.
- Use content hashes on updates. If the note changed since it was read, stop and reconcile the conflict.
- If the vault is unavailable, fall back to an incremental package and say clearly that no direct write occurred.

## Required workflow

1. Confirm the knowledge scope and target vault when they materially affect classification. For a current-conversation request with a clear topic, proceed without extra questions.
2. Inventory inputs and detect exact duplicates by content hash where local bytes are available.
3. Separate durable knowledge into note types: concept, decision, requirement, evidence, process, project, task, reference, or person/organization.
4. Preserve source meaning. Mark unresolved contradictions; do not silently merge incompatible claims.
5. Apply the schema in [knowledge-schema.md](references/knowledge-schema.md).
   Reuse [note-template.md](assets/note-template.md) and [project-hub-template.md](assets/project-hub-template.md) when creating new managed notes.
6. Link every new durable note to at least one hub or parent. Add relevant related and replacement links when supported by evidence.
7. Preserve formal source files in the attachment area. Markdown is the primary reading and search surface.
8. For an existing vault, deliver only changed or new files as an incremental package. Never include or overwrite the .obsidian directory unless the user explicitly requests a settings change.
9. Validate the staged vault or update with [validate_graph.py](scripts/validate_graph.py). Fix all error-level findings before delivery.
10. Package with [build_ewforge.py](scripts/build_ewforge.py) for the default mobile one-click workflow. Use [package_increment.py](scripts/package_increment.py) only for a requested ZIP workflow.

## Conversation synthesis rules

- Capture decisions with rationale, date, status, and the alternatives that were rejected when stated.
- Capture requirements with owner, acceptance condition, dependencies, and source conversation.
- Distinguish a confirmed fact from an assumption, proposal, preference, or open question.
- Prefer one stable note per durable subject. Update or replace it instead of creating a near-duplicate.
- Do not copy an entire chat transcript into every note. Keep a source note when traceability is useful, then link distilled notes to it.
- Never invent links to notes that do not exist. When the target vault is unavailable, use an explicit proposed-link marker and list it in the handoff.

## Delivery contract

Each delivery must state:

- scope processed;
- notes created, updated, archived, or skipped;
- unresolved conflicts or missing sources;
- exact destination folder;
- validation outcome;
- whether the package is a full import or incremental update.
- the exact `.ewforge` filename for one-click import.

For detailed classification and version behavior, read [workflow.md](references/workflow.md). For acceptance checks, read [acceptance.md](references/acceptance.md).
