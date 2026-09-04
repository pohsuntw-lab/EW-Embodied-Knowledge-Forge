# Guided knowledge conversation

## Purpose

Help the user decide where knowledge belongs before the conversation produces another isolated file.

## Start-of-topic sequence

1. Read vault status and its configured interaction mode.
2. Search existing hubs and notes using the user's actual topic, named project, product, organization, and explicit terms.
3. Estimate routing confidence from title, aliases, project, domain, tags, and content matches.
4. Take one of three actions:

   - High confidence: announce the selected topic in one sentence and continue.
   - Ambiguous: show two or three mutually exclusive topic choices.
   - No match: ask whether to create a topic, attach it beneath a suggested parent, or keep it temporary.

Never ask the user to design folders or metadata. Translate their answer into the schema.

## During conversation

Maintain a private working map of:

- confirmed knowledge;
- proposals and assumptions;
- decisions with rationale;
- requirements and acceptance tests;
- evidence and source artifacts;
- open questions;
- tasks, owners, and deadlines;
- changes that supersede old knowledge.

Forge only durable content. Do not store greetings, repetition, frustration, or intermediate wording unless it changes a decision or requirement.

## Checkpoint triggers

Create or update notes when any of these occurs:

- the user confirms a decision;
- a stable explanation or method is completed;
- a requirement and acceptance condition are clear;
- a formal document is generated;
- the user corrects existing knowledge;
- the topic changes substantially;
- the user ends or pauses the work.

In guided-auto mode, routine writes after topic confirmation do not need repeated approval. In preview mode, show the planned note changes before writing.

## New topic question

Ask one compact question:

> 目前找不到明確對應的主題。這次內容要建立為新主題、掛到建議的既有主題下，還是暫時不存？

Offer two or three concrete choices derived from the vault. Do not present generic folders when real candidates exist.

## Relationship question

Ask only when the relationship changes meaning:

> 這項內容同時接近 A 與 B。你希望它以哪一個為主題，另一個作為相關連結？

## End-of-turn receipt

Report:

- created or updated note titles;
- target paths;
- important relationships;
- superseded versions;
- unresolved conflicts;
- whether the write was direct or packaged.
