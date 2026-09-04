# Standard Obsidian Vault ZIP format

EW Knowledge Forge v0.4.0 outputs conventional ZIP files by default. A standalone forge produces one ZIP. A complete-project forge produces resumable volumes that all contain the same top-level Vault folder. Complete knowledge content is the default; navigation and checkpoint files never replace substantive source or semantic notes.

## Required structure

```text
Vault-Name/
├── README-START-HERE.md
├── 使用說明-請先閱讀.md
├── 00-Home/
│   ├── Project Home.md
│   ├── Source Register.md
│   └── Forge Progress.md
└── ... linked Markdown notes ...
```

Requirements:

- Exactly one top-level Vault folder.
- UTF-8 paths and Markdown content.
- No `.obsidian` directory, credentials, temporary files, absolute paths, or executables.
- All durable notes use the knowledge schema and valid wikilinks.
- Both usage guides are required and must name the generated Vault.
- Prefer Markdown-only packages when the user already owns the binary sources.

The ZIP itself is not opened by Obsidian. The user first extracts it and then opens the resulting top-level folder as a Vault. No Obsidian community plugin is required.

For a complete project, numbered ZIP volumes are required unless the inventoried corpus is clearly safe for one pass. Each volume must contain the identical top-level Vault folder so users can extract all volumes into one common destination and merge them. Include Part00 with the start page, source register, progress page, manifest, and merge instructions. Apart from the three identical built-in guide files injected into every volume, later volumes must use unique content paths. Deliver `FORGE-CHECKPOINT.md` beside each ZIP, not as a replacement for the Vault contents.

Recommended filenames:

- `<Vault-Name>_Part00_Start.zip`
- `<Vault-Name>_Part01_<batch-slug>.zip`
- `<Vault-Name>_Part02_<batch-slug>.zip`
- `<Vault-Name>_Part99_Final.zip` when the final batch count was unknown
- `<Vault-Name>_FORGE-CHECKPOINT_rNN.md`

The latest successfully delivered checkpoint is authoritative. Failed attempts must not advance the revision or next-volume number.

For an existing Vault, state that merging the extracted folder is manual. Never claim automatic backup, collision handling, or conflict-safe updates for the standard ZIP.

## Legacy format

The `.ewforge` format is retained only for explicit advanced or compatibility requests. Do not expose it as the default while no public companion importer is available.
