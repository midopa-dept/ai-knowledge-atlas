#!/usr/bin/env python3
"""Validate Registry Schema v0.1 and mechanically observable Git invariants.

No allocation or writes. Branch history validation does not establish issuance.
Semantic identity continuity and retirement closure require editorial review.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REGISTRY = 'registry/nodes.jsonl'
MACRO = 'KNOWLEDGE_GRAPH_L1.md'
FIELDS = ('id', 'canonical_key', 'title', 'kind', 'concept_type', 'concept_role',
          'macro_area', 'scope', 'boundary', 'aliases', 'former_keys', 'status',
          'retirement_reason')
REQUIRED = {'id', 'canonical_key', 'title', 'kind', 'macro_area', 'scope', 'status'}
KEY = re.compile(r'[a-z][a-z0-9]*(?:_[a-z0-9]+)*(?:\.[a-z][a-z0-9]*(?:_[a-z0-9]+)*)+', re.ASCII)
TYPES = {'concept', 'operation', 'mechanism', 'method', 'system', 'phenomenon', 'engineering_pattern'}
ROLES = {'atomic', 'bridge', 'integration'}


class ValidationError(ValueError):
    """A rule violation with source context."""


def require(condition, where, rule):
    if not condition:
        raise ValidationError(f'{where}: {rule}')


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def unique_members(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f'member {key!r}', 'duplicate JSON object member')
        result[key] = value
    return result


def reject_constant(value):
    raise ValidationError(f'non-standard JSON constant {value}')


def parse_jsonl(data, source):
    require(not data.startswith(b'\xef\xbb\xbf'), source, 'UTF-8 BOM forbidden')
    require(b'\r' not in data, source, 'LF-only line endings required')
    require(data.endswith(b'\n'), source, 'final newline required')
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValidationError(f'{source}: invalid UTF-8 at byte {exc.start}') from exc
    rows = []
    for line, raw in enumerate(text.split('\n')[:-1], 1):
        where = f'{source}:{line}'
        require(bool(raw.strip()), where, 'blank record forbidden')
        try:
            record = json.loads(raw, object_pairs_hook=unique_members, parse_constant=reject_constant)
        except (ValueError, RecursionError) as exc:
            raise ValidationError(f'{where}: {exc}') from exc
        require(isinstance(record, dict), where, 'one JSON object per physical line required')
        require(raw == json.dumps(record, ensure_ascii=False, separators=(',', ':')),
                where, 'canonical compact JSON with readable Unicode required')
        rows.append(record)
    return rows


def parse_macro_areas(data, source=MACRO):
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValidationError(f'{source}: invalid UTF-8') from exc
    start = '## 3. Level-1 Macro Areas'
    end = '## 4. Boundary와 Cross-Domain Connections'
    lines = text.splitlines()
    require(lines.count(start) == lines.count(end) == 1, source, 'macro section boundaries missing or ambiguous')
    begin, finish = lines.index(start), lines.index(end)
    require(begin < finish, source, 'macro section boundaries out of order')
    keys = []
    for index in range(begin + 1, finish):
        line = lines[index]
        if line.startswith('####'):
            match = re.fullmatch(r'#### ([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*) — (\S.*)', line)
            require(match is not None, f'{source}:{index + 1}', 'malformed macro-area heading')
            keys.append(match.group(1))
    require(len(keys) == len(set(keys)), source, 'duplicate macro-area key')
    require(len(keys) == 60, source, f'expected 60 current macro areas; found {len(keys)}')
    return set(keys)


def string_list(value, where, unique=False):
    require(isinstance(value, list) and bool(value), where, 'non-empty string array required')
    require(all(nonempty(item) for item in value), where, 'list entries must be non-empty strings')
    if unique:
        require(len(value) == len(set(value)), where, 'duplicate list entry')


def validate_records(rows, macros, source=REGISTRY):
    ids, keys, owners = set(), set(), {}
    previous = 0
    for line, row in enumerate(rows, 1):
        where = f'{source}:{line} [{row.get("id", "?")} / {row.get("canonical_key", "?")}]'
        require(REQUIRED <= row.keys(), where, f'missing required fields: {sorted(REQUIRED - row.keys())}')
        require(row.keys() <= set(FIELDS), where, f'unsupported fields: {sorted(row.keys() - set(FIELDS))}')
        require(list(row) == [f for f in FIELDS if f in row], where, 'canonical field order required')
        for field in REQUIRED:
            require(nonempty(row[field]), where, f'{field} must be a non-empty string')
        node_id = row['id']
        require(re.fullmatch(r'K[0-9]{4,}', node_id, re.ASCII) is not None, where, 'invalid ASCII K syntax')
        try:
            number = int(node_id[1:])
        except ValueError as exc:
            raise ValidationError(f'{where}: invalid K number') from exc
        require(number > 0 and node_id == f'K{number:04d}', where, 'positive K with canonical zero-padding required')
        require(node_id not in ids, where, 'duplicate K ID')
        require(number > previous, where, 'numeric K ascending order required')
        ids.add(node_id)
        previous = number
        key = row['canonical_key']
        require(KEY.fullmatch(key) is not None, where, 'invalid canonical-key syntax')
        require(key not in keys, where, 'duplicate canonical key')
        keys.add(key)
        require(row['kind'] == 'concept', where, 'kind must be concept')
        require(row['status'] in {'active', 'retired'}, where, 'unsupported status')
        for field, choices in [('concept_type', TYPES), ('concept_role', ROLES)]:
            if field in row:
                require(isinstance(row[field], str) and row[field] in choices, where, f'invalid {field}')
        for field in ('aliases', 'former_keys'):
            if field in row:
                string_list(row[field], f'{where} {field}', unique=True)
        former = row.get('former_keys', [])
        require(all(KEY.fullmatch(k) is not None for k in former), where, 'invalid former-key syntax')
        require(key not in former, where, 'current key duplicated in former_keys')
        for owned in [key] + former:
            require(owned not in owners or owners[owned] == node_id, where, f'key {owned!r} belongs to another K')
            owners[owned] = node_id
        if 'boundary' in row:
            boundary = row['boundary']
            require(isinstance(boundary, dict) and bool(boundary), where, 'boundary must be a non-empty object')
            require(boundary.keys() <= {'includes', 'excludes'}, where, 'unsupported boundary member')
            require(list(boundary) == [f for f in ('includes', 'excludes') if f in boundary], where, 'boundary member order required')
            for field, value in boundary.items():
                string_list(value, f'{where} boundary.{field}')
        if row['status'] == 'active':
            require(row['macro_area'] in macros, where, 'active macro_area is not current')
            require('retirement_reason' not in row, where, 'active retirement_reason forbidden')
        else:
            require(nonempty(row.get('retirement_reason')), where, 'retired retirement_reason required and non-empty')
    return {row['id']: row for row in rows}


def validate_history(current, history, source=REGISTRY):
    """Compare one snapshot with strict ancestor snapshots (label, ID map).

    A working tree uses HEAD and all its ancestors. Missing historical snapshots
    are empty maps, so deletion of the whole file is detected as well.
    """
    past_ids, canonical, owners, retired = set(), {}, {}, {}
    for label, snapshot in history:
        for node_id, row in snapshot.items():
            past_ids.add(node_id)
            canonical.setdefault(node_id, set()).add(row['canonical_key'])
            for key in [row['canonical_key']] + row.get('former_keys', []):
                require(key not in owners or owners[key][0] == node_id, source,
                        f'historical key {key!r} has conflicting K owners at {label}')
                owners[key] = (node_id, label)
            if row['status'] == 'retired':
                if node_id in retired:
                    require(retired[node_id][0] == row['macro_area'], source,
                            f'{node_id}: conflicting retired home at {label}')
                retired[node_id] = (row['macro_area'], label)
    missing = past_ids - current.keys()
    require(not missing, source, f'issued/committed K deletion: {sorted(missing)}')
    maximum = max((int(k[1:]) for k in past_ids), default=0)
    for line, (node_id, row) in enumerate(current.items(), 1):
        where = f'{source}:{line} [{node_id} / {row["canonical_key"]}]'
        if node_id not in past_ids:
            require(int(node_id[1:]) > maximum, where, f'new K must exceed historical max {maximum}; gap backfill forbidden')
        if node_id in retired:
            home, label = retired[node_id]
            require(row['status'] == 'retired', where, f'retired K resurrection forbidden; retired at {label}')
            require(row['macro_area'] == home, where, f'retired home changed from {home} at {label}')
        expected = canonical.get(node_id, set()) - {row['canonical_key']}
        actual = set(row.get('former_keys', []))
        require(expected <= actual, where, f'rename missing historical former_keys: {sorted(expected - actual)}')
        require(actual <= expected, where, f'former_keys lack actual same-K canonical history: {sorted(actual - expected)}')
        for key in [row['canonical_key']] + row.get('former_keys', []):
            if key in owners:
                owner, label = owners[key]
                require(owner == node_id, where, f'historical key {key!r} reserved by {owner} at {label}')


def git(root, *args):
    result = subprocess.run(['git', '-C', str(root), *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        raise ValidationError(f'Git {args[0]} failed: {result.stderr.decode("utf-8", errors="replace").strip()}')
    return result.stdout


def committed_file(root, revision, path):
    exists = git(root, 'ls-tree', '--name-only', revision, '--', path)
    if not exists.strip():
        return None
    return git(root, 'show', f'{revision}:{path}')


def validate_repository(root, revision=None):
    root = Path(root)
    require(git(root, 'rev-parse', '--is-shallow-repository').strip() == b'false', root,
            'complete Git history required; shallow repository unsupported')
    target = git(root, 'rev-parse', '--verify', '--end-of-options', f'{revision or "HEAD"}^{{commit}}').decode().strip()
    lines = git(root, 'rev-list', '--reverse', '--topo-order', '--parents', target).decode().splitlines()
    ancestors, snapshots, introductions = {}, {}, {}
    for entry in lines:
        commit, *parents = entry.split()
        prior = set()
        for parent in parents:
            prior.add(parent)
            prior.update(ancestors[parent])
        ancestors[commit] = prior
        data = committed_file(root, commit, REGISTRY)
        source = f'{commit}:{REGISTRY}'
        if data is None:
            snapshot = {}
        else:
            macro = committed_file(root, commit, MACRO)
            require(macro is not None, source, 'historical macro authority missing')
            snapshot = validate_records(parse_jsonl(data, source), parse_macro_areas(macro, f'{commit}:{MACRO}'), source)
        history = [(c, snapshots[c]) for c in snapshots if c in prior]
        validate_history(snapshot, history, source)
        previous_ids = {k for _, old in history for k in old}
        for node_id in snapshot.keys() - previous_ids:
            require(node_id not in introductions, source,
                    f'{node_id}: independent branch K reuse; earlier introduction {introductions.get(node_id)}')
            introductions[node_id] = commit
        snapshots[commit] = snapshot
    if revision is not None:
        require(committed_file(root, target, REGISTRY) is not None, f'{target}:{REGISTRY}', 'target registry missing')
        current = snapshots[target]
    else:
        try:
            data = (root / REGISTRY).read_bytes()
            macro = (root / MACRO).read_bytes()
        except OSError as exc:
            raise ValidationError(f'{root}: target file read failed: {exc}') from exc
        current = validate_records(parse_jsonl(data, REGISTRY), parse_macro_areas(macro), REGISTRY)
        validate_history(current, list(snapshots.items()), REGISTRY)
    return len(current), len(snapshots)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--revision', help='validate a committed tree instead of the working tree')
    args = parser.parse_args(argv)
    try:
        root = Path(__file__).resolve().parents[1]
        count, commits = validate_repository(root, args.revision)
    except (ValidationError, OSError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        return 1
    print(f'PASS: {count} records; schema, serialization, identity and history ({commits} commits).')
    print('Semantic continuity and retirement closure require review; this is not an issuance operation.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
