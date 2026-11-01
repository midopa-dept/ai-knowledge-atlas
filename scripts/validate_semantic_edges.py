#!/usr/bin/env python3
"""Validate current Semantic Edge Schema v0.1 structure and its Node Registry.

No writes, inference, edge-history restrictions or semantic admission decisions.
"""
import argparse
from collections import defaultdict, deque
from pathlib import Path
import re
import sys

import validate_registry as registry
from validate_registry import ValidationError, nonempty, parse_jsonl, require

GRAPH = 'registry/semantic_edges.jsonl'
FIELDS = ('source', 'relation', 'target')
RELATIONS = {'component_of', 'generalizes', 'applied_in', 'used_to_analyze',
             'motivates', 'explains', 'contrasts_with', 'mathematically_related'}
SYMMETRIC = {'contrasts_with', 'mathematically_related'}
DAGS = ('component_of', 'generalizes')


def k_number(value, where):
    require(re.fullmatch(r'K[0-9]{4,}', value, re.ASCII) is not None,
            where, 'invalid ASCII K syntax')
    try:
        number = int(value[1:])
    except ValueError as exc:
        raise ValidationError(f'{where}: invalid K number') from exc
    require(number > 0 and value == f'K{number:04d}', where,
            'positive K with canonical zero-padding required')
    return number


def validate_records(rows, nodes, source=GRAPH):
    """Validate edges against an already validated same-snapshot node index."""
    seen, symmetric_seen = set(), set()
    ordering = []
    adjacency = {relation: defaultdict(list) for relation in DAGS}
    for line, row in enumerate(rows, 1):
        where = f'{source}:{line}'
        require(set(row) == set(FIELDS), where, 'exactly source/relation/target fields required')
        require(list(row) == list(FIELDS), where, 'canonical field order required')
        for field in FIELDS:
            require(nonempty(row[field]), where, f'{field} must be a non-empty string')
        s, relation, t = (row[field] for field in FIELDS)
        sn, tn = k_number(s, where), k_number(t, where)
        require(relation in RELATIONS, where, f'unsupported relation {relation!r}')
        for endpoint in (s, t):
            require(endpoint in nodes, where, f'unknown K {endpoint}')
            require(nodes[endpoint]['kind'] == 'concept', where, f'{endpoint}: endpoint must be concept')
            require(nodes[endpoint]['status'] == 'active', where, f'{endpoint}: endpoint must be active')
        require(s != t, where, 'self-edge forbidden')
        triple = (s, relation, t)
        require(triple not in seen, where, 'exact duplicate triple')
        seen.add(triple)
        if relation in SYMMETRIC:
            require((t, relation, s) not in symmetric_seen, where, 'reverse symmetric duplicate')
            symmetric_seen.add(triple)
        ordering.append((sn, relation, tn))
        if relation in DAGS:
            adjacency[relation][s].append(t)
    # Check after duplicate detection so canonical-plus-reverse gives a specific error.
    for line, (sn, relation, tn) in enumerate(ordering, 1):
        if relation in SYMMETRIC:
            require(sn < tn, f'{source}:{line}', 'symmetric numeric orientation required')
        if line > 1:
            require(ordering[line - 2] < (sn, relation, tn), f'{source}:{line}',
                    'numeric source / ASCII relation / numeric target ascending order required')
    for relation, graph in adjacency.items():
        degree = {}
        for s, targets in graph.items():
            degree.setdefault(s, 0)
            for t in targets:
                degree[t] = degree.get(t, 0) + 1
        queue = deque(k for k, count in degree.items() if count == 0)
        visited = 0
        while queue:
            node = queue.popleft()
            visited += 1
            for target in graph.get(node, ()):
                degree[target] -= 1
                if degree[target] == 0:
                    queue.append(target)
        require(visited == len(degree), source, f'{relation} cycle forbidden')
    return len(rows)


def validate_repository(root, revision=None):
    root = Path(root)
    target = registry.git(root, 'rev-parse', '--verify', '--end-of-options',
                          f'{revision or "HEAD"}^{{commit}}').decode().strip()
    paths = (GRAPH, registry.REGISTRY, registry.MACRO)
    if revision is None:
        inputs = {path: (root / path).read_bytes() for path in paths}
    else:
        inputs = {path: registry.committed_file(root, target, path) for path in paths}
        for path, data in inputs.items():
            require(data is not None, f'{target}:{path}', 'target file missing')
    # Preserve K lifecycle/history checks without examining historical edge files.
    registry.validate_repository(root, target if revision is not None else None)
    label = lambda path: f'{target}:{path}' if revision is not None else path
    nodes = registry.validate_records(
        parse_jsonl(inputs[registry.REGISTRY], label(registry.REGISTRY)),
        registry.parse_macro_areas(inputs[registry.MACRO], label(registry.MACRO)),
        label(registry.REGISTRY))
    count = validate_records(parse_jsonl(inputs[GRAPH], label(GRAPH)), nodes, label(GRAPH))
    if revision is None:
        require(registry.git(root, 'rev-parse', 'HEAD').decode().strip() == target,
                root, 'HEAD changed during validation')
        require(all((root / path).read_bytes() == data for path, data in inputs.items()),
                root, 'working-tree input changed during validation')
    return count


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--revision', help='validate a committed tree instead of the working tree')
    args = parser.parse_args(argv)
    try:
        count = validate_repository(Path(__file__).resolve().parents[1], args.revision)
    except (ValidationError, OSError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        return 1
    print(f'PASS: {count} semantic edges; serialization, schema, endpoints, ordering and cycles; Node Registry valid.')
    print('Structural validity does not establish semantic review or canonical admission.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
