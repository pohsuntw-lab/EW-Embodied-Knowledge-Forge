# EW Enterprise Secure Knowledge Forge — Architecture

Version: 0.5.0

## Trust boundary

The ChatGPT skill is a governance and packaging control, not an endpoint DLP product. Content visible in a cloud chat has already crossed the enterprise boundary. Therefore the safe sequence is classify first, sanitize locally when required, then provide only an approved derivative.

## Components

| Component | Responsibility | MVP |
| --- | --- | --- |
| Enterprise Forge Skill | Intake, classification, routing, forging, approval, receipt | Yes |
| Enterprise policy reference | P0–P3 rules, hard stops, metadata | Yes |
| Existing Forge core | Full-fidelity notes, checkpoints, graph validation, ZIP construction | Reused |
| Enterprise validator | Structural controls and conservative secret-pattern checks | Yes |
| Local AI-DLP Agent | Pre-upload inspection, OCR, metadata stripping, tokenization, enforcement | Later |
| Enterprise Brain | Identity, RBAC, signed policy, rehydration map, formal indexing | Integration boundary |

## Processing routes

- `cloud-approved`: P0 or policy-approved P1 in an approved enterprise AI environment.
- `cloud-sanitized`: P2 derivative produced outside the chat; the original and rehydration map remain local.
- `local-only`: P2 or P3 handled by enterprise-controlled EdgeAI.
- `blocked`: classification, authorization, ownership, or destination is unresolved.

## Package topology

```text
<Vault>/
├── 00-Home/
├── 00-Governance/
│   ├── Security Intake.md
│   ├── Source Register.md
│   └── Approval Register.md
├── 10-Candidates/
├── 20-Published/
├── 90-Sources/
├── FORGE-MANIFEST.json
├── README-START-HERE.md
└── 使用說明-請先閱讀.md
```

Obsidian does not enforce row- or note-level permissions. A package must contain only material intended for one audience. Cross-audience distribution requires separate packages or an external access-controlled system.

## Note security metadata

Enterprise candidate and published notes add:

- `confidentiality`: `P0|P1|P2|P3`
- `processing_route`: `cloud-approved|cloud-sanitized|local-only`
- `source_ids`
- `audience`
- `approval_status`: `candidate|approved|rejected|superseded|withdrawn`
- `approved_by`
- `approved_at`
- `redaction_status`: `none|required|sanitized|not-applicable`

Approval metadata must not be fabricated. If the approver or time is unknown, the note remains a candidate.

## Deterministic validation

`validate_enterprise_package.py` validates:

- mandatory governance files and manifest;
- forbidden `.obsidian`, executable, key, and credential-container files;
- representative private-key, API-token, and password-assignment patterns;
- no approved note without matching approval metadata;
- no P3 note routed through a cloud route.

The validator is defense-in-depth. Passing it is not proof that a package contains no confidential information.

## Future Local AI-DLP Agent

The next phase should run before ChatGPT and provide file-type extraction, OCR, exact-data matching, enterprise dictionaries, metadata stripping, reversible local tokenization, policy signatures, and audit logging. The skill consumes only its sanitized derivative and signed report.

