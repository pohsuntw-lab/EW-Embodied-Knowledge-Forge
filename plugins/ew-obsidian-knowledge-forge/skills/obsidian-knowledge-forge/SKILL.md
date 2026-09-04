---
name: obsidian-knowledge-forge
description: Turn ChatGPT conversations, generated documents, and user-provided sources into a validated standard ZIP Vault that opens directly in Obsidian without an Obsidian plugin. Use when users ask to organize chats or documents for Obsidian, build a knowledge graph, connect material to existing notes, or create an Obsidian-ready export.
---

# EW Embodied Knowledge Forge / 具象知識鍛造器

Turn meaningful conversations and documents into reusable, linked Markdown knowledge that ordinary users can open in Obsidian.

## Default outcome

Deliver one validated standard `.zip` containing one top-level Vault folder:

> Chat in ChatGPT → download ZIP → unzip → open the folder as an Obsidian Vault.

Do not require an API key or any Obsidian community plugin. Do not generate `.ewforge` unless the user explicitly requests the legacy or advanced format.

Every ZIP must contain:

- one clearly named top-level Vault folder;
- Obsidian-ready Markdown notes and folders;
- a hub note that links the knowledge graph;
- `README-START-HERE.md` in English;
- `使用說明-請先閱讀.md` in Traditional Chinese.

Read [package-format.md](references/package-format.md) before building a ZIP.

## Language

- Conduct the workflow in the user's language.
- Use Traditional Chinese for branded Chinese output unless requested otherwise.
- Keep schema keys, knowledge IDs, versions, and technical filenames stable in English/ASCII.
- For bilingual packages, create equivalent English and Traditional Chinese notes with `language`, `translation_of`, and a `related` link.

## Inputs and Vault boundary

Use only the visible conversation, generated files, uploaded sources, or Vault notes/indexes the user explicitly provides.

- Never imply access to a complete ChatGPT history, phone storage, iCloud, or Obsidian Vault.
- If no Vault index is supplied, create safe proposed links inside the new Vault.
- If a Vault index or notes are supplied, reuse confirmed hubs, paths, and `knowledge_id` values.
- Never package `.obsidian`, credentials, temporary files, executable payloads, or unrelated material.

## Forge workflow

1. Determine the durable topic and a short, filesystem-safe Vault name.
2. If two or more supplied topics are plausible, ask one compact choice question.
3. Extract only durable concepts, decisions, requirements, evidence, processes, projects, tasks, references, people, and organizations.
4. Separate confirmed facts from proposals, assumptions, disputes, preferences, and open questions.
5. Apply [knowledge-schema.md](references/knowledge-schema.md) and reuse the bundled note and hub templates.
6. Link every durable note to a hub or parent with `up`. Add `related`, `replaces`, and `source_refs` only when supported.
7. Add both bundled ZIP usage guides at the Vault root, replacing the placeholder Vault name.
8. Validate the staged Vault with `scripts/validate_graph.py`. Fix every error.
9. Build the ZIP with `scripts/build_vault_zip.py`. Run a ZIP integrity test.
10. Deliver the ZIP and immediately show the appropriate mobile and desktop instructions.

## ZIP delivery instructions

Always state that the ZIP has been prepared but has not been imported into Obsidian.

For iPhone/iPad:

1. Download the ZIP.
2. Open Apple's Files app and tap the ZIP once to unzip it.
3. Move the extracted Vault folder into `On My iPhone/Obsidian` or `iCloud Drive/Obsidian`.
4. Open Obsidian and choose **Open folder as vault**.
5. Select the extracted Vault folder and open its start-here or hub note.

For Android:

1. Download and extract the ZIP with the Files app.
2. Move the extracted Vault folder to a location Obsidian can access.
3. Open Obsidian, choose **Open folder as vault**, and select it.

For Windows/macOS:

1. Download and extract the ZIP.
2. Open Obsidian and choose **Open folder as vault**.
3. Select the extracted top-level Vault folder.

If the exact label differs by Obsidian version or language, tell the user to send a screenshot and guide them one screen at a time. Never claim to control the user's device.

## Version and conflict rules

- Keep `knowledge_id` stable when wording or filenames change.
- Increment patch for corrections, minor for compatible additions, and major for meaning-breaking changes.
- Do not silently merge contradictions. Mark them disputed or ask the user.
- A standard ZIP is best for a new Vault or manual folder import. For automatic conflict-safe updates to a large existing Vault, explain that ZIP import is manual and request an exported index or relevant notes before merging.

## What not to forge

Do not preserve greetings, repetition, emotional venting, intermediate wording, or transient planning unless it changes a durable decision or requirement.

Exclude secrets, credentials, `.obsidian` settings, absolute paths, path traversal, temporary files, and executable code unrelated to the requested knowledge.

## Delivery receipt

Report:

- ZIP filename and whether it is a new Vault or manual incremental update;
- topics and source scope processed;
- notes created, updated, superseded, skipped, or proposed;
- top-level Vault folder and hub note;
- validation and ZIP integrity results;
- unresolved conflicts or missing source material;
- concise device-appropriate import steps;
- a clear statement that the ZIP is ready but not yet imported into Obsidian.

