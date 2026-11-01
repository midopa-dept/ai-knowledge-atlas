"""Schema and history regression tests; all Git mutations use temporary repos."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'validate_registry.py'
spec = importlib.util.spec_from_file_location('validate_registry', SCRIPT)
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
MACRO_BYTES = (SCRIPT.parents[1] / v.MACRO).read_bytes()
MACROS = v.parse_macro_areas(MACRO_BYTES)


def record(**changes):
    row = dict(id='K0001', canonical_key='example.original', title='Example', kind='concept',
               macro_area='MATH-FOUND', scope='A coherent example scope.', status='active')
    row.update(changes)
    return {key: row[key] for key in v.FIELDS if key in row}


def encode(rows):
    return (''.join(json.dumps(r, ensure_ascii=False, separators=(',', ':')) + '\n' for r in rows)).encode()


def index(rows):
    return {r['id']: r for r in rows}


class SnapshotTests(unittest.TestCase):
    def check(self, rows=None, data=None):
        return v.validate_records(v.parse_jsonl(data if data is not None else encode(rows), 'fixture.jsonl'), MACROS, 'fixture.jsonl')

    def bad(self, rows=None, data=None, rule=None):
        with self.assertRaisesRegex(v.ValidationError, rule or '.'):
            self.check(rows, data)

    def test_valid_minimal_active(self):
        self.check([record()])

    def test_valid_optional_boundary(self):
        self.check([record(boundary={'includes': ['One'], 'excludes': ['Two']})])
        self.check([record(boundary={'excludes': ['Two']})])

    def test_valid_optional_classifications_aliases(self):
        self.check([record(concept_type='method', concept_role='bridge', aliases=['Example method'])])

    def test_valid_retired_noncurrent_home_and_open_reason(self):
        self.check([record(status='retired', macro_area='OLD-HOME', retirement_reason='reviewed_custom_reason')])

    def test_title_alias_need_not_be_globally_unique(self):
        self.check([record(aliases=['shared']), record(id='K0002', canonical_key='example.second', aliases=['shared'])])

    def test_valid_numeric_order_and_gap(self):
        self.check([record(id='K9999'), record(id='K10000', canonical_key='example.second')])
        self.check([record(), record(id='K0003', canonical_key='example.third')])

    def test_invalid_k_zero(self):
        self.bad([record(id='K0000')], rule='positive K')

    def test_invalid_k_padding(self):
        for value in ['K00001', 'K00000', 'K001', 'K０００１', 'K0001\n']:
            with self.subTest(value=value): self.bad([record(id=value)])

    def test_duplicate_k(self):
        self.bad([record(), record(canonical_key='example.second')], rule='duplicate K')

    def test_numeric_order_violation(self):
        self.bad([record(id='K10000'), record(id='K9999', canonical_key='example.second')], rule='ascending')

    def test_duplicate_key(self):
        self.bad([record(), record(id='K0002')], rule='duplicate canonical key')

    def test_key_syntax(self):
        for key in ['Single', 'a', 'a..b', 'a._b', 'a.b_', 'a.b__c', 'a.b-c', 'a.2b', 'a.b\n', 'a.é']:
            with self.subTest(key=key): self.bad([record(canonical_key=key)], rule='syntax')

    def test_valid_semantic_digits_in_key(self):
        self.check([record(canonical_key='example.model2_v3')])

    def test_noncurrent_active_macro(self):
        self.bad([record(macro_area='OLD-HOME')], rule='not current')

    def test_active_retirement_reason(self):
        self.bad([record(retirement_reason='duplicate')], rule='forbidden')

    def test_retired_without_reason(self):
        self.bad([record(status='retired')], rule='retirement_reason')

    def test_unknown_field(self):
        row = record(); row['source_candidates'] = ['candidate.handle']
        self.bad([row], rule='unsupported fields')

    def test_required_fields(self):
        for field in v.REQUIRED:
            row = record(); del row[field]
            with self.subTest(field=field): self.bad([row], rule='missing required')

    def test_empty_and_wrong_required_types(self):
        for field in v.REQUIRED:
            for value in [None, '', '  ', [], 1, True]:
                with self.subTest(field=field, value=value): self.bad([record(**{field: value})])

    def test_invalid_enums(self):
        for field, value in [('kind', 'formal_object'), ('status', 'candidate'), ('concept_type', 'unknown'), ('concept_role', 'medium'), ('concept_type', [])]:
            with self.subTest(field=field): self.bad([record(**{field: value})])

    def test_optional_list_structure(self):
        for field in ['aliases', 'former_keys']:
            for value in [None, [], '', [''], [' '], [1], ['a.b', 'a.b']]:
                with self.subTest(field=field, value=value): self.bad([record(**{field: value})])

    def test_invalid_former_key(self):
        self.bad([record(former_keys=['not-valid'])], rule='former-key syntax')

    def test_current_key_in_former(self):
        self.bad([record(former_keys=['example.original'])], rule='current key duplicated')

    def test_snapshot_current_former_ownership(self):
        self.bad([record(former_keys=['example.past']), record(id='K0002', canonical_key='example.past')], rule='another K')
        self.bad([record(former_keys=['example.past']), record(id='K0002', canonical_key='example.second', former_keys=['example.past'])], rule='another K')

    def test_empty_boundary(self):
        for value in [{}, None, [], {'includes': []}, {'excludes': [' ']}, {'unknown': ['x']}]:
            with self.subTest(value=value): self.bad([record(boundary=value)])

    def test_boundary_order(self):
        self.bad([record(boundary={'excludes': ['x'], 'includes': ['y']})], rule='boundary member order')

    def test_field_order(self):
        row = record(); row['title'] = row.pop('title')
        self.bad([row], rule='field order')

    def test_duplicate_json_member(self):
        self.bad(data=encode([record()]).replace(b'"title":"Example"', b'"title":"Example","title":"Other"'), rule='duplicate JSON')

    def test_nested_duplicate_json_member(self):
        self.bad(data=encode([record(boundary={'includes': ['x']})]).replace(b'"includes":["x"]', b'"includes":["x"],"includes":["y"]'), rule='duplicate JSON')

    def test_nonstandard_constants(self):
        for constant in [b'NaN', b'Infinity', b'-Infinity']:
            with self.subTest(constant=constant):
                self.bad(data=encode([record()]).replace(b'"Example"', constant), rule='non-standard')

    def test_bom(self):
        self.bad(data=b'\xef\xbb\xbf' + encode([record()]), rule='BOM')

    def test_invalid_utf8(self):
        self.bad(data=b'\xff\n', rule='UTF-8')

    def test_crlf(self):
        self.bad(data=encode([record()]).replace(b'\n', b'\r\n'), rule='LF-only')

    def test_blank_line(self):
        self.bad(data=encode([record()]) + b'\n', rule='blank record')

    def test_missing_final_newline(self):
        self.bad(data=encode([record()])[:-1], rule='final newline')

    def test_nonobject_comment_trailing_comma_multiline(self):
        for data in [b'[]\n', b'// comment\n', b'{"x":1,}\n', b'{\n"x":1\n}\n']:
            with self.subTest(data=data): self.bad(data=data)

    def test_json_escaped_newline_in_string(self):
        self.check([record(scope='One line\nAnother line')])

    def test_canonical_compact_serialization(self):
        self.bad(data=json.dumps(record()).encode() + b'\n', rule='compact JSON')
        self.bad(data=b' ' + encode([record()]), rule='compact JSON')

    def test_readable_unicode_serialization(self):
        self.check([record(title='Concept \u03b1')])
        self.bad(data=(json.dumps(record(title='Concept \u03b1'), separators=(',', ':')) + '\n').encode(), rule='readable Unicode')

    def test_macro_authority_parser(self):
        self.assertEqual(len(v.parse_macro_areas(MACRO_BYTES)), 60)
        for data in [MACRO_BYTES.replace(b'#### MATH-FOUND', b'#### MATH-DISCRETE', 1),
                     MACRO_BYTES.replace(b'#### MATH-FOUND', b'##### MATH-FOUND', 1),
                     MACRO_BYTES.replace(b'#### MATH-FOUND', b'### MATH-FOUND', 1),
                     MACRO_BYTES.replace(b'## 3. Level-1 Macro Areas', b'## Missing')]:
            with self.subTest(data=data[:20]), self.assertRaises(v.ValidationError): v.parse_macro_areas(data)


class HistoryRuleTests(unittest.TestCase):
    def history(self, current, *past):
        v.validate_history(index(current), [(f'commit-{i}', index(rows)) for i, rows in enumerate(past)])

    def test_issued_k_deletion(self):
        with self.assertRaisesRegex(v.ValidationError, 'deletion'): self.history([], [record()])

    def test_gap_backfill(self):
        old = record(id='K0003')
        with self.assertRaisesRegex(v.ValidationError, 'backfill'):
            self.history([record(id='K0002', canonical_key='example.new'), old], [old])

    def test_new_id_after_max(self):
        self.history([record(), record(id='K0003', canonical_key='example.new')], [record()])

    def test_rename_without_former(self):
        with self.assertRaisesRegex(v.ValidationError, 'rename missing'):
            self.history([record(canonical_key='example.new')], [record()])

    def test_valid_rename(self):
        self.history([record(canonical_key='example.new', former_keys=['example.original'])], [record()])

    def test_return_to_same_k_historical_key(self):
        middle = record(canonical_key='example.new', former_keys=['example.original'])
        self.history([record(former_keys=['example.new'])], [record()], [middle])

    def test_invented_former_key(self):
        with self.assertRaisesRegex(v.ValidationError, 'lack actual'):
            self.history([record(former_keys=['candidate.handle'])])

    def test_historical_key_reuse(self):
        renamed = record(canonical_key='example.new', former_keys=['example.original'])
        with self.assertRaisesRegex(v.ValidationError, 'reserved by'):
            self.history([renamed, record(id='K0002')], [record()])

    def test_dropped_former_key(self):
        middle = record(canonical_key='example.middle', former_keys=['example.original'])
        with self.assertRaisesRegex(v.ValidationError, 'rename missing'):
            self.history([record(canonical_key='example.new', former_keys=['example.middle'])], [record()], [middle])

    def test_retired_resurrection(self):
        with self.assertRaisesRegex(v.ValidationError, 'resurrection'):
            self.history([record()], [record(status='retired', retirement_reason='duplicate')])

    def test_retired_home_preservation(self):
        old = record(status='retired', macro_area='OLD-HOME', retirement_reason='duplicate')
        self.history([old], [old])
        with self.assertRaisesRegex(v.ValidationError, 'retired home changed'):
            self.history([dict(old, macro_area='MATH-FOUND')], [old])


class GitHistoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='registry-validator-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.env = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull)
        self.run_git('init', '-q')
        self.run_git('config', 'user.name', 'Registry Fixture')
        self.run_git('config', 'user.email', 'fixture@example.invalid')
        self.run_git('config', 'commit.gpgsign', 'false')
        (self.root / v.MACRO).write_bytes(MACRO_BYTES)
        (self.root / 'scripts').mkdir()
        shutil.copyfile(SCRIPT, self.root / 'scripts/validate_registry.py')
        self.commit('baseline')

    def run_git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.root), *args], env=self.env, stderr=subprocess.STDOUT).decode().strip()

    def write(self, rows):
        (self.root / 'registry').mkdir(exist_ok=True)
        (self.root / v.REGISTRY).write_bytes(encode(rows))

    def commit(self, message):
        self.run_git('add', '.')
        self.run_git('commit', '-qm', message)
        return self.run_git('rev-parse', 'HEAD')

    def cli(self, *args):
        return subprocess.run([sys.executable, '-B', str(self.root / 'scripts/validate_registry.py'), *args], capture_output=True, text=True)

    def test_first_population_before_and_after_commit(self):
        self.write([record()])
        self.assertEqual(v.validate_repository(self.root)[0], 1)
        self.commit('first registry')
        self.assertEqual(v.validate_repository(self.root, 'HEAD')[0], 1)
        self.assertEqual(v.validate_repository(self.root)[0], 1)

    def test_committed_revision_distinct_from_working_tree(self):
        self.write([record()]); self.commit('first registry')
        self.write([record(canonical_key='example.changed')])
        self.assertEqual(self.cli('--revision', 'HEAD').returncode, 0)
        self.assertNotEqual(self.cli().returncode, 0)

    def test_cli_missing_registry(self):
        self.assertNotEqual(self.cli().returncode, 0)
        self.assertNotEqual(self.cli('--revision', 'HEAD').returncode, 0)

    def test_cli_bad_revision(self):
        self.assertNotEqual(self.cli('--revision', 'not-a-revision').returncode, 0)

    def test_deleted_file_then_restored_is_invalid(self):
        self.write([record()]); self.commit('first registry')
        (self.root / v.REGISTRY).unlink(); self.commit('invalid deletion')
        self.write([record()]); self.commit('restoration cannot hide deletion')
        with self.assertRaisesRegex(v.ValidationError, 'deletion'): v.validate_repository(self.root, 'HEAD')

    def test_committed_rename_history(self):
        self.write([record()]); self.commit('first registry')
        self.write([record(canonical_key='example.new', former_keys=['example.original'])]); self.commit('rename')
        self.assertEqual(v.validate_repository(self.root, 'HEAD')[0], 1)

    def test_unrelated_branch_ignored(self):
        baseline = self.run_git('rev-parse', 'HEAD')
        self.run_git('checkout', '-qb', 'unrelated')
        self.write([record(id='K0500')]); self.commit('unrelated registry')
        self.run_git('checkout', '-q', '--detach', baseline)
        self.write([record()])
        self.assertEqual(v.validate_repository(self.root)[0], 1)

    def test_merge_shared_history(self):
        self.write([record()]); base = self.commit('first registry')
        self.run_git('checkout', '-qb', 'left')
        (self.root / 'left.txt').write_text('left'); self.commit('left')
        self.run_git('checkout', '-qb', 'right', base)
        (self.root / 'right.txt').write_text('right'); self.commit('right')
        self.run_git('merge', '--no-ff', '-qm', 'merge', 'left')
        self.assertEqual(v.validate_repository(self.root, 'HEAD')[0], 1)

    def test_independent_branch_allocation_reuse(self):
        base = self.run_git('rev-parse', 'HEAD')
        self.run_git('checkout', '-qb', 'left')
        self.write([record()]); self.commit('left allocation')
        self.run_git('checkout', '-qb', 'right', base)
        self.write([record()]); self.commit('right allocation')
        self.run_git('merge', '--no-ff', '-qm', 'merge independent allocations', 'left')
        with self.assertRaisesRegex(v.ValidationError, 'independent branch K reuse'):
            v.validate_repository(self.root, 'HEAD')

    def test_shallow_history_fails(self):
        self.write([record()]); head = self.commit('first registry')
        (self.root / '.git/shallow').write_text(head + '\n')
        with self.assertRaisesRegex(v.ValidationError, 'shallow'): v.validate_repository(self.root)


if __name__ == '__main__':
    unittest.main()
