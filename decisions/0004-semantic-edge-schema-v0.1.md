# ADR 0004 — Semantic Edge Schema v0.1 Canonicalization

Status: ACCEPTED — 2026-09-11

## Context

[Medium Knowledge Registry v1](../registry/README.md)의 최초 canonical admission으로 493 active Concepts / 0 retired, K0001–K0493 issuance가 완료됐다. 다음 K는 K0494다. 이제 지식 객체 사이의 관계를 표현할 record와 운영 규칙이 필요하지만 실제 graph population은 별도 checkpoint다.

Baseline은 `f8435fbe536baebd2f44e75633430fd375c7b074` (`docs: admit medium knowledge registry v1`)이며 preflight에서 local main, origin/main, actual remote HEAD/main의 일치와 clean working tree를 확인했다. 설계 입력은 사용자가 제공한 “AI Knowledge Book — Semantic Edge Schema v0.1 Canonicalization” 명세와 승인된 계획이다. 이번 작업은 문서 canonicalization과 정적 대조이며 실제 관계 admission이나 별도 graph audit를 수행한 것이 아니다.

[Ontology v1.0](../ONTOLOGY_V1.md)은 FROZEN이다. [Node Identity](../NODE_IDENTITY.md), [Registry Schema](../REGISTRY_SCHEMA.md), [Macro Skeleton](../KNOWLEDGE_GRAPH_L1.md)과 canonical node records를 보존한다. Node Identity의 넓은 semantic vocabulary 예시에 learning-order relations가 등장하지만 이는 새 storage profile을 강제하지 않는다. Ontology의 prerequisite DAG 분리와 정밀 prerequisite 원칙에 맞춰 profile을 제한한다.

## Decision

- [SEMANTIC_EDGE_SCHEMA.md](../SEMANTIC_EDGE_SCHEMA.md)를 canonical Semantic Edge Schema v0.1로 채택한다. **Semantic Edge Schema v0.1 is canonical; the Medium Semantic Graph has not yet been populated.**
- Base canonical record는 required string fields `source`, `relation`, `target`만 갖는다. Optional/extra field는 없다. Assertion identity는 `(source, relation, target)`이며 edge stable ID를 발급하지 않는다.
- Endpoint는 current Registry의 active Concept K만 허용한다. Unknown/retired/non-Concept endpoint와 모든 self-edge를 금지한다.

Initial Medium Concept Edge Profile은 정확히 **8개**, directed **6개**, symmetric **2개**다.

| Relation | Semantics | Direction |
| --- | --- | --- |
| `component_of` | directed | component → whole |
| `generalizes` | directed | more general → specialization |
| `mathematically_related` | symmetric | 수학적 관계의 fallback |
| `contrasts_with` | symmetric | 중요한 peer contrast |
| `applied_in` | directed | reused Concept/method → consuming Concept |
| `used_to_analyze` | directed | analysis Concept/method → analyzed Concept |
| `motivates` | directed | motivating problem/need/structure → motivated Concept |
| `explains` | directed | explanatory Concept → explained Concept |

- `specializes`는 **derived inverse only**다. `A generalizes B`만 저장하고 `B specializes A`는 query/display에서 도출한다. Ontology relation을 삭제·deprecated·deferred로 선언하지 않는다.
- `requires`, `recommended`, `deepens`는 Initial semantic profile에서 제외하고 Learning 설계로 분리한다. `identity_or_decomposition`, `historically_leads_to`, engineering relations인 `caused_by`, `manifested_as`, `detected_by`, `mitigated_by`, `enforced_by`는 Initial Profile에서 deferred다.
- Directed orientation은 semantic하며 numeric K 순서로 뒤집지 않는다. Symmetric relations는 정확히 `contrasts_with`, `mathematically_related`이며 **numeric(source) < numeric(target)** 로만 저장한다. Exact/reverse symmetric duplicate를 금지한다.
- `component_of`와 `generalizes`는 각각의 relation subgraph에서 2-node 및 더 긴 cycle을 금지한다. 다른 directed relations나 전체 graph에 global DAG 규칙을 부과하지 않는다. 같은 pair의 복수 relation은 각자 Directness / Materiality Test를 통과할 때 허용한다.
- Graph는 sparse, curated, explicitly reviewed assertions로 유지한다. 최소 degree·connectivity·hub quota를 요구하지 않으며 edge absence는 관계 부정이 아닌 현재 미채택을 뜻한다. Canonical JSONL에 transitive closure를 자동 materialize하지 않는다.
- 향후 path는 `registry/semantic_edges.jsonl`이다. UTF-8/no BOM/LF/final newline, physical line당 compact standard JSON object 하나, no comments/trailing comma/duplicate members/blank records를 따른다. Field order는 source → relation → target, file sort는 numeric source → relation ASCII lexical → numeric target이다.
- K continuity가 있는 rename/macro migration/scope refinement는 endpoint를 유지한다. Retirement 때 모든 incident current edges를 review하여 retired endpoint를 제거하며 lineage successor로 자동 rewrite하지 않는다.
- 부적절해진 edge는 current JSONL에서 삭제한다. Edge status/tombstone/lineage를 만들지 않는다. Git이 과거 상태를 보존하며 같은 triple의 미래 재등록은 허용한다. Future validator는 historical edge deletion/reuse 금지를 검사하지 않는다.
- Rich proposal의 reason/review_note와 canonical triple을 분리한다. Isolated proposal workers → barrier → fresh-context independent auditor → freeze → external/design review → 단일 canonical integration writer 순서를 후속 운영 원칙으로 둔다. Worker 수는 고정하지 않는다.

## Rationale

### Minimal triple vs rich edge objects

Current semantic assertion과 admission 이유·review 이력을 한 record에 넣으면 editorial workflow와 canonical relation data가 결합된다. Reason/provenance는 rich proposal과 review/audit provenance에 남기고 canonical storage는 최소 triple로 유지한다. Claim Status는 Ontology의 Claim-level 속성이며 edge에 부여하지 않는다. 이 선택은 canonical file 자체만으로 상세 admission 이유를 조회할 수 없다는 비용을 수반한다. Factual/research claim의 출처 요구를 면제하지 않는다.

### Edge ID 없음

K는 지속적인 지식 객체의 identity여서 삭제·재사용 금지가 필요하다. Edge는 current assertion의 triple로 구별할 수 있어 별도 ID allocation, renumbering, tombstone, edge lifecycle graph가 불필요하다. 삭제와 동일 triple 재등록은 Git으로 추적한다. 향후 edge 자체를 외부 object로 참조해야 할 강한 요구가 생기면 명시적 schema revision으로 검토한다.

### Sparse curated graph

가능한 모든 relation이나 global connectivity를 목표로 하면 hub downstream 연결과 약한 관계가 과밀해질 수 있다. Directness / Materiality Test로 독자가 놓치기 쉬운 중요한 관계를 선별한다. 이는 모든 지식 관계의 완전성을 보장하지 않으며 absence를 부정으로 해석할 수 없다는 trade-off다. Mathematically_related는 구체적인 구성·일반화·재사용·분석 relation을 대신하는 편의적 만능 edge가 아니다.

### Generalizes only와 symmetric canonicalization

Generalizes/specializes를 함께 저장하면 같은 assertion의 inverse를 중복 관리해야 한다. Generalizes를 저장하고 specializes를 view로 두면 Ontology vocabulary를 유지하면서 일관성을 확보한다. 두 symmetric relation도 numeric orientation 하나로 저장하여 reverse duplicates와 diff 변동을 줄인다. 이는 serialization 결정이며 semantic direction을 부여하지 않는다.

### Deferred relations

Learning-order relations는 별도 Learning Graph에서 설계한다. 정밀 required prerequisite에는 reason, required mastery, target Learning Objective 또는 target depth가 필요하므로 bare K→K requires로 대신하지 않는다. Recommended/deepens는 required prerequisite가 아니다.

Identity_or_decomposition은 n-ary/equation structure, direction, conditions, formal validity를 다룰 Formal Object 및 identity/derivation 표현이 먼저 필요하다. Historically_leads_to는 factual/historical Claim 성격으로 source/provenance를 요구하므로 Claim/Evidence 구조와 함께 검토한다. Engineering 5개 관계는 Concept-only registry를 넘어 Failure Mode, Engineering Invariant, Trade-off 등의 지원과 endpoint typing을 구체화한 뒤 다룬다. 이러한 profile 제한은 Ontology relation 삭제가 아니다.

### No automatic transitive closure

Canonical storage는 explicitly reviewed assertion registry다. Generalizes/component_of chain에서 도출 가능한 모든 triple을 저장하면 직접 채택한 관계와 추론 결과를 혼동하고 중복·과밀화를 키운다. Query tooling은 나중에 closure를 계산할 수 있으나 canonical materialization에는 독립적인 review가 필요하다.

## Consequences

Schema는 canonical이지만 actual Semantic Graph는 unpopulated다. 이번 변경은 schema, 이 ADR, 두 index, Registry 안내, Project State의 여섯 문서뿐이다. Ontology/Node Identity/Registry Schema/Macro Skeleton/node JSONL은 byte-identical로 유지한다. Semantic edge file, proposal batches, lineage, permanent edge validator, Learning Objective, Prerequisite Requirement, 추가 K issuance를 만들지 않으며 기존 Registry validator도 수정하지 않는다.

후속 작업은 proposal orchestration → isolated batch generation → cross-batch integration audit → admission proposal freeze → external/design review → semantic_edges.jsonl materialization → permanent edge validation → canonical Medium Semantic Graph v1이다. Worker는 canonical graph나 다른 batch를 수정하지 않고 cross-batch conflict를 issue로 전달한다. Independent auditor는 duplicate, reverse symmetric duplicate, relation ambiguity, cross-batch conflict, hub overpopulation, canonical orientation을 통합 검토한다. Learning Objective graph와 Prerequisite Requirement는 이후 별도 단계다.

Future structural validator는 JSONL·supported fields/types·relation profile·endpoint existence/active Concept·self-edge·duplicates·symmetric orientation·component/generalization cycles·sorting을 검사한다. Node K/history invariants와 구별하며 historical edge 삭제/재등록을 금지하지 않는다. Relation 의미, directness/materiality, 자동 추론 여부, retirement audit 완결성은 구조 검사만으로 증명할 수 없다.

이번 validation은 schema/ADR fields와 8/6/2 relation 집합·정책 일치, illustrative fixture의 정적 대조, 보호 bytes, 493-node Registry 보존, 금지 artifacts 부재, 상대 links, 변경 범위, git diff --check다. 실제 수행 결과는 검증 후 아래에 기록하며 실제 edge admission이나 graph semantic audit로 보고하지 않는다.

### Repository static validation — 2026-09-11

임시 repository 밖 script와 문맥 대조로 required fields 3개, profile 8개 / directed 6개 / symmetric 2개의 정확한 집합, inverse 및 미지원 목록의 schema/ADR 일치를 확인했다. Illustrative JSONL field order·compact serialization·sorting, 24개 invalid structural fixture와 별도의 retired endpoint fixture, 허용되는 reciprocal/mixed-relation cycles 및 same-pair multiple relations를 정적으로 확인했다. 자동 closure와 admission/review 규칙은 문맥 검토이며 실제 graph에서 실증한 것이 아니다.

상대 Markdown links 144개와 fragment 1개, 여섯 파일 변경 범위, git diff --check를 통과했다. Baseline 대비 보호 다섯 파일을 포함한 모든 비대상 tracked file은 byte-identical이다. 기존 Registry validator의 working tree/HEAD 검사가 모두 PASS였으며 493 active / 0 retired, K0001–K0493, next K0494가 유지된다. Semantic edge/lineage JSONL, edge proposal, permanent edge validator는 생성하지 않았다. Actual semantic edges admitted = 0이다. Commit/push 결과는 checkpoint 완료 보고에서 별도로 확인한다.
