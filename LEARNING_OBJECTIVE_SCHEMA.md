Status: CANONICAL — Learning Objective Schema v0.1

# Learning Objective Schema

## 1. Purpose, authority and checkpoint scope

이 문서는 Learning Objective의 stable identity, 최소 record, Concept grounding, lifecycle과 미래 canonical serialization을 정의한다. **Schema-only checkpoint: no objective population / no LO issuance.** Schema 정의 자체는 objective admission이 아니다.

Canonical precedence는 [FROZEN Ontology v1.0](ONTOLOGY_V1.md) → [Node Identity](NODE_IDENTITY.md) → [Registry Schema](REGISTRY_SCHEMA.md) → [Semantic Edge Schema](SEMANTIC_EDGE_SCHEMA.md) → [canonical Node Registry](registry/nodes.jsonl) → [canonical Semantic Graph](registry/semantic_edges.jsonl) → 이 schema다. [Macro Skeleton](KNOWLEDGE_GRAPH_L1.md)의 classification과 prerequisite 분리 원칙도 보존한다. 결정 배경은 [ADR 0005](decisions/0005-learning-objective-schema-v0.1.md), 현재 상태는 PROJECT_STATE, 저장 위치 안내는 [learning/README](learning/README.md)에 둔다.

Ontology §2.1의 Knowledge / Learning / Exposition 분리, §2.2의 reason·required mastery·target objective/depth 요구, §2.3의 Reading is not mastery, §5의 Learning Layer와 §6의 Evidence Layer를 구체화한다. Node Identity가 후속 설계로 남긴 Learning namespace를 정의하며 K의 의미나 기존 canonical 문서·data를 변경하지 않는다.

현재 Knowledge Layer는 504 active Concepts / 0 retired, K0001–K0504 / next K0505와 603 semantic assertions다. 이 checkpoint는 실제 LO, Objective Dependency, Prerequisite Requirement, mastery/depth assignment, Evidence Requirement, Task Model, Practice, lineage, K allocation이나 manuscript를 생성하지 않는다.

## 2. Stable LO identity and issuance

Learning Objective는 statement text와 별개인 first-class stable reference target이다. Objective Dependency, Prerequisite Requirement, Evidence Requirement, Task Model/Exercise coverage와 Q-matrix, publication cross-reference가 같은 수행 객체를 참조할 수 있어야 한다. Statement나 Concept 집합을 identity key로 사용하지 않는다.

- Syntax: ASCII full-match `LO[0-9]{4,}`. 숫자 부분은 양의 정수이며 그 정수를 최소 4자리로 zero-padding한 결과와 정확히 일치해야 한다.
- Valid syntax: `LO0001`, `LO0492`, `LO9999`, `LO10000`. Invalid: `LO0000`, `LO1`, `LO00001`, `Learning001`, `K0505`.
- ID에는 domain, order, importance, difficulty, mastery, depth 의미가 없다. K와 LO는 별도 namespace다.
- Issued ID는 retired를 포함하여 globally unique하며 삭제·재사용·재번호화하지 않는다. Gap은 허용하되 backfill이나 분야별 range 예약을 금지한다.
- 최초 allocation은 LO0001부터, 이후는 retired 및 canonical issuance history를 포함한 최대 issued 번호 다음부터 단조 증가한다. 과거 ID의 부재는 재사용 근거가 아니다.

미래 운영 순서는 candidate/pilot review → admission set approval → canonical main 동기화 → single-writer allocation → structural/history validation 및 semantic review → canonical registry commit이다. Main이 바뀌면 allocation 전에 최신 issuance history를 재확인한다.

**LO ID는 canonical Learning Objective Registry에 대한 validated commit이 canonical remote `main`으로 수용될 때 공식 발급된다.** Local draft, staging, candidate/pilot handle 및 문서 예시의 LO syntax는 공식 issuance나 reservation이 아니다. Candidate는 registry lifecycle status가 아니다.

이 checkpoint에서 **officially issued LO count = 0; next potential allocation = LO0001 (unissued and unreserved)**. Learning Objective ID syntax and allocation policy defined. No Learning Objective IDs have been issued.

## 3. Record schema

Active와 retired 모두 아래 네 base fields를 가진다. 정의되지 않은 추가 field는 금지하며 `null`로 빈 값을 채우지 않는다. 문자열은 공백만인 값을 허용하지 않는다.

| Field | JSON type | Contract |
| --- | --- | --- |
| `id` | string | §2의 stable LO identity |
| `statement` | string | 학습자의 observable performance, 대상, identity를 구별하는 핵심 조건을 기술 |
| `concepts` | array of strings | 하나 이상의 canonical Concept K; 중복 없이 numeric K ascending; §4의 endpoint 규칙 |
| `status` | string | 정확히 `active` 또는 `retired` |

일반 optional fields는 없다. 다음은 lifecycle 보존을 위한 유일한 조건부 field다.

| Field | `active` | `retired` |
| --- | --- | --- |
| `retirement_reason` | 존재 금지 | Non-empty string 필수 |

Retirement reason은 폐기된 수행을 설명하는 최소 정보다. 고정 reason enum은 만들지 않으며 reason만으로 reference-audit closure를 증명하지 않는다. `kind = learning_objective`는 이 registry의 암묵적 type으로, `kind` field를 저장하지 않는다.

별도 `scope`, `conditions`, `boundary`는 v0.1에 두지 않는다. Identity와 observable performance를 구별하는 조건은 statement 안에 명시한다. Authoring convenience만으로 field를 늘리지 않는다. 향후 pilot에서 이 방식의 한계가 확인되면 명시적인 schema revision으로 검토한다.

`mastery`, `target_depth`, `terminal`, `enabling`, `core`, `recommended`, `enrichment`, `required`, `elective`, `difficulty`, exercise count, prerequisites/required_by, evidence/task models, chapter/volume/publication order, claim status 및 authoring provenance는 supported fields가 아니다. 이 정보의 필요성을 폐기하는 것이 아니라 해당 layer에서 관리한다.

## 4. Concept grounding

**1 Concept != 1 Learning Objective.** Concept 하나에 0, 1 또는 복수 objectives가 가능하고, 하나의 objective가 여러 Concepts를 직접 비교·통합하는 것도 가능하다. `primary_concept`나 단일 macro owner를 요구하지 않는다.

- `concepts`는 non-empty이며 각각 Registry Schema의 K syntax/padding을 따른다. 같은 K 중복을 금지하고 숫자 부분의 정수 오름차순으로 저장한다.
- Active LO의 모든 K는 current Node Registry에 존재하고 `kind = concept`, `status = active`여야 한다.
- Grounding은 수행의 직접적인 개념적 기반이다. 모든 배경지식, transitive prerequisites, 의미적으로 연결된 모든 이웃을 나열하는 목록이 아니다. Grounding으로 prerequisite를 선언하거나 유도하지 않는다.
- Multi-Concept 적절성은 statement가 해당 Concepts를 직접 사용·비교·통합하는지 editorial review로 판단한다. Registry의 canonical scope/boundary를 존중한다.
- Concept title/key/home 변경은 K identity가 유지되면 LO identity 변경을 요구하지 않는다. Grounding 정정은 같은 수행 의도를 보존하는지 검토하며 기계적으로 SAME LO로 판정하지 않는다.

K retirement closure에는 해당 K를 grounding하는 모든 active LO의 reference audit가 포함된다. 같은 수행을 유지하는 정정은 SAME LO로 가능하지만 핵심 수행이 바뀌면 신규 LO 또는 retirement를 검토한다. K lineage successor로 자동 치환하지 않는다.

Retired LO tombstone은 retirement 당시 마지막 `statement`와 `concepts`를 보존한다. 이 historical grounding은 존재하는 Concept K를 요구하지만 이후 retired된 K를 허용한다. Unknown/non-Concept K는 retired LO에도 금지한다. Historical reference를 current active grounding으로 오해하지 않는다.

### Coverage와 quota의 구별

Ontology §13.2의 **Working/Deep 핵심 Concept에는 measurable Learning Objective가 있어야 한다**는 의무를 보존한다. 후속 target/curriculum context가 정해졌을 때 coverage를 확인한다. 이는 현재 모든 504 Concepts에 최소 1개를 생성하거나, Concept당 정확히 N개·macro별 같은 개수·graph degree 비례 수량을 요구하는 규칙이 아니다. Objective 수는 실제 performance decomposition으로 결정한다.

## 5. Observable-performance admissibility

중심 질문은 “학습자가 관찰 가능한 조건에서 무엇을 수행할 수 있는가”다. Statement는 action, performance object, identity를 구별하는 핵심 조건과 범위를 판별할 만큼 구체적이어야 한다. 모든 objective에 정형화된 조건 문구를 강제하지는 않는다.

`understand`, `know`, `be familiar with`, `learn`, `appreciate`처럼 mental state만 표현하는 동사는 중심 observable action으로 인정하지 않는다. `calculate`, `derive`, `construct`, `identify`, `classify`, `compare`, `explain`, `interpret`, `diagnose`, `analyze`, `prove`, `design`, `select and justify`, `apply`는 가능한 예이며 canonical enum이나 자동 승인 목록이 아니다. Bloom taxonomy를 schema로 만들지 않는다.

Observable verb를 사용해도 수행 대상·조건·범위가 모호하면 editorial review를 통과하지 못한다. Explanation은 관찰 가능한 설명 산출을 요구해야 하며 단순히 “알고 있다”의 대용 표현이어서는 안 된다. Reading/completion 여부는 mastery evidence가 아니다.

하나의 coherent performance를 이루는 계산과 결과 해석, 선택과 정당화는 함께 표현할 수 있다. 독립적으로 달성·평가할 수행을 편의상 묶었다면 분리를 검토한다. 동사 개수만으로 split을 강제하지 않는다. Semantic duplication은 다른 wording이나 grounding 목록만으로 정당화되지 않는다.

## 6. Lifecycle and identity continuity

Continuity test: 기존 LO reference를 따라간 사람이 변경 후에도 같은 learner performance를 요구받는가? Learner action, performance object, 핵심 조건, 기존 downstream reference의 의미를 함께 검토한다. 이는 semantic judgment이며 문자열 similarity threshold가 아니다.

| Change | Policy |
| --- | --- |
| 문법·명료성 개선, 이미 의도한 조건의 명시화, 수행 의도를 유지하는 scope clarification | Continuity 확인 후 SAME LO |
| Action, performance object 또는 핵심 조건이 materially 달라짐 | NEW LO; 옛 수행의 유효성에 따라 기존 LO 유지 또는 retirement |
| True split: 독립 수행 bundle을 분리하여 원본을 유지할 이유가 없음 | 원본 retired; 모든 successor는 NEW LO |
| True merge: 기존 수행들을 새로운 통합 수행이 대체함 | 원본들 retired; 통합 수행은 NEW LO |
| 기존 수행들이 여전히 유효한 상태에서 통합 수행 추가 | 기존 LO 유지; 통합 수행은 NEW LO |
| 동일 수행의 duplicate | 의미 검토로 survivor 하나 유지, duplicate retired; 먼저 공식 발급된 LO를 우선하고 예외 이유 기록 |

`retired`는 terminal state다. 부활·삭제·ID 재사용을 금지하며 마지막 statement/grounding과 retirement reason을 tombstone으로 유지한다. 특정 curriculum의 미사용, elective 전환, 출판 미노출 자체는 retirement 이유가 아니다. Successor가 없는 retirement도 가능하다.

Retirement 전에 현재 존재하는 Objective Dependencies, Prerequisite/Evidence Requirements, Task Models/Exercises, Curriculum/Pathway 및 publication cross-references 등 모든 current reference를 찾아 각각 migrate/split/remove를 의미 검토하고 결과를 검증한다. References가 없으면 검색 범위와 없음의 확인을 기록한다. Historical references와 tombstones는 보존한다.

Reason, successor가 있으면 그 identity, continuity 판단 및 reference-audit 결과는 추적 가능한 repository 변경 기록에 남긴다. Lineage는 자동 reference rewrite 규칙이 아니다. 이번에는 별도 LO lineage file/full schema나 `split_into`, `merged_into`, `replaced_by` 같은 inline fields를 만들지 않는다. 실제 lifecycle event가 필요할 때 후속 설계에서 정형 lineage storage를 검토한다.

Schema와 record의 일반 revision은 Git history로 관리한다. Per-record `schema_version`, `revision`, version counter는 두지 않는다. Issuance/non-reuse/terminal retirement 검증은 current snapshot뿐 아니라 canonical history와 대조해야 한다.

## 7. Deterministic serialization

미래 canonical registry path는 `learning/objectives.jsonl`이다. 이 schema-only checkpoint에서는 empty file도 생성하지 않는다. Human-readable catalog를 만들 경우 JSONL의 derived view로 두며 별도 canonical source를 운영하지 않는다.

- UTF-8, no BOM, LF-only, final newline.
- Physical line당 JSON object 하나. String 내부 줄바꿈은 필요한 JSON escape로 표현한다.
- Compact standard JSON; comma/colon 뒤 불필요한 공백 없음. 읽을 수 있는 Unicode는 그대로 보존하고 필요한 escaping은 수행한다.
- Blank records, comments, trailing commas, duplicate object members, NaN/Infinity 금지.
- Numeric LO ID ascending; `concepts`는 numeric K ascending. Lexical sort로 대체하지 않는다.
- Field order: `id` → `statement` → `concepts` → `status` → `retirement_reason`. 존재하는 field만 이 순서로 쓴다. 이는 deterministic serialization convention이며 JSON key order에 의미를 부여하지 않는다.

## 8. Mastery boundary

Ontology §5.3의 일반 수행 수준을 유지한다.

| Level | Mastery |
| --- | --- |
| 0 | Unfamiliar |
| 1 | Recognition |
| 2 | Operational |
| 3 | Conceptual |
| 4 | Derivational / Transfer |

Mastery는 objective의 immutable intrinsic field가 아니다. `LO.mastery`는 저장하지 않는다. 후속 Prerequisite Requirement, curriculum target/profile, evidence/mastery judgment에서 필요한 수준과 관찰 증거를 연결한다.

같은 LO를 참조하는 Course A와 B가 서로 다른 required mastery threshold를 요구할 수 있다. 그러나 threshold가 LO의 수행 의미를 바꾸지는 않는다. 계산 수행에 더 높은 숫자를 붙이는 것만으로 derivation/transfer 수행이 되지 않으며, 핵심 수행이 달라지면 다른 objective가 필요하다. 개별 정답 하나로 mastery 전체를 입증하지 않는 Ontology §6.1도 유지한다.

## 9. Target Depth boundary

Ontology §5.4의 `Overview`, `Working`, `Deep`은 책의 설명 깊이이며 Mastery와 별도 축이다. Objective intrinsic property로 `target_depth`를 저장하지 않는다. 후속 target/profile 또는 Prerequisite Requirement에서 관련 context를 연결한다. Depth나 mastery로 LO ID/순서를 encode하지 않으며 이번에는 값을 배정하지 않는다.

## 10. Curriculum and publication boundary

Ontology §5.5·§11.5에 따라 terminal/enabling은 특정 Curriculum/Pathway 안에서의 역할이다. `terminal`, `enabling`, core/recommended/enrichment, required/elective, chapter/course role을 objective record에 넣지 않는다. 같은 objective가 다른 pathway에서 다른 역할을 맡을 수 있다.

Chapter, volume, publication order와 visibility는 objective identity가 아니다. Ontology §12.1·§13.7의 learner-facing 목표와 자기학습에 필요한 정보 제공, learner closure 의무는 유지한다. 이번에는 curriculum/publication storage를 정의하지 않는다.

## 11. Objective Dependency and Prerequisite Requirement boundary

Ontology §5.2의 Objective Dependency를 인정하며 정밀 learning dependency의 중심은 Objective Graph다. Ontology §2.2·§5.6에 따라 required prerequisite에는 reason, required mastery, target Learning Objective 또는 target depth가 필요하다. Ontology §13.1의 required-prerequisite acyclicity도 유지한다.

Objective record에는 `requires`, `prerequisites`, `depends_on`, `required_by` arrays를 넣지 않는다. Bare LO adjacency만으로 정밀 prerequisite를 canonicalize하지 않는다.

[Prerequisite Requirement Schema v0.1](PREREQUISITE_REQUIREMENT_SCHEMA.md)은 공식 source LO와 실제 필요한 `performance`·명시적 partial/whole 범위를 연결한다. Partial에는 `excludes`가 필수이며 원 LO statement가 해당 수행을 직접 포함해야 한다. 전체 LO 이수 의무나 자동 LO split을 뜻하지 않는다. 현재 profile은 target LO 필수·Target Depth optional이며 ability별 Required Mastery와 Depth를 구별한다.

Prerequisite Requirement가 유일한 canonical semantic source이며 [Objective Dependency Schema v0.1](OBJECTIVE_DEPENDENCY_SCHEMA.md)은 **Prerequisite Requirement → Objective Dependency projection**을 정의한다. Projection은 source commit·Requirement ID·route/pointer·부분 수행·Context·Mastery와 query를 보존한다. OR 대안은 동시 의무가 아니며 `recommended`, `deepens`는 required DAG·진입 차단·필수 closure에 포함하지 않는다. 독립적으로 편집하는 Dependency Registry나 공식 Dependency ID를 만들지 않는다.

모든 active required Requirements의 모든 OR route/AND ability를 포함한 LO 합집합 DAG를 보수적 admission gate로 사용하고 Context별·양립 가능한 전체 조합·선택 route도 검토한다. 배타적 Context의 union-only cycle도 HOLD한다. 합집합은 cycle 검사 전용이며 실제 경로의 필수성 증명이 아니다. Unknown compatibility의 경로 export는 HOLD한다. Concept grounding이나 Semantic Graph에서 prerequisites를 자동 추론하지 않는다.

두 Schema의 정본화는 Registry 생성·PR ID 발급/예약·관계 admission·graph population을 승인하지 않는다. 해당 데이터 작업은 별도 exact admission set 승인으로 남긴다.

## 12. Evidence boundary

Learning Objective는 학습자가 무엇을 수행할 수 있어야 하는지, Evidence Requirement는 달성 판단에 어떤 관찰이 충분한지를 정의한다. Ontology §6의 연결은 Learning Objective → Evidence Requirement → Task Model → Exercise Instances다.

Question type, exercise ID, rubric, pass threshold, 정답 문제 수, Evidence Requirement나 Task Model을 objective record에 넣지 않는다. 중요 objective의 evidence, 복수 evidence form이 필요한 경우의 coverage, observable verb와 Practice/Assessment의 constructive alignment는 후속 설계에서 충족한다. 이번에 evidence/task/practice 생성이나 mastery judgment를 수행하지 않는다.

## 13. Future initial admission and pilot

Initial admission profile은 implicit kind=learning_objective, status=active, 최소 1개 active Concept grounding, observable performance statement와 금지 metadata 부재다. 구조 검사와 semantic review 및 admission 승인을 모두 거쳐 적용한다. 이번에는 profile 정의만 하고 적용하지 않는다.

다음 checkpoint는 **Learning Objective Pilot v0.1**이며 504개 전체 population이 아니다. 권장 12–20 Concepts에 basic mathematics, proof/derivation mathematics, probability/statistics, software engineering, formal methods, classical AI, ML/DL, Transformer/LLM, Agent, Harness, evaluation, safety/security를 의도적으로 포함한다.

Pilot은 pre-population authoring artifact이며 공식 LO ID를 발급·예약하지 않는다. Granularity, multi-objective Concept, multi-Concept performance, wording, duplicate performance, identity continuity, grounding, future mastery/prerequisite compatibility를 stress-test한다. 이후 granularity/identity audit → 필요한 schema correction → pilot freeze → full objective population orchestration design 순서다. 이번 checkpoint에서 pilot을 실행하지 않는다.

## 14. Illustrative fixtures

**ILLUSTRATIVE ONLY — NOT ISSUED — NOT REGISTRY DATA.** 아래 JSONL은 문서 내부의 독립 fixture다. LO 번호는 설명용이며 발급·예약되지 않았다. Fixture marker는 JSON 밖에 있으며 임시 검증이 valid/invalid/editorial 사례를 구분하기 위한 표시다. Canonical data loader의 입력은 미래 registry path 하나뿐이며 Markdown code fences를 population 입력으로 수집하지 않는다.

### Single-Concept performance

Current Registry의 K0105 = Shannon Information and Entropy로 resolve한 예시다.

<!-- LO-FIXTURE single-concept EXPECT=valid CONTEXT=current -->
```jsonl
{"id":"LO0001","statement":"Given a finite discrete probability distribution, calculate its Shannon entropy and explain how the value changes when probability mass becomes more or less concentrated.","concepts":["K0105"],"status":"active"}
```
<!-- /LO-FIXTURE -->

### Multi-Concept performance

K0107 = Cross-Entropy, K0108 = Kullback–Leibler Divergence다. 두 양을 직접 비교하는 하나의 수행이며 임의 primary owner를 지정하지 않는다.

<!-- LO-FIXTURE multi-concept EXPECT=valid CONTEXT=current -->
```jsonl
{"id":"LO0002","statement":"Given two finite discrete probability distributions on the same outcome space, compare their cross-entropy and KL divergence by calculating each quantity, interpreting their difference, and identifying the support conditions for finite values.","concepts":["K0107","K0108"],"status":"active"}
```
<!-- /LO-FIXTURE -->

### Invalid editorial statements

다음은 구조상 valid여도 observable performance가 없어 editorial invalid다. 기계적인 verb blacklist로 의미 검토를 대체하지 않는다.

<!-- LO-FIXTURE understand EXPECT=editorial-invalid CONTEXT=current -->
```jsonl
{"id":"LO0001","statement":"Understand entropy.","concepts":["K0105"],"status":"active"}
```
<!-- /LO-FIXTURE -->

“Know the Transformer.” 역시 수행·대상 조건이 분명한 observable action을 제시하지 않아 editorial invalid다.

### Invalid structural records

<!-- LO-FIXTURE empty-concepts EXPECT=invalid CONTEXT=current -->
```jsonl
{"id":"LO0001","statement":"Calculate entropy.","concepts":[],"status":"active"}
```
<!-- /LO-FIXTURE -->

Empty grounding은 최소 1개 Concept 규칙 위반이다.

<!-- LO-FIXTURE unknown-concept EXPECT=invalid CONTEXT=current -->
```jsonl
{"id":"LO0001","statement":"Calculate entropy.","concepts":["K9999"],"status":"active"}
```
<!-- /LO-FIXTURE -->

K9999는 checkpoint baseline Registry에 없는 unknown endpoint다.

현재 실제 retired K는 0이다. 아래 두 fixture만 독립 가상 Registry에서 K0105가 retired Concept인 상황을 가정하며 실제 K0105의 active 상태를 변경하지 않는다.

<!-- LO-FIXTURE retired-endpoint EXPECT=invalid CONTEXT=synthetic-retired-k0105 -->
```jsonl
{"id":"LO0001","statement":"Calculate entropy.","concepts":["K0105"],"status":"active"}
```
<!-- /LO-FIXTURE -->

Active LO는 retired endpoint를 허용하지 않는다. 반면 다음은 historical tombstone 구조의 예시이며 lifecycle closure를 증명하지 않는다.

<!-- LO-FIXTURE retired-tombstone EXPECT=valid CONTEXT=synthetic-retired-k0105 -->
```jsonl
{"id":"LO0001","statement":"Calculate entropy.","concepts":["K0105"],"status":"retired","retirement_reason":"Superseded by a materially different performance."}
```
<!-- /LO-FIXTURE -->

<!-- LO-FIXTURE terminal EXPECT=invalid CONTEXT=current -->
```jsonl
{"id":"LO0001","statement":"Calculate entropy.","concepts":["K0105"],"status":"active","terminal":true}
```
<!-- /LO-FIXTURE -->

Terminal은 curriculum-relative role이며 unsupported field다.

<!-- LO-FIXTURE depth EXPECT=invalid CONTEXT=current -->
```jsonl
{"id":"LO0001","statement":"Calculate entropy.","concepts":["K0105"],"status":"active","target_depth":"Deep"}
```
<!-- /LO-FIXTURE -->

Target Depth는 objective intrinsic field가 아니다.

<!-- LO-FIXTURE prerequisites EXPECT=invalid CONTEXT=current -->
```jsonl
{"id":"LO0001","statement":"Calculate entropy.","concepts":["K0105"],"status":"active","prerequisites":["LO0002"]}
```
<!-- /LO-FIXTURE -->

Prerequisites는 embedded array가 아니라 후속 Requirement와 dependency projection에서 다룬다.

<!-- LO-FIXTURE duplicate-concepts EXPECT=invalid CONTEXT=current -->
```jsonl
{"id":"LO0002","statement":"Compare cross-entropy and KL divergence.","concepts":["K0107","K0107","K0108"],"status":"active"}
```
<!-- /LO-FIXTURE -->

Concept 중복은 금지한다.

<!-- LO-FIXTURE unsorted-concepts EXPECT=invalid CONTEXT=current -->
```jsonl
{"id":"LO0002","statement":"Compare cross-entropy and KL divergence.","concepts":["K0108","K0107"],"status":"active"}
```
<!-- /LO-FIXTURE -->

Concepts는 numeric K ascending이어야 한다.

## 15. Validation and limits

| 검증 종류 | 확인 대상 |
| --- | --- |
| Mechanical | LO/K syntax·padding, fields/types, standard JSON/serialization/order, ID uniqueness, Concept endpoint existence/type/status, concepts uniqueness/order, status/retirement_reason 계약 |
| History / procedure | Issuance 시점, issued ID 보존·비재사용, monotonic allocation, retired terminal state, tombstone 보존, reference-audit 기록 |
| Editorial | Observable performance, granularity, semantic duplication, multi-Concept appropriateness, identity continuity, statement scope와 grounding 의미 |

Structural validator는 objective 품질이나 semantic continuity, retirement closure를 증명하지 않는다. Mental-state 예시도 구조 검사와 editorial 실패를 분리한다.

이 checkpoint는 문서 fixture와 repository 밖 임시 검증을 사용한다. `scripts/validate_learning_objectives.py`, `tests/test_validate_learning_objectives.py`는 생성하지 않는다. Permanent validator는 pilot/final admission schema가 충분히 stress-test된 후 도입한다.

기존 Registry/Semantic Edge validators와 tests 및 full suite, 상대 links/fragments, git diff --check, 승인된 여섯 파일 변경 범위, 보호 canonical 문서 5개와 두 JSONL의 baseline byte equality, objective/dependency/prerequisite/lineage data 및 새 validator 부재를 확인한다. 실제 검증 결과는 ADR에 기록하고 최종 commit/remote 상태는 완료 보고에서 확인한다. Schema 예시 검토는 pilot 실행이나 objective admission이 아니다.
