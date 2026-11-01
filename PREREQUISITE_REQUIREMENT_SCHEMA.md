상태: **정본 — Prerequisite Requirement Schema v0.1 / 데이터 admission 없음**

# Prerequisite Requirement Schema v0.1

## 1. 목적·권위·승인 범위

이 문서는 Prerequisite Requirement의 의미·identity·record·Context·능력 참조·Mastery·lifecycle·serialization·admission 계약의 정본이다. [Ontology v1.0](ONTOLOGY_V1.md) §2.2·5.6·13.1, [Node Identity](NODE_IDENTITY.md), [Registry Schema](REGISTRY_SCHEMA.md), [Learning Objective Schema](LEARNING_OBJECTIVE_SCHEMA.md)의 상위 계약과 경계를 유지한다. Concept grounding은 배경 선수지식 목록이 아니며 Semantic Graph에서 정밀 prerequisite를 자동 복사하지 않는다.

2026-10-13 (Asia/Seoul)의 실제 사용자 승인 원문·여섯 경로 범위는 [ADR 0007](decisions/0007-prerequisite-requirement-objective-dependency-schema-v0.1.md)에 기록한다. 승인 입력은 commit `218ac532747092c9e3bc70f4bd5151fcfff174cb`의 Schema Proposal §2–4·6–7·9와 Decision Packet이다. 후보·Pilot·검토의 당시 PENDING 지위는 역사로 보존한다.

Requirement는 유일한 canonical semantic source다. [Objective Dependency Schema](OBJECTIVE_DEPENDENCY_SCHEMA.md)는 이 원천에서 파생하는 query·projection·Context compatibility·보수적 required union DAG gate·export를 정의한다. 동일 계약을 별도 Dependency Registry에서 편집하지 않는다.

이 계약은 수행·표현의 설계 판단이다. 학습효과·학습자 측정·교정된 cut score를 실증하지 않는다. 공식 LO statement와 Concept scope/boundary는 의미 대응의 입력이며 관계의 지원 여부를 자동 보증하지 않는다. 이 checkpoint는 Schema만 정본화하며 Registry 생성·PR ID 발급/예약·관계 admission·전체817 population은 수행하지 않는다.

## 2. Requirement identity·ID·미래 저장 위치

한 record는 **특정 target LO·context에서 하나의 need를 지원하는 능력 묶음/대체 경로에 대한 판단**이다. 여러 independent required records는 함께 필요하다. 하나의 OR-of-AND record는 각 대안이 같은 need를 대신 충족한다는 의미 계약이다. `need`는 ‘새 토큰의 다음 레이어 입력을 산출’처럼 target에서 사용하는 결과를 지정하고 `reason`은 그것이 왜 필요한지/어떻게 도움·심화를 주는지 말한다. 이유 없는 edge는 없다.

미래 PR ID의 ASCII full-match 문법은 `PR[0-9]{4,}`다. 숫자 부분은 양의 정수를 최소 4자리로 zero-padding한 표현이며 LO/K와 분리된 namespace다. 번호에는 분야·순서·중요도·난이도 의미가 없다. Retired를 포함한 issued ID는 유일하며 삭제·재사용·재번호화·gap backfill·분야별 range 예약을 금지한다. Canonical issuance history의 최대 issued 번호 이후로 단조 증가하며 single Git writer가 admission 승인 후 allocation한다.

**공식 PR 발급은 검증된 Registry commit이 실제 canonical remote `main`에 수용되는 시점이다.** Local draft·staging·local commit·candidate handle은 공식 발급이나 예약이 아니다. 이번에는 구체 PR ID를 하나도 발급하거나 예약하지 않는다.

미래 단일 Registry 경로는 `learning/prerequisite_requirements.jsonl`이다. Requires와 supported recommended/deepens를 relation으로 구별하여 같은 계약에 저장한다. 별도 Dependency·Skill·Context ID나 Registry를 도입하지 않는다. 별도 데이터 admission 승인 전 이 파일은 **빈 파일도 생성하지 않는다**. 설명용 ILLUSTRATIVE_RECORDS의 handle·wrapper·fixture_note·source_commit 자리표시자는 정본 field나 issuance가 아니다.

Duplicate identity는 bare pair가 아니다. 동일 target/context/relation/need와 동일 route 능력·범위·threshold 계약은 중복 후보로 막는다. 자연어 동의어는 의미 검토한다. 같은 pair도 부분/Mastery/Context/route가 다르면 각각 보존한다. 파생 adjacency 처리 경계는 Objective Dependency Schema §3을 따른다.

## 3. D1 — 부분 능력 참조

공식 LO 출처와 필요한 수행 부분을 함께 사용한다. `ability.source_lo`는 능력을 가르치고 찾아갈 공식 참조이며 수강·전체 달성의 선행 의무가 아니다. `performance`는 관찰 가능한 action·대상·핵심 조건을 가진 최소 능력이다. `scope: partial|whole`을 반드시 명시하고 partial에는 원 LO에서 요구하지 않는 부분을 `excludes`로 적는다. Whole도 명시적 의미 검토를 거치며 기본값으로 취급하지 않는다.

자연어 범위는 ‘softmax 부분’ 같은 제목만으로 통과하지 않는다. 어느 입력에서 무엇을 산출/설명하고 target의 어느 단계에 쓰이는지 대조한다. 원 LO가 해당 수행을 **직접 포함**해야 하며, 생성·설계 능력으로부터 독해 능력을 당연히 포함한다고 추론하지 않는다. Statement의 인용문 복사는 선택적 작성 근거이지 독립 source가 아니다. 승인된 부분 범위·배제·source LO·입력 revision을 함께 추적한다. 문자열 hash만으로 부분 대응의 유효성을 판정하지 않는다.

원 LO의 statement/grounding/status가 달라지면 SAME LO 정정이어도 연결된 모든 Requirement를 영향 목록으로 올리고 revalidation 완료 전 새 projection을 유효하다고 발행하지 않는다. 자연어 의미가 materially 달라지면 §8의 신규 Requirement 정책을 따른다. 자동 split·LO 의미 변경은 없다.

독립 LO/Skill 객체는 독립적으로 가르치고 평가할 coherent 수행이 반복적으로 재사용되고, 기존 LO의 부분 참조로 안정적인 경계를 표현할 수 없거나 원 statement가 그 능력을 포함하지 않을 때 별도 canonicalization으로 검토한다. 새 Skill identity는 LO와 다른 운영상 필요가 입증된 경우에만 설계한다. 이번에 새 LO·Skill ID를 발급하지 않는다.

## 4. D2 — 요구 존재·충족·이수 이력

요구 존재와 독자별 충족은 별도 계층으로 관리한다. Requirement existence는 목표/context에 필요한 능력, satisfaction은 특정 독자가 그 능력을 확보했다는 판단, completion은 특정 교육 단위 이력이다. Completion은 하나의 입력일 수 있지만 satisfaction의 자동 증명이 아니다. 독자의 상태는 `satisfied / not_satisfied / unknown`처럼 후속 계층에서 해석할 수 있으나 이번 Schema에 그 record나 DB를 정의하지 않는다.

같은 context와 자료에서 독자 세 명(이 책 학습, 외부 교재 학습, 실무 경험)은 동일 Requirement와 동일 projection을 받는다. 근거 충분한 만족 판정이면 개인 경로의 ‘남은 요구’ view가 줄어들 수 있다. 그 view는 원 Requirement/입력 revision/독자 판단을 참조하며 canonical graph를 수정하지 않는다. 능력 보유와 실행 함수 제공은 다르다. 후자는 task context 자체를 바꾸므로 D3의 재판정 대상이다. Entry Profile의 assumed mastery를 실제 측정으로 표시하지 않는다.

## 5. D3 — Context·Resources·OR-of-AND

최소 Context / Resources 구조를 사용하며 능력 요구에만 비재귀 OR-of-AND를 허용한다. Context는 target 수행의 사례 범위와 자료 계약이다. 학습자의 현재 mastery·course history를 넣지 않는다. Inline `context.key`는 target LO에 상대적인 authoring locator이며 새 공식 Context namespace가 아니다. 동일성은 `(target.lo, context.key)`로 선언하되 같은 key를 사용하는 모든 current records의 context 전체와 target depth가 정확히 같아야 한다. 자료 계약이 materially 바뀌면 새 key를 쓰고 영향을 받은 Requirement는 신규/retire 검토한다. 오탈자 정정은 동일성 검토 후 SAME key로 가능하다. Git이 revision을 관리한다.

이 Schema는 context를 각 Requirement에 inline으로 둔다. 따라서 같은 target/context를 쓰는 records에 표현 복제가 생기지만 **동일 계약만 허용하는 equality 검사**로 독립 변경을 차단한다. 현재 profile에 별도 Context Registry/ID/lifecycle을 더하는 비용을 피하는 선택이다. 반복이 실제 운영 부담이 되면 별도 Schema 변경으로 factor out하며 두 계약 source를 동시에 유지하지 않는다.

`context.conditions`는 non-empty 자연어 사례 조건이다. `context.resources`에는 필수성에 영향을 주는 자료를 모두 명시하고, 각 자료의 `availability`를 `provided / absent / unknown`으로 구별한다. Omission은 ‘자료 없음’이 아니라 계약에 기술하지 않았다는 뜻이다. 중요 자료를 omission으로 숨기면 admission HOLD다. 제공 자료에는 내용/인터페이스, 대신 처리하는 능력 범위(`replaces`), 독자에게 남는 능력(`residual`)을 적는다. 공식 제공은 도출을, 셀 절차표는 첨자 재표현을, 실행 함수는 내부 계산을 일부 대신하지만 산술·축 독해·호출·갱신 기록까지 자동 대체하지 않는다. `replaces`는 대응을 검토할 서술이지 수행 충족의 자동 증명이 아니다. 필요한 능력을 대체하지 않는 입력 자료는 `replaces`를 생략할 수 있다.

실제 제공 artifact가 있으면 `ref`로 repository path와 Git commit을 연결한다. 아직 집필 전이면 description의 자료 계약을 사용한다. 향후 교재 발행에서는 실제 artifact가 그 계약을 충족하는지 확인하기 전 supported context로 적용하지 않는다. 이 세션에서 제공 artifact나 본문을 만들지 않는다.

한 target/context의 모든 required Requirements는 **AND**다. 한 Requirement의 `any_of`는 같은 명시적 `need`를 충족하는 대체 경로이며, 각 경로의 `all_of` 능력은 **AND**다. 교재/실무처럼 같은 능력의 획득 이력만 다른 것은 OR 경로가 아니라 D2의 satisfaction 문제다. 동등한 다른 수행 방식은 reason과 범위 대응이 승인된 경우에만 OR로 쓴다. 자료가 내부 연산을 대신하는 경우에는 다른 context를 만들고 남는 능력을 다시 기술한다. ‘능력이 있음 OR 도구가 있음’이라는 불투명한 단일 edge를 저장하지 않는다.

임의 NOT, 부등식, 중첩 조건·재귀 logic, 경로 간 조건 참조는 지원하지 않는다. 유한한 선택지별 능력 묶음으로 열거할 수 없는 조건은 HOLD 및 Schema extension 문제다. 필수 자료가 unknown이거나 사례 범위가 판정 불가능하면 requirement admission HOLD다. Unknown을 absent로 간주하거나 가장 낙관적인 route를 고르지 않는다.

Context compatibility와 전체 조합의 export HOLD는 [Objective Dependency Schema §4](OBJECTIVE_DEPENDENCY_SCHEMA.md#4-context-compatibility)에서 정의한다.

## 6. D5 — Required Mastery

[Ontology §5.3](ONTOLOGY_V1.md#53-mastery)의 scale을 유지한다.

| 단계 | Mastery |
| --- | --- |
| 0 | Unfamiliar |
| 1 | Recognition |
| 2 | Operational |
| 3 | Conceptual |
| 4 | Derivational / Transfer |

Requirement 능력별 integer 0–4와 `mastery_reason`을 사용한다. 같은 LO라도 필요한 부분과 context가 다르면 threshold가 다를 수 있다. 각 route의 능력은 자체 문턱을 가져야 하며 root 하나의 숫자로 여러 부분/대안을 덮지 않는다. 0은 Unfamiliar이므로 실제 필수 **능력**을 요구한다고 하면서 0을 부여하는 제안은 의미 HOLD다. 1은 식별/인식 자체가 필요한 경우, 2는 주어진 규칙으로 실제 계산·적용을 실행해야 하는 경우, 3은 입력/출력의 의미·조건·지원 주장/한계를 구별·설명해야 하는 경우, 4는 원 능력에 대응하는 도출/전이를 실제로 사용해야 하는 경우에만 정당화한다. 이는 일반 Ontology 수준을 이 객체에 적용하는 설계 기준이며 새 mastery scale이 아니다.

a02/a03/a16은 식·연산 실행으로 2, a17/b07/b11은 흐름·근거 범위 해석으로 3이라는 기존 설계 판단을 표현한다. Target가 어렵거나 설계 수행이라는 이유로 4를 자동 붙이지 않는다. 숫자가 LO의 action을 바꾸지 않으며 기존 계산 LO에 4를 붙여 증명 목표를 만들 수 없다. Mastery와 설명 깊이 `Overview|Working|Deep`은 별도다.

Provenance의 `basis=design_judgment`는 현재 profile의 판단 근거 수준이다. 후속 실증으로 문턱을 교정하려면 실제 관측 source를 추가하고 별도 의미 재승인을 거친다. 비교 가능한 모집단/조건/수행 범위의 evidence인지 확인해야 하며 한 문제 정답을 전체 Mastery의 증거로 취급하지 않는다. Threshold-only 교정이 같은 need/performance를 유지하면 SAME PR의 Git 변경으로 가능하나 영향을 받은 downstream projection과 개인 만족 판정은 재검토 대상이다. Need나 action 자체가 바뀌면 새 identity다.

필요 수준의 근거가 부족하면 후보 HOLD다. Canonical active record에 `null`, 임시 2/3 또는 unresolved status를 넣지 않는다. Evidence Requirement/Task Model/Rubric/측정 시스템은 이번에 작성하지 않는다.

## 7. 정확한 record·nested fields·serialization 계약

모든 object는 아래 정의한 members만 허용한다. String은 non-empty, 배열은 별도 언급 없으면 non-empty·중복 금지, optional은 값이 없으면 생략하며 null 금지다. Record에 학습자, 만족 상태, 수강 완료, generic metadata, version counter를 넣지 않는다.

| Field | Type / 필수성 | 계약 |
| --- | --- | --- |
| `id` | string / 필수 | §2의 PR ID 문법 |
| `target` | object / 필수 | `lo`: active 공식 LO 필수; `depth`: Overview/Working/Deep optional. LO-only profile이며 depth-only target는 아직 지원하지 않음 |
| `context` | object / 필수 | 아래 최소 조건·자료 계약 |
| `relation` | enum / 필수 | requires / recommended / deepens |
| `need` | string / 필수 | target에서 사용하는 구체 수행 결과 또는 지원 지점 |
| `any_of` | array / 필수 | 하나 이상 route. Route object는 `all_of` 능력 배열 하나만 가짐; 재귀 없음 |
| `reason` | string / 필수 | 해당 need의 필요성 또는 비필수 도움/심화. 학습순서/동일 K만으로 대체 금지 |
| `provenance` | object / 필수 | 입력 snapshot과 판단 근거·정확 위치 |
| `status` | enum / 필수 | active / retired, 지원/미결 판단과 구별되는 최소 lifecycle |
| `retirement_reason` | string / retired에서만 필수 | active에서는 금지. Tombstone은 마지막 semantic fields를 보존 |

Target는 **LO 필수 / depth optional**을 첫 운영 profile로 제한한다. Ontology의 target objective **또는** depth 계약을 LO로 충족하며, 아직 identity·grounding을 정의하지 않은 depth-only scope를 임의 문자열로 넣지 않는다. Depth-only 필요가 실제 발생하면 별도 Schema extension으로 결정한다.

| Context field | Type | 계약 |
| --- | --- | --- |
| `key` | string | target-local locator. ASCII full-match `[a-z][a-z0-9]*(?:-[a-z0-9]+)*`; 수행 조건·자료 계약이 같으면 같은 key |
| `conditions` | string | target statement를 바꾸지 않는 사례 범위·입력 조건 |
| `resources` | array / optional | 필요성에 영향을 주는 자료가 있을 때 필수; 아래 resource object들 |

Resource object members: `key`(같은 context 내 유일, Context key와 같은 syntax), `availability`(provided/absent/unknown), `description`(자료 내용·입출력·축·scope 필수). Provided이면 `residual` non-empty string 필수, `replaces` string optional(능력 대체가 있으면 필수), `ref: {path, commit}` optional. Absent/unknown에서는 replaces/residual/ref 금지다. Unknown은 후보 기록에서만 쓸 수 있고 active admission에 금지한다. Ref path는 repository 상대 경로, commit은 실제 존재하는 40자리 Git commit이다. 필요한 자료 역할을 통합/분리하는 의미는 key regex로 보증하지 않는다.

| Ability field | Type / 조건 | 계약 |
| --- | --- | --- |
| `source_lo` | string / 필수 | active LO. 직접 포함된 수행의 출처, completion 요건 아님 |
| `scope` | enum / 필수 | partial / whole |
| `performance` | string / 필수 | 실제 필요한 action·대상·조건 |
| `excludes` | array of strings / partial에서 필수 | 원 LO의 수행 중 필수로 선언하지 않는 범위; whole에서는 금지 |
| `required_mastery` | integer / requires에서 필수 | 0–4의 숫자; 0은 의미 HOLD. 비필수에서 금지 |
| `mastery_reason` | string / requires에서 필수 | 왜 그 수준의 능력이 필요한가; 비필수에서 금지 |

같은 route 안 동일 source LO의 서로 다른 부분은 허용하지만 exact ability 중복은 금지한다. OR route의 exact 중복도 금지한다. 서로 다른 threshold가 같은 source에서 필요하면 부분별 의미를 보존하고 전체 LO의 최대 mastery 하나로 합치지 않는다.

Provenance object: `input_commit`(40자리 실제 Git snapshot), `basis`(이번 첫 profile에서는 정확히 `design_judgment`), `refs`(non-empty array). 각 ref는 `path`와 `locator` non-empty strings를 갖는다. Locator는 JSONL의 stable LO/K ID와 필요 field, pilot handle 또는 문서 절/제목을 사용한다. 모든 source/target LO와 판단에 직접 쓴 Concept scope/boundary, pilot 사례와 context 계약 위치를 input commit에서 resolve할 수 있어야 한다. Physical line만으로 stable identity를 대신하지 않는다. 모든 refs는 이 snapshot에 대해 읽으며 최신 내용으로 자동 치환하지 않는다. 후속 empirical basis enum/storage는 실제 evidence 설계 때 Schema revision으로 명시한다. 일반 `revision`, timestamp, author, audit pass boolean은 record에 추가하지 않는다. 승인·검토·중요 변경 이유는 repository admission/change packet과 Git history에서 추적한다.

정본 JSONL은 UTF-8/no BOM/LF/final newline, compact standard JSON, physical line당 object 하나, duplicate members/NaN/Infinity/blank record 금지다. Numeric PR ID ascending; field order는 위 record 표 순서, target는 lo/depth, context는 key/conditions/resources, resource는 key/availability/description/replaces/residual/ref, ability는 표 순서, provenance는 input_commit/basis/refs다. Route·ability·resource·ref 배열 순서는 저자가 선언한 순서를 보존한다. 순서가 논리적 AND/OR의 우선순위를 뜻하지 않으며 projection pointer는 commit에서만 유효하다. 재정렬은 Git 변경과 ref 재생성을 요구한다.

### 미결·부정의 위치

Unresolved/HOLD는 candidate judgment다. Unsupported/rejected도 해당 맥락의 부정 판단이며 정본 active Requirement에 포함하지 않는다. Canonical status는 active/retired만이고 candidate supported status를 복사하지 않는다. Candidate와 역사 검토에서 이유를 보존하되 graph에 투영하지 않는다. 이미 발급한 관계가 잘못되었다면 삭제 대신 retired tombstone과 영향 검토를 남긴다. 미결을 수용할 빈 source LO나 provisional mastery를 만들지 않는다.

## 8. Lifecycle·authoring·validation·admission

Requirement continuity 질문은 ‘기존 참조가 여전히 같은 target 수행·context·need와 능력 의무를 가리키는가’다. 오탈자·이미 의도한 부분의 명료화·동일 수행의 threshold 교정은 의미 확인/영향 재검토 뒤 SAME PR. Target LO/context 계약/need/relation, 요구되는 능력의 의무나 OR 경로가 materially 바뀌면 NEW PR이며 옛 record 유지/retire를 검토한다. True split/merge는 옛 identity retirement와 새 identities, ID 재사용 없음이다. 모든 active→retired는 terminal이고 마지막 계약과 reason을 보존한다. 미래 issuance/history 검사는 현재 snapshot뿐 아니라 canonical main 이력과 대조한다.

입력 source/target LO의 변경·retirement 또는 직접 참조 Concept scope/boundary의 변경은 영향받는 Requirement를 찾아 의미 재검토한다. 새 source/target를 lineage로 자동 redirect하지 않는다. LO retirement closure의 current-reference audit에 Requirements와 파생 export를 포함한다. Retired PR의 source/target LO는 존재해야 하지만 현재 retired이어도 역사 참조로 허용한다. Active projection은 모든 endpoints active/모든 관련 재검토 완료를 요구한다. 원 Concept은 grounding 입력일 뿐 새 Concept→LO prerequisite를 유도하지 않는다.

Writer의 최소 입력은 target LO 원문, 수행 사례/context·자료 계약, 사용되는 need·최소 능력/배제 부분과 source LO, target 단계와 실패 반사실을 설명하는 reason, required 문턱과 그 이유, 대체 route별 동등성 이유, 정확 snapshot/provenance다. 독자 이수 목록·분야 관습·Semantic Graph requires는 admission 입력의 이유를 대신하지 못한다. OR route마다 모든 능력을 함께 갖추면 같은 need를 충족하는 이유를 root reason에 명시한다.

| 검사 | 기계 지원 | 의미·인간 책임 |
| --- | --- | --- |
| 구조·참조 | closed fields/type/enum/padding/non-empty/active endpoints/refs resolve/unknown 차단 | 출처가 수행을 직접 포함하는지, partial의 명료성 |
| Context | 동일 target/key equality·자료 key 중복·제공/부재 표기 | target 수행 보존, 자료 충분성·대체/잔여, 전체 조합 compatibility |
| Required | 문턱·reason 존재, OR/AND 구조, exact projection·all routes union DAG·self-edge·duplicate 후보 | 실제 필요성, branch 동등성·독립 능력의 conjunction, Mastery 수준의 설계 근거 |
| 운영 | SHA/commit·history·retired 불변성·허용 diff·source 변경 영향 탐색 | continuity·migration·영향 재검토·admission set 승인 |

Admission gate는 (1) 이 Schema의 **인간 승인과 canonicalization**(2026-10-13 승인; 이 checkpoint에서 정본화), (2) concrete Requirement candidates의 구조·새 관계 의미 검토 및 인간 **exact admission set** 승인, (3) main 동기화·single writer allocation·검증·normal commit/non-force remote main 수용이다. Schema 승인으로 Pilot9 또는 미결4나 전체817를 등록하지 않는다. AI PASS는 (1)/(2)의 인간 승인을 대체하지 않는다.

Schema 변경은 지원 field/type/논리/profile/gate·identity 계약의 변경으로 별도 Schema 결정·승인을 요구한다. Requirement 데이터 변경은 승인된 contract 안의 특정 의미 판단·threshold/자료·lifecycle 변경으로 affected meaning/admission 승인을 거친다. Candidate 검토 중 contract를 조용히 바꾸지 않는다. Pending 의미 검토는 candidate/change packet에서 관리하고 canonical record에 generic review status를 추가하지 않는다. 필요한 기존 record와 영향 목록이 있으면 검토 완료까지 새로운 validated export를 중지한다.
