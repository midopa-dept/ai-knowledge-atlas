# ADR 0005 — Learning Objective Schema v0.1

Status: ACCEPTED — 2026-09-13

## Context

Canonical Medium Semantic Graph v1 완료 뒤 Learning Layer의 storage와 identity를 구체화한다. Baseline은 `8adc31e691068ed3d1ca6c68139d3ac24bee5c74` (`graph: admit medium semantic graph v1`)이다. Preflight에서 clean `main`, local HEAD = origin/main = actual remote main = baseline을 확인했다. Registry는 504 active / 0 retired / K0001–K0504 / next K0505, Semantic Graph는 603 assertions이며 Learning Objective data file은 없다.

설계 입력은 사용자가 제공한 “AI Knowledge Book — Learning Objective Schema v0.1” 명세와 승인한 read-only 설계 계획이다. 이번 결과는 repository 문서 canonicalization과 정적 검증이며 objective population, pilot stress-test 또는 교육적 효과의 실증이 아니다.

[FROZEN Ontology v1.0](../ONTOLOGY_V1.md) §2·§5·§6을 우선한다. [Node Identity](../NODE_IDENTITY.md)는 Learning namespace를 후속 설계로 남겼으며 [Registry Schema](../REGISTRY_SCHEMA.md)와 [Semantic Edge Schema](../SEMANTIC_EDGE_SCHEMA.md)는 Learning data와 learning-order relations를 이미 분리한다. 제안과의 canonical conflict는 발견하지 않았다. Ontology §13.2의 Working/Deep 핵심 Concept coverage 의무는 context가 정해진 뒤 적용하며 모든 Concept에 최소 1개 objective를 요구하는 quota로 확대하지 않는다.

## Decision

- [LEARNING_OBJECTIVE_SCHEMA.md](../LEARNING_OBJECTIVE_SCHEMA.md)를 **CANONICAL — Learning Objective Schema v0.1**로 채택한다.
- Stable opaque ID는 `LO[0-9]{4,}`와 양수·최소 4자리 canonical padding을 사용한다. K와 별도 namespace이며 번호에 의미를 부여하지 않는다. Validated objective registry commit의 canonical remote `main` 수용이 공식 issuance 시점이다.
- Issued ID 삭제·재사용·재번호화·gap backfill·range reservation을 금지한다. Future allocation은 canonical history 최대 번호 이후 단일 writer가 수행한다. Candidate/pilot은 발급·예약 대상이 아니다.
- Required fields는 `id`, `statement`, `concepts`, `status`; 일반 optional fields는 없다. `retirement_reason`만 retired에 필수이고 active에는 금지하는 조건부 field다. 별도 scope/conditions/boundary와 per-record version은 두지 않는다.
- Active LO는 최소 1개 current active Concept K에 grounding한다. Concepts는 unique/numeric ascending이며 primary owner를 강제하지 않는다. Retired tombstone은 마지막 statement/grounding을 보존하고 존재하는 retired Concept의 historical reference를 허용한다.
- Meaning-preserving clarification은 SAME LO다. 핵심 action/object/conditions 변경, true split·true merge는 신규 identity를 요구한다. Retirement는 terminal이며 reason과 current-reference audit를 요구한다. Lineage storage는 후속 설계이며 successor 자동 rewrite를 금지한다.
- Observable performance를 editorial admission rule로 둔다. 고정 verb enum/Bloom schema는 만들지 않는다. 계산과 결과 해석 같은 coherent performance를 허용하되 독립 수행 bundle은 분리 검토한다.
- Mastery, Target Depth, terminal/enabling, curriculum/publication metadata, prerequisites, Evidence/Task/Practice 및 Claim metadata를 objective record에 넣지 않는다.
- 정밀 `requires`는 후속 first-class Prerequisite Requirement에서 Objective Dependency로 projection할 수 있게 하며 두 canonical sources를 중복 저장하지 않는다. Requirement는 prerequisite objective/concept, target objective 또는 target depth, required mastery, reason을 갖춰야 한다. Recommended/deepens storage는 별도 후속 설계다.
- Future path는 `learning/objectives.jsonl`이다. UTF-8/no BOM/LF/final newline, compact standard JSONL, duplicate members와 blank records 금지, numeric LO order, field order `id → statement → concepts → status → retirement_reason`을 사용한다.
- [learning/README](../learning/README.md)는 **SCHEMA-ONLY — NO OBJECTIVE POPULATION** 상태를 알린다. Issued LO 0 / next potential allocation LO0001, unissued and unreserved. 이번에는 objective data나 영구 validator를 생성하지 않는다.

## Rationale and alternatives rejected

### Stable LO identity rather than statement-as-identity

Evidence, dependency, coverage와 publication references는 표현이 개선되어도 같은 수행을 가리켜야 한다. Statement hash/text identity는 문법 수정에도 references를 바꾸며 의미적 continuity를 표현하지 못한다. Stable ID는 issuance history와 retirement 관리 비용이 있지만 reference 안정성을 제공한다.

### Multi-Concept grounding and no one-Concept/one-Objective rule

비교·통합 수행은 여러 Concepts를 직접 사용한다. 강제 primary owner나 1:1 mapping은 수행을 왜곡하거나 artificial split을 유도한다. Concepts당 0·1·복수를 허용하되 grounding을 배경 prerequisite 전수 목록으로 사용하지 않는다. Ontology의 조건부 coverage 의무는 후속 context에서 별도 확인한다.

### Minimal statement and lifecycle data

Action/object/핵심 조건을 statement로 식별할 수 있어 별도 scope/conditions/boundary는 현재 필요하지 않다. Authoring convenience보다 단일 수행 정의를 우선한다. 반면 retired record가 폐기된 이유를 잃지 않도록 retirement_reason은 최소 조건부 field로 채택한다. Historical grounding을 active endpoint 규칙으로 강제하면 tombstone을 왜곡하므로 active/current와 retired/historical 규칙을 구분한다.

### Mastery is not intrinsic

Mastery 0–4는 수행 수준과 evidence 판단의 축이며 pathway/prerequisite 요구 threshold는 context에 따라 달라질 수 있다. LO.mastery 고정은 수행 정의와 context를 결합한다. 서로 다른 threshold가 LO 수행 의미를 바꿀 수는 없으며 핵심 수행 변화는 신규 objective로 처리한다.

### Target Depth is not intrinsic

Overview/Working/Deep은 Ontology의 설명 깊이 축이며 Mastery와 동일하지 않다. Objective에 고정하면 설명/target context와 수행 identity가 결합하므로 후속 profile/requirement에서 연결한다.

### Terminal/enabling and curriculum metadata are not intrinsic

Ontology가 명시한 pathway-relative 역할이다. Core/recommended/enrichment, required/elective 및 publication 위치 역시 objective의 영구 속성으로 저장하지 않는다. Learner-facing 목표·증거·closure 의무는 유지한다.

### Prerequisites and evidence are not embedded

Bare adjacency는 reason·required mastery·target context를 잃는다. Detailed Requirement와 requires adjacency를 이중 canonicalize하면 불일치가 생길 수 있어 projection을 우선한다. Recommended/deepens는 required와 구별한다. Evidence Requirement는 충분한 관찰의 기준이고 LO는 수행 정의이므로 rubric·threshold·Task Model도 별도 layer다.

### Pilot before population and permanent validator

Cross-domain 12–20 Concepts의 pre-population pilot으로 granularity·identity·grounding·observable wording·future mastery/prerequisite compatibility를 확인한 뒤 schema를 보정한다. 곧바로 504 Concepts를 채우거나 아직 stress-test되지 않은 schema를 permanent validator로 고정하지 않는다. 이 checkpoint에는 문서 fixture와 temporary validation이 적합하다.

## Consequences

후속 authoring은 schema review, pilot, 필요시 correction, pilot freeze, full population orchestration design을 따른다. Objective 수나 Concept별 quota는 없다. Initial admission profile은 active LO, 최소 1개 active Concept grounding, observable performance와 금지 metadata 부재를 요구하지만 이번에 적용하지 않는다.

일반 revision은 Git으로 추적하고 retirement 이유·successors가 있으면 해당 identities·reference audit 결과를 변경 기록에 남긴다. 정형 LO lineage 및 Objective Dependency/Prerequisite Requirement/Evidence schema는 후속 설계로 남는다. 이는 현재 checkpoint의 미해결 conflict가 아니라 명시적인 scope boundary다.

변경은 schema, 이 ADR, learning README, root README, decisions README, PROJECT_STATE의 여섯 파일이다. Ontology, Node Identity, Registry Schema, Semantic Edge Schema, Macro Skeleton, nodes.jsonl, semantic_edges.jsonl은 byte-identical로 보존한다. K issuance, LO issuance, objective/dependency/prerequisite/mastery/depth/evidence/task/practice population은 0이다. 완료 후 pilot을 시작하지 않는다.

## Validation

Preflight에서 기존 Registry/Semantic Edge validators는 working tree와 HEAD 모두 PASS, 개별 tests 61/56개와 full suite 117개 PASS였다. 보호 7개 파일의 baseline byte equality와 clean working tree를 확인했다.

구현 validation은 문서의 labeled illustrative fixtures 및 추가 임시 serialization/lifecycle fixtures, schema/ADR/state 정책 정합성, editorial review, 상대 links/fragments, git diff --check, 여섯 파일 변경 범위, 모든 비대상 tracked bytes 보존, 금지 artifacts 부재, 기존 validators/tests를 확인한다. Fixture 검증은 실제 LO admission이나 pilot 실행이 아니며 구조 검사만으로 semantic quality와 lifecycle closure를 증명하지 않는다. 최종 수행 결과는 검증 후 아래에 기록하며 commit/push와 실제 remote 상태는 완료 보고에서 구분한다.

### Repository validation — 2026-09-13

- 문서 marker로 분리한 12개 illustrative fixtures의 예상 구조 통과/실패를 확인했다. Mental-state statement는 구조상 통과하지만 editorial invalid임을 분리했다. 추가 invalid fixtures 45개로 ID/padding, unsupported fields, retirement_reason 계약, concepts, duplicate members, JSON/encoding/line endings/order를 확인했고, valid padding/numeric order/retired tombstone과 non-Concept endpoint 거부도 확인했다. 모두 임시 검증이며 공식 LO records가 아니다.
- Editorial 대조에서 single-Concept 예시는 실제 K0105 scope, multi-Concept 예시는 K0107/K0108 scope에 grounding됨을 확인했다. Coherent 계산/해석 및 비교 수행, statement의 조건, identity/lifecycle 정책, Mastery/Depth/curriculum/prerequisite/evidence 경계와 Ontology의 조건부 coverage 의무를 검토했다. Pilot stress-test나 실제 objective admission으로 보고하지 않는다.
- Working-tree Registry validator와 Semantic Edge validator PASS; Registry tests 61개, semantic-edge tests 56개, full existing suite 117개 모두 PASS.
- 상대 Markdown links 270개와 fragment 1개 PASS; schema/ADR의 identity·record·layer·pilot 정책과 안내/상태 문서 정합성 확인. git diff --check 및 새 문서 UTF-8/LF/whitespace 검사 PASS.
- 변경 범위는 승인된 여섯 파일과 일치한다. Baseline 대비 보호 canonical 7개 파일을 포함한 모든 비대상 tracked files가 byte-identical이다. 504 active Concepts / 0 retired / next K0505와 603 semantic assertions를 보존했다.
- learning에는 README만 존재한다. objectives.jsonl, objective dependency/prerequisite/lineage registries 및 permanent LO validator/tests는 생성하지 않았다. Official LO issuance 0 / next potential LO0001, unissued and unreserved. Pilot, mastery/depth assignment, Evidence/Task/Practice 및 manuscript 작업을 수행하지 않았다.

Committed-revision validators와 최종 local/origin/actual remote 일치 및 clean tree는 이 문서를 포함한 commit 생성 후 확인하여 완료 보고에 기록한다.
