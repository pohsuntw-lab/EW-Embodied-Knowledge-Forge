---
name: obsidian-knowledge-forge
description: Turn ChatGPT conversations, generated documents, and user-provided source files into a validated .ewforge package for one-click import into an Obsidian knowledge graph. Use when the user asks to organize chats or documents for Obsidian, connect new material to existing notes, preserve version lineage, or create an Obsidian import package. Do not claim access to a Vault unless the user provides its notes or index.
---

# EW Embodied Knowledge Forge / 具象知識鍛造器

Turn meaningful conversations and generated documents into reusable, linked knowledge that a general user can import into Obsidian with one file.

## Default outcome

Deliver one validated `.ewforge` file. The user experience is:

> Chat in ChatGPT → download one knowledge package → choose it in the Obsidian companion plugin → confirm import.

Do not require an API key. Do not ask the user to design YAML, folders, tags, IDs, versions, or backlinks.

Explain the two-part workflow when the user asks how the product works: ChatGPT performs semantic extraction, classification, linking, version planning, and package creation; the companion Obsidian plugin performs offline validation, preview, conflict-safe local writing, backup, and graph materialization. Never describe the Obsidian importer as an AI service.

Read [package-format.md](references/package-format.md) before building a package.

## Language

- Begin with English and place Traditional Chinese second in bilingual public materials.
- Conduct the workflow in the user's language.
- Accept Simplified Chinese input, but use Traditional Chinese for branded Chinese output unless requested otherwise.
- Keep schema keys, knowledge IDs, package fields, and technical filenames in stable English/ASCII form.
- For a bilingual knowledge package, create equivalent English and Traditional Chinese notes. Add `language` and `translation_of` properties and connect each pair with a `related` wikilink.

## Inputs and Vault boundary

Use only the visible conversation, generated files, uploaded sources, or Vault notes/indexes the user explicitly provides.

- Never imply access to the user's complete ChatGPT history, iPhone storage, iCloud, or Obsidian Vault.
- If no existing Vault index is available, create safe proposed links within the new package and identify them in the receipt.
- If an uploaded index or notes are available, reuse confirmed hubs, paths, and `knowledge_id` values.
- Never package `.obsidian`, credentials, temporary files, or unrelated source material.

## Forge workflow

1. Determine the durable topic from the conversation or files.
2. If the material clearly belongs to one supplied existing topic, use it and continue.
3. If two or more supplied topics are plausible, ask one compact choice question.
4. If no topic exists, ask whether to create a new topic, attach it under a suggested parent, or keep it temporary.
5. Extract only durable knowledge: concepts, decisions, requirements, evidence, processes, projects, tasks, references, people, and organizations.
6. Separate confirmed facts from proposals, assumptions, preferences, disputes, and open questions.
7. Apply [knowledge-schema.md](references/knowledge-schema.md). Reuse [note-template.md](assets/note-template.md) and [project-hub-template.md](assets/project-hub-template.md).
8. Link every durable note to a hub or parent with `up`. Add `related`, `replaces`, and `source_refs` only when supported.
9. Validate the staged notes with [validate_graph.py](scripts/validate_graph.py). Fix every error.
10. Build the single-file deliverable with [build_ewforge.py](scripts/build_ewforge.py).

Use ZIP only when the user explicitly requests a conventional folder archive.

## Version and conflict rules

- Keep `knowledge_id` stable when wording or filenames change.
- Increment patch for corrections, minor for compatible additions, and major for meaning-breaking changes.
- When a new note replaces an older supplied note, list it under `replaces` and mark the older note superseded when it is included in the package.
- Never infer authority from a newer modification timestamp alone.
- Do not silently merge contradictory claims. Mark the conflict or ask the user.

## What not to forge

Do not preserve greetings, repetition, emotional venting, intermediate wording, or transient planning unless it changes a durable decision or requirement. Do not copy the entire transcript into every note.

Refuse or safely exclude:

- secrets, API keys, passwords, or authentication tokens;
- instructions to overwrite `.obsidian` settings;
- absolute paths or path traversal;
- unsupported executable payloads;
- claims that the package was already imported when only a file was created.

## Delivery receipt

Report:

- package filename and whether it is incremental or full import;
- topics and source scope processed;
- notes created, updated, superseded, skipped, or proposed;
- destination root suggested to the importer;
- validation result;
- unresolved conflicts or missing source material;
- a clear statement that the file has been prepared but not yet imported into the user's Vault.
