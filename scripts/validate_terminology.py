#!/usr/bin/env python3
"""Validate current Korean terminology structure against Policy v0.1.

No writes, terminology-history restrictions, translation or semantic review.
"""
import argparse
from collections import defaultdict
from pathlib import Path
import re
import sys

import validate_registry as registry
from validate_registry import ValidationError, parse_jsonl, require
from validate_semantic_edges import k_number

CONCEPTS = 'terminology/concept_labels.jsonl'
TERMS = 'terminology/terms.jsonl'
CONCEPT_FIELDS = ('concept_id', 'preferred_ko', 'display_policy', 'acronym', 'avoid_ko', 'note')
TERM_FIELDS = ('term_key', 'english', 'preferred_ko', 'display_policy', 'acronym', 'avoid_ko', 'context_note')
TERM_KEY = re.compile(r'[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)+', re.ASCII)
DISPLAYS = {'ko', 'ko_en_first', 'english', 'acronym', 'ko_acronym_first'}
KOREAN = {'ko', 'ko_en_first', 'ko_acronym_first'}
ACRONYM = {'acronym', 'ko_acronym_first'}


def clean_string(value):
    return isinstance(value, str) and bool(value) and value == value.strip()


def validate_records(rows, nodes, source=CONCEPTS, *, general=False):
    """Validate one current terminology file using a validated node index."""
    fields = TERM_FIELDS if general else CONCEPT_FIELDS
    identity = 'term_key' if general else 'concept_id'
    note = 'context_note' if general else 'note'
    required = {identity, 'display_policy'} | ({'english'} if general else set())
    seen, ordering, surfaces = set(), [], defaultdict(list)
    for line, row in enumerate(rows, 1):
        where = f'{source}:{line}'
        require(required <= row.keys(), where, 'missing required fields')
        require(row.keys() <= set(fields), where, 'unknown field')
        require(list(row) == [f for f in fields if f in row], where, 'canonical field order required')
        for field, value in row.items():
            if field != 'avoid_ko':
                require(clean_string(value), where, f'{field}: non-empty string without surrounding whitespace required')
        key = row[identity]
        if general:
            require(TERM_KEY.fullmatch(key) is not None, where, 'invalid term_key syntax')
            order = key
            surfaces[row['english']].append((where, row))
        else:
            order = k_number(key, where)
            require(key in nodes, where, f'unknown K {key}')
            require(nodes[key]['kind'] == 'concept', where, 'endpoint must be concept')
            require(nodes[key]['status'] == 'active', where, 'endpoint must be active')
        require(key not in seen, where, f'duplicate {identity}')
        seen.add(key)
        ordering.append(order)
        display = row['display_policy']
        require(display in DISPLAYS, where, 'unknown display_policy')
        require(('preferred_ko' in row) == (display in KOREAN), where, 'preferred_ko conditional presence violated')
        require(('acronym' in row) == (display in ACRONYM), where, 'acronym conditional presence violated')
        if 'avoid_ko' in row:
            avoided = row['avoid_ko']
            require(isinstance(avoided, list) and bool(avoided), where, 'avoid_ko: non-empty array required')
            require(all(clean_string(v) for v in avoided), where, 'avoid_ko: non-empty strings without surrounding whitespace required')
            require(len(set(avoided)) == len(avoided), where, 'avoid_ko: duplicate value')
            require(avoided == sorted(avoided), where, 'avoid_ko: Unicode code-point ascending order required')
            require(row.get('preferred_ko') not in avoided, where, 'avoid_ko contains preferred_ko')
            require(note in row, where, f'{note} required with avoid_ko')
    require(ordering == sorted(ordering), source, 'physical records must be in ascending order')
    for surface, entries in surfaces.items():
        if len(entries) > 1:
            for where, row in entries:
                require('context_note' in row, where, f'context_note required for repeated English surface {surface!r}')
    return len(rows)


def validate_repository(root, revision=None):
    root = Path(root)
    target = registry.git(root, 'rev-parse', '--verify', '--end-of-options',
                          f'{revision or "HEAD"}^{{commit}}').decode().strip()
    paths = (CONCEPTS, TERMS, registry.REGISTRY, registry.MACRO)
    if revision is None:
        inputs = {path: (root / path).read_bytes() for path in paths}
    else:
        inputs = {path: registry.committed_file(root, target, path) for path in paths}
        for path, data in inputs.items():
            require(data is not None, f'{target}:{path}', 'target file missing')
    # K lifecycle belongs to the Registry; terminology snapshots have no lifecycle checks.
    registry.validate_repository(root, target if revision is not None else None)
    label = lambda path: f'{target}:{path}' if revision is not None else path
    nodes = registry.validate_records(
        parse_jsonl(inputs[registry.REGISTRY], label(registry.REGISTRY)),
        registry.parse_macro_areas(inputs[registry.MACRO], label(registry.MACRO)),
        label(registry.REGISTRY))
    counts = tuple(validate_records(parse_jsonl(inputs[path], label(path)), nodes,
                                    label(path), general=path == TERMS)
                   for path in (CONCEPTS, TERMS))
    if revision is None:
        require(registry.git(root, 'rev-parse', 'HEAD').decode().strip() == target,
                root, 'HEAD changed during validation')
        require(all((root / path).read_bytes() == data for path, data in inputs.items()),
                root, 'working-tree input changed during validation')
    return counts


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--revision', help='validate a committed tree instead of the working tree')
    args = parser.parse_args(argv)
    try:
        concepts, terms = validate_repository(Path(__file__).resolve().parents[1], args.revision)
    except (ValidationError, OSError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        return 1
    print(f'PASS: {concepts} Concept labels; {terms} general terms; {concepts + terms} total; '
          'serialization, schema, endpoints, conditional fields, sorting and context rules; Node Registry valid.')
    print('Structural validity does not establish semantic review or canonical admission.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
