# AI Knowledge Atlas

[한국어](README.md) · English

This repository publishes the **knowledge structure and the first chapter** of AI Knowledge Book, a project to write one non-linear Korean textbook that runs from basic mathematics to AI, LLMs, agents, and harness engineering. The rest of the book is still being written in a private repository.

It contains three things:

1. **A knowledge graph and learning objectives.** 504 concepts, 603 semantic relations, 817 learning objectives, and 491 Korean terminology entries (437 general terms, 54 concept labels), together with the schemas, policies, and decision records that define them.
2. **Deterministic validators and tests.** Four standard-library Python tools that check the data against the schemas, and 159 tests.
3. **The Transformer chapter (review candidate).** An 11-section chapter, "Attention and Transformer": the main text (241 pages) and a separate detailed solutions volume (114 pages) as PDF and Markdown source, with lab code that runs on a CPU.

Most documents and the chapter are written in Korean; concept records and parts of the schemas are in English.

## Why the knowledge structure came first

When a 60-chapter book is written over many sessions, the same concept easily gets different names in different chapters, or an explanation goes on without a prerequisite. So these were fixed before the manuscript:

- **Stable node identity.** Each concept has an ID such as `K0001`, a `canonical_key`, a scope, and include/exclude boundaries. Issued IDs are never reused or renumbered; retirement and merges are kept as records ([NODE_IDENTITY.md](NODE_IDENTITY.md)).
- **A narrow set of relation types.** Concepts are linked only by defined semantic relations. Graph links alone do not decide the reading order ([SEMANTIC_EDGE_SCHEMA.md](SEMANTIC_EDGE_SCHEMA.md)).
- **Learning objectives separate from concepts.** A learning objective states what the reader can do afterwards and is grounded in concepts. Every one of the 504 concepts is covered by at least one objective ([LEARNING_OBJECTIVE_SCHEMA.md](LEARNING_OBJECTIVE_SCHEMA.md)).
- **Prerequisites as a separate contract.** Only the schema for prerequisite requirements (condition, mastery level, reason) is canonical. No prerequisite data has been admitted yet ([PREREQUISITE_REQUIREMENT_SCHEMA.md](PREREQUISITE_REQUIREMENT_SCHEMA.md)).
- **English meaning, Korean wording.** The canonical meaning of each concept is kept in English; the Korean terms used in the book are managed by a separate policy and data set ([KOREAN_AUTHORING_TERMINOLOGY_POLICY.md](KOREAN_AUTHORING_TERMINOLOGY_POLICY.md)).
- **External sources as evidence.** Technical explanations rest on external papers, textbooks, and official documentation. The registry and ontology here manage the book's scope and are never cited as evidence for technical facts ([TEXTBOOK_AUTHORING_POLICY.md](TEXTBOOK_AUTHORING_POLICY.md), [ADR 0014](decisions/0014-external-knowledge-authority-and-anti-self-reference.md)).

## Contents

| Path | Contents |
| --- | --- |
| [ONTOLOGY_V1.md](ONTOLOGY_V1.md) | Definitions of the basic objects: concepts, relations, objectives (frozen) |
| [KNOWLEDGE_GRAPH_L1.md](KNOWLEDGE_GRAPH_L1.md) | 12 navigation groupings and 60 macro areas |
| [NODE_IDENTITY.md](NODE_IDENTITY.md) · [REGISTRY_SCHEMA.md](REGISTRY_SCHEMA.md) · [SEMANTIC_EDGE_SCHEMA.md](SEMANTIC_EDGE_SCHEMA.md) | Concept IDs and lifecycle, registry records, semantic relations |
| [LEARNING_OBJECTIVE_SCHEMA.md](LEARNING_OBJECTIVE_SCHEMA.md) · [PREREQUISITE_REQUIREMENT_SCHEMA.md](PREREQUISITE_REQUIREMENT_SCHEMA.md) · [OBJECTIVE_DEPENDENCY_SCHEMA.md](OBJECTIVE_DEPENDENCY_SCHEMA.md) | Learning objectives, prerequisite requirements, dependencies between objectives |
| [PUBLICATION_STRUCTURE.md](PUBLICATION_STRUCTURE.md) · [TEXTBOOK_AUTHORING_POLICY.md](TEXTBOOK_AUTHORING_POLICY.md) · [KOREAN_AUTHORING_TERMINOLOGY_POLICY.md](KOREAN_AUTHORING_TERMINOLOGY_POLICY.md) | 12-part / 60-chapter structure, question-driven authoring policy, Korean terminology policy |
| [decisions/](decisions/README.md) | Decision records 0001–0014 behind the canonical documents |
| [registry/](registry/README.md) | `nodes.jsonl` (504 concepts), `semantic_edges.jsonl` (603 relations) |
| [learning/](learning/README.md) | `objectives.jsonl` (817 learning objectives) |
| [terminology/](terminology/README.md) | 437 Korean terms, 54 concept labels |
| [references/](references/README.md) | Bibliography policy. `bibliography.bib` is still empty; the Transformer chapter keeps its references inside the manuscript |
| `scripts/` · `tests/` | Four validators and their tests |
| [chapters/transformer/](chapters/transformer/README.md) | Transformer chapter: manuscript, PDFs, figures, labs |

## Running the checks

Only the Python 3 standard library is used (checked on Python 3.15). The validators use the `git` command and Git history, so run them inside a full (non-shallow) clone.

```bash
python3 scripts/validate_registry.py
python3 scripts/validate_semantic_edges.py
python3 scripts/validate_learning_objectives.py
python3 scripts/validate_terminology.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

Passing means the data follows the schemas and reference rules. It does not mean the concept definitions or objective statements are pedagogically right.

## Status and limits

- The knowledge structure (concepts, relations, objectives, terminology) is registered as canonical. The order of parts, chapter numbers 1–60, and section layout are not decided. The order of records and ID numbers is not a reading order.
- There are 0 prerequisite requirement records. Only the schema is canonical.
- The Transformer chapter is a **review candidate** that passed independent technical, pedagogical, and full-page reviews and a correction re-review. The author's final editorial and publication approval, and any test with real readers, have not happened.
- This is a copy taken from one point (2026-10-16) of the private development repository. Private candidates and work records that the documents pointed to were not copied. Such links were reduced to plain text, and `candidates/…` paths in the text refer to locations in the development repository.

## License

- **Code** (`scripts/`, `tests/`, and the `.py` files and lab environment files under `chapters/transformer/`): [MIT License](LICENSE)
- **Everything else** (documents, manuscript, PDFs, figures, data): [CC BY-NC-SA 4.0](LICENSE-CONTENT.md)

See [LICENSE-CONTENT.md](LICENSE-CONTENT.md) for the exact split.
