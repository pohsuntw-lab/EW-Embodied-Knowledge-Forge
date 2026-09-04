# Full-fidelity completeness standard

Use this standard for every document corpus or long conversation unless the user explicitly requests summary-only output.

## User-selected compression level

Obtain one explicit choice before file generation:

| Level | Target reduction | Intended result |
| --- | ---: | --- |
| A — Full preservation | 0–10% | Complete usable detail; remove only noise and duplication |
| B — Balanced organization | 20–35% | Shorter reading with core detail, evidence, conditions, and exceptions intact |
| C — High condensation | 50–65% | Compact operational knowledge with provenance and critical safeguards intact |

The percentage is an auditable target range, not a promise of exact character counts. Estimate it from readable source text versus packaged readable text, excluding YAML and navigation boilerplate. Record the selected level, estimated result, and any reason the target could not be met.

## Required preservation

Create a source register before synthesis. For every selected source, record its name, type, processing status, destination note or notes, and any limitation. Coverage must be 100% of selected sources; every skipped source needs a visible reason.

For each source, preserve all applicable:

- definitions and distinctions;
- claims, rationale, and supporting evidence;
- requirements, rules, constraints, and prohibitions;
- procedures, sequence, inputs, outputs, roles, and handoffs;
- conditions, thresholds, exceptions, failure modes, and recovery paths;
- examples, measurements, acceptance criteria, and limitations;
- decisions, disputes, assumptions, and open questions;
- provenance, version, and source references.

## Anti-overcompression gates

A package fails validation when any of these is true:

1. A selected source appears only as a filename, heading list, or one-paragraph abstract.
2. A hub or MOC is the only representation of substantive source material.
3. A long source has neither a readable full-text source note nor multiple substantive notes that collectively preserve its usable content.
4. A note asserts a conclusion while dropping the source's conditions, exceptions, evidence, or uncertainty.
5. Source coverage is below 100% without an explicit user-approved exclusion.

For sources longer than roughly 1,500 words, prefer one full-text source note plus linked semantic notes. Full text is an evidence layer; semantic notes are the reusable knowledge layer. Include both when feasible.

## Large corpus volumes

When one ZIP or one pass would risk truncation, use complete-project mode and split the Vault into numbered ZIP volumes. Every volume must contain the same top-level Vault folder name. Put shared root files in Part00, keep all other paths unique, and include:

- `分卷ZIP安裝與合併說明.md`;
- a list of all required volumes and their order;
- the exact common extraction destination;
- a final expected Markdown note count;
- a warning not to open each volume as a separate Vault.

Coverage is cumulative across checkpoints, not inferred from conversation memory. Every completed batch must update `FORGE-CHECKPOINT.md`. A source is not processed until its notes and ZIP pass validation. The final coverage calculation must use the checkpoint source register and must not silently omit historical conversations the active chat cannot access.

The checkpoint itself is not a substitute for substantive notes. Keep it compact: stable identities, statuses, paths, counts, volume filenames, conflicts, and the next action only.

## Completion receipt

Report selected compression level and target, estimated achieved reduction, mode, selected sources, processed sources, deferred and skipped sources, full-text source notes, synthesized knowledge notes, total Markdown notes, current and cumulative volume counts, checkpoint revision, graph validation, checkpoint validation, ZIP integrity, and unresolved limitations. Do not call a batch or project complete if these checks are unknown.
