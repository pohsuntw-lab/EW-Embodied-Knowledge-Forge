# Standard Obsidian Vault ZIP format

EW Knowledge Forge v0.3 outputs a conventional ZIP by default. It contains one top-level folder that can be opened directly as an Obsidian Vault after extraction.

## Required structure

```text
Vault-Name/
├── README-START-HERE.md
├── 使用說明-請先閱讀.md
├── 00-Home/
│   └── Project Home.md
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

For an existing Vault, state that merging the extracted folder is manual. Never claim automatic backup, collision handling, or conflict-safe updates for the standard ZIP.

## Legacy format

The `.ewforge` format is retained only for explicit advanced or compatibility requests. Do not expose it as the default while no public companion importer is available.

