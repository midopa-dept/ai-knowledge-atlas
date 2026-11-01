# ADR 0002 — Stable Node Identity Canonicalization

Status: ACCEPTED — 2026-09-10

## Context

[Macro Skeleton v0.2](../KNOWLEDGE_GRAPH_L1.md)의 60개 영역 이후 medium-resolution Node Registry를 만들기 전에, 분류·명칭 변경과 지식 객체의 identity 변경을 구별하는 운영 기준이 필요하다. [ADR 0001](0001-macro-skeleton-v0.2.md)은 macro classification과 향후 stable K identity를 분리하는 방향을 기록했다. 이번 결정은 그 후속 구체화이며 [Ontology v1.0](../ONTOLOGY_V1.md)의 변경이 아니다.

시작 HEAD는 `fc43cd84deac7c98b878cf8840306bc63f7294ee`다. 설계 입력은 사용자가 2026-09-10 제공한 “AI Knowledge Book — Stable Node Identity Rules Canonicalization” 작업 명세와 승인된 구현 계획이다. Stable Node Identity 설계 및 lifecycle stress test 완료는 사용자 제공 설계 입력으로 기록한다. 이번 repository 작업의 validation은 규칙·사례·문서 간 정적 대조이며, 별도 설계 세션의 stress test를 재실행하거나 실제 registry 동작을 실증한 결과가 아니다.

## Decision

- [NODE_IDENTITY.md](../NODE_IDENTITY.md)를 stable node identity와 lifecycle의 canonical operating specification으로 채택한다. 상세 규칙·절차·예시·validation invariant는 그 문서에 유지한다.
- K는 지속적인 지식 객체 identity이고 canonical key·title·macro classification·exposition 위치와 구별한다. Identity continuity가 유지되면 K를 유지한다.
- Candidate에는 K를 발급하지 않는다. Review와 admission 뒤 단일 integration writer가 allocation하며, canonical branch의 registry commit 수용을 issuance 기준으로 삼는다. Issued 번호와 특정 K에 속했던 canonical key는 다른 identity에 재사용하지 않는다.
- Decomposition, true split, duplicate merge, true semantic merge, integration을 구별한다. Retirement는 terminal이며 tombstone으로 보존한다.
- Registry lineage는 provenance다. Ontology semantic relation을 확장하지 않고 semantic edge rewrite를 자동 결정하지 않는다. Retirement closure에는 current-reference audit가 필요하다.
- 일반 revision history는 Git으로 관리한다. Full registry schema, 실제 K records, 타 layer namespace, 영구 validation pipeline은 후속 작업으로 남긴다.

## Rationale

Stable identity와 수정 가능한 semantic locator를 분리하면 명칭·분류·출판 위치 변경에도 기존 reference의 의미를 유지할 수 있다. 중심 질문과 downstream reuse를 보는 Ontology의 Concept 분리 기준을 continuity 판단에 적용하면 이름이 같다는 이유만으로 서로 다른 지식을 같은 K에 덮어쓰는 것을 피할 수 있다.

Coherent한 원본이 남는 decomposition과 원본 identity가 끝나는 true split은 reference에 미치는 영향이 다르다. Duplicate의 기존 identity 보존과 새로운 의미를 만드는 true merge도 구별해야 한다. Terminal retirement와 key 비재사용은 오래된 reference의 해석을 보존하는 대신 tombstone과 history 관리 비용을 수반한다.

Lineage는 과거 객체의 이동을 설명하지만 각 prerequisite나 Learning Objective가 실제로 어떤 새 객체를 요구하는지까지 결정하지 않는다. 전수 reference audit와 semantic review는 이 차이를 다루기 위한 운영 비용이다.

단일 integration writer는 현재 규모에서 병렬 candidate authoring과 충돌 없는 issuance를 함께 지원한다. Distributed allocator, 분야별 range 예약, node별 중복 version system은 현재 필요에 비해 복잡도를 높이므로 도입하지 않는다.

## Consequences

후속 registry 작업은 먼저 K 없는 candidate를 만들고 cohesion·scope·split·merge·dependency를 검토한 뒤 admission과 allocation을 수행한다. Current/former key의 소유 history와 retired records를 보존해야 하며, lifecycle 변경에는 의미 판단과 reference audit가 필요하다. Snapshot 검사만으로 과거 ID/key 재사용이나 semantic correctness를 검증할 수는 없다.

운영 규칙은 확정됐지만 실제 medium-resolution registry, issued K 목록, required/optional field schema는 아직 없다. 후속 schema는 Ontology의 Knowledge Layer와 이 운영 규칙을 함께 적용한다. Macro Skeleton의 60-area 구조·hub·traversal·migration과 동결된 Ontology는 이번 결정으로 변경하지 않는다.

이번 documentation checkpoint는 운영 문서, 이 ADR, 두 문서 index, 프로젝트 상태, macro map의 identity 관련 문구에 한정한다. Validation은 시작 HEAD 대비 Ontology byte 동일성, macro map §3–§6 및 60개 key/name 보존, 규칙·사례 정적 대조, 상대 링크, whitespace, 변경 범위를 확인한다. 실제 registry validator 실행이나 별도 stress-test 재실행으로 보고하지 않는다.

2026-09-10 정적 검증 결과: Ontology와 승인 범위 밖의 모든 tracked file은 시작 HEAD와 byte-identical이다. Macro map §3–§6 전체 및 순서가 있는 60개 key/name이 동일하다. 운영 문서의 16개 invariant, 예시의 active/retired status, 필수 lifecycle·key·audit·allocation 규칙을 확인했다. 저장소의 상대 Markdown 링크 32개가 유효하며 fragment는 없다. 운영 규칙과 ADR 및 lifecycle 사례를 대조하고 candidate/금지 ID/resurrection/자동 rewrite 관련 문맥을 검토했다. 이는 문서 검사이며 실제 K를 발급하거나 registry schema·validator를 생성하지 않았다.
