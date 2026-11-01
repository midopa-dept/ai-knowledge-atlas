#!/usr/bin/env python3
"""Learning Objective Schema v0.1의 현재 구조와 Concept grounding을 검사한다.

읽기 전용 검사다. Git 발급 이력, 의미 품질, 인간 승인과 원격 수용은 판정하지 않는다.
"""
import argparse
from pathlib import Path
import re
import sys

import validate_registry as registry
from validate_registry import ValidationError, nonempty, parse_jsonl, require

OBJECTIVES = 'learning/objectives.jsonl'
FIELDS = ('id', 'statement', 'concepts', 'status', 'retirement_reason')
REQUIRED = set(FIELDS[:4])


def identity_number(value, prefix, where):
    require(isinstance(value, str) and
            re.fullmatch(prefix + r'[0-9]{4,}', value, re.ASCII) is not None,
            where, f'{prefix} ASCII 형식이 필요하다')
    try:
        number = int(value[len(prefix):])
    except ValueError as exc:
        raise ValidationError(f'{where}: {prefix} 번호가 잘못됐다') from exc
    require(number > 0 and value == f'{prefix}{number:04d}', where,
            f'{prefix} 양수와 최소 4자리 canonical padding이 필요하다')
    return number


def validate_records(rows, nodes, source=OBJECTIVES):
    """같은 snapshot의 검증된 Concept index를 사용한다. 이력 검사는 별도다."""
    seen, previous = set(), 0
    for line, row in enumerate(rows, 1):
        where = f'{source}:{line}'
        require(REQUIRED <= row.keys(), where, '필수 field가 누락됐다')
        require(row.keys() <= set(FIELDS), where, '미지원 field가 있다')
        require(list(row) == [f for f in FIELDS if f in row], where,
                'canonical field 순서가 필요하다')
        for field in ('id', 'statement', 'status'):
            require(nonempty(row[field]), where, f'{field}: 비어 있지 않은 문자열이 필요하다')
        number = identity_number(row['id'], 'LO', where)
        require(row['id'] not in seen, where, 'LO ID 중복이다')
        require(number > previous, where, 'numeric LO 오름차순이 필요하다')
        seen.add(row['id'])
        previous = number
        require(row['status'] in {'active', 'retired'}, where, '미지원 status다')
        if row['status'] == 'active':
            require('retirement_reason' not in row, where, 'active의 retirement_reason은 금지다')
        else:
            require(nonempty(row.get('retirement_reason')), where,
                    'retired의 비어 있지 않은 retirement_reason이 필요하다')
        concepts = row['concepts']
        require(isinstance(concepts, list) and bool(concepts), where,
                'concepts: 비어 있지 않은 배열이 필요하다')
        numbers = [identity_number(k, 'K', where) for k in concepts]
        require(len(concepts) == len(set(concepts)), where, 'Concept grounding 중복이다')
        require(numbers == sorted(numbers), where, 'numeric K 오름차순이 필요하다')
        for k in concepts:
            require(k in nodes, where, f'알 수 없는 Concept {k}')
            require(nodes[k]['kind'] == 'concept', where, f'{k}: concept가 필요하다')
            if row['status'] == 'active':
                require(nodes[k]['status'] == 'active', where, f'{k}: active Concept가 필요하다')
    return len(rows)


def validate_repository(root, revision=None):
    root = Path(root)
    target = registry.git(root, 'rev-parse', '--verify', '--end-of-options',
                          f'{revision or "HEAD"}^{{commit}}').decode().strip()
    paths = (OBJECTIVES, registry.REGISTRY, registry.MACRO)
    if revision is None:
        inputs = {path: (root / path).read_bytes() for path in paths}
    else:
        inputs = {path: registry.committed_file(root, target, path) for path in paths}
        for path, data in inputs.items():
            require(data is not None, f'{target}:{path}', '검사할 파일이 없다')
    label = lambda path: f'{target}:{path}' if revision is not None else path
    nodes = registry.validate_records(
        parse_jsonl(inputs[registry.REGISTRY], label(registry.REGISTRY)),
        registry.parse_macro_areas(inputs[registry.MACRO], label(registry.MACRO)),
        label(registry.REGISTRY))
    count = validate_records(parse_jsonl(inputs[OBJECTIVES], label(OBJECTIVES)), nodes,
                             label(OBJECTIVES))
    if revision is None:
        require(registry.git(root, 'rev-parse', 'HEAD').decode().strip() == target,
                root, '검사 중 HEAD가 변경됐다')
        require(all((root / p).read_bytes() == data for p, data in inputs.items()),
                root, '검사 중 입력 bytes가 변경됐다')
    return count


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--revision', help='working tree 대신 지정한 Git commit의 구조를 검사한다')
    args = parser.parse_args(argv)
    try:
        count = validate_repository(Path(__file__).resolve().parents[1], args.revision)
    except (ValidationError, OSError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        return 1
    print(f'PASS: Learning Objective {count}개; 직렬화·field·ID·lifecycle 구조·Concept grounding.')
    print('Git 발급 이력·의미 품질·인간 승인·원격 수용은 별도 확인이 필요하다.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
