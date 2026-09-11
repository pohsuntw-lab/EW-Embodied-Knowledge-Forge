# AGENTS.md — Enterprise Secure Forge v0.5.0

## Scope

Implement the enterprise skill inside the existing `ew-obsidian-knowledge-forge` plugin. Preserve the personal skill and its behavior unless a shared release or validation change is necessary.

## Non-negotiable rules

- Never describe the ChatGPT skill as pre-upload technical DLP.
- Classification happens before requesting source body content.
- P3 is local-only. P2 is local-only or uses a locally sanitized derivative.
- Already-visible content receives a non-retroactivity warning.
- No generated approval identities, times, policy decisions, or compliance claims.
- No candidate note enters `20-Published/` without explicit human approval.
- Do not package secrets, token maps, `.obsidian`, executables, or absolute local paths.
- Preserve the existing full-fidelity, checkpoint, graph, and ZIP invariants.

## Commands

```bash
npm run check
python3 /root/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/ew-obsidian-knowledge-forge/skills/enterprise-secure-knowledge-forge
python3 /root/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/ew-obsidian-knowledge-forge
npm run release
```

## Definition of done

- Five specifications agree.
- Both skills validate.
- Enterprise validator has positive and negative tests.
- Submission and legal materials state the same limits.
- Release ZIP includes both skills and no forbidden payload.
- GitHub commit is pushed and verified before ChatGPT Platform publication.

## Stop conditions

Stop before weakening P2/P3 routing, changing public access, adding an external server, using real enterprise secrets in tests, or publishing to ChatGPT without the user's authorization.

