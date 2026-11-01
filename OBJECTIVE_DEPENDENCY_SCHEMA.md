상태: **정본 — Objective Dependency Schema v0.1 / Dependency population 없음**

# Objective Dependency Schema v0.1

## 1. 목적·단일 의미 원천

[Prerequisite Requirement Schema](PREREQUISITE_REQUIREMENT_SCHEMA.md)가 유일한 canonical semantic source다. Objective Dependency는 Requirement와 query context에서 파생한다. 이 문서는 승인 입력 commit `218ac532747092c9e3bc70f4bd5151fcfff174cb`의 Schema Proposal §5 계약을 정본화한다. 실제 사용자 승인·대안·비용은 [ADR 0007](decisions/0007-prerequisite-requirement-objective-dependency-schema-v0.1.md)에 기록한다.

출력은 context-labeled view이며 source는 Requirement 하나다. Objective Dependency에 공식 ID를 발급하거나 별도 manually edited canonical Registry를 만들지 않는다. `source_lo → target_lo`는 해당 Context와 선택 route에서 명시된 능력이 target 수행을 가능하게 한다는 뜻이다. Source LO 전체 이수나 모든 Context에서의 무조건 필수성을 뜻하지 않는다. 능력 충족·학습 이력은 Requirement Schema §4의 별도 후속 계층이며 개인 view가 canonical Requirement를 바꾸지 않는다.

## 2. D4 — Query·projection envelope·추적성

Query는 source Registry commit, 선택 target/context 집합, optional selected LO 집합을 고정한다. source records가 미재검증 상태면 해당 query는 HOLD다. Projection envelope는 `source_commit`, `contexts`, `mode`, `items`를 필수로 가진다. Query에 선정 LO 집합을 지정했다면 optional `selected_los`에 그 집합을 중복 없이 numeric LO ascending으로 보존한다. `mode`는 `alternatives`(선택 전 group view) 또는 `selected_routes`(유효한 경로 선택 후 adjacency)다. Bare global mode는 학습 경로 export로 제공하지 않는다.

각 item 필수 정보는 `source_lo`, `target_lo`, `relation`, `context_key`, `requirement_ref: {id, pointer}`, `route`, `ability_scope`, `performance`다. Pointer는 예컨대 `/any_of/0/all_of/0`; 배열 위치는 독립 identity가 아니므로 **commit + PR ID + pointer**를 함께 resolve한다. Requires에는 `required_mastery`를 복사하고 원본 reason·Mastery 이유·자료 계약을 ref로 복원한다. 다른 field를 손으로 고치지 않으며 원 source와 exact 대응을 검사한다. `selected_los`가 있으면 모든 item에 `outside_selection` boolean을 저장하며 source 또는 target LO 중 하나라도 그 집합 밖이면 true다. `selected_los`가 없으면 이 field는 금지/생략한다. 이로써 source commit과 query envelope에서 exact 재계산할 수 있다. 이는 전체 Registry 밖이나 미등록 endpoint라는 뜻이 아니다.

OR가 하나보다 많으면 `alternatives`의 각 branch item은 선택 후보다. `relation=requires`가 있더라도 모든 branch를 개별 필수 능력으로 읽지 않는다. Envelope mode·Requirement group·route를 삭제한 edge export는 invalid다. `selected_routes`는 Requirement마다 정확히 한 유효 route를 선택하고 그 route의 all_of를 함께 투영한다. 이것은 해당 route를 택한 조건부 요구이며 다른 route가 없다는 뜻이 아니다. 독자 만족을 선택 근거로 사용하는 개인 view도 원 Requirement를 바꾸지 않는다.

Recommended/deepens는 같은 상세 source format의 `relation` 값으로 저장하되 required mastery field를 금지한다. 방향은 ‘선행/연결 능력이 target에 도움/심화를 제공’하는 `source → target`이며 필수 순서가 아니다. Required DAG·진입 blocking·closure에 포함하지 않는다. 별도 canonical advisory source를 두지 않는다. 여러 능력 묶음의 AND/OR는 advisory의 도움 조건일 뿐 required로 승격하지 않는다.

`source_commit`은 Requirement Registry가 실제 존재하는 Git snapshot이며 `provenance.input_commit`의 판단 입력 snapshot과 구별한다. `contexts`는 query의 target/context 집합을 `target_lo`와 `key`로 보존한다. `requirement_ref.id`는 원 PR ID, `pointer`는 해당 ability 위치, `route`는 그 pointer의 `any_of` 배열 index다. `ability_scope`와 `performance`는 원 ability에서 복사한다. 원본 reason·Context·partial의 excludes·mastery_reason·Target Depth는 동일 snapshot의 Requirement ref로 복원한다. `source_commit + Requirement ID + pointer + query`로 projection을 재구성할 수 있어야 한다. 새 convenience field나 독립 Dependency 의미 source를 추가하지 않는다.

## 3. Required와 비필수·중복·adjacency

`requires`, `recommended`, `deepens`의 원 relation을 보존한다. 비필수의 AND/OR는 도움 조건이며 required 의무가 아니다. 비필수는 required DAG·진입 차단·필수 closure에서 제외한다. 중복 후보의 의미 기준은 [Requirement Schema §2](PREREQUISITE_REQUIREMENT_SCHEMA.md)를 따른다. 그래프의 adjacency dedup은 모든 원 item refs를 묶는 파생 index로만 가능하며 의미 record를 삭제·병합하지 않는다. Context가 다른 pair를 무조건 edge로 집계하지 않는다.

## 4. Context compatibility

**Context compatibility:** 같은 target의 서로 다른 key도 자동 배타적이지 않다. 필수 자료의 provided/absent 계약과 핵심 조건을 대조하여 `compatible / incompatible / unknown`을 query의 파생 판단표로 기록한다. 같은 자료 역할의 제공/부재가 상충하고 같은 수행 occurrence를 지칭하면 incompatible이다. 서로 다른 occurrence를 지칭하면 ‘같은 자료 역할’만으로 배타성을 판정하지 않는다. 완전한 자원 공통 enum이나 compatibility Registry를 만들지 않는다. 자연어 key 비교·서로 다른 context 이름·pairwise compatible만으로 전체 조합의 양립성을 보증하지 않는다. 여러 목표의 context 조합은 공유 artifact/occurrence·조건의 **전체 조합**을 의미 검토하고 근거를 남긴다. Unknown 조합에서는 유효한 경로·추이 prerequisite를 주장하지 않는다.

## 5. 보수적 Required union DAG admission gate

[Ontology §13.1](ONTOLOGY_V1.md#131-knowledge)의 required cycle 금지를 약화하지 않는다. **모든 active required Requirements의 모든 OR route/AND ability를 포함한 LO 합집합 DAG**를 canonical admission gate로 사용하며 Context별·의미적으로 양립 가능한 전체 Context 조합·선택 route graph도 검토한다. Context별 DAG만으로 통과시키거나 배타성을 union 예외로 적용하지 않는다.

합집합은 **모든 active requires records의 모든 OR route/AND ability**에서 LO pair를 모은다. 비필수·retired·미결·rejected는 제외한다. 이는 가능한 선수 지원 후보를 보수적으로 모은 **cycle 검사 전용 graph**이며 한 독자의 커리큘럼이나 모든 branch가 동시에 required라는 의미 graph가 아니다. OR 때문에 불필요한 cycle 거절이 생길 수 있다는 비용을 숨기지 않는다. 같은 source/target self-edge도 HOLD다. 부분 능력 사이의 실제 순환이 없더라도 LO로 투영되어 자기 edge가 생기면 자동 예외를 두지 않는다.

**서로 다른 배타적 context의 union에만 cycle이 있고 실제 모든 적용 조합이 DAG여도 canonical admission은 HOLD**다. 최소 cycle witness와 Requirement refs·context·route를 남긴다. 실제로 잘못된 필요성/범위/자료 계약을 수정할 수 있으면 해당 제안만 재검토한다. 합집합 gate를 통과시키기 위해 정당한 관계를 임의로 recommended로 낮추거나 LO를 split하지 않는다. 타당한 조건부 관계를 허용하려면 별도 인간 승인으로 §13.1 적용 범위를 명시해야 한다. 이 Schema는 그 예외를 도입하지 않는다.

현재 전체 active Requirement union과 신규 admission을 합쳐 gate를 검사한다. 같은 context의 required graph와 승인된 compatible target/context 조합의 selected-route graph도 검사한다. Unknown compatibility면 그 조합의 학습 경로 export는 HOLD; union PASS가 compatibility를 증명하지 않는다. Union DAG면 모든 부분집합도 DAG지만 조건 선택 오류·source exact 대응을 잡는 조건별 검사를 유지한다. 파일럿의 작은 DAG PASS를 전체817 DAG의 증명으로 쓰지 않는다.

## 6. Closure·reduction·export 경계

양립 불가능한 context 사이에서는 추이 closure를 추론하지 않는다. 조건부 A→B, B→C라도 같은 양립 가능한 조건/선택 route이고 중간 LO의 요구 부분과 제공 능력이 대응하는지 검토해야 A의 **어떤 부분**이 C를 지원하는지 말할 수 있다. Node-level reachability를 새로운 직접 Requirement의 reason으로 사용하지 않는다. Global union reachability는 탐색 신호일 뿐 경로/필수성 증명이 아니다.

Transitive reduction은 source Requirement를 삭제하지 않는다. 시각화용 reduced view에서도 숨긴 item refs·context·route·복원 mapping을 유지하고 전체 view로 돌아갈 수 있어야 한다. Graph export는 source commit/group/route/부분/Context refs를 잃으면 ‘정밀 Dependency export’로 제공하지 않는다. 원 Requirement 계약이 있어야 graph artifact가 유효하다.

구조·source exact 대응·필수/비필수 분리·mode/group/route 보존·선정 집합의 boolean·합집합 및 조건별 DAG·재검토 상태를 검사한다. Compatibility·중간 수행 대응·대안 동등성은 의미 검토이며 숫자 reachability만으로 증명하지 않는다. Unknown 또는 incompatible Context 조합은 유효한 경로 export로 제공하지 않는다. Schema-only 정본화는 실제 graph population이나 전체817의 준비 충분성 검증이 아니다. 이번에는 projection 파일·graph engine·영구 validator를 생성하지 않는다.
