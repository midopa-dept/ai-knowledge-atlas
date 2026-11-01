Status: CANONICAL — KOREAN TERMINOLOGY V1

# Canonical terminology registries

이 상태는 검증된 admission commit이 canonical remote `main`에 non-force fast-forward push로 수용된 시점부터 적용한다. Local files, staging branch 또는 local commit만으로 canonical admission을 뜻하지 않는다.

[Korean Authoring & Terminology Policy v0.1](../KOREAN_AUTHORING_TERMINOLOGY_POLICY.md)이 publication language, terminology authority, display와 schema 규칙의 canonical source다. Policy v0.1의 semantic rules는 유지한다.

- [concept_labels.jsonl](concept_labels.jsonl): canonical K-backed Korean publication labels — **54 records**. Identity는 기존 `concept_id`이며 별도 terminology ID가 없다.
- [terms.jsonl](terms.jsonl): canonical general technical terminology — **437 records**. `term_key`는 authoring sense key다.
- 현재 canonical terminology entries: **491**. 최초 v1 admission146개에 T4-B 승인345개를 추가했다. 수량은 schema quota가 아니다.

English [Node Registry](../registry/nodes.jsonl)의 identity/title/key/scope/boundary와 [Semantic Graph](../registry/semantic_edges.jsonl)는 semantic authority다. Terminology는 publication/authoring 표현의 authority이며 alternate Knowledge Registry가 아니다.

Sparse authority: entry의 부재는 해당 K/sense의 exact canonical entry가 현재 없다는 뜻이다. 한국어 번역이 불가능하다는 뜻이 아니며 전체 504 Concepts나 모든 기술 명사를 자동 등록하지 않는다. Unknown occurrences는 policy의 precedence와 unknown-term workflow를 따른다. English/acronym retention도 승인된 표기다.

## Validation

```sh
python3 scripts/validate_terminology.py
python3 scripts/validate_terminology.py --revision HEAD
python3 -B -m unittest discover -s tests -p 'test_validate_terminology.py'
```

Validator는 현재 구조·serialization·active K·조건부 fields·정렬·avoid·repeated-English context를 검사한다. 의미 품질이나 한국어 surface 충돌의 안전성을 자동 판정하지 않으며 terminology에 K/LO issuance lifecycle을 부여하지 않는다. Current 필수 JSONL이 없으면 실패한다.

## Admission provenance and next work

v0.2 freeze의 **PASS / 25 + 121 / HOLD 0** source를 필드와 physical order 변경 없이 복사했다. Admission audit이 검증과 boundary를 기록한다. v0.1 T4 audit의 PASS WITH HOLD 및 v0.2 freeze 원본은 historical provenance다.

LO29 terminology coverage는 **READY**다. Korean publication-language validation이나 semantic-equivalence audit 완료를 뜻하지 않는다. English LO Pilot과 L1–L4 artifacts는 보존하며 official LO는 **0**, `learning/objectives.jsonl`은 absent다. 이 문단의 READY는 최초 v1 admission 당시 coverage 결과다. 이후 Korean LO Pilot29의 변환·감사·최종 동결 이력은 PROJECT_STATE에 보존한다. 현재 다음 작업은 별도 T5 Resolution이다.

## T4-B 추가 입고 및 후속 경계

T4-B 실제 입고 checkpoint는 입력 `0c925fd23b85401a8465afd3bb811cba29c48d36`의 T4-A exact 승인 잠금을 사용해345개(Concept29/general316)를 추가했다. 현재54/437/491개이며 기존146개 record의 의미·필드·개별 직렬화를 보존했다. 입고 mapping에 identity별 canonical physical line과 승인 hash/source lineage를 연결한다. 새로운 Concept K는 발급하지 않았다.

T4-A의 제외5개와 과거 제거267개는 입고하지 않았다. English 유지 항목에는 preferred_ko를 생성하지 않았고 승인된 display·note·한정어와 대체 경로를 그대로 보존했다. Registry504/Graph603 및 동결 영어817/FLOP·기존 심사 artifacts는 불변이다.

Canonical authority 생성 이후에도 TI1473/occurrence1707/collision109/original scope946의 HOLD와 multi-entry TI292의 all-of는 유지한다. 각 occurrence에 적용 가능하다는 독립 Resolution은 후속 T5 책임이다. 정확 T5 입력을 참조한다. T4-B 완료·remote 수용 확인 뒤 STOP하며 T5·T Closure·한국어 LO·공식LO·자동 후속은 실행하지 않는다.
