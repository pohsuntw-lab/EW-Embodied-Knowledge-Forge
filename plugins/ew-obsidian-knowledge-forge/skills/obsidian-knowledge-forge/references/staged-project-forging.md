# Resumable complete-project forging

Use this workflow when a user wants an entire ChatGPT Project, historical conversations, or a large mixed corpus forged into one Obsidian Vault.

## Design goal

The project must survive context limits, a closed app, a failed generation, and a move to a new chat. Never depend on hidden history or the model remembering earlier batches.

## Phase 1 — Establish the project passport

Ask for or derive the project name, filesystem-safe `project_id`, Vault name, language, compression level, and whether this is a new Vault or a manual update. Create `FORGE-CHECKPOINT.md` from the bundled template. Assign a date-qualified `forge_id` so similar project names cannot collide.

The checkpoint is the portable control plane. It contains identities, statuses, paths, counts, and unresolved issues. It must not contain full source text or long summaries.

## Phase 2 — Inventory before synthesis

Guide the user to enumerate source units. A unit may be one current conversation, one exported conversation, one long document, a small coherent group of short documents, or a prior Forge volume supplied for verification.

Assign every unit a stable `source_id` such as `CHAT-001`, `DOC-001`, or `FILE-001`. Record title, type, approximate date, status, intended volume, and limitations.

Allowed source statuses are `planned`, `received`, `processing`, `processed`, `deferred`, `skipped`, and `conflict`.

Never mark a source `processed` until its notes, graph validation, checkpoint validation, ZIP build, and ZIP integrity test have all succeeded.

## Phase 3 — Select a safe batch

Prefer semantic boundaries over exact token estimates:

- one long conversation per batch;
- one long document per batch;
- up to three medium related sources per batch;
- several short files only when they form one coherent topic.

If one source is too large, split it by stable section boundaries and assign child IDs such as `DOC-004-A` and `DOC-004-B`. Record the parent relationship. Do not cut through a table, procedure, decision trail, or quoted evidence block.

Do not reload earlier source bodies merely to maintain continuity. Use stable IDs, existing note paths, the checkpoint, and short hub summaries.

## Phase 4 — Forge one batch

For the selected batch:

1. Confirm source IDs and the next volume number.
2. Create readable source notes under `90-Sources/<source_id>/` when allowed and useful.
3. Create substantive semantic notes in topic folders.
4. Link every durable note upward to the project hub or a confirmed area hub.
5. Update `00-Home/Source Register.md` and `00-Home/Forge Progress.md` inside the volume.
6. Avoid rewriting notes from prior volumes unless the checkpoint explicitly records an update or replacement.
7. Use unique paths for new files to prevent accidental overwrite during extraction.

Validate Part00 directly. For Part01 and later, run `validate_graph.py <staging> --checkpoint <latest-checkpoint>` so wikilinks into earlier volumes are accepted only when their paths are recorded in the checkpoint.

Name volumes `<Vault-Name>_PartNN_<batch-slug>.zip`.

Use `Part00` for shared root files, project passport, source register, progress page, and merge instructions. Subsequent parts contain unique source and semantic note paths. A final index update may use `Part99-Final` when the total number of batches was unknown at the start.

## Phase 5 — Checkpoint and handoff

After successful validation and ZIP creation, mark completed sources `processed`, record the delivered ZIP filename and cumulative counts, increment `checkpoint_revision`, set `next_volume`, list the next planned source IDs, record conflicts, and generate the updated checkpoint.

Tell the user to retain both files. To continue in a fresh chat, the user invokes the skill, chooses **Continue**, uploads `FORGE-CHECKPOINT.md`, and supplies only the next source batch.

## Phase 6 — Finish the project

Completion requires:

- every registered source is `processed` or has an explicit user-approved `skipped` reason;
- cumulative source coverage is 100%;
- every volume filename is listed;
- expected Markdown note count is recorded;
- unresolved conflicts are visible;
- the final hub links every area or source collection;
- the user receives exact extraction and merge instructions.

Never claim the whole project is complete based only on the current chat or project memory.

## Historical ChatGPT conversations

ChatGPT may not expose every past conversation to the active model. Guide the user through this capture loop:

1. Open one relevant historical conversation.
2. Invoke EW Knowledge Forge and choose **Continue**.
3. Upload the current `FORGE-CHECKPOINT.md`.
4. Ask to forge the visible conversation as the next source unit.
5. Download the returned ZIP volume and updated checkpoint.
6. Repeat with the next conversation.

If the product cannot attach a checkpoint in the historical chat, ask the user to copy or export that conversation into a new chat together with the checkpoint. Do not invent access to inaccessible messages.
