# Enterprise forging workflow

## Registers first

Create `00-Governance/Security Intake.md` and `00-Governance/Source Register.md` before substantive forging. Each source row includes source ID, title/type, owner, class, audience, boundary status, route, sanitization status, authorization status, and processing status.

## Candidate notes

Candidate notes preserve the full meaning allowed by their routed source while separating facts, proposals, assumptions, disputes, and unresolved questions. Store them under `10-Candidates/` with:

```yaml
confidentiality: P1
processing_route: cloud-approved
source_ids:
  - SRC-001
audience:
  - operations
approval_status: candidate
approved_by: null
approved_at: null
redaction_status: not-applicable
```

## Output review

Before approval, review candidate notes for:

- identifiers or exact values reconstructed from context;
- secrets or authentication material;
- facts joined across sources in a way that raises sensitivity;
- cross-audience leakage;
- unsupported claims or missing provenance;
- filenames, metadata, comments, or hidden content copied from a source.

This is a reasoned review unless a technical local DLP report is supplied. Do not label it as an automated DLP scan.

## Approval gate

Approval requires the user to provide the authorized approver's identity, decision, scope, and effective time. Record it in `00-Governance/Approval Register.md`. Only then may the approved note be placed under `20-Published/` with `approval_status: approved`.

If approval is outside the chat, accept an approval record supplied by the user but label its evidence type accurately. Do not fabricate a signature or verify authority that cannot be verified.

## Withdrawal and supersession

Preserve lineage for withdrawn or superseded knowledge. Exclude it from the current published index and record the decision in the approval register and manifest.

