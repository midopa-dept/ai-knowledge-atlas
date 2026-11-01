Status: CANONICAL — Medium Knowledge Registry v1

# Medium Knowledge Registry

[nodes.jsonl](nodes.jsonl)은 canonical Medium Concept Registry의 유일한 Concept data source다. 최초 population은 **493 active Concepts / 0 retired / K0001–K0493**였다. Formal Methods expansion admission은 **K0494–K0504**의 11개 active Concepts를 추가했다. 현재 합계는 **504 active Concepts / 0 retired / K0001–K0504**, 다음 unissued 번호는 **K0505**다. 이 확장 상태와 공식 issuance는 검증된 expansion admission commit이 canonical remote `main`에 수용된 시점부터 적용된다. Local working tree나 staging branch의 번호만으로 공식 issuance를 주장하지 않는다.

## Authority와 allocation

- Schema authority: [REGISTRY_SCHEMA.md](../REGISTRY_SCHEMA.md).
- Identity / issuance / lifecycle authority: [NODE_IDENTITY.md](../NODE_IDENTITY.md).
- Macro classification authority: [KNOWLEDGE_GRAPH_L1.md](../KNOWLEDGE_GRAPH_L1.md).
- Frozen semantic authority: [ONTOLOGY_V1.md](../ONTOLOGY_V1.md).
- Current project phase: PROJECT_STATE.md.

최초 admission은 사용자 제공 외부 설계 review 승인과 read-only gate 통과를 근거로 final v0.2 proposal의 정확한 493개 record를 변환했다. Allocation order는 해당 파일의 physical JSONL record order다. Row 1 → K0001, row 493 → K0493이며 title/key/home/scope/boundary를 exact data transformation으로 보존했다. Semantic normalization을 다시 수행한 결과가 아니다.

Formal Methods admission은 사용자 제공 external/design review의 **ADMISSION APPROVED — ADD 11 / MERGE 0 / DEFER 0 / HOLD 0**와 read-only gate를 근거로 approved proposal의 physical row order를 그대로 적용했다. FM-01 → K0494부터 FM-11 → K0504까지 title/key/home/scope/boundary를 정확히 변환하고 기존 493행은 byte-identical prefix로 보존했다.

IDs에는 domain, order, importance 의미가 없다. 최초 contiguous range는 deterministic batch allocation의 결과이며 분야별 range 예약이 아니다. 향후 admission은 macro area와 무관하게 retired와 canonical issuance history를 포함한 최대 issued 번호 다음부터 시작한다. Issued ID 삭제·재사용·재번호화와 gap backfill은 금지한다.

## Provenance와 layer 분리

Candidate artifacts와 admission mapping은 historical authoring provenance이며 두 번째 canonical Registry source가 아니다. Mapping은 Registry ID와 proposal source/resolution만 연결한다. Proposal-only provenance, candidate handles의 former-key history, DROP tombstone을 node records에 만들지 않는다.

Formal Methods admission mapping도 **AUTHORING PROVENANCE / NOT CANONICAL CONCEPT DATA**다. 11행의 `issued_id`, exact-copy `candidate_handle`, `proposal_decision`만 기록한다. 이 expansion은 신규 admission 11개뿐이며 retirement, rename, split, merge, lineage event 및 candidate handle 유래 `former_keys`는 0이다.

Pre-admission SPLIT은 issued identity의 lifecycle split이 아니다. 이 첫 admission에는 retirement나 lifecycle event가 없으므로 lineage를 생성하지 않았다. Semantic Graph는 Node Registry와 별도다. Learning, Claim, Evidence, Practice, Exposition data와 prerequisite adjacency를 registry nodes에 중복하지 않는다.

## Semantic Graph status

[Semantic Edge Schema v0.1](../SEMANTIC_EDGE_SCHEMA.md) is canonical.
[Medium Semantic Graph v1](semantic_edges.jsonl) contains **603 current canonical assertions** under Semantic Edge Schema v0.1. Canonical Concept data는 `nodes.jsonl`, canonical semantic relation data는 `semantic_edges.jsonl`로 분리한다.

이 graph admission 상태는 검증된 admission commit이 canonical remote `main`에 non-force fast-forward로 수용된 시점부터 적용된다. Local/staging 파일 존재는 공식 admission이 아니다. Admission audit은 frozen v0.2의 603/603 exact triple projection과 검증 provenance를 기록한다.

## Validation

Python 3.9 이상과 Git을 사용하며 Python third-party dependency는 없다. Repository root에서 실행한다.

```bash
python3 scripts/validate_registry.py
python3 scripts/validate_registry.py --revision HEAD
python3 -B -m unittest discover -s tests -p 'test_validate_registry.py'
python3 scripts/validate_semantic_edges.py
python3 scripts/validate_semantic_edges.py --revision HEAD
python3 -B -m unittest discover -s tests -p 'test_validate_semantic_edges.py'
```

기본 명령은 working-tree `registry/nodes.jsonl`을, `--revision`은 지정 commit의 registry와 macro 문서를 검증한다. 성공은 exit 0, 실패는 non-zero이며 오류에 file, line, ID/key와 violated rule을 가능한 한 표시한다. Committed history는 해당 revision 또는 HEAD에서 reachable한 ancestry만 사용한다. 무관한 branches와 candidate/proposal 예시는 발급 이력에 포함하지 않는다.

검사는 UTF-8/no BOM/LF/final newline, standard JSON과 duplicate member, schema fields/types/enums, field/boundary order, K syntax/padding/numeric order, key uniqueness/ownership, optional metadata, active macro membership와 retired reason을 포함한다. Macro keys는 canonical heading에서 추출하며 60개인지 확인한다. Generic validator는 future gap을 허용하고 최초 493개 batch constants를 hard-code하지 않는다.

History 검사는 committed ID 삭제·삭제 후 재등장, 독립 branch의 K 중복 allocation, historical max 이하 신규 allocation, historical current/former-key의 타 K 재사용, rename 추적과 former-key provenance, retired 부활과 기존 tombstone home 변경을 검사한다. 각 commit은 strict ancestry와 비교하므로 최초 Registry commit 자체는 historical conflict가 아니다. Shallow history, missing target, Git 조회 실패는 PASS로 처리하지 않는다. Branch history 검사는 pre-issuance consistency check로도 쓰이며 공식 issuance 여부를 자동 선언하지 않는다.

Git snapshot은 semantic identity continuity, split/merge 정당성, 최초 retirement 시점 내부 사건의 순서나 home의 의미적 타당성, reference-audit closure를 완전히 증명하지 못한다. 특히 active→retired 전환에서의 home 판단은 Node Identity에 따른 별도 semantic review 대상이며 기존 retired home 보존 검사와 구분한다.

최초 admission의 493/493 exact proposal transformation, K0001–K0493 contiguous allocation, 60-area coverage와 493행 provenance mapping은 별도 one-time validation으로 확인했다. General build pipeline이나 GitHub Actions workflow는 이번 checkpoint에 포함하지 않는다.

두 번째 admission에서는 기존 493행 prefix의 byte equality, 신규 11/11 exact transformation과 mapping, 504 active / 0 retired, K0001–K0504의 gap 없는 범위, next K0505, 전체 canonical key 504개 uniqueness와 60-area validity를 별도 one-time validation으로 확인한다. 기존 validator와 tests는 그대로 사용하며 이 batch의 수량·범위를 generic validator에 hard-code하지 않는다.

Semantic-edge validator는 working tree 또는 지정된 committed tree의 graph와 같은 snapshot의 Registry/macro를 검증하며 기존 Registry validator의 schema·K history 검사를 재사용한다. Missing graph는 실패한다. Graph의 serialization·정확한 세 fields·8-profile·active Concept endpoints·중복·symmetric orientation·정렬·component_of/generalizes cycles를 검사한다. Edge 삭제·동일 triple 재등록에 history 금지를 부과하지 않으며 603개 수량, 분포, connectivity나 density를 generic 규칙으로 강제하지 않는다. Directness/materiality와 의미적 admission은 별도 review 대상이다.
