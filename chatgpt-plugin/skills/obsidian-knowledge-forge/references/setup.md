# Vault connection setup

## Local desktop mode

Use when Codex and the Obsidian Vault are available on the same computer or mounted filesystem.

1. Ask the user to select or paste the exact Vault folder.
2. Call configure_vault with that path and the selected mode.
3. The connector must verify that the folder exists and contains .obsidian.
4. Call vault_status and search_notes before routing the first topic.

The connector writes Markdown only, rejects hidden/settings paths, performs conflict checks on updates, and exposes no delete operation.

## Guided modes

- guided-auto: ask once when a topic is new or ambiguous, then write durable knowledge at checkpoints.
- preview: show the planned note changes before each write.
- manual: write only when explicitly requested.

Default to guided-auto when the user asks for systematic knowledge forging. Use preview when they ask to approve every change.

## Mobile-only or cloud ChatGPT mode

A cloud ChatGPT session cannot directly reach an unconnected iPhone, iCloud, or local desktop Vault. Do not claim otherwise.

Use one of:

- incremental ZIP: safe universal fallback;
- a user-authorized connected storage location that actually contains the Vault;
- a future hosted synchronization service with explicit authentication and write permissions.

Do not request account passwords or expose a local Vault to the public internet. If no connector is present, package the changes and state that the user must place them into the Vault.

## Existing knowledge

On first connection, inventory only Markdown metadata and searchable text required for routing. Do not rewrite the vault merely to normalize it. Propose a separate migration if legacy notes lack the knowledge schema.
