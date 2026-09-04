# Acceptance criteria

A delivery passes only when:

- every durable note has a unique knowledge_id;
- every durable note declares project, domain, note_type, version, status, created, updated, up, related, replaces, source_refs, and tags;
- every current note has at least one valid up link;
- all internal wiki links resolve or are explicitly declared as proposed links;
- exact duplicate files are not copied into the primary reading area;
- superseded notes are marked and linked to their replacement;
- formal source files remain available as attachments when required;
- the package contains no .obsidian directory unless explicitly authorized;
- the package contains no temporary download or lock files;
- an incremental package contains only intended additions and replacements;
- the handoff reports counts, conflicts, skipped items, destination, and validation status.

Warnings are acceptable only when disclosed and caused by unavailable source material rather than a packaging defect.
