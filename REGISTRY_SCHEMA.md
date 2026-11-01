Status: CANONICAL — Registry Schema v0.1

# Medium Knowledge Registry Schema

## 1. 문서 지위와 지원 범위

**Registry Schema v0.1 is canonical and was canonicalized before the first Registry population.** 당시 schema-only checkpoint에서는 admission과 K issuance가 0이었으며 Registry를 생성하지 않았다. 현재 Registry 상태는 [registry/README.md](registry/README.md)와 PROJECT_STATE.md에서 관리한다. 이 문서는 schema를 정의하며 자체적으로 admission을 수행하지 않는다. 아래의 “이번 checkpoint” 및 미생성·후속 작업 설명은 당시 schema canonicalization의 범위와 provenance를 기록한다.

이 schema는 [FROZEN Ontology v1.0](ONTOLOGY_V1.md)의 **Medium-resolution Concept records**를 직렬화한다. [Stable Node Identity](NODE_IDENTITY.md)는 identity·allocation·lifecycle의 authoritative rule이고, [Macro Skeleton v0.2](KNOWLEDGE_GRAPH_L1.md)는 현재 60개 macro-area key의 기준이다. 이 문서는 세 문서의 의미를 변경하지 않는다. 결정 배경은 [ADR 0003](decisions/0003-registry-schema-v0.1.md)을 참조한다.

현재 지원하는 `kind`는 `concept`뿐이다. Ontology 전체 Knowledge kinds의 complete serialization을 지원한다고 주장하지 않는다. Node Identity의 YAML, `type`/`role`, inline lineage 사례는 identity 설명용이며 이 schema의 field 이름이나 serialization을 미리 확정한 record가 아니다.

404-candidate snapshot은 PRE-ADMISSION / NON-REGISTRY로 유지한다. 이 schema는 candidate를 admission하거나 per-candidate scope를 완성하지 않는다. Snapshot의 당시 다음 단계 설명은 checkpoint history이며 현재 진행 상태는 PROJECT_STATE에서 관리한다.

## 2. Base Concept Record

아래 required fields는 active와 retired 모두에 존재한다. 문자열은 공백만으로 된 값을 허용하지 않는다. Optional field에 값이 없으면 생략하며 `null`을 사용하지 않는다. v0.1 record는 아래 표와 §3의 조건부 field만 지원한다. 정의되지 않은 field를 임의 추가하지 않는다.

### Required fields

| Field | JSON type | Semantics / validation |
| --- | --- | --- |
| `id` | string | Immutable Knowledge Graph identity. §4의 K 형식과 NODE_IDENTITY의 allocation·issuance 규칙을 따른다. |
| `canonical_key` | string | Human-readable semantic locator. Stable identity가 아니며 동일 K에서 rename 가능하다. §4의 syntax·history reservation을 따른다. |
| `title` | string | Human-facing canonical display title. Global uniqueness를 요구하지 않는다. |
| `kind` | string | Literal `concept`만 지원한다. |
| `macro_area` | string | 하나의 canonical home. Active는 current Macro Skeleton key 정확히 하나, retired는 retirement 당시 마지막 home이다. Array는 허용하지 않는다. |
| `scope` | string | Concept가 소유하는 semantic 범위. 하나의 중심 질문과 intended scope를 식별할 만큼 구체적이어야 한다. 고정 글자 수 제한은 없다. |
| `status` | string | `active` 또는 `retired`. Candidate는 registry status가 아니다. |

### Optional fields

| Field | JSON type | Semantics / validation |
| --- | --- | --- |
| `concept_type` | string | Ontology 대표 type: `concept`, `operation`, `mechanism`, `method`, `system`, `phenomenon`, `engineering_pattern`. 억지 분류하지 않으며 없어도 admission 가능하다. |
| `concept_role` | string | `atomic`, `bridge`, `integration`. Medium-resolution이라는 이유로 `atomic`을 자동 부여하지 않는다. |
| `aliases` | array of strings | 자연어 용어, 약어, 역사적·분야별 명칭. Global uniqueness는 요구하지 않는다. |
| `former_keys` | array of strings | 동일 K가 canonical repository history에서 과거 사용한 canonical key. 각 값은 §4 syntax를 따른다. 다른 K나 provisional candidate의 key를 가져오지 않는다. |
| `boundary` | object | Scope 보완용 authoring/semantic metadata. 아래 규칙을 따른다. Graph edge가 아니다. |

List entry도 공백만으로 된 문자열을 허용하지 않는다. 값이 없는 optional list는 빈 array 대신 생략한다. `aliases`와 `former_keys` 각각의 list 내부에서 동일 문자열 duplicate를 금지한다. 별도의 case-folding이나 자연어 동의어 정규화를 identity 규칙으로 만들지 않는다.

`boundary`의 지원 member는 `includes`와 `excludes`이며 각각 optional string array다. 존재하면 둘 중 최소 하나에 non-empty entry가 있어야 한다. 값이 없는 쪽은 생략한다. Boundary 문자열로 `requires`, `component_of` 등의 edge를 선언하지 않는다.

다음 상황에서는 admission review에서 boundary 작성을 강하게 요구한다. 이는 모든 Concept에 boundary를 기계적으로 강제하거나 자동 admission 판정을 내리는 규칙은 아니다.

- Canonical-home 충돌을 겪었거나 cross-domain ambiguity가 큰 Concept
- Bridge / integration node
- 이름이 유사한 adjacent node가 있는 경우
- Scope만으로 semantic ownership이 명확하지 않은 경우

## 3. Active / Retired와 Initial Admission Profile

| Validation | `active` | `retired` |
| --- | --- | --- |
| Base required fields | 모두 필요 | 모두 필요; tombstone 삭제 금지 |
| `macro_area` | Current Macro Skeleton의 valid key | Retirement 시점의 마지막 canonical home 보존 |
| `retirement_reason` | Field 존재 금지 | Non-empty string 필수 |
| Lifecycle | NODE_IDENTITY에 따른 운영 | Terminal state; active로 부활·K 재사용 금지 |

`retirement_reason`은 retired에만 필요한 조건부 field다. 현재 정의된 **대표 vocabulary**는 `duplicate`, `true_split`, `true_merge`, `erroneous_concept`, `superseded_by_semantically_different_node`다. 이는 exhaustive ontology enum이 아니다. 구조 검사는 non-empty string을 요구하며, 새로운 canonical reason의 도입은 schema/identity compatibility 검토를 거친다.

미래 Macro Skeleton revision 때 retired record의 `macro_area`를 current key에 억지로 맞추지 않는다. Current-macro membership 검사는 active에만 적용한다. Retired home의 역사적 타당성은 retirement 시점의 canonical history와 대조한다. Active reclassification은 identity continuity를 유지하면 SAME K이며, rename이 없으면 `former_keys`를 만들지 않는다.

Retirement reason의 존재만으로 retirement closure가 완료되는 것은 아니다. NODE_IDENTITY의 reason에 맞는 lineage, current-reference audit와 semantic migration 검토가 필요하다. Successor가 없는 retirement도 가능하다. Lineage serialization은 §7의 별도 후속 작업이다.

### Initial Medium Concept Admission Profile

Base schema와 최초 batch의 admission profile을 구분한다. 현재 404-candidate batch에서 **실제로 admission된 Concept**의 최초 record에 적용할 추가 제약은 다음 두 개다.

- `kind = concept`
- `status = active`

404개 모두에게 K를 주는 규칙이 아니다. Per-candidate scope/boundary normalization, proposed title/key/home review, final admission audit와 admission set approval 이후 적용한다. 이번 checkpoint에서는 profile을 정의만 하고 적용하지 않는다. 최초 batch에는 retired record가 없다.

운영 순서는 candidate review → admission → single-writer K allocation → validation → canonical registry commit이다. Allocation 전 canonical main을 동기화하며 공식 issuance 시점은 NODE_IDENTITY에 따라 canonical registry commit이 main history에 받아들여진 순간이다.

## 4. Identity, Key Syntax와 Uniqueness

### K identity

`id`는 `K` + 최소 4자리 decimal이며 번호는 양의 정수다. 예: `K0001`, `K0127`, `K9999`, `K10000`. 이 문서의 모든 구체적 K는 설명용이다.

구조 검사는 ASCII full-match `K[0-9]{4,}`에 더해 숫자 부분이 양수이고, 해당 양의 정수를 최소 4자리로 zero-padding한 결과와 정확히 같은지 대조한다. 따라서 `K0000`, `K00000`, `K001`, 불필요하게 padding한 `K00001`은 invalid다. Numeric sort는 문자열 사전순이 아니라 숫자 부분의 정수 순서다.

Issued K는 삭제·재사용·재번호화하지 않는다. 최초 allocation은 K0001부터, 이후는 retired와 canonical issuance history를 포함한 최대 issued 번호 다음부터 단조 증가한다. Gap backfill이나 분야별 range 예약은 금지한다. 실제 allocation은 이 checkpoint 밖이다.

### Canonical key syntax

NODE_IDENTITY의 lowercase dot-separated semantic namespace와 segment 내부 underscore 규칙을 다음 ASCII **full-match** syntax로 구체화한다.

```regex
[a-z][a-z0-9]*(?:_[a-z0-9]+)*(?:\.[a-z][a-z0-9]*(?:_[a-z0-9]+)*)+
```

최소 두 segment를 dot로 연결하고 각 segment는 소문자로 시작한다. 이후 소문자·semantic 숫자와 내부 underscore를 허용한다. 공백, 대문자, hyphen, 빈 segment, 선행·후행·연속 underscore는 허용하지 않는다. 이 syntax는 이번 schema의 serialization convention이며 Ontology kind 정의의 변경이 아니다.

Chapter/part/order/macro numbering을 encode하지 않는다. Current macro key를 기계적으로 prefix하는 규칙도 없다. 숫자를 허용하는 것은 의미상 필요한 명칭을 위한 것이며 순서 encoding 허가가 아니다. 이러한 naming stability와 의미 검토는 regex만으로 판정할 수 없다. Dot hierarchy는 `component_of`, `requires` 등의 relation을 자동 의미하지 않는다.

### Uniqueness / history reservation

- Retired를 포함한 모든 record의 `id`와 current `canonical_key`는 각각 globally unique다.
- 한 K의 canonical repository history에 등장한 current/former key는 다른 K에 재사용하지 않는다. Retired K의 key도 예약을 유지한다.
- Canonical key rename은 동일 K를 유지하고 이전 key를 `former_keys`에 남긴다. Current key가 자신의 `former_keys`에 동시에 존재하면 invalid다.
- Duplicate merge에서도 다른 K의 key를 survivor의 current/former key로 이전하지 않는다. 원래 tombstone과 별도 lineage를 통해 조회한다.
- Title·alias는 globally unique하지 않아도 된다. Alias ambiguity 자체는 identity violation이 아니다. Alias와 former identifier를 혼합하지 않는다.
- Current snapshot의 중복 검사만으로 canonical history reservation을 증명할 수 없다. Historical key 삭제·재사용 여부는 Git의 canonical registry history와 대조한다.

### Candidate handle != canonical_key

`probability.conditional_distributions`, `transformer.kv_cache`, `harness.verification`은 현재 snapshot의 provisional candidate handles다. Schema canonicalization이나 snapshot commit은 이를 canonical key로 승격·예약하지 않는다. `former_keys` history도 발생시키지 않는다.

후속 admission review에서 handle을 그대로 채택하거나 rename / split / merge / drop할 수 있다. Handle 문자열이 schema regex를 통과해도 canonical admission이나 key 소유권을 뜻하지 않는다. Candidate provenance와 origin handle은 Concept record field가 아니다.

## 5. JSONL Canonical Serialization과 Version Management

Canonical node serialization은 **JSON Lines (`.jsonl`)**다. 향후 실제 registry의 권장 canonical path는 `registry/nodes.jsonl`이다. **이번 schema-only checkpoint에서는 이 파일을 생성하지 않는다.**

- UTF-8, BOM 없이 LF line ending과 마지막 newline을 사용한다.
- Physical line 하나당 JSON object 하나를 저장한다. String 내부 줄바꿈은 JSON escape로 표현한다.
- Blank record, comment, trailing comma, 중복 object member를 금지한다. Standard JSON을 사용하며 NaN/Infinity 같은 비표준 값도 허용하지 않는다.
- Optional field는 값이 없으면 생략한다. `null`이나 빈 optional list로 채우지 않는다.
- Records는 numeric K ID ascending order로 정렬한다.
- Canonical writer는 한 줄에 compact JSON을 쓰고 comma/colon 뒤의 불필요한 공백을 넣지 않는다. 읽을 수 있는 Unicode 문자열은 그대로 보존하며 필요한 JSON escaping은 수행한다.

JSON object의 key order는 **semantic하지 않다**. Git diff readability를 위한 deterministic serialization convention으로 다음 순서를 고정한다. 존재하는 field만 이 상대 순서로 쓴다.

```text
id
canonical_key
title
kind
concept_type
concept_role
macro_area
scope
boundary
aliases
former_keys
status
retirement_reason
```

Boundary member는 존재하는 것만 `includes`, `excludes` 순서로 쓴다. List entry는 저장된 순서를 보존한다. Identity uniqueness와 list 내부 duplicate 검사는 순서와 별개다.

`schema_version`, `node_version`, `revision` 같은 per-record version counter를 두지 않는다. Schema definition은 이 문서와 Git history가, 개별 node revision은 Git이 관리한다. Migration이 필요하면 명시적인 repository-level migration으로 수행한다.

향후 human-readable catalog는 canonical JSONL로부터 생성할 수 있다. Markdown/YAML catalog를 두 번째 canonical source로 운영하지 않는다.

## 6. Admission Criteria와 Record Data의 구분

Admission은 구조 검증과 의미 검토를 함께 요구한다. 아래 질문의 답이나 pass boolean을 Concept record에 저장하지 않는다. `cohesion_pass`, `duplicate_pass`, `practice_pass` 등은 supported fields가 아니다.

| Criterion | Admission review question |
| --- | --- |
| Cohesion | 하나의 중심 질문으로 설명 가능한가? |
| Objective viability | 독립적이고 observable한 Learning Objective를 만들 수 있는가? |
| Prerequisite coherence | 필요한 prerequisite의 reason·mastery·target objective/depth를 일관되게 정의할 수 있는가? |
| Downstream coherence | Downstream에서 독립적으로 재사용되는가, dependency 차이가 분리를 요구하는가? |
| Practice coherence | 별도 Practice Bank의 필요성 및 학습 수행 범위가 Concept 경계와 맞는가? |
| Canonical home | 현재 macro-area 하나를 home으로 정할 수 있는가? |
| Boundary clarity | Scope와 필요한 includes/excludes로 이웃 Concept와 구별되는가? |
| Duplicate check | 기존 또는 함께 검토 중인 지식 객체와 중복되지 않는가? |
| Knowledge-object identity | 제목 묶음이나 출판 단위가 아니라 지속적인 Concept identity인가? |
| Naming stability | Proposed title/key가 순서·일시적 배치에 의존하지 않고 의미를 나타내는가? |
| Ontology-layer correctness | Learning, Claim, Exposition, Practice 등 다른 layer 객체를 Concept로 잘못 등록하지 않았는가? |

이 질문들은 이번 404개 candidate에 대해 재실행하거나 통과 판정하지 않는다. 구조적으로 valid한 illustrative record도 admission·semantic completeness를 입증하지 않는다.

## 7. Canonical Home와 Layer / Graph Separation

Active Concept에는 하나의 canonical macro home만 있다. Cross-domain reuse를 `macro_area` array로 표현하지 않는다.

- Gradient Descent의 home은 `MATH-OPT`; DL/RL에서의 reuse는 향후 semantic relations / Occurrences로 표현한다.
- Transformer KV Cache Mechanism의 home은 `TRANSFORMER`; KV-cache memory management는 `AI-SYSTEMS`의 별도 systems Concept로 검토한다.

이 설명은 candidate의 scope를 최종 확정하거나 edge를 생성하지 않는다. Macro map의 대표 주제에는 reuse가 포함될 수 있으므로 등장 영역을 모두 node membership으로 변환하지 않는다.

| 별도 관리 대상 | Node record에서 제외하는 data와 이유 |
| --- | --- |
| Learning Layer | Learning Objective, Objective Dependency, required mastery, target depth, prerequisite reason, Prerequisite Requirement. Concept identity와 학습 수행 요구를 구분한다. |
| Evidence / Practice Layer | Evidence Requirement, Task Model, Exercise, Practice Bank, Essential 여부, practice counts. 학습 증거와 활동 설계를 Concept에 중복하지 않는다. |
| Exposition Layer | Primary explanation / review / re-entry 위치, publication occurrence·visibility. 지식 자체와 설명 위치·출판 projection을 구분한다. |
| Epistemic Layer | Claim, Claim Status, citation, source, `last_reviewed`, `valid_as_of`. 근거와 시간적 유효성은 claim 단위로 추적한다. |
| Curriculum / 별도 authoring 설계 | `core`, `recommended`, `enrichment`는 curriculum-relative이며 Concept absolute property가 아니다. `spine`, `branch`, generic node-level `maturity`도 v0.1 field로 정의하지 않는다. |
| Derived authoring signals | Graph centrality/reuse는 graph에서 얻는 검토 신호이며 canonical manually-entered node property가 아니다. |
| Candidate / 작업 이력 | Candidate provenance, origin candidate handle, author/session metadata는 admission 입력·작업 provenance이며 Concept의 semantic record에 넣지 않는다. |

특히 `foundational_theory`, `established_research`, `frontier_research`, `interpretive_framework`, `practical_heuristic`은 Concept 전체가 아니라 Claim의 status다. 위 제외는 Ontology의 학습·근거·출판 요구를 없애는 것이 아니라 해당 layer에서 관리한다는 뜻이다.

Node record 내부의 `requires`, `applied_in` 등 adjacency list를 canonical edge source로 두지 않는다. Node Registry, Semantic Graph, Registry Lineage는 서로 분리한다. 향후 `registry/semantic_edges.jsonl`, `registry/lineage.jsonl` 같은 경로가 가능하지만 이번에는 파일이나 full schema를 만들지 않는다.

Registry lineage의 `split_into`, `merged_into`, `duplicate_of`, `replaced_by`, `extracted_to`는 Ontology semantic relations와 다른 graph의 vocabulary다. NODE_IDENTITY의 target 존재·cycle 금지·reference audit 규칙은 유지한다. **Lifecycle lineage는 semantic edge를 자동 rewrite하지 않는다.**

Bare Concept-level prerequisite를 무분별하게 만들지 않는다. Ontology의 정밀한 required prerequisite는 reason, required mastery, target Learning Objective 또는 target depth를 필요로 한다. Detailed `requires`는 후속 Learning Objective / Prerequisite Requirement 설계와 함께 다루며 node schema에는 prerequisite field를 넣지 않는다.

## 8. Illustrative Examples

**Illustrative only — not issued K IDs / not registry entries.** 아래 모든 K·key·record·변경 전후 상태는 독립적인 설명용 fixture다. K/key 발급·예약이나 404개 candidate의 admission을 뜻하지 않는다. 서로 다른 시점의 before/after를 하나의 registry에 중복 저장하지 않는다. JSONL 예시는 한 physical line당 object 하나다.

### 8.1 Minimal active Concept

```jsonl
{"id":"K0001","canonical_key":"probability.conditional_distribution","title":"Conditional Distribution","kind":"concept","macro_area":"MATH-PROB","scope":"조건을 부여했을 때 확률분포가 어떻게 정의되는지와 조건에 따른 분포의 해석을 다룬다.","status":"active"}
```

### 8.2 Concept with concept_type / cross-domain reuse

```jsonl
{"id":"K0002","canonical_key":"optimization.gradient_descent","title":"Gradient Descent","kind":"concept","concept_type":"method","macro_area":"MATH-OPT","scope":"미분 가능한 목적함수의 음의 gradient 방향으로 반복 갱신하는 최적화 방법과 step size의 역할을 다룬다.","status":"active"}
```

DL/RL에서 사용해도 home은 하나다. `applied_in`이나 추가 macro membership을 record에 넣지 않는다.

### 8.3 Integration Concept with boundary

```jsonl
{"id":"K0003","canonical_key":"decision.state_observation_belief","title":"State–Observation–Belief Relationship","kind":"concept","concept_role":"integration","macro_area":"AI-DECISION","scope":"부분 관측 의사결정에서 환경 상태, 관측, belief가 어떤 서로 다른 역할을 가지며 어떻게 연결되는지 설명한다.","boundary":{"includes":["환경 상태와 관측의 구별","의사결정에 사용하는 belief의 역할"],"excludes":["Agent 실행 ledger와 checkpoint의 영속성"]},"status":"active"}
```

### 8.4 Canonical-key rename + former_keys

동일 identity의 이전 canonical key가 `probability.conditional_prob_distribution`이었다는 가상의 history 뒤 상태다. Alias는 자연어 명칭이며 이전 identifier와 다르다.

```jsonl
{"id":"K0127","canonical_key":"probability.conditional_distribution","title":"Conditional Distribution","kind":"concept","macro_area":"MATH-PROB","scope":"조건에 따른 확률분포의 정의와 해석을 다룬다.","aliases":["conditional law"],"former_keys":["probability.conditional_prob_distribution"],"status":"active"}
```

§8.1과 §8.4는 별도 fixture다. 같은 registry에 넣으면 다른 K의 current key 중복으로 invalid다.

### 8.5 Retired Concept

```jsonl
{"id":"K0332","canonical_key":"information.surprisal","title":"Surprisal","kind":"concept","macro_area":"MATH-INFO","scope":"단일 사건의 확률에 따른 자기정보량을 다룬다.","status":"retired","retirement_reason":"duplicate"}
```

이는 node 구조만의 예시다. 완전한 retirement closure에는 별도 duplicate lineage와 current-reference audit가 필요하다. Survivor의 K나 다른 K의 key를 이 record의 `former_keys`로 옮기지 않는다.

### 8.6 Macro migration

설명용 before/after이며 실제 과거 registry가 있다는 뜻은 아니다. Autoencoder의 home을 DL에서 REP로 재분류해도 지식 identity와 key가 같으면 SAME K다. 현재 home은 REP이며 before는 역사적 fixture다.

Before:

```jsonl
{"id":"K0400","canonical_key":"representation.autoencoder","title":"Autoencoder","kind":"concept","macro_area":"DL","scope":"입력을 잠재 표현으로 인코딩하고 복원하는 학습 구조와 재구성 목적을 다룬다.","status":"active"}
```

After:

```jsonl
{"id":"K0400","canonical_key":"representation.autoencoder","title":"Autoencoder","kind":"concept","macro_area":"REP","scope":"입력을 잠재 표현으로 인코딩하고 복원하는 학습 구조와 재구성 목적을 다룬다.","status":"active"}
```

별도 미래 revision 가정에서 MATH-INFO key가 current set에서 사라져도 §8.5의 retired record는 `macro_area: MATH-INFO`를 유지한다. 같은 key를 가진 active record는 새 current classification으로 migration해야 한다. 이 가정은 실제 Macro Skeleton revision이 아니다.

### 8.7 Cross-domain mechanism boundary

```jsonl
{"id":"K0500","canonical_key":"transformer.kv_cache_mechanism","title":"Transformer KV Cache Mechanism","kind":"concept","concept_type":"mechanism","macro_area":"TRANSFORMER","scope":"Autoregressive Transformer decoding에서 과거 token의 key/value를 재사용하여 반복 계산을 줄이는 메커니즘을 다룬다.","boundary":{"includes":["과거 token의 key/value 재사용"],"excludes":["Serving 시스템의 cache 메모리 할당과 eviction 정책"]},"status":"active"}
```

### 8.8 Invalid patterns

| Pattern | Invalid 이유 / 검토 수준 |
| --- | --- |
| Candidate에 admission 전 `id: K0001` 부여 | Admission/allocation 절차 위반; 문법 검사만으로 판정 불가 |
| `macro_area: ["MATH-OPT", "DL", "RL"]` | 단일 string home 규칙 위반 |
| Active에 `retirement_reason` 포함 | Lifecycle 조건 위반 |
| Retired에 `retirement_reason` 없음 또는 공백 | 조건부 required 위반 |
| 다른 K가 사용한 canonical key 재사용 | Global uniqueness / history reservation 위반; history 대조 필요 |
| `claim_status: "frontier_research"`를 Concept에 저장 | Unsupported field 및 Epistemic Layer 혼합 |
| Node 내부 `requires: ["K0001"]` | Unsupported adjacency 및 prerequisite 설계 우회 |
| Candidate handle을 자동으로 `canonical_key`로 승격 | Admission/key review 절차 위반; regex 통과와 무관 |
| `core: true` | Unsupported curriculum-relative metadata |
| `kind: "formal_object"`, `formal_type: "theorem"` | v0.1 미지원 kind/field |
| `canonical_key: "Probability.foo"` 또는 `"probability..foo"` | Key syntax 위반 |
| Current key가 자기 `former_keys`에 존재 | Per-record hygiene 위반 |
| `boundary: {}` 또는 `aliases: [""]` | Non-empty metadata 규칙 위반 |
| `schema_version`, `node_version`, `revision` 추가 | Per-record version counter 미지원 |

## 9. Future Extension과 Validation 경계

다음은 명시적 schema extension/revision의 대상이며 v0.1 지원으로 선언하지 않는다.

- Formal Object serialization; Engineering Invariant, Failure Mode, Trade-off, Misconception, Notation, Entity/Role
- Semantic Edge Registry schema와 Registry Lineage serialization details
- Learning Object schemas와 Claim / Evidence Source schemas
- Atomic Knowledge Registry expansion

예를 들어 `kind: formal_object`, `formal_type: theorem`은 미래 설계 가능성일 뿐 현재 valid record가 아니다. Atomic expansion에서도 필요한 kind를 명시적으로 설계하며 현재 Concept schema가 완전한 universal schema라고 가정하지 않는다.

후속 validation은 record 구조·필드·enum·JSONL·정렬·현재 uniqueness 검사, Git canonical history의 issuance·key reservation·retired home 대조, semantic admission·identity continuity·reference audit를 구분한다. 구조 검사만으로 의미적 타당성을 입증하지 않는다.

이번 checkpoint의 validation은 문서 계약과 illustrative valid/invalid fixture의 임시 정적 검사, 링크·diff 및 보호 문서/404 snapshot 보존에 한정한다. 실제 registry validator 실행이나 candidate admission audit 완료로 보고하지 않는다. 영구 validator와 build pipeline은 만들지 않는다.
