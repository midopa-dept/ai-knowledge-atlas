Status: CANONICAL LEARNING OBJECTIVE ADMISSION COMPLETE / 817 ACTIVE LO ISSUED

# Learning Layer storage

이 directory는 Learning Layer의 canonical storage location이다. [Learning Objective Schema v0.1](../LEARNING_OBJECTIVE_SCHEMA.md)이 stable LO identity, record, Concept grounding, lifecycle 및 layer 경계를 정의한다. 결정 배경은 [ADR 0005](../decisions/0005-learning-objective-schema-v0.1.md), 현재 프로젝트 상태는 PROJECT_STATE를 참조한다.

## 현재 Canonical Learning Objective Registry

- 공식 Registry: [learning/objectives.jsonl](objectives.jsonl), **817 active / 0 retired / 817 issued**, LO0001–LO0817.
- Registry SHA-256: `578b54496f4fd0ddbfa7c6e9abb5adf90bbba4fac4d65972340b1b663a68a8dc`.
- Admission checkpoint에 인간 승인 원문(2026-10-13, Asia/Seoul)과 exact identity를 기록했다. 승인된 Frozen Proposal817의 SHA-256은 `c5e1dd8fddb2f8d7e7956fd591e8c54d87f39f0247c23f524423957ddb7329d3`다. 한국어 statement·원순서·ordered Concepts를 각각817/817 exact로 보존했다. Multi-Concept31·coverage504/504 유지, 추가·제외·수정0이다.
- 전체 canonical main 이력에서 이전 Registry·issued/retired/예약0을 확인했다. Single-writer initial allocation은 FLOP0001→LO0001, …, FLOP0817→LO0817이다. FLOP는 pre-admission handle이었다. 공식 LO 번호는 교육 순서·난이도·중요도를 뜻하지 않는다.
- 최대 issued LO0817 / 다음 allocation LO0818. 발급된 ID는 retired를 포함해 삭제·재사용·재번호화하지 않는다. 과거 부재나 gap을 재사용 근거로 삼지 않는다.
- [LO 구조 validator](../scripts/validate_learning_objectives.py)와 [regression tests](../tests/test_validate_learning_objectives.py)는 직렬화·field·ID·lifecycle 구조·Concept endpoint를 확인한다. 의미 품질·인간 승인·Git 발급 이력·retirement closure·원격 수용은 별도 확인 사항이다.
- 선수관계·Objective Dependency·Mastery/Target Depth·Evidence Requirement·Task Model·Exercise·Curriculum/Pathway·목차·집필은 아직 미작성이다. 이번 admission 뒤 자동 실행하지 않는다.

**공식 issuance와 위 완료 상태는 검증된 Registry commit의 actual remote canonical `main` 수용 시 효력을 갖는다.** Local draft/staging/commit만으로는 공식 발급이 아니다. 최종 Git SHA·non-force push·local HEAD=origin/main=actual remote main·clean 결과는 Git history와 사용자 최종 보고에서 확인한다.

## Canonical Prerequisite / Objective Dependency Schemas v0.1

2026-10-13 (Asia/Seoul) 인간 승인에 따라 [Prerequisite Requirement Schema v0.1](../PREREQUISITE_REQUIREMENT_SCHEMA.md)과 [Objective Dependency Schema v0.1](../OBJECTIVE_DEPENDENCY_SCHEMA.md)을 정본화했다. 승인 원문·D1–D5·대안·보수적 DAG 비용은 [ADR 0007](../decisions/0007-prerequisite-requirement-objective-dependency-schema-v0.1.md), LO와의 경계는 [LO Schema §11](../LEARNING_OBJECTIVE_SCHEMA.md#11-objective-dependency-and-prerequisite-requirement-boundary)을 참조한다.

미래 Requirement Registry 경로는 `learning/prerequisite_requirements.jsonl`이다. Requirement가 부분/whole 수행·Context·Resources·OR-of-AND·Required Mastery·reason·provenance의 유일한 의미 원천이며 Dependency는 query와 Registry commit에서 파생한다. 별도 공식 Dependency ID나 독립적으로 편집하는 Dependency Registry를 두지 않는다.

현재 **PR Registry 없음 / PR ID 발급·예약0 / 관계 admission0 / Canonical Objective Dependency population 없음**이다. 위 미래 경로는 빈 파일도 생성하지 않았다. 기존 공식 LO **817 active / 0 retired / LO0001–LO0817**과 위 Registry SHA는 유지한다. 기존 Pilot required9·미결4와 Schema fixtures는 정본 데이터가 아니다. Concrete Requirement admission·전체817 관계 population·Mastery Evidence·Task Model·Curriculum/Pathway·본문은 별도 승인 범위이며 자동 실행하지 않는다.

## 이전 pilot·schema checkpoint의 역사

아래 미발급·미등록·다음 단계 문구는 각 pilot/schema checkpoint 당시 상태다. Pilot 원본·감사·freeze는 불변이며 현재 공식 Registry의 별도 source가 아니다.

**Learning Objective Schema v0.1은 canonical이며 English Learning Objective Pilot v0.1은 pre-admission semantic reference pilot이다.** Pilot candidates는 **PILOT / PRE-ADMISSION / NON-REGISTRY / NO LO ISSUANCE**이며 이 learning directory의 canonical registry가 아니다. 16개 stress-test anchors, 29개 final candidates(single-Concept 24 / multi-Concept 5)에 대한 fresh-context L4 audit의 verdict는 **PASS**, holds 0이다. Schema/Ontology와 Knowledge Registry/Semantic Graph는 변경하지 않았다.

`PILOT001` 등의 handle은 stable identity나 예약, future LO number assignment가 아니다. 이 pilot은 granularity·identity·statement-only/grounding·Mastery/Target Depth 분리·future prerequisite/evidence compatibility를 검토한 editorial learning-design artifact이며 학습효과의 실증이 아니다. External/design granularity review **PASS**는 이번 policy checkpoint에서 사용자가 제공한 외부 설계 검토 결과이며 재실행한 검증이 아니다. **Policy canonicalization 당시에는 Korean publication-language validation을 수행하지 않았다.** 기존 English 29개 unchanged final freeze는 수행하지 않고 모든 pilot artifacts를 byte-identical로 보존한다. [Korean Authoring & Terminology Policy](../KOREAN_AUTHORING_TERMINOLOGY_POLICY.md)에 따라 향후 canonical LO statement는 기본적으로 한국어로 작성한다. Policy canonicalization 당시 다음 계획은 **Korean Terminology Pilot → high-risk terminology review → terminology pilot freeze → 별도 Korean LO Pilot 변환 → semantic-equivalence audit → Korean LO Pilot final freeze → full LO population orchestration**이었다. 해당 policy checkpoint에서 terminology population·LO 번역·freeze·admission 및 전체 population은 수행하지 않았다. Schema defect가 발견되는 후속 검토에서는 별도 schema checkpoint로 해결하며 pilot 도중 판정 기준을 변경하지 않는다.

## Korean Learning Objective Pilot v0.1

Korean counterpart 29개의 transformation과 Korean publication-language validation이 완료됐으며, fresh-context semantic-equivalence audit는 **PASS**다. English semantic reference와 handle/ordered grounding **29/29 exact**를 유지한다. **PILOT / PRE-ADMISSION / NON-REGISTRY / NO LO ISSUANCE** 상태이며 canonical LO population은 여전히 없다. Official LO **0**, learning/objectives.jsonl absent; transformation 당시 final Korean pilot external/design approval record와 final freeze는 후속 단계였다.

Human editorial calibration v0.1으로 29개 승인 base wording과 전후·이유를 보존하고 publication statement를 갱신했다. Fresh-context KL5 최종 **PASS / EQUIVALENT 29 / HOLD 0**; PILOT011 neural 조건 복원은 승인 원문과 분리된 semantic repair로 기록했다. 기존 KL4는 baseline historical audit다. Human editorial calibration completed and semantically revalidated; 해당 calibration checkpoint에서는 final freeze, LO allocation/admission, full population을 수행하지 않았다.

Final Korean pilot freeze **PASS**: exact current Korean 29개는 full Learning Objective population 설계·감사를 위한 **approved final pilot reference objectives**다. English 29·Korean 29 및 handles/ordered grounding 29/29 exact, single-Concept 24 / multi-Concept 5, human approval 29/29, KL5 PASS 29/29, terminology compliance PASS. Schema/policy amendment 없음. Canonical LO가 아니며 official LO 0, objectives.jsonl absent, ID allocation/reservation 없음.

후속 workers는 canonical English Knowledge semantics, LO Schema v0.1, Canonical Korean Terminology v1과 final Korean Pilot 29를 granularity·한국어 wording 참고로 사용한다. Concept별 objective 수나 문장 형식 template으로 적용하지 않으며 Concept-per-objective quota는 없다. Human calibration은 later manuscript/style research용 provenance로 보존하며 Style Guide·자동 편집 policy·validator·harness는 만들지 않는다. Permanent LO validator는 concrete earlier need가 없으면 actual canonical admission에서 도입한다. Full population orchestration design은 다음 checkpoint이며 이번에는 시작하지 않는다.
