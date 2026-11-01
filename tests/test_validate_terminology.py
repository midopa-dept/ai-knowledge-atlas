"""Terminology structure and snapshot tests; Git writes use temporary repos."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import validate_terminology as v


def encode(rows):
    return ''.join(json.dumps(r, ensure_ascii=False, separators=(',', ':')) + '\n' for r in rows).encode()


def record(general=False, display='ko_en_first', **changes):
    row = {'term_key': 'example.term', 'english': 'example'} if general else {'concept_id': 'K0001'}
    if display in v.KOREAN:
        row['preferred_ko'] = '용어'
    row['display_policy'] = display
    if display in v.ACRONYM:
        row['acronym'] = 'EX'
    row.update(changes)
    fields = v.TERM_FIELDS if general else v.CONCEPT_FIELDS
    return {k: row[k] for k in fields if k in row} | {k: val for k, val in row.items() if k not in fields}


class StructuralTests(unittest.TestCase):
    def setUp(self):
        self.nodes = {f'K{n:04d}': {'kind': 'concept', 'status': 'active'} for n in (1, 2, 9999, 10000)}

    def check(self, rows=None, data=None, general=False):
        return v.validate_records(v.parse_jsonl(data if data is not None else encode(rows), 'fixture'),
                                  self.nodes, 'fixture', general=general)

    def bad(self, rows=None, data=None, general=False, rule='.'):
        with self.assertRaisesRegex(v.ValidationError, rule):
            self.check(rows, data, general)

    def test_all_displays(self):
        for general in (False, True):
            for display in sorted(v.DISPLAYS):
                with self.subTest(general=general, display=display):
                    self.check([record(general, display)], general=general)

    def test_optional_notes_and_avoid(self):
        for general in (False, True):
            note = 'context_note' if general else 'note'
            for extras in ({note: 'Reason'}, {note: 'Reason', 'avoid_ko': ['A', '가']}):
                with self.subTest(general=general, extras=extras):
                    self.check([record(general, **extras)], general=general)

    def test_repeated_english_valid(self):
        self.check([record(True, context_note='First sense'), record(True, term_key='example.two', context_note='Second sense')], general=True)

    def test_repeated_english_missing_context(self):
        self.bad([record(True, context_note='First sense'), record(True, term_key='example.two')], general=True, rule='repeated English')

    def test_korean_collision_allowed(self):
        self.check([record(), record(concept_id='K0002')])
        self.check([record(True), record(True, term_key='example.two', english='other')], general=True)

    def test_numeric_k_order(self):
        self.check([record(concept_id='K9999'), record(concept_id='K10000')])
        self.bad([record(concept_id='K10000'), record(concept_id='K9999')], rule='ascending')

    def test_invalid_k(self):
        for key in ('K0', 'K0000', 'K00001', 'K１000', 'k0001', 'K-001'):
            with self.subTest(key=key): self.bad([record(concept_id=key)])

    def test_unknown_k(self): self.bad([record(concept_id='K0003')], rule='unknown K')
    def test_duplicate_k(self): self.bad([record(), record()], rule='duplicate')

    def test_retired_k(self):
        self.nodes['K0001']['status'] = 'retired'
        self.bad([record()], rule='active')

    def test_nonconcept_k(self):
        self.nodes['K0001']['kind'] = 'notation'
        self.bad([record()], rule='concept')

    def test_term_key_syntax(self):
        for key in ('single', 'Example.term', 'a..b', 'a.b-c', 'a.한글', '1a.b'):
            with self.subTest(key=key): self.bad([record(True, term_key=key)], general=True, rule='term_key')
        # Policy regex intentionally permits consecutive and trailing underscores.
        self.check([record(True, term_key='a__.b_')], general=True)

    def test_duplicate_term_key(self): self.bad([record(True), record(True)], general=True, rule='duplicate')
    def test_term_sort(self): self.bad([record(True, term_key='z.a'), record(True)], general=True, rule='ascending')

    def test_required_fields(self):
        for general, fields in ((False, ('concept_id', 'display_policy')), (True, ('term_key', 'english', 'display_policy'))):
            for field in fields:
                row = record(general); del row[field]
                with self.subTest(field=field): self.bad([row], general=general, rule='required')

    def test_unknown_display(self): self.bad([record(display='unknown')], rule='display_policy')

    def test_conditional_fields(self):
        for general in (False, True):
            for display in sorted(v.DISPLAYS):
                for field in ('preferred_ko', 'acronym'):
                    row = record(general, display)
                    if field in row: del row[field]
                    else: row = record(general, display, **{field: 'Unexpected'})
                    with self.subTest(general=general, display=display, field=field):
                        self.bad([row], general=general, rule=field)

    def test_avoid_errors(self):
        for general in (False, True):
            note = 'context_note' if general else 'note'
            for avoided in ([], ['a', 'a'], ['나', '가'], ['용어'], [1], [None], [''], [' a'], 'a', None):
                with self.subTest(general=general, avoided=avoided):
                    self.bad([record(general, avoid_ko=avoided, **{note: 'Reason'})], general=general, rule='avoid_ko')
            self.bad([record(general, avoid_ko=['가'])], general=general, rule=note)

    def test_string_types_and_whitespace(self):
        for general in (False, True):
            base = record(general, 'ko_acronym_first', **{('context_note' if general else 'note'): 'Reason'})
            for field in base:
                for value in ('', ' ', ' x', 'x ', None, 1, True, [], {}):
                    row = dict(base); row[field] = value
                    with self.subTest(general=general, field=field, value=value):
                        self.bad([row], general=general, rule='string')

    def test_field_order(self): self.bad([dict(reversed(list(record().items())))], rule='field order')
    def test_unknown_field(self): self.bad([record(status='active')], rule='unknown field')

    def test_json_errors(self):
        data = encode([record()])
        cases = {'utf8': b'\xff\n', 'bom': b'\xef\xbb\xbf' + data, 'crlf': data.replace(b'\n', b'\r\n'),
                 'newline': data[:-1], 'blank': data + b'\n', 'empty': b'', 'object': b'[]\n',
                 'trailing comma': data.replace(b'}', b',}'), 'comment': b'// comment\n',
                 'duplicate': data.replace(b'"concept_id":', b'"concept_id":"K0001","concept_id":'),
                 'compact': data.replace(b':', b': ', 1), 'unicode': json.dumps(record()).encode() + b'\n'}
        for constant in ('NaN', 'Infinity', '-Infinity'):
            cases[constant] = ('{"note":' + constant + '}\n').encode()
        for name, raw in cases.items():
            with self.subTest(name=name): self.bad(data=raw)


class RepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git('init', '-q')
        self.git('config', 'user.name', 'Fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        for path in (v.registry.MACRO,): self.write(path, (SCRIPTS.parent / path).read_bytes())
        node = dict(id='K0001', canonical_key='example.node', title='Example', kind='concept', macro_area='MATH-FOUND', scope='Example scope.', status='active')
        self.write(v.registry.REGISTRY, encode([node]))
        self.write(v.CONCEPTS, encode([record()]))
        self.write(v.TERMS, encode([record(True), record(True, term_key='example.two', english='other')]))
        for name in ('validate_registry.py', 'validate_semantic_edges.py', 'validate_terminology.py'):
            self.write('scripts/' + name, (SCRIPTS / name).read_bytes())
        self.commit()

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.root), *args], stderr=subprocess.PIPE)

    def write(self, path, data):
        p = self.root / path; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(data)

    def commit(self):
        self.git('add', '.'); self.git('commit', '-qm', 'Fixture')

    def test_working_and_revision(self):
        self.assertEqual(v.validate_repository(self.root), (1, 2))
        self.assertEqual(v.validate_repository(self.root, 'HEAD'), (1, 2))
        self.write(v.CONCEPTS, b'bad\n')
        with self.assertRaises(v.ValidationError): v.validate_repository(self.root)
        self.assertEqual(v.validate_repository(self.root, 'HEAD'), (1, 2))

    def test_same_revision_registry(self):
        data = (self.root / v.registry.REGISTRY).read_bytes().replace(b'"active"', b'"retired","retirement_reason":"Ended"')
        self.write(v.registry.REGISTRY, data)
        with self.assertRaises(v.ValidationError): v.validate_repository(self.root)
        self.assertEqual(v.validate_repository(self.root, 'HEAD'), (1, 2))
        self.commit()
        with self.assertRaises(v.ValidationError): v.validate_repository(self.root, 'HEAD')

    def test_deletion_and_readdition(self):
        original = (self.root / v.TERMS).read_bytes()
        self.write(v.TERMS, encode([record(True)])); self.commit()
        self.assertEqual(v.validate_repository(self.root, 'HEAD'), (1, 1))
        self.write(v.TERMS, original); self.commit()
        self.assertEqual(v.validate_repository(self.root, 'HEAD'), (1, 2))

    def test_missing_files(self):
        for path in (v.CONCEPTS, v.TERMS):
            with self.subTest(path=path):
                original = (self.root / path).read_bytes(); (self.root / path).unlink()
                with self.assertRaises(OSError): v.validate_repository(self.root)
                self.commit()
                with self.assertRaisesRegex(v.ValidationError, 'missing'): v.validate_repository(self.root, 'HEAD')
                self.write(path, original); self.commit()

    def test_invalid_revision(self):
        with self.assertRaises(v.ValidationError): v.validate_repository(self.root, 'no-such-revision')

    def test_input_change(self):
        original = v.registry.validate_repository
        def changed(*args):
            result = original(*args)
            self.write(v.TERMS, encode([record(True)]))
            return result
        with patch.object(v.registry, 'validate_repository', side_effect=changed):
            with self.assertRaisesRegex(v.ValidationError, 'input changed'): v.validate_repository(self.root)

    def test_head_change(self):
        original = v.registry.validate_repository
        def changed(*args):
            result = original(*args)
            self.git('commit', '--allow-empty', '-qm', 'Changed HEAD')
            return result
        with patch.object(v.registry, 'validate_repository', side_effect=changed):
            with self.assertRaisesRegex(v.ValidationError, 'HEAD changed'): v.validate_repository(self.root)

    def test_cli(self):
        command = [sys.executable, '-B', str(self.root / 'scripts/validate_terminology.py')]
        for args in ([], ['--revision', 'HEAD']):
            result = subprocess.run(command + args, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('PASS: 1 Concept labels; 2 general terms', result.stdout)
        self.write(v.TERMS, b'bad\n')
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('FAIL:', result.stderr)


if __name__ == '__main__':
    unittest.main()
