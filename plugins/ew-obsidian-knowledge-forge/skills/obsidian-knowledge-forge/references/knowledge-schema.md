# Knowledge note schema

Use YAML properties on durable notes. Keep property names in English for stable queries; content and titles may use the user's language.

## Required properties

    ---
    knowledge_id: project-domain-slug
    title: Human-readable title
    project: Project name
    domain: Domain or subsystem
    note_type: concept
    version: 1.0.0
    status: current
    created: 2026-09-04
    updated: 2026-09-04
    up:
      - "[[Path/Parent hub]]"
    related: []
    replaces: []
    source_refs: []
    tags:
      - project/example
    ---

## Controlled values

**note_type**

- concept
- decision
- requirement
- evidence
- process
- project
- task
- reference
- person
- organization

**status**

- draft
- proposed
- current
- superseded
- archived
- disputed

## Identity and version rules

- knowledge_id is stable across filename changes.
- A changed title does not create a new identity.
- Minor wording corrections update the existing note and patch version.
- New compatible detail increments the minor version.
- A breaking conceptual or contractual change increments the major version.
- When one note replaces another, the new note lists the old note under replaces; the old note becomes superseded.
- Never infer that a later modification date means a document is authoritative. Use explicit version evidence and user decisions.

## Relationship rules

- up: parent topic, project hub, or area map.
- related: useful lateral relationship supported by content.
- replaces: earlier notes made obsolete by this note.
- source_refs: conversation note, attachment, URL, meeting, or document supporting the content.
- A link is not evidence by itself. Explain important relationships in the body.

## Suggested body

    # Title

    ## Summary

    ## Durable knowledge

    ## Decisions or requirements

    ## Relationships

    ## Open questions

    ## Sources

Use only the sections the note needs.
