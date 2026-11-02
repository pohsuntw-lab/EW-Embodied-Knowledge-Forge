# Classification and routing

## Boundary question

Ask whether source body content is already visible in the current chat before asking anything about the content itself. If visible, mark it `already-visible`; the skill cannot reverse that disclosure.

## Classification guide

| Class | Indicators | Default route |
| --- | --- | --- |
| P0 Public | Already approved for public distribution | `cloud-approved` or `local-only` |
| P1 Internal | Routine internal process or training material without sensitive identifiers or competitive detail | Enterprise-approved AI or `local-only` |
| P2 Confidential | Customer/supplier identity, quote, cost, contract, operational parameter, non-public architecture, source code, detailed incident data | `cloud-sanitized` or `local-only` |
| P3 Restricted | Password, token, private key, regulated personal data, critical recipe, crown-jewel know-how, unpublished patent disclosure, security exploit detail | `local-only` |

When indicators span classes, use the highest class. Customer policy may raise a class or prohibit a route. Never lower a class merely to finish the task.

## Sanitized derivative

A P2 cloud derivative must be prepared outside the cloud chat. Remove or locally tokenize identifiers and unnecessary exact values while preserving the relationships needed for reasoning. The rehydration map remains in the enterprise environment and is never included in prompts, manifests, checkpoints, or ZIPs.

Record:

- original source ID, without embedding protected content;
- sanitization operator or system, if supplied;
- sanitization time, if supplied;
- method category;
- derivative hash, when available;
- residual-risk reviewer and decision, when supplied.

Do not call a derivative anonymous when re-identification remains possible. Prefer `sanitized` or `tokenized`.

## Route decision

Use `blocked` if any of these are unresolved:

- source owner or processing authority;
- class;
- intended audience;
- enterprise-approved AI environment;
- required sanitization evidence;
- required human reviewer.

Do not ask the user to reveal protected content to help decide whether revealing it is safe. Ask for metadata or route to a local reviewer.

