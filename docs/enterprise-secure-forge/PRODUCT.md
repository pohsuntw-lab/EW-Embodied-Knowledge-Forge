# EW Enterprise Secure Knowledge Forge — Product Specification

Version: 0.5.0  
Status: Approved MVP blueprint  
Publisher: Embodied Worker Co., Ltd. / 具象職人股份有限公司

## Problem

Enterprises want employees to turn conversations and documents into durable knowledge, but a normal upload-first workflow can expose confidential material before its sensitivity is assessed. A ChatGPT skill can govern user behavior and package outputs; it cannot retroactively protect content already uploaded or replace endpoint, browser, CASB, or gateway DLP.

## Intended users

- Department knowledge stewards preparing source batches.
- Security or compliance reviewers defining allowed processing routes.
- Business approvers deciding whether candidate knowledge may be published.
- Enterprise Brain administrators importing approved Vault packages.

## MVP outcome

Add a separate `enterprise-secure-knowledge-forge` skill to the existing EW Knowledge Forge plugin. It must require a security intake before asking for source content, classify each source P0–P3, route work to approved cloud, redacted cloud, or local-only processing, keep candidate and published knowledge separate, and emit an auditable Forge Manifest and delivery receipt.

## Data classes

| Class | Meaning | Default route |
| --- | --- | --- |
| P0 Public | Approved public information | Approved cloud or local |
| P1 Internal | Routine internal information | Enterprise-approved AI environment |
| P2 Confidential | Customer, pricing, operational, contractual, or technical information | Local redaction/tokenization before any cloud use, or local-only |
| P3 Restricted | Credentials, secrets, regulated personal data, critical formulas, unpublished patent material, or crown-jewel know-how | Local-only; never request upload to a cloud chat |

Customer policy may make routing stricter, never weaker than the hard prohibitions in this specification.

## MVP modules

1. Security intake and deployment-boundary disclosure.
2. Source register with P0–P3 classification and processing route.
3. Safe routing decision: approved cloud, redacted cloud, local-only, or blocked pending approval.
4. Candidate knowledge generation with provenance and sensitivity metadata.
5. Human approval gate before published knowledge is created.
6. Enterprise package validation and Forge Manifest generation.

## Primary journey

1. User invokes the enterprise skill.
2. Skill explains that files must not be uploaded until classified.
3. User identifies the enterprise/project and whether source content is already present in the chat.
4. Skill registers source metadata without requesting sensitive body content.
5. Each source receives a class, route, owner, intended audience, and approval state.
6. P0/P1 content may proceed in the approved environment. P2 proceeds only from a sanitized derivative or local route. P3 stops and routes local-only.
7. Knowledge is forged into a candidate area.
8. Output is reviewed for sensitive reconstruction and provenance.
9. An authorized person approves or rejects publication.
10. Only approved content enters the published area and formal index.

## Required package contents

- `00-Governance/Security Intake.md`
- `00-Governance/Source Register.md`
- `00-Governance/Approval Register.md`
- `10-Candidates/` when unapproved notes exist
- `20-Published/` for approved notes
- `FORGE-MANIFEST.json`
- Existing EW Knowledge Forge home, progress, guides, and source-preservation artifacts

## Explicit exclusions

- No claim of automatic endpoint interception or real-time network blocking.
- No automatic guarantee that content is free of confidential data.
- No storage of tokenization rehydration maps inside the Vault ZIP.
- No automatic cross-department access enforcement by Obsidian; different audiences require separate Vaults or an external access-controlled repository.
- No compliance certification or legal conclusion.
- No automatic publication without named human approval.

## Success evidence

- A clean P0/P1 test batch completes and produces a valid enterprise Vault ZIP.
- A P2 batch cannot proceed to cloud processing without a recorded sanitized derivative or local-only route.
- A P3 source is stopped before the skill requests its contents.
- Already-uploaded content triggers a non-retroactivity warning.
- Candidate knowledge cannot appear under `20-Published/` without an approval record.
- The validator detects prohibited files and representative high-risk secret patterns.

