# Changelog / 更新紀錄

## 0.4.1 — 2026-09-05

- Replaced the knowledge-network composer icon with the official black-and-gold Embodied Worker elephant logo.
- Pointed both `composerIcon` and `logo` to the same PNG brand asset in the published plugin package.
- Synchronized the root and marketplace plugin manifests.

## 0.4.0 — 2026-09-04

- Renamed the public display name to **EW_knowledge_forge** while preserving the existing internal plugin identity.
- Added resumable, batch-by-batch forging for complete ChatGPT projects.
- Added portable `FORGE-CHECKPOINT.md` state for continuing safely in a new conversation.
- Added incremental Obsidian Vault ZIP volumes, source coverage checks, merge instructions, and recovery rules.
- Made full-fidelity knowledge preservation the default and prevented outline-only delivery.

## 0.3.0 — 2026-09-04

- Changed the default deliverable from `.ewforge` to a standard Obsidian Vault ZIP.
- Removed the Obsidian companion plugin requirement from the normal user workflow.
- Added deterministic ZIP building and integrity validation.
- Required one top-level Vault folder, a knowledge hub, and linked Markdown notes.
- Added English and Traditional Chinese instructions inside every generated ZIP.
- Added direct iPhone, iPad, Android, Windows, and macOS import instructions to delivery responses.
- Retained `.ewforge` only as an explicitly requested legacy/advanced format.

## 0.2.0 — 2026-09-04

- Prepared a public skills-only ChatGPT/Codex plugin for the universal Plugins Directory.
- Added a GitHub repo marketplace, bilingual listing, policies, starter prompts, and reviewer test cases.
- Moved the local Vault MCP prototype out of the public package so the public workflow needs no server, account, or API key.

## 0.1.1 — 2026-09-04

- Standardized the bilingual name as **EW Embodied Knowledge Forge / 具象知識鍛造器**.
- Put English first and Traditional Chinese second across the ChatGPT plugin and README.
- Confirmed the knowledge-forging skill is bundled and declared by the ChatGPT plugin.

## 0.1.0 — 2026-09-04

- First bilingual release.
- Added the original `.ewforge` importer and knowledge-package generator.
- Added safe-path validation, SHA-256 verification, conflict copies, and optional version backups.
- Added the official Embodied Worker elephant brand artwork.
