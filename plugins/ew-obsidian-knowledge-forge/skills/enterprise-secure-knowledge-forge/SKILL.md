---
name: enterprise-secure-knowledge-forge
description: Govern enterprise knowledge forging into auditable Obsidian Vault packages with pre-upload classification, cloud/local routing, candidate-to-approved publication, and explicit AI-DLP boundaries. Use for company SOPs, internal documents, departmental knowledge, confidential source planning, security review, or Enterprise Brain ingestion; use obsidian-knowledge-forge for personal or non-governed forging.
---

# EW Enterprise Secure Knowledge Forge

Turn enterprise sources into traceable knowledge without encouraging an upload-first workflow. This skill governs decisions and packaging inside ChatGPT; it is not endpoint DLP and cannot undo disclosure of content already visible to the current AI service.

## MCP JSON output

Keep this governance workflow available even though the third starter card now opens MCP knowledge forging. For MCPserver/JSON output, apply the same classification, routing and named-approval gates, then use `../mcp-knowledge-forge/SKILL.md`. Preserve classification, audience, route and approval evidence in each JSON record. The existing Obsidian output requirements below remain applicable to Vault output. Do not assert that JSON metadata enforces server permissions.


## First response: classify before content

Do not ask the user to upload, paste, quote, or summarize source body content in the first response.

Say briefly:

- do not provide source contents until the route is decided;
- this skill cannot retroactively protect content already present in the chat;
- P2/P3 sources may require local preparation or local-only forging.

Then ask only whether the source content is already present in the current chat: `yes`, `no`, or `partly`.

If `yes` or `partly`, record `boundary_status: already-visible` and state plainly that the security intake is prospective, not retroactive. Do not imply that deleting, redacting, or excluding the content from the final ZIP removes it from the AI service.

## Security intake

Read [classification-and-routing.md](references/classification-and-routing.md) before classifying sources. Gather one consequential decision at a time:

1. enterprise or project identity;
2. source title/type and owner, using metadata only;
3. intended audience;
4. likely P0–P3 class;
5. approved processing environment;
6. chosen route and required human approval.

If a fact is unknown, record it as unknown and use `blocked`. Never invent policy, ownership, classification, an approved AI environment, or an approver.

## Hard routing rules

- P0: approved cloud or local processing.
- P1: enterprise-approved AI environment or local processing.
- P2: local-only, or `cloud-sanitized` using a derivative prepared before upload. Keep originals and rehydration maps local.
- P3: local-only. Never request its body content in a cloud chat.
- Unknown class, authority, or environment: blocked pending a decision.

A user's request to proceed does not override these rules. Do not accept real credentials, private keys, passwords, authentication tokens, or rehydration maps.

## Forge modes

After intake, offer only routes actually allowed by the source register:

- `cloud-approved` for P0 or approved P1;
- `cloud-sanitized` for a locally prepared P2 derivative;
- `local-only` for P2/P3 or policy-selected local work;
- `blocked` when required evidence is missing.

For local-only work in a cloud chat, prepare a bounded handoff or processing specification without requesting protected source contents. Do not claim that local processing has occurred.

For complete projects, reuse the personal forge's resumable batch mechanics. Read `../obsidian-knowledge-forge/references/staged-project-forging.md`, then apply this skill's security gates before every batch. For note completeness, schema, and package rules, reuse the corresponding personal-forge references unless this skill imposes a stricter rule.

## Candidate and publication lifecycle

Read [enterprise-forging.md](references/enterprise-forging.md) before producing notes.

- Put unapproved knowledge in `10-Candidates/`.
- Require explicit approval by a named authorized person before copying or moving knowledge into `20-Published/`.
- Do not infer approval from silence, upload, authorship, job title, or a request to finish quickly.
- Preserve source IDs, class, route, audience, redaction status, approval status, and lineage.
- A single package serves one audience. Obsidian does not enforce note-level access control; separate audiences require separate packages or an external access-controlled store.

## Required enterprise package

In addition to the personal forge's required home, progress, guides, source records, and validation artifacts, include:

- `00-Governance/Security Intake.md`
- `00-Governance/Source Register.md`
- `00-Governance/Approval Register.md`
- `FORGE-MANIFEST.json`
- `10-Candidates/` when candidates exist
- `20-Published/` only for approved notes

Read [manifest-schema.md](references/manifest-schema.md) before creating the manifest. Never package original P2/P3 files, tokenization maps, credentials, `.obsidian`, executables, temporary files, or absolute local paths.

## Validation

Run the existing graph, checkpoint, and ZIP validators. Before packaging, also run:

```bash
python3 scripts/validate_enterprise_package.py <vault-root>
```

Treat this scan as defense-in-depth, not proof of confidentiality or regulatory compliance. A failed check blocks packaging. A passed check still requires human review.

## Delivery receipt

Report:

- enterprise, project, package audience, and processing environment;
- sources by P0–P3 class and route;
- already-visible, sanitized, locally deferred, blocked, processed, and skipped sources;
- candidate, approved, rejected, superseded, and withdrawn notes;
- named approvals actually supplied by the user;
- graph, checkpoint, enterprise scan, and ZIP integrity results;
- unresolved security decisions and the exact next action.

State that the ZIP is prepared but not imported, that the skill is not endpoint DLP, and that content already supplied to the AI service was not protected retroactively.


## Integrated living wiki (v0.6)

During every authorized forge batch, apply [living-wiki.md](references/living-wiki.md). Wiki impact assessment and source-backed topic drafts are part of forging, not a second user task. Preserve existing intake, source fidelity, classification, audience and approval gates. Run `python3 scripts/validate_wiki.py <vault-root>` before ZIP packaging and include its actual result in the receipt. Never claim installation, background maintenance or MCP publication from a generated ZIP.

For an existing Enterprise Brain connection, read [runtime integration](references/enterprise-brain-runtime.md). Use only available authorized tools; otherwise deliver the portable package and report the server integration boundary.
