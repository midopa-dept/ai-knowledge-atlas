Status: CANONICAL — Stable Node Identity and Lifecycle Rules

# Knowledge Graph Node Identity

## 1. 목적과 적용 범위

이 문서는 canonical Knowledge Graph node의 stable identity와 lifecycle 운영 규칙이다. [Ontology v1.0](ONTOLOGY_V1.md)은 FROZEN이며 변경하지 않는다. 결정의 배경과 trade-off는 [ADR 0002](decisions/0002-stable-node-identity.md), 현재 macro classification은 [Macro Skeleton v0.2](KNOWLEDGE_GRAPH_L1.md)를 참조한다.

Knowledge / Learning / Exposition을 분리한다. Concept 분리는 Ontology v1.0의 하나의 중심 질문, 독립 Learning Objective와 구체적 prerequisite 가능성, downstream independent reuse를 따른다. Downstream dependency나 별도 Learning Objective·Practice Bank가 다르면 별도 node로 나눈다. Domain / terminology / scope metadata는 Concept identity 자체가 아니다.

`K####`는 canonical Knowledge Graph node identity의 namespace다. Learning, Evidence, Practice, Epistemic Layer의 모든 객체를 K에 넣지 않는다. Learning Objective, Evidence Requirement, Task Model, Exercise, Claim, Evidence Source의 별도 namespace는 후속 설계 대상이며 `LO####`, `ER####`, `TM####` 등도 이번에 확정하지 않는다. K가 Knowledge Layer의 어떤 subtype까지 적용되는지는 실제 registry schema에서 Ontology와 맞춰 구체화한다.

이 문서는 full registry schema나 실제 medium-resolution registry가 아니다. 모든 K ID·key·record와 lifecycle 사례는 **illustrative example**이며 실제 발급·등록·예약을 뜻하지 않는다. Required/optional field와 저장 형식은 후속 registry 설계에서 결정한다.

## 2. Stable identity와 K 형식

K는 현재 title, canonical key, macro classification, 설명 위치가 아니라 지식 객체의 지속적인 identity다. 의미적 identity가 유지되면 title rename, canonical key rename, alias 추가·수정, macro-area reclassification, exposition 이동, 설명 정교화, scope refinement에도 같은 K를 유지한다.

- 형식은 `K` + 최소 4자리 decimal integer다: `K0001`, `K0002`, …, `K9999`, `K10000`, ….
- `K0000`은 금지한다. 번호는 양의 정수이며 발급 시 최소 4자리로 zero-padding한다.
- 번호에 domain, 학습순서, 중요도, macro area 의미를 부여하지 않는다.
- `MATH-K001`, `RL-K001`, `K1000~1999 = Mathematics` 같은 분야별 prefix/range 예약은 금지한다.
- 번호 gap은 허용한다. Issued 번호는 재사용하거나 재번호화하지 않는다.

Macro classification과 node identity는 독립이다.

## 3. Candidate, admission과 issuance

Draft candidate에는 K ID를 발급하지 않는다. Candidate는 registry lifecycle status가 아니다.

```text
candidate
→ scope review
→ split / merge / rename review
→ dependency review
→ registry admission
→ K allocation
→ validation
→ canonical commit
```

K가 공식적으로 **issued**되는 시점은 canonical registry가 canonical branch인 `main`의 repository history에 commit되어 받아들여진 순간이다. 로컬 draft의 임시 번호나 canonical history에 들어가지 않은 번호는 issued ID가 아니다. Allocation은 admission 후 수행하지만 canonical commit 전까지는 공식 issuance가 아니다.

Canonical history에 한 번 issued된 K는 오류가 발견되어도 삭제·재사용하지 않는다. 필요한 경우 retired tombstone으로 보존한다. 실제 registry allocation은 retired를 포함한 issued K records의 최대 번호 다음부터 단조 증가한다. 빈 번호를 backfill하지 않으며, 과거 issued 번호의 부재를 재사용 근거로 삼지 않는다. Issued record가 없는 최초 allocation은 `K0001`부터 시작한다.

## 4. Canonical key, former keys와 aliases

`canonical_key`는 검색하고 이해하기 쉬운 semantic locator이며 stable identity 자체가 아니다.

- Lowercase, dot-separated semantic namespace를 사용한다. Segment 내부 underscore를 사용할 수 있다.
- 예: `probability.conditional_distribution`, `transformer.scaled_dot_product_attention`, `agent.tool_invocation`, `harness.state_reconciliation`.
- Chapter/part number나 learning order를 넣지 않는다. Current macro area를 기계적으로 prefix하는 규칙을 만들지 않는다.
- Dot hierarchy는 `component_of`, `requires` 등 semantic relation을 자동으로 뜻하지 않는다. 관계는 별도 graph edge로 표현한다.

Canonical key는 안정적으로 운영하되 immutable하지 않다. 예를 들어 K0127의 `probability.conditional_prob_distribution`을 `probability.conditional_distribution`으로 rename해도 identity가 같으면 K0127을 유지한다. 이전 key는 `former_keys`로 추적한다.

Canonical repository history에서 특정 K에 사용된 current/former canonical key는 이후 **다른 K에 재사용하지 않는다**. Retired K의 key도 이 규칙을 따른다. Candidate 단계에서만 사용되고 canonical history에 들어가지 않은 key는 이 예약 규칙의 대상이 아니다.

| Metadata | 의미 | 예 |
| --- | --- | --- |
| `aliases` | 자연어 용어, 약어, 역사적 명칭, 분야별 alternative terminology | `conditional law` |
| `former_keys` | 과거 canonical repository identifier | `probability.conditional_prob_distribution` |

자연어 alias와 과거 identifier를 혼합하지 않는다.

## 5. Identity Continuity Test

기존 K 유지 여부의 핵심 질문은 다음과 같다.

> 변경 전 K ID를 참조한 사람이 변경 후 같은 K를 따라갔을 때 여전히 같은 지식 대상을 가리킨다고 자연스럽게 말할 수 있는가?

보조 판단 기준:

1. 중심 질문이 동일한가?
2. 핵심 의미가 동일한가?
3. 기존 downstream relation의 상당 부분이 여전히 의미적으로 유효한가?
4. 기존 Learning Objective가 본질적으로 다른 능력을 요구하게 되지는 않았는가?
5. 과거의 “Kxxxx를 참조하라”는 reference가 변경 후 오해를 만들지 않는가?

이는 semantic judgment이며 고정 percentage threshold가 아니다. Rename과 macro-area reclassification은 의미가 같으면 SAME K다. 기존 중심 질문을 더 정확하게 좁히거나 명료화하는 scope refinement도 continuity를 유지하면 SAME K다.

Scope broadening으로 기존 narrow concept을 편의상 umbrella로 팽창시키지 않는다. 예를 들어 K0200 Self-Attention을 K0200 Attention으로 바꾸면서 cross-attention 등 독립 개념을 모두 흡수하는 것은 단순 rename이 아니다. Broader integration concept이 필요하면 새 K를 검토한다.

## 6. Extraction / Decomposition과 True Split

### Extraction / Decomposition

세부 node를 추출한 뒤에도 원본이 독립적이고 coherent한 지식 객체로 남으면 decomposition이다. 원본은 active와 SAME K를 유지하고 새 세부 Concept에는 NEW K를 부여한다.

예: K0400 Attention에서 K0810 Scaled Dot-Product Attention과 K0811 Multi-Head Attention을 추가해도 K0400은 active다. `extracted_to`로 추출 provenance를 기록할 수 있다. Semantic relation은 후속 graph 설계에서 별도로 판단한다. 이는 true split이 아니다.

### True Split

원본이 독립적인 복수 Concept을 잘못 bundle했고 분리 후 원본을 coherent한 Concept로 유지할 이유가 없다면 true split이다. 원본은 retired, **모든 successor는 NEW K**다. 원본 ID를 어느 한 successor에게 임의 상속하지 않는다.

```yaml
# Illustrative lifecycle example; 실제 registry record가 아님.
# K0830: Event Conditional Probability — NEW K
# K0831: Conditional Distribution — NEW K
id: K0500
title: Conditional Probability & Conditional Distribution
status: retired
retirement_reason: true_split
split_into:
  - K0830
  - K0831
```

Broad/integration node 자체가 독립적으로 유효하면 retire하지 않고 decomposition으로 처리한다.

## 7. Duplicate Merge, True Semantic Merge와 Integration

### Duplicate Merge

두 K가 동일한 지식 객체를 중복 등록한 경우다. **먼저 canonical하게 issued된 K를 우선 survivor로 한다**는 기본 heuristic을 적용한다. 번호 크기나 좋은 title 자체로 issuance 순서를 대체하지 않는다. Survivor 선택은 identity 검토에 근거하며 기본 heuristic에서 벗어나는 판단은 이유를 기록한다.

예: 먼저 issued된 K0140 Self-Information과 K0332 Surprisal이 동일 Concept이면 K0140은 active를 유지하고 Surprisal을 alias로 수용할 수 있다.

```yaml
# Illustrative lifecycle example
id: K0332
status: retired
retirement_reason: duplicate
duplicate_of: K0140
```

Duplicate는 하나의 survivor만 가진다. 더 최신 node의 좋은 title/scope/metadata는 continuity를 유지하는 범위에서 survivor로 가져올 수 있다. 단, 다른 K에 속했던 current/former key는 survivor의 canonical key나 former key로 이전하지 않는다. 이전 identifier는 원래 tombstone과 lineage를 통해 조회한다.

### True Semantic Merge

기존 A와 B가 독립 Concept로 유지될 이유가 사라지고 새로운 C가 대체하는 경우다. 예: K0100 A와 K0200 B를 각각 `status: retired`, `retirement_reason: true_merge`, `merged_into: K0900`으로 기록하고 C에는 NEW K0900을 부여한다. A/B 중 하나의 ID를 C에 재사용하지 않는다.

### Integration Node

기존 Concept들이 여전히 유효하고 그 관계를 설명하는 integration Concept을 추가하는 것은 merge가 아니다. State, Observation, Belief는 모두 active와 기존 K를 유지하고 State–Observation–Belief Relationship에는 NEW K를 부여한다.

## 8. Retirement와 Current Graph

Registry의 canonical lifecycle status는 현재 **`active`와 `retired` 두 개뿐**이다. Candidate는 아직 K가 없는 authoring 단계다.

`retired`는 identity-ending terminal state다. Retired K는 active로 부활시키지 않고, 삭제하거나 다른 Concept에 재사용하지 않는다. Tombstone은 identity, 이전 key와 중요한 lineage를 조회할 수 있도록 보존한다.

대표 retirement reason:

- `duplicate`
- `true_split`
- `true_merge`
- `erroneous_concept`
- `superseded_by_semantically_different_node`

이유에 맞는 lineage를 기록한다. 오류 Concept처럼 successor가 없는 retirement도 가능하다. 모든 retirement에 대체 node를 억지로 만들지 않는다.

현재 Curriculum에서 미사용, 특정 pathway에서 제외, 본권 미노출, Instructor's Guide에서만 사용, Deep 경로 전용, 특정 edition 미표시는 그 자체로 retirement 이유가 아니다. 이는 curriculum/publication projection 문제다.

현재 canonical semantic graph는 원칙적으로 active node를 대상으로 한다. 새 current semantic relation의 source/target으로 retired K를 사용하지 않는다. Retirement closure에서는 현재 reference를 감사·정리한다. Retired K는 lineage, migration, historical lookup, old reference resolution을 위해 남고 registry lineage edge에서는 사용할 수 있다.

## 9. Registry Lineage와 Semantic Graph의 분리

| Graph | Vocabulary | 역할 |
| --- | --- | --- |
| Semantic Graph | `requires`, `deepens`, `component_of`, `applied_in` 등 Ontology v1.0 관계 | 지식 사이의 의미적 관계 |
| Registry Lineage Graph | `split_into`, `merged_into`, `duplicate_of`, `replaced_by`, `extracted_to` | Identity 변화와 추출 provenance |

Lineage의 방향은 원본에서 successor/survivor/추출 node로 향한다. `split_into`는 true split의 복수 successor, `merged_into`는 true semantic merge의 새 결과, `duplicate_of`는 중복의 단일 survivor, `replaced_by`는 의미적으로 다른 대체 node, `extracted_to`는 원본을 유지하는 추출을 나타낸다. 이는 최소 provenance vocabulary이며 full field schema를 확정하는 표가 아니다.

Lineage target은 존재해야 하며 lineage graph에는 cycle이 없어야 한다. Successor가 나중에 다시 retired될 수 있으므로 역사적 lineage를 지우거나 target이 영원히 active여야 한다고 요구하지 않는다. 후속 lineage와 tombstone으로 추적한다.

Lifecycle relation을 Ontology v1.0의 semantic Knowledge Relations에 추가하지 않는다. 특히 Ontology의 `identity_or_decomposition`과 registry의 extraction/split provenance를 혼동하지 않는다.

### Lineage는 Semantic Edge Rewrite Rule이 아니다

```text
K0100 requires K0200
K0200 split_into [K0300, K0301]
```

이 사실만으로 `K0100 requires K0300`과 `K0100 requires K0301`을 자동 생성하지 않는다. K0100이 실제로 어느 successor를 prerequisite로 요구하는지는 개별 의미 판단이 필요하다.

**Lifecycle provenance는 reference migration 후보를 알려줄 뿐 semantic relation을 자동 변환하지 않는다.** Duplicate redirect나 후보 탐색을 자동화할 수 있어도 semantic migration 자체를 기계적으로 자동 결정하지 않는다.

## 10. Retirement Reference Audit

K retirement를 닫기 전에 **모든 current reference를 전수 감사**한다. 향후 존재하는 다음 layer를 모두 대상으로 한다.

- Knowledge edges
- Learning Objectives와 Objective Dependencies
- Prerequisite Requirements와 Evidence Requirements
- Task Models와 Exercises / Activities
- Expositions / Occurrences와 Cross-references
- Claims와 Review Plans
- Curricula / Pathways와 publication metadata

```text
retirement proposed
→ find all current references
→ semantic review of each reference
→ migrate / split / remove references
→ validate
→ retirement closure
```

각 reference의 의도에 따라 migrate, split, remove를 판단하고 처리·검증 결과를 추적 가능하게 남긴다. 발견과 redirect 후보 제안은 자동화할 수 있지만 의미 판단을 생략하지 않는다. Reference가 없는 경우도 탐색 범위와 없음의 확인을 남긴다. Historical reference와 lineage/tombstone은 current semantic graph와 구별하여 보존한다. Audit 완료는 retirement closure의 조건이며 별도 lifecycle status를 추가하는 절차가 아니다.

## 11. Parallel Authoring과 Git History

병렬 authoring 세션은 candidate에 K를 임의 발급하지 않는다.

```text
parallel candidate authoring
→ candidate review
→ integration / canonicalization session
→ sync canonical main
→ single-writer K allocation
→ validation
→ canonical commit
```

현재는 단일 integration writer로 충분하다. Main이 바뀌면 최신 canonical issuance와 key history를 다시 확인한 뒤 allocation을 검증한다. 실제 필요 전에는 block reservation이나 distributed allocator를 추가하지 않는다.

일반 수정 이력은 Git이 담당한다. 모든 node에 `node_version`, `revision_number`, `last_modified_version` 같은 중복 version system을 만들지 않는다. Split, merge, retirement 등 중요한 identity lineage 사건은 registry metadata와 필요 시 ADR에 남긴다.

## 12. Illustrative Node Record와 사례 요약

아래는 identity 설명용이며 required/optional schema나 실제 등록이 아니다.

```yaml
id: K0127
canonical_key: probability.conditional_distribution
title: Conditional Distribution
macro_area: MATH-PROB

type: concept
role: atomic

scope: >
  다른 확률변수 또는 사건에 조건을 걸었을 때
  확률분포가 어떻게 정의되고 사용되는지를 다룬다.

aliases:
  - conditional law
former_keys: []
status: active
```

| 사례 | Identity 처리 |
| --- | --- |
| Autoencoder: DL → REP reclassification | SAME K |
| Attention에서 Multi-Head Attention 추출 | Attention SAME K·active, Multi-Head NEW K |
| Conditional Probability + Conditional Distribution true split | OLD K retired, TWO NEW K |
| Surprisal / Self-Information duplicate | 먼저 canonical issued된 K 우선 유지, duplicate K retired |
| State + Observation + Belief integration | 기존 K 모두 active 유지, relationship node NEW K |
| Concept의 exposition 위치 이동 | SAME K |

## 13. 후속 Registry Validation Invariants

다음은 후속 validator 및 review workflow가 확인해야 할 최소 invariant다. 이번에는 영구 validator script를 구현하지 않는다.

1. 모든 issued K ID는 유일하다.
2. K 형식은 `K` + 최소 4자리 숫자다.
3. `K0000`은 금지한다.
4. Issued K를 재사용하지 않는다.
5. Active canonical key는 유일하다.
6. Canonical history에서 사용한 current/former key를 다른 K에 재사용하지 않는다.
7. Current macro classification은 해당 시점 canonical Macro Skeleton과 일치한다.
8. Current semantic graph가 retired node를 새 endpoint로 참조하지 않는다.
9. Retired split/merge/replacement의 명시된 successor가 존재하고 lineage가 유효하다.
10. Lineage graph에 cycle이 없다.
11. True split successor는 모두 해당 split에서 새로 발급하는 ID다.
12. True semantic merge 결과도 해당 merge에서 새로 발급하는 ID다.
13. Duplicate merge는 하나의 survivor만 가진다.
14. Candidate node에는 issued K ID가 없다.
15. Retirement closure 전에 current-reference audit가 완료되어야 한다.
16. Lifecycle lineage 변경이 semantic edge를 자동 rewrite하지 않는다.

형식·중복·target 존재·cycle·macro membership은 구조 검사로 지원한다. Issuance·key 재사용·새 ID 여부는 canonical history와 대조한다. Continuity, lineage 사건의 의미적 타당성, reference migration과 audit 완결성, 자동 rewrite 금지는 semantic review 및 변경 절차 검토가 필요하다. 문자열 검사 통과만으로 semantic correctness를 입증하지 않는다.
