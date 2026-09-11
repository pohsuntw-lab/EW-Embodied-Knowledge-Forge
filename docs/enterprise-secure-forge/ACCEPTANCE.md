# EW Enterprise Secure Knowledge Forge — Acceptance

Version: 0.5.0

## A. Invocation and boundary

- A1: An enterprise knowledge-forging request selects the enterprise skill rather than the personal skill.
- A2: The first response warns the user not to upload source content before classification.
- A3: If content is already attached or pasted, the skill states that its checks cannot retroactively prevent disclosure.
- A4: The skill never claims to be technical DLP, encryption, access control, or compliance certification.

## B. Classification and routing

- B1: Every selected source has a stable source ID and P0–P3 class before substantive forging.
- B2: P0 defaults to approved cloud or local processing.
- B3: P1 requires an enterprise-approved AI environment or local processing.
- B4: P2 requires a sanitized derivative produced locally or a local-only route.
- B5: P3 never triggers a request to upload body content and is routed local-only.
- B6: Unknown classification or approval produces `blocked`, not an optimistic default.

## C. Knowledge lifecycle

- C1: Unapproved notes remain under `10-Candidates/`.
- C2: Publication requires a named authorized approver and recorded approval time.
- C3: Approved notes under `20-Published/` retain source IDs and security metadata.
- C4: Different audiences are not mixed into one package merely because Markdown links can connect them.
- C5: Revoked or superseded knowledge is traceable and excluded from the current published index.

## D. Package controls

- D1: Every package contains the three governance registers and `FORGE-MANIFEST.json`.
- D2: No `.obsidian`, executable, credential, private-key, temporary, or absolute-path payload is packaged.
- D3: Rehydration maps and original P2/P3 files are never included in cloud-produced packages.
- D4: Existing graph, checkpoint, and ZIP integrity validators still pass.
- D5: Enterprise validator exits nonzero for prohibited files, representative credential patterns, cloud-routed P3 content, or unapproved published notes.

## E. Release

- E1: The plugin manifest lists both skills through `./skills/` and uses version `0.5.0`.
- E2: Submission listing, starter prompts, privacy policy, terms, test cases, and release notes describe the security boundary consistently.
- E3: `npm run check` passes.
- E4: A ChatGPT release ZIP is generated and contains both skill folders.
- E5: GitHub is updated before any ChatGPT Platform upload.

