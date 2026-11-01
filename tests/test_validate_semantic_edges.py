"""Current-edge structural tests; Git mutations are confined to temporary repos."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import validate_semantic_edges as v

MACRO_BYTES = (SCRIPTS.parent / v.registry.MACRO).read_bytes()


def edge(source='K0001', relation='applied_in', target='K0002'):
    return dict(source=source, relation=relation, target=target)


def node(number, **changes):
    row = dict(id=f'K{number:04d}', canonical_key=f'example.node{number}', title='Example',
               kind='concept', macro_area='MATH-FOUND', scope='Example scope.', status='active')
    row.update(changes)
    return row


def encode(rows):
    return ''.join(json.dumps(r, ensure_ascii=False, separators=(',', ':')) + '\n' for r in rows).encode()


def ordered(rows):
    return sorted(rows, key=lambda r: (int(r['source'][1:]), r['relation'], int(r['target'][1:])))


class StructuralTests(unittest.TestCase):
    def setUp(self):
        self.nodes = {r['id']: r for r in [node(n) for n in (1, 2, 3, 4, 9999, 10000)]}

    def check(self, rows=None, data=None):
        return v.validate_records(v.parse_jsonl(data if data is not None else encode(rows), 'fixture'), self.nodes)

    def bad(self, rows=None, data=None, rule='.'):
        with self.assertRaisesRegex(v.ValidationError, rule):
            self.check(rows, data)

    def test_valid_directed(self):
        self.check([edge('K0002', target='K0001')])

    def test_valid_symmetric(self):
        for relation in v.SYMMETRIC:
            with self.subTest(relation=relation): self.check([edge(relation=relation)])

    def test_distinct_relations_same_pair(self):
        self.check([edge(), edge(relation='used_to_analyze')])

    def test_disconnected_graph(self):
        self.check([edge(), edge('K0003', target='K0004')])

    def test_permitted_directed_cycles(self):
        for relation in ('applied_in', 'used_to_analyze', 'motivates', 'explains'):
            with self.subTest(relation=relation):
                self.check([edge(relation=relation), edge('K0002', relation, 'K0001')])

    def test_applied_in_long_cycle(self):
        self.check([edge(), edge('K0002', target='K0003'), edge('K0003', target='K0001')])

    def test_mixed_cycle_valid(self):
        self.check([edge(relation='component_of'), edge('K0002', 'generalizes', 'K0001')])

    def test_explicit_transitive_edge_valid(self):
        self.check([edge(relation='generalizes'), edge(relation='generalizes', target='K0003'),
                    edge('K0002', 'generalizes', 'K0003')])

    def test_numeric_boundary_valid(self):
        self.check([edge('K9999', 'contrasts_with', 'K10000'), edge('K10000', target='K0001')])

    def test_invalid_utf8(self): self.bad(data=b'\xff\n', rule='UTF-8')
    def test_bom(self): self.bad(data=b'\xef\xbb\xbf' + encode([edge()]), rule='BOM')
    def test_crlf(self): self.bad(data=encode([edge()]).replace(b'\n', b'\r\n'), rule='LF-only')
    def test_missing_final_newline(self): self.bad(data=encode([edge()])[:-1], rule='final newline')
    def test_blank_line(self): self.bad(data=encode([edge()]) + b'\n', rule='blank record')

    def test_duplicate_member(self):
        self.bad(data=encode([edge()]).replace(b'"source":"K0001"', b'"source":"K0001","source":"K0001"'), rule='duplicate JSON')

    def test_nonobject(self): self.bad(data=b'[]\n', rule='JSON object')
    def test_trailing_comma(self): self.bad(data=encode([edge()]).replace(b'}', b',}'))

    def test_comments_multiline(self):
        for data in [b'// comment\n', b'{\n"source":"K0001"\n}\n']:
            with self.subTest(data=data): self.bad(data=data)

    def test_nonstandard_constants(self):
        for value in (b'NaN', b'Infinity', b'-Infinity'):
            with self.subTest(value=value):
                self.bad(data=encode([edge()]).replace(b'"K0001"', value), rule='non-standard')

    def test_noncompact(self): self.bad(data=(json.dumps(edge())+'\n').encode(), rule='compact JSON')

    def test_escaped_serialization(self):
        self.bad(data=encode([edge()]).replace(b'K0001', b'\\u004b0001'), rule='compact JSON')
        self.bad(data=encode([edge()]).replace(b'applied_in', b'\\u03b1'), rule='readable Unicode')

    def test_field_order(self):
        row=edge(); row['source']=row.pop('source'); self.bad([row], rule='field order')

    def test_extra_fields(self):
        for field in ('reason','evidence_basis','edge_id','status','confidence','weight','version',
                      'revision','created_at','updated_at','citation','claim_status'):
            with self.subTest(field=field): self.bad([dict(edge(), **{field:'x'})], rule='exactly')

    def test_missing_fields(self):
        for field in v.FIELDS:
            row=edge(); del row[field]
            with self.subTest(field=field): self.bad([row], rule='exactly')

    def test_wrong_types_and_empty(self):
        for field in v.FIELDS:
            for value in (None, 1, True, [], {}, '', ' '):
                row=edge(); row[field]=value
                with self.subTest(field=field, value=value): self.bad([row], rule='non-empty string')

    def test_invalid_k_syntax(self):
        for value in ('K001','K0000','K00001','K０００１','k0001','K0001\n'):
            for field in ('source','target'):
                row=edge(); row[field]=value
                with self.subTest(value=value, field=field): self.bad([row], rule='K|padding')

    def test_unknown_k(self): self.bad([edge(target='K0500')], rule='unknown K')

    def test_retired_k(self):
        self.nodes['K0002']['status']='retired'; self.bad([edge()], rule='active')

    def test_nonconcept_endpoint(self):
        self.nodes['K0002']['kind']='formal_object'; self.bad([edge()], rule='concept')

    def test_self_edge(self): self.bad([edge(target='K0001')], rule='self-edge')
    def test_unknown_relation(self): self.bad([edge(relation='custom')], rule='unsupported relation')
    def test_specializes(self): self.bad([edge(relation='specializes')], rule='unsupported relation')

    def test_learning_relations(self):
        for r in ('requires','recommended','deepens'):
            with self.subTest(relation=r): self.bad([edge(relation=r)], rule='unsupported relation')

    def test_deferred_relations(self):
        for r in ('identity_or_decomposition','historically_leads_to','caused_by','manifested_as',
                  'detected_by','mitigated_by','enforced_by'):
            with self.subTest(relation=r): self.bad([edge(relation=r)], rule='unsupported relation')

    def test_wrong_symmetric_orientation(self):
        for r in v.SYMMETRIC:
            with self.subTest(relation=r): self.bad([edge('K10000',r,'K9999')], rule='orientation')

    def test_reverse_duplicate(self):
        for r in v.SYMMETRIC:
            with self.subTest(relation=r):
                self.bad([edge(relation=r),edge('K0002',r,'K0001')], rule='reverse symmetric duplicate')

    def test_exact_duplicate(self): self.bad([edge(),edge()], rule='exact duplicate')
    def test_source_numeric_disorder(self):
        self.bad([edge('K10000'),edge('K9999')], rule='ascending')
    def test_relation_lexical_disorder(self):
        self.bad([edge(relation='used_to_analyze'),edge()], rule='ascending')
    def test_target_numeric_disorder(self):
        self.bad([edge(target='K10000'),edge(target='K9999')], rule='ascending')

    def cycle(self, relation, length):
        rows=[edge(f'K{i:04d}', relation, f'K{i+1:04d}') for i in range(1,length)]
        rows.append(edge(f'K{length:04d}',relation,'K0001'))
        self.bad(rows, rule=f'{relation} cycle')

    def test_component_two_cycle(self): self.cycle('component_of',2)
    def test_component_long_cycle(self): self.cycle('component_of',4)
    def test_generalizes_two_cycle(self): self.cycle('generalizes',2)
    def test_generalizes_long_cycle(self): self.cycle('generalizes',4)


class GitSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='semantic-validator-')
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.env=dict(os.environ,GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL=os.devnull)
        self.git('init','-q'); self.git('config','user.name','Edge Fixture')
        self.git('config','user.email','fixture@example.invalid'); self.git('config','commit.gpgsign','false')
        (self.root/'scripts').mkdir(); (self.root/'registry').mkdir()
        for script in ('validate_registry.py','validate_semantic_edges.py'):
            shutil.copyfile(SCRIPTS/script,self.root/'scripts'/script)
        (self.root/v.registry.MACRO).write_bytes(MACRO_BYTES)
        self.write_nodes([node(1),node(2),node(3)])
        self.base=self.commit('registry baseline')

    def git(self,*args):
        return subprocess.check_output(['git','-C',str(self.root),*args],env=self.env,stderr=subprocess.STDOUT).decode().strip()
    def write_nodes(self,rows): (self.root/v.registry.REGISTRY).write_bytes(encode(rows))
    def write(self,rows): (self.root/v.GRAPH).write_bytes(encode(rows))
    def commit(self,message):
        self.git('add','.'); self.git('commit','-qm',message); return self.git('rev-parse','HEAD')
    def cli(self,*args):
        return subprocess.run([sys.executable,'-B',str(self.root/'scripts/validate_semantic_edges.py'),*args],capture_output=True,text=True)
    def good(self,*args):
        result=self.cli(*args); self.assertEqual(result.returncode,0,result.stderr)
    def bad(self,*args): self.assertNotEqual(self.cli(*args).returncode,0)

    def test_first_population_and_revision(self):
        self.write([edge()]); self.good(); sha=self.commit('graph'); self.good('--revision',sha)

    def test_working_vs_revision(self):
        self.write([edge()]); self.commit('graph')
        self.write([edge(relation='requires')]); self.bad(); self.good('--revision','HEAD')

    def test_missing_graph(self):
        self.bad(); self.bad('--revision','HEAD')
        self.write([edge()]); self.commit('graph'); (self.root/v.GRAPH).unlink()
        self.bad(); self.good('--revision','HEAD')

    def test_bad_revision(self): self.bad('--revision','not-a-revision')

    def test_deletion_allowed(self):
        self.write([edge(),edge('K0002',target='K0003')]); self.commit('two edges')
        self.write([edge()]); self.good(); sha=self.commit('delete one edge'); self.good('--revision',sha)

    def test_readd_allowed(self):
        original=[edge(),edge('K0002',target='K0003')]
        self.write(original); self.commit('two edges')
        self.write([edge()]); self.commit('delete edge')
        self.write(original); self.good(); sha=self.commit('reviewed re-add'); self.good('--revision',sha)

    def test_invalid_historical_edges_not_enforced(self):
        self.write([edge(relation='requires')]); self.commit('bad old edge')
        self.write([edge()]); self.commit('correct current edge'); self.good('--revision','HEAD')

    def test_registry_snapshot_distinction(self):
        self.write([edge()]); old=self.commit('graph')
        self.write_nodes([node(1),node(2,status='retired',retirement_reason='erroneous_concept'),node(3)])
        self.bad(); self.good('--revision',old)
        self.commit('retire endpoint'); self.bad('--revision','HEAD'); self.good('--revision',old)

    def test_invalid_registry_serialization(self):
        self.write([edge()]); self.commit('graph')
        path=self.root/v.registry.REGISTRY; path.write_bytes(b'\xef\xbb\xbf'+path.read_bytes())
        self.bad(); self.good('--revision','HEAD')

    def test_registry_history_enforced(self):
        self.write([edge()]); self.commit('graph')
        self.write_nodes([node(1,canonical_key='example.renamed'),node(2),node(3)])
        self.bad(); self.commit('untracked rename'); self.bad('--revision','HEAD')

    def test_macro_snapshot_distinction(self):
        self.write([edge()]); old=self.commit('graph')
        (self.root/v.registry.MACRO).write_bytes(b'invalid macro\n')
        self.bad(); self.good('--revision',old)
        self.commit('bad macro'); self.bad('--revision','HEAD'); self.good('--revision',old)

    def test_input_drift_detected(self):
        self.write([edge()])
        original=v.registry.validate_repository
        def mutate(*args,**kwargs):
            result=original(*args,**kwargs)
            self.write([edge(target='K0003')])
            return result
        with patch.object(v.registry,'validate_repository',side_effect=mutate):
            with self.assertRaisesRegex(v.ValidationError,'input changed'): v.validate_repository(self.root)


if __name__ == '__main__': unittest.main()
