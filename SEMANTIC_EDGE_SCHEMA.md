Status: CANONICAL — Semantic Edge Schema v0.1

# Medium Semantic Edge Schema

## 1. 문서 지위와 적용 범위

**Semantic Edge Schema v0.1 remains canonical. Medium Semantic Graph v1 is populated at [registry/semantic_edges.jsonl](registry/semantic_edges.jsonl), with 603 explicitly reviewed Concept↔Concept assertions.** 현재 [Node Registry](registry/README.md)는 504 active Concepts / 0 retired, K0001–K0504이며 다음 K는 K0505다. 이 admission 상태는 검증된 admission commit의 canonical remote `main` 수용 시점부터 적용하며 local/staging 파일 존재만으로 성립하지 않는다.

이 문서는 schema 의미를 유지하며 현재 상태만 동기화한다. 최초 schema-only checkpoint의 검증·미생성 범위는 아래에서 역사적 기록으로 구분한다. 이 문서 자체는 edge나 K를 발급·등록하지 않는다.

Canonical precedence는 [FROZEN Ontology v1.0](ONTOLOGY_V1.md) → [Node Identity](NODE_IDENTITY.md) → [Registry Schema](REGISTRY_SCHEMA.md) → [Macro Skeleton](KNOWLEDGE_GRAPH_L1.md) → [canonical Registry v1](registry/nodes.jsonl) → 이번 implementation specification 순이다. 상위 문서의 의미와 기존 node identity/title/key/home/scope를 변경하지 않는다. 결정 배경은 [ADR 0004](decisions/0004-semantic-edge-schema-v0.1.md), 현재 진행 상태는 PROJECT_STATE에 둔다.

| 관리 대상 | 책임 |
| --- | --- |
| Node Registry | Knowledge object identity |
| Semantic Graph | Knowledge object 사이의 semantic relation |
| Learning Graph | Learning Objective, prerequisite, mastery |
| Registry Lineage | K identity lifecycle provenance |

이번 schema는 두 번째만 다룬다. Node Identity §9의 `requires`·`deepens` 예시는 lineage와 구별되는 넓은 Ontology vocabulary의 설명이며 이번 storage profile의 허용 목록이 아니다. Ontology §4의 prerequisite DAG / general concept connection graph 분리와 §2.2·§5.6의 정밀 prerequisite 원칙을 유지한다. Macro map의 화살표·grouping·hub, canonical key의 dot hierarchy, node boundary는 admitted edge가 아니며 자동 변환하지 않는다.

## 2. Base Semantic Edge Record

Required fields는 다음 세 개뿐이며 optional field는 없다. 모든 값은 JSON string이다.

| Field | Type | Contract |
| --- | --- | --- |
| `source` | string | Current Registry의 active Concept K |
| `relation` | string | §3 Initial Medium Concept Edge Profile의 정확한 literal |
| `target` | string | Current Registry의 active Concept K |

Current assertion의 identity는 **(source, relation, target)** triple이다. 별도 immutable edge ID를 발급하지 않는다. `edge_id`, `status`, `version`, `revision`, `reason`, `confidence`, `weight`, `created_at`, `updated_at`, `author`, `source_document`, `citation`, `claim_status`를 비롯한 모든 추가 field는 v0.1에서 금지한다.

Endpoint는 [Registry Schema §4](REGISTRY_SCHEMA.md#4-identity-key-syntax와-uniqueness)의 K syntax와 padding을 따르며 `registry/nodes.jsonl`에 존재하고 `kind = concept`, `status = active`여야 한다. Unknown K, retired K, non-Concept endpoint와 모든 `source == target` self-edge를 금지한다.

## 3. Initial Medium Concept Edge Profile

Ontology의 Knowledge Relations vocabulary 전체를 변경하지 않고, 첫 Medium Concept↔Concept graph의 canonical storage에 허용하는 operational subset을 아래 **8개**로 제한한다. Directed 6개, symmetric 2개다.

| Relation | Semantics | Direction / admission boundary |
| --- | --- | --- |
| `component_of` | directed | component → whole. Source가 target의 구조적·개념적 구성요소로서 정체성/메커니즘 설명에 실질적으로 참여한다. 단순 사용은 component가 아니다. |
| `generalizes` | directed | more general → specialization. 동일한 중심 지식 질문을 공유하며 target이 source에 제약·특수 구조·특정 조건을 추가한다. 넓은 분야라는 이유만으로 사용하지 않는다. |
| `mathematically_related` | symmetric | 실질적인 수학적 관계를 더 구체적인 profile relation으로 표현하기 어렵거나 부정확할 때만 쓰는 fallback이다. |
| `contrasts_with` | symmetric | 두 peer Concept의 차이를 명시적으로 아는 데 semantic/learning 가치가 클 때 사용한다. 단순히 다른 모든 pair를 연결하지 않는다. |
| `applied_in` | directed | reused Concept/method → consuming Concept. Source의 지식·방법·메커니즘이 target의 구성·실행·정식화에 직접 재사용된다. Constitutive component일 필요는 없다. |
| `used_to_analyze` | directed | analysis Concept/method → analyzed Concept. 이미 정의된 target의 특성·동작·실패·구조를 분석하는 도구나 관점이다. |
| `motivates` | directed | motivating problem/need/structure → motivated Concept. Target 도입의 conceptual need 또는 problem setting을 제공한다. 단순 historical precedence가 아니다. |
| `explains` | directed | explanatory Concept → explained Concept. 동작·구조·현상을 이해하는 conceptual frame이다. `generalizes`, `component_of`, `used_to_analyze`가 더 정확하면 해당 relation을 우선한다. |

`applied_in`은 target을 구성/수행할 때 source를 쓰는 관계이고, `used_to_analyze`는 target을 분석할 때 쓰는 관계다. `mathematically_related`보다 `component_of`, `generalizes`, `applied_in`, `used_to_analyze`로 정확히 표현할 수 있으면 이를 우선한다. Fallback relation으로 graph를 과밀화하지 않는다.

### Ontology vocabulary와 미지원 storage forms

| Relation(s) | Current storage policy | 이유 / 후속 설계 |
| --- | --- | --- |
| `requires`, `recommended`, `deepens` | Initial semantic profile에서 제외 | Learning-order layer에서 다룬다. Bare K→K `requires`를 만들지 않는다. 정밀 required prerequisite에는 reason, required mastery, target Learning Objective 또는 target depth가 필요하다. Recommended/deepens를 required prerequisite로 취급하지 않는다. |
| `specializes` | **Derived inverse only**, 직접 저장 금지 | `A generalizes B`를 저장하고 query/display에서 `B specializes A`를 도출한다. Ontology relation의 삭제·deprecation·보류가 아니라 stored inverse의 중복을 피하는 규칙이다. |
| `identity_or_decomposition` | Initial Profile에서 deferred | `A = B + C`의 n-ary/equation structure, direction, conditions, formal validity를 binary triple 하나로 충분히 표현하기 어렵다. Formal Object 및 identity/derivation 표현과 함께 검토한다. |
| `historically_leads_to` | Initial Profile에서 deferred | Factual/historical Claim 성격이 강하므로 source/provenance 없이 대량 canonicalize하지 않는다. Claim/Evidence provenance와 함께 검토한다. |
| `caused_by`, `manifested_as`, `detected_by`, `mitigated_by`, `enforced_by` | Engineering relations deferred | 현재 Registry는 Concept-only다. Failure Mode, Engineering Invariant, Trade-off 등 Knowledge kinds의 registry 지원 및 endpoint typing과 함께 설계한다. |

## 4. Direction, Duplicate와 Cycle Invariants

Directed relations의 방향은 semantic하다. Numeric K 순서에 맞춰 source/target을 뒤집지 않는다.

Symmetric relations는 정확히 `contrasts_with`, `mathematically_related` 두 개다. Semantic direction은 없지만 canonical serialization orientation은 **numeric(source) < numeric(target)** 이다. 반대 방향 triple은 저장하지 않는다.

- 동일 `(source, relation, target)`의 exact duplicate를 금지한다.
- Symmetric reverse duplicate는 금지하며 reverse orientation 자체가 invalid다.
- `generalizes`와 derived `specializes`를 둘 다 저장하지 않는다.
- 같은 pair에 서로 다른 relation은 각각 독립적으로 §5의 admission test를 통과하면 허용한다. 예를 들어 `A applied_in B`와 `A used_to_analyze B`가 각각 의미 있을 수 있으나 relation 수를 늘리는 것이 목표는 아니다.
- **`component_of` subgraph와 `generalizes` subgraph는 각각 cycle이 없어야 한다.** 2-node reciprocal cycle과 더 긴 cycle 모두 invalid다. Generalization cycle은 identity/scope 모델의 모순으로 본다.
- `applied_in`, `used_to_analyze`, `motivates`, `explains`에는 일반적인 global acyclicity를 요구하지 않는다. Reciprocal/cyclic conceptual relations가 가능하다. 전체 graph나 여러 relation을 합친 graph에 global DAG 규칙을 부과하지 않는다.
- 모든 relation에 self-edge 금지를 적용한다.

## 5. Sparse Curated Graph와 Admission

Semantic Edge Registry는 **Sparse, curated, explicitly reviewed graph**다. Exhaustive relation database가 아니다. 모든 node degree ≥ 1, 전체 graph connected, 모든 macro area 간 연결, hub별 최소 edge 수, 가능한 모든 reuse relation materialization을 요구하지 않는다.

Edge absence는 “두 Concept 사이에 관계가 존재하지 않는다”는 logical assertion이 아니다. “현재 canonical curated graph에서 explicit relation으로 채택되지 않았다”는 뜻이다.

### Directness / Materiality Test

> 이 edge가 없으면 독자가 두 Concept 사이의 중요한 구성·특수화·직접 재사용·분석·대조·설명 관계를 놓치는가?

아니라면 저장하지 않는 것을 기본으로 한다. Functions, Probability, Optimization, Representation, Evaluation 같은 global hubs에서 가능한 모든 downstream connection을 생성하지 않는다. 구조 검사 통과만으로 의미적 admission을 승인할 수 없다.

### No automatic inference/materialization

Canonical JSONL에는 explicitly reviewed triples만 저장한다. `A generalizes B`와 `B generalizes C`로부터 `A generalizes C`를 자동 추가하지 않는다. `component_of` chain도 동일하다. Query tooling은 나중에 transitive closure를 계산할 수 있으나 canonical JSONL은 closure database가 아니다. 도출 가능한 triple도 별도 직접성·실질성 review 없이 채택하지 않는다.

## 6. Canonical Serialization

Canonical path는 [registry/semantic_edges.jsonl](registry/semantic_edges.jsonl)이다. 최초 schema-only checkpoint에서는 생성하지 않았으며 Medium Semantic Graph v1 admission에서 populated되었다.

- UTF-8, no BOM, LF, final newline을 사용한다.
- Physical line 하나당 JSON object 하나를 저장한다. Blank record, comments, trailing comma, duplicate JSON members를 금지한다.
- Standard JSON만 허용한다. NaN/Infinity 등의 비표준 값은 금지한다.
- Compact serialization으로 comma/colon 뒤 불필요한 공백을 넣지 않는다.
- Canonical field order는 아래와 같다. JSON object member order의 의미가 아니라 deterministic serialization convention이다.

```text
source
relation
target
```

File ordering은 **numeric source K → relation ASCII lexical → numeric target K** ascending이다. Symmetric orientation을 먼저 적용한 뒤 같은 규칙으로 정렬한다. K numeric parsing/padding은 Registry Schema를 따른다.

Illustrative sort order only; these are not admitted edges:

```text
K0010 applied_in K0200
K0010 component_of K0050
K0010 generalizes K0030
K0011 applied_in K0020
```

## 7. Node Changes와 Edge Deletion Lifecycle

K identity가 유지되는 title rename, canonical-key rename, macro-area migration, scope refinement는 endpoint 변경을 요구하지 않는다. Edge가 title/key/home 대신 K를 참조하므로 같은 지식 객체로의 reference를 유지할 수 있다.

K retirement 시 그 K가 source/target인 모든 current semantic edges를 review한다. Retired endpoint는 current registry에 남기지 않으며, Node Identity의 current-reference audit와 retirement closure를 따른다. `old K split_into new K1,new K2` 같은 lineage는 semantic rewrite rule이 아니다. Successor마다 관계의 의미를 재검토하고 migrate/split/remove를 판단한다. 자동 successor rewrite를 금지한다.

Edge에는 stable identity를 발급하지 않으므로 assertion이 더 이상 타당하지 않으면 current JSONL에서 제거한다. Edge status=retired, tombstone, renumbering, edge lifecycle/lineage graph를 만들지 않는다. 과거 graph state는 Git history가 보존한다. 미래에 동일 triple이 다시 타당하면 review 후 재등록할 수 있다. 이는 issued K identity의 삭제·재사용 금지와 다르다.

Edge validator는 historical edge deletion이나 동일 triple 재사용을 금지해서는 안 된다. Current graph structural validity와 retired endpoint 부재를 검사한다. Edge 자체를 외부 object로 참조할 강한 요구가 생기면 별도 schema revision으로 ID 도입을 검토한다.

## 8. Proposal, Claim Provenance와 Parallel Authoring

Population에서는 reason/review_note 등 rich working artifact를 사용할 수 있다. **Rich proposal → review/audit → minimal canonical registry**로 진행한다. Reason은 review/admission provenance이며 canonical triple의 field가 아니다. 최초 schema-only checkpoint에서는 proposal artifact를 만들지 않았다. Graph v1은 frozen v0.2 proposal의 세 필드 projection으로 admission되며, 상세 결과는 admission audit에 둔다.

Initial Profile의 edge는 curriculum/editorial Knowledge Graph assertion이다. `foundational_theory`, `established_research`, `frontier_research`, `interpretive_framework`, `practical_heuristic`은 Ontology에 따른 Claim-level status이며 edge 전체에 부여하지 않는다. Factual/research claim의 근거·출처 요구를 없애는 것이 아니다. 특히 historical relation은 Claim/Evidence 설계까지 보류한다.

Graph proposal generation은 병렬화할 수 있으나 worker가 canonical `registry/semantic_edges.jsonl`에 동시에 쓰면 안 된다.

- Worker는 isolated proposal artifact만 작성한다.
- Canonical graph 직접 수정과 다른 batch proposal 직접 수정을 금지한다.
- Cross-batch conflict는 issue로 전달한다.
- 모든 worker 완료 barrier 뒤 fresh-context independent integration auditor가 exact duplicate, reverse symmetric duplicate, relation ambiguity, cross-batch conflict, hub overpopulation, canonical orientation을 통합 검토한다.

```text
E0 Orchestrator
→ E1 ... En isolated proposal workers
→ barrier
→ E-final independent graph auditor
→ edge admission proposal freeze
→ external/design review
→ single integration writer: canonical semantic_edges.jsonl
```

Implementation-specific worker 수는 canonical rule로 고정하지 않는다. 최초 schema-only checkpoint에서는 worker를 실행하거나 edge proposal generation을 시작하지 않았다.

## 9. Illustrative Examples

**Illustrative relation examples. K identifiers are examples unless explicitly resolved from current Registry.** 아래 예시는 모두 **example of possible syntax, not an admitted edge**다. 실제 Registry endpoint를 resolve하여 관계를 승인한 것이 아니다.

### Relation templates

`Kxxxx`, `Kyyyy`는 placeholder이며 valid K ID가 아니다. 실제 record는 §2 endpoint 검사를 통과해야 한다.

```jsonl
{"source":"Kxxxx","relation":"component_of","target":"Kyyyy"}
{"source":"Kxxxx","relation":"generalizes","target":"Kyyyy"}
{"source":"Kxxxx","relation":"applied_in","target":"Kyyyy"}
{"source":"Kxxxx","relation":"contrasts_with","target":"Kyyyy"}
```

Conceptual illustrations: Multi-Head Attention component_of Transformer Block; Fourier Transform applied_in Time–Frequency Audio Features. 이는 방향과 의미를 설명하며 actual K↔K admission이 아니다.

### Independent serialization fixture

다음 fixture는 K0100·K0200·K0300이 active Concepts인 별도 가상 Registry를 가정한다. 현재 K의 실제 의미를 재정의하지 않는다. JSONL 구조·정렬·방향 설명용이며 semantic admission 증거가 아니다.

```jsonl
{"source":"K0100","relation":"contrasts_with","target":"K0200"}
{"source":"K0100","relation":"mathematically_related","target":"K0300"}
{"source":"K0300","relation":"applied_in","target":"K0100"}
```

마지막 directed edge는 source가 target보다 커도 방향을 유지한다.

### Invalid patterns

아래 A/B/C는 서로 다른 가상 active K의 약칭이며 stored ID가 아니다. Unknown/retired는 별도 fixture의 조건이다. 현재 Registry에는 retired K가 없다.

| Pattern | Invalid 이유 / 검토 수준 |
| --- | --- |
| Source 또는 target이 fixture Registry에 없는 K | Unknown endpoint |
| Source 또는 target이 fixture의 retired K | Current endpoint는 active Concept만 허용 |
| `source == target` | 모든 relation에서 self-edge 금지 |
| `A requires B` | Learning-order relation은 Initial Profile 미지원 |
| `A specializes B` 직접 저장 | `B generalizes A`만 저장; specializes는 derived inverse |
| `A identity_or_decomposition B` | 현재 profile에서 deferred |
| `A caused_by B` 등 engineering relation | 현재 profile에서 deferred |
| 동일 `A applied_in B`를 두 번 저장 | Exact duplicate |
| K0200 contrasts_with K0100 | Symmetric numeric orientation 위반 |
| K0100 contrasts_with K0200과 그 반대 동시 저장 | Reverse duplicate 및 orientation 위반 |
| A component_of B, B component_of A | Component cycle |
| A component_of B, B component_of C, C component_of A | 더 긴 component cycle |
| A generalizes B, B generalizes A | Generalization cycle |
| A generalizes B, B generalizes C, C generalizes A | 더 긴 generalization cycle |
| Canonical record에 `reason` 또는 `confidence` 추가 | 세 필드 외 unsupported field |
| Canonical record에 `edge_id` 또는 `status: retired` / tombstone 추가 | Edge stable identity/lifecycle object 미지원 |
| Chain에서 closure edge를 review 없이 자동 materialize | Admission/inference 정책 위반; JSON 구조 검사만으로 판정 불가 |

## 10. Validation과 Historical Schema Checkpoint 경계

[Permanent edge validator](scripts/validate_semantic_edges.py)와 [regression tests](tests/test_validate_semantic_edges.py)는 Graph v1 admission에서 추가되었다. 기존 Node Registry validator의 K/history invariants와 semantic-edge validation을 논리적으로 구분한다. Working-tree 검증은 `python3 scripts/validate_semantic_edges.py`, committed-tree 검증은 `python3 scripts/validate_semantic_edges.py --revision HEAD`로 실행한다.

Current structural checks: JSONL validity, supported fields/types, relation enum/profile, source/target syntax·existence·active Concept typing, self-edge, exact duplicates, symmetric orientation, component_of cycles, generalizes cycles, canonical field/file sorting. Historical edge deletion/reuse 금지 검사는 추가하지 않는다.

Directness/materiality, relation 선택, hub 과밀화, inference provenance, retirement review 완결성은 별도 의미·절차 검토다. Structural validation이 이를 증명하지 않는다.

최초 schema-only checkpoint의 validation은 schema/ADR fields·relation lists·counts·정책과 illustrative fixtures의 임시 정적 대조, 상대 Markdown links, protected bytes, 변경 범위, Registry 보존, `git diff --check`였다. 당시 결과는 실제 graph validation/admission이나 연구적 효과 검증이 아니며 ADR의 validation 기록에 보존한다. Graph v1의 구조 검증과 admission provenance는 별도 admission audit에서 기록한다.

최초 schema-only checkpoint에서는 `registry/semantic_edges.jsonl`, `registry/lineage.jsonl`, edge proposals, permanent edge validator를 생성하지 않았고 `scripts/validate_registry.py`도 수정하지 않았다. Graph v1 admission에서는 semantic edge population과 permanent edge validator만 추가했다. Learning Objective, Prerequisite Requirement, Registry lineage 및 추가 K issuance는 이 admission 범위 밖이다.
