"""LO 구조 계약의 유효·무효 사례를 검사한다. 의미·발급 판정은 포함하지 않는다."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import validate_learning_objectives as v


def objective(number=1, **changes):
    row = dict(id=f'LO{number:04d}', statement='주어진 값을 계산한다.',
               concepts=['K0001'], status='active')
    row.update(changes)
    return row


def encode(rows):
    return ''.join(json.dumps(r, ensure_ascii=False, separators=(',', ':')) + '\n'
                   for r in rows).encode('utf-8')


class StructuralTests(unittest.TestCase):
    def setUp(self):
        self.nodes = {f'K{n:04d}': dict(kind='concept', status='active')
                      for n in (1, 2, 9999, 10000)}
        self.nodes['K0003'] = dict(kind='concept', status='retired')
        self.nodes['K0004'] = dict(kind='formal_object', status='active')

    def check(self, rows=None, data=None):
        return v.validate_records(v.parse_jsonl(data if data is not None else encode(rows),
                                               'fixture'), self.nodes)

    def bad(self, rows=None, data=None, rule='.'):
        with self.assertRaisesRegex(v.ValidationError, rule):
            self.check(rows, data)

    def test_numeric_order_and_gaps(self):
        self.assertEqual(self.check([objective(2), objective(9999),
                                     objective(10000, concepts=['K9999', 'K10000'])]), 3)
        self.bad([objective(10000), objective(9999)], rule='numeric LO')

    def test_duplicate_id(self):
        self.bad([objective(), objective()], rule='ID 중복')

    def test_identity_syntax(self):
        for prefix, field in [('LO', 'id'), ('K', 'concepts')]:
            for value in (prefix+'0000', prefix+'1', prefix+'00001', prefix+'０００１',
                          prefix.lower()+'0001', prefix+'0001\n', None, True, 1, {}):
                value = [value] if field == 'concepts' else value
                with self.subTest(field=field, value=value):
                    self.bad([objective(**{field: value})], rule='ASCII|padding|문자열')

    def test_required_and_unsupported_fields(self):
        for field in v.REQUIRED:
            row = objective(); del row[field]
            with self.subTest(field=field): self.bad([row], rule='필수')
        for field in ('proposal_handle', 'mastery', 'target_depth', 'prerequisites',
                      'kind', 'revision', 'terminal', 'evidence'):
            with self.subTest(field=field):
                self.bad([objective(**{field: 'x'})], rule='미지원 field')

    def test_field_order(self):
        row = objective(); row['id'] = row.pop('id')
        self.bad([row], rule='field 순서')

    def test_strings_and_status(self):
        for field in ('statement', 'status'):
            for value in ('', ' ', None, 1, True, [], {}):
                with self.subTest(field=field, value=value):
                    self.bad([objective(**{field: value})], rule='문자열')
        self.bad([objective(status='candidate')], rule='미지원 status')

    def test_grounding_array(self):
        for value in ([], None, 'K0001', {}, True):
            with self.subTest(value=value): self.bad([objective(concepts=value)], rule='배열')
        self.bad([objective(concepts=['K0001', 'K0001'])], rule='grounding 중복')
        self.bad([objective(concepts=['K0002', 'K0001'])], rule='numeric K')

    def test_endpoints(self):
        self.bad([objective(concepts=['K0005'])], rule='알 수 없는')
        self.bad([objective(concepts=['K0004'])], rule='concept가')
        self.bad([objective(concepts=['K0003'])], rule='active Concept')

    def test_retired_tombstone(self):
        self.check([objective(status='retired', concepts=['K0003'], retirement_reason='수행 대체')])
        for value in ('', ' ', None, 1):
            with self.subTest(value=value):
                self.bad([objective(status='retired', retirement_reason=value)], rule='retirement_reason')
        self.bad([objective(status='retired')], rule='retirement_reason')
        self.bad([objective(retirement_reason='x')], rule='active의')
        self.bad([objective(status='retired', concepts=['K0005'], retirement_reason='x')], rule='알 수 없는')

    def test_serialization(self):
        valid = encode([objective()])
        cases = [(b'\xef\xbb\xbf'+valid, 'BOM'), (valid.replace(b'\n', b'\r\n'), 'LF-only'),
                 (valid[:-1], 'final newline'), (valid+b'\n', 'blank record'),
                 (b'\xff\n', 'UTF-8'), (b'[]\n', 'JSON object'),
                 ((json.dumps(objective(), ensure_ascii=False)+'\n').encode(), 'compact'),
                 (valid.replace(b'"id":"LO0001"', b'"id":"LO0001","id":"LO0001"'), 'duplicate JSON'),
                 (valid.replace(b'}', b',}'), '.'), (b'//comment\n', '.'),
                 (valid.replace(b'LO0001', b'\\u004cO0001'), 'compact')]
        for data, rule in cases:
            with self.subTest(rule=rule): self.bad(data=data, rule=rule)
        for value in (b'NaN', b'Infinity', b'-Infinity'):
            with self.subTest(value=value):
                self.bad(data=valid.replace(b'"active"', value), rule='non-standard')

    def test_schema_fixtures(self):
        text = (Path(__file__).resolve().parents[1] / 'LEARNING_OBJECTIVE_SCHEMA.md').read_text()
        import re
        fixtures = re.findall(r'<!-- LO-FIXTURE (\S+) EXPECT=(\w+) CONTEXT=(\S+) -->\n```jsonl\n(.*?)\n```',
                              text, re.DOTALL)
        self.assertTrue(fixtures)
        for name, expected, context, raw in fixtures:
            with self.subTest(name=name):
                data = (Path(__file__).resolve().parents[1] / v.registry.REGISTRY).read_bytes()
                nodes = {r['id']: r for r in v.parse_jsonl(data, 'canonical Concepts')}
                if context == 'synthetic-retired-k0105': nodes['K0105']['status'] = 'retired'
                check = lambda: v.validate_records(v.parse_jsonl((raw+'\n').encode(), name), nodes)
                if expected == 'invalid':
                    with self.assertRaises(v.ValidationError): check()
                else:
                    check()  # editorial 사례는 구조상 유효하다.

    def test_working_tree_and_revision(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            git = lambda *args: v.registry.git(root, *args)
            git('init', '-q')
            git('config', 'user.name', '검증 fixture')
            git('config', 'user.email', 'fixture@example.invalid')
            git('config', 'commit.gpgsign', 'false')
            for path in (v.registry.REGISTRY, v.registry.MACRO):
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((Path(__file__).resolve().parents[1] / path).read_bytes())
            target = root / v.OBJECTIVES
            target.parent.mkdir(parents=True)
            target.write_bytes(encode([objective()]))
            git('add', '.')
            git('commit', '-qm', '구조 검증 fixture')
            self.assertEqual(v.validate_repository(root), 1)
            self.assertEqual(v.validate_repository(root, 'HEAD'), 1)
            target.write_bytes(encode([objective(concepts=['K9999'])]))
            with self.assertRaisesRegex(v.ValidationError, '알 수 없는'):
                v.validate_repository(root)
            self.assertEqual(v.validate_repository(root, 'HEAD'), 1)


if __name__ == '__main__':
    unittest.main()
