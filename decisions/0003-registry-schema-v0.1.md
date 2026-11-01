# ADR 0003 — Registry Schema v0.1 Canonicalization

Status: ACCEPTED — 2026-09-10

## Context

404-node pre-admission checkpoint 이후 실제 admission 전에 canonical Concept record의 구조와 serialization을 정해야 한다. [Stable Node Identity](../NODE_IDENTITY.md)는 K·key·lifecycle 규칙을 확정했지만 full record schema와 저장 형식은 남겨 두었다. [Ontology v1.0](../ONTOLOGY_V1.md)은 FROZEN이며 이번 결정은 그 Medium-resolution Concept subset의 repository serialization이다.

시작 HEAD는 `d75f29bb7bc7a1d6d995c8b68439651207627636` (`docs: checkpoint medium node candidates v0.1`)이다. 설계 입력은 사용자가 2026-09-10 제공한 “AI Knowledge Book — Registry Schema v0.1 Canonicalization” 명세와 승인한 구현 계획이다. 이 결정은 후보의 semantic admission 검토나 기존 설계 세션의 stress-test를 재실행한 결과가 아니다.

## Decision

- [REGISTRY_SCHEMA.md](../REGISTRY_SCHEMA.md)를 canonical Registry Schema v0.1로 채택한다. 실제 Medium Registry는 아직 admitted/populated되지 않았다.
- 현재 지원은 `kind = concept`의 Medium-resolution Concept다. Required fields는 `id`, `canonical_key`, `title`, `kind`, `macro_area`, `scope`, `status`; optional fields는 `concept_type`, `concept_role`, `aliases`, `former_keys`, `boundary`다. `retirement_reason`은 retired에만 필수이고 active에는 금지한다.
- Canonical serialization은 JSONL이다. 미래 권장 path는 `registry/nodes.jsonl`이며 이번에는 생성하지 않는다. UTF-8·line-oriented JSON·numeric K 정렬·고정 field serialization order를 사용한다. Object key order는 JSON semantics가 아니다.
- Active Concept는 current macro-area 하나를 canonical home으로 갖는다. Retired tombstone은 retirement 시점의 마지막 home을 보존하고 미래 current-key membership을 강제하지 않는다. Retirement reason은 non-empty string이며 기존 대표 vocabulary를 exhaustive ontology enum으로 확대 해석하지 않는다.
- Identity·key history 비재사용과 terminal retirement는 NODE_IDENTITY를 따른다. Canonical key syntax와 per-record hygiene는 schema에서 구체화한다. Current key uniqueness는 retired를 포함하고 title/alias에는 global uniqueness를 요구하지 않는다.
- Initial Medium Concept Admission Profile은 `kind=concept`, `status=active`다. 이는 admission된 최초 records에 적용할 profile이며 404개 전체의 admission이나 이번 profile 적용을 뜻하지 않는다.
- Node Registry, Semantic Graph, Registry Lineage 및 Learning / Evidence·Practice / Exposition / Epistemic data를 분리한다. Lineage는 semantic edge 자동 rewrite 규칙이 아니다. Admission criteria는 review 과정에 두며 node boolean으로 저장하지 않는다.
- Schema/node revision은 문서와 Git history로 관리한다. 타 Knowledge kinds, atomic expansion과 타 layer/edge/lineage serialization은 명시적인 후속 revision으로 남긴다.

## Rationale

### JSONL vs Markdown/YAML

JSONL은 machine-readable canonical source로 standard JSON parser를 사용할 수 있고, record별 line-oriented diff와 대규모 registry 확장, deterministic validation에 적합하다. Markdown 표는 긴 scope·boundary와 구조적 validation에 불편하고 YAML은 이번 최소 record에 추가 serialization 선택지를 요구한다. JSONL의 긴 한 줄은 사람이 직접 읽기에 불리할 수 있으므로 향후 human-readable catalog를 canonical JSONL에서 생성할 수 있다. 두 개의 canonical source를 운영하지 않는다.

### Minimal schema vs rich node object

Concept의 identity와 semantic scope를 학습목표·mastery·Claim status·citation·출판 위치와 함께 저장하면 같은 정보를 여러 layer에서 수정해야 한다. Minimal schema는 Ontology의 책임 분리를 보존한다. Curriculum의 core/enrichment, derived centrality, candidate provenance도 Concept의 absolute semantic property로 만들지 않는다. 상세한 prerequisite는 reason·mastery·target objective/depth를 갖춘 후속 Learning 설계에서 다룬다.

### Concept-only support vs premature universal schema

Ontology에는 여러 Knowledge kinds가 있지만 아직 complete serialization이 정해지지 않았다. 현재 Medium Concept subset만 지원하면 실제 필요에 맞춰 atomic expansion과 non-Concept kinds를 설계할 수 있다. `kind` 하나만 추가했다고 Formal Object나 Engineering Invariant의 필수 구조까지 지원한다고 주장하지 않는다.

### Single canonical macro home

같은 Concept의 cross-domain reuse를 여러 macro membership으로 저장하면 semantic ownership과 단순 사용을 혼동하기 쉽다. Home 하나를 두고 reuse는 graph relation / Occurrence로 표현한다. Macro classification은 revision 가능하고 K identity와 독립이므로 재분류에도 동일 identity를 유지할 수 있다. Retired home은 현재 분류보다 historical lookup을 위해 보존한다.

## Consequences

후속 registry authoring과 validation은 schema의 field 계약·serialization convention과 identity history를 함께 따라야 한다. 구조 검사는 key syntax·현재 중복·active macro membership 등을 확인할 수 있지만, 과거 key 재사용·semantic continuity·retirement reference audit는 history 및 의미 검토가 필요하다. Retirement reason의 구조적 유효성이 lifecycle closure를 대신하지 않는다.

다음 작업은 404개 candidate의 scope/boundary normalization, proposed title/key/home review, final cohesion/duplicate/admission audit다. Admission set approval 이후 canonical main 동기화·single-writer allocation·JSONL materialization·validation·canonical registry commit으로 진행한다. Handle은 계속 provisional이며 snapshot commit과 이 schema commit은 key reservation이나 former-key history를 만들지 않는다.

이번 checkpoint는 schema와 이 ADR 및 네 안내/상태 문서의 6개 파일에 한정한다. Ontology, Node Identity, Macro Skeleton과 404 snapshot은 byte-identical로 보존한다. K issuance·registry admission·실제 registry 생성·per-candidate scope 작성·edge/lineage schema 확정은 수행하지 않는다. 영구 validator를 만들지 않으며 validation은 임시 fixture와 문서의 정적 대조다. 실제 수행 결과와 최종 commit/remote 상태는 checkpoint 완료 보고에서 구분해 보고한다.
