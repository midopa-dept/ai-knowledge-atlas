# ADR 0007 — Prerequisite Requirement / Objective Dependency Schema v0.1

상태: **인간 승인 완료 / Schema-only 정본화 / 데이터 admission 없음**
결정일: 2026-10-13 (Asia/Seoul)

## 1. 실제 인간 승인과 입력 identity

사용자가 2026-10-13 (Asia/Seoul) ChatGPT 메인 오케스트레이션 채팅에서 승인했고 이 정본화 세션의 지시로 전달한 원문:

> «candidates/prerequisite-schema-decision-v0.1/의 D1–D5, 부분 능력 참조, 능력 충족과 이력 분리, Context와 OR-of-AND, Requirement 단일 의미 원천 및 추적 가능한 Dependency projection, Required Mastery 및 PR ID/lifecycle, 보수적 합집합 DAG gate를 하나의 Schema 정책으로 승인한다. 위 여섯 경로의 Schema-only 정본화를 허용한다. Registry 생성·ID 발급·관계 admission 및 전체 population은 별도 승인으로 남긴다.»

이것은 실제 사용자 승인이다. 기존 독립 AI 검토의 PASS를 인간 승인으로 승격한 기록이 아니다. 최신 명시적 승인으로 Schema 대기 상태를 종료하며 후보 파일의 당시 PENDING 표시는 역사로 보존한다.

실제 시작 repository는 `midopa-dept/ai-knowledge-book`, branch `main`, local HEAD=origin/main=actual remote main=`218ac532747092c9e3bc70f4bd5151fcfff174cb`, working tree clean이었다. `git ls-remote origin refs/heads/main`으로 원격을 조회했고 ADR 0007 및 신규 Schema 경로 충돌이 없음을 확인했다. 승인 입력6파일은 이 commit의 bytes와 일치한다.

| 승인 입력 | SHA-256 |
| --- | --- |
| README | `9c681e32a96823b15fdbbe5f1f3a9219bb24aafd03a048bcc4c316f7970e9847` |
| SCHEMA_PROPOSAL | `4422602254e8817c40451175134fe5af417c2814e36e9253ca30cbd7c2cc39d2` |
| DECISION_PACKET | `d2ff5295133ab6098ca2c616ffd33ef3719e7465ba3745966157ace27ff6d986` |
| ILLUSTRATIVE_RECORDS | `e12ea3704b7462a34524db1cee94cef29eea25d1841405ab18c94fa155196dc0` |
| REVIEW | `f2c9b5fe263b99e1ae6bef7c1083940b18db938e7b60ca74c241024ba82cf261` |
| VALIDATION | `ca8902971e1e955621f73b8533bef3ed4a70e9718e3f7ffedd664a9c59092710` |

직접 의미 입력은 Proposal, 인간 승인 범위 입력은 Decision Packet이다. 최종 독립 검토의 Proposal·fixture hash와 일치하므로 **PASS_FOR_SCHEMA_DECISION_ONLY / 잔여 결함0**을 해당 입력의 기존 근거로 재사용한다. 최초 검토의 선정 집합 추적 결함1과 국소 수정 확인1은 REVIEW에 보존한다. 신규 AI review·817 LO 의미 감사·Pilot42 또는 required9 재심사는 하지 않는다.

## 2. 선택한 D1–D5와 포기한 대안

| 결정 | 채택 및 이유 | 포기한 대안·비용 |
| --- | --- | --- |
| D1 | 공식 LO를 source identity로 유지하고 실제 `performance`, partial/whole, partial의 `excludes`를 명시한다. 원 statement의 direct inclusion을 검토하여 과잉 요구를 막는다. | Whole-LO 원자 요구는 간단하지만 필요하지 않은 수행까지 의무화한다. 새 LO/Skill 분해는 독립 identity·lifecycle 운영 범위가 크므로 별도 결정으로 남긴다. 부분 수행 의미 검토와 source LO 변경 영향 재검토 비용을 수용한다. |
| D2 | Requirement existence, learner-specific satisfaction, course/unit completion history를 분리한다. 외부 교재·실무에서 얻은 능력도 후속 만족 판단의 입력이 될 수 있다. | 개인 상태를 Requirement에 넣거나 독자 능력에 따라 canonical graph를 고치면 의미 source와 개인 evidence가 섞인다. 후속 Entry Profile/Mastery Evidence의 대응 판단 비용은 남는다. |
| D3 | Inline Context·자료 provided/absent/unknown·대체/잔여 수행과 한정적 비재귀 OR-of-AND를 사용한다. 동일 target/key의 전체 Context·Target Depth equality를 요구한다. | 자연어 조건만으로는 자료 상태와 대체 범위 추적이 부족하다. 범용 DSL·임의 NOT·재귀 논리는 과도하다. Inline 계약 중복/equality, 제공 자료 충분성, OR route 동등성, 자연어 전체 Context 조합 compatibility의 의미 검토 비용을 수용한다. |
| D4 | Requirement가 단일 의미 원천이며 commit·PR ID·pointer·route·query·부분 수행·Mastery·Context를 복원하는 Dependency projection을 파생한다. | Bare pair는 부분/OR/조건을 지우고, 독립 context-labeled Registry는 두 의미 source를 만든다. Snapshot과 query의 exact 대응 검사 비용을 수용한다. `selected_los`와 source/target 기준 boolean 보완을 포함한다. |
| D5 | Required Mastery를 ability별 integer 0–4와 `mastery_reason`으로 보존한다. 문턱은 설계 판단이며 Target Depth·측정·LO intrinsic field와 분리한다. | Intrinsic Mastery는 LO 경계와 충돌한다. Evidence까지 모든 문턱을 비워 두면 required 계약을 충족하지 못한다. 0 또는 근거 부족은 HOLD하고 실제 evidence 교정은 후속 승인·Schema revision 경계로 남긴다. |

## 3. 보수적 union DAG gate와 비용

모든 active requires Requirements의 모든 OR route/AND ability를 포함한 LO 합집합 DAG를 canonical admission gate로 채택한다. 현재 active union과 신규 admission을 합쳐 검사하고 Context별·양립 가능한 전체 Context 조합·선택 route도 검토한다. 비필수·retired·미결·rejected는 required graph에서 제외한다.

Context별 DAG만으로는 동시 조합을 놓친다. 양립 가능한 조합별 DAG만으로 배타적 Context의 union cycle을 허용하는 대안은 Ontology §13.1의 적용 범위를 제한하는 별도 인간 결정을 필요로 하므로 채택하지 않았다. **Union-only cycle도 HOLD**하며 self-edge·부분 수행을 자동 예외로 처리하지 않는다. Minimum cycle witness와 Requirement/context/route refs를 남긴다.

이 정책은 타당한 조건부 관계까지 HOLD할 수 있다. OR나 배타적 Context의 유효 관계를 합집합 gate가 거절하는 비용을 공개적으로 수용한다. Gate를 통과시키려 정당한 required 관계를 무단 recommended로 낮추거나 LO를 split하지 않는다. 예외가 필요하면 별도 인간 Ontology 적용 범위 결정으로 다룬다.

합집합은 cycle 검사 전용이다. 모든 OR branch를 한 독자의 동시 이수 의무로 바꾸지 않으며 union reachability를 실제 필수성·새 직접 Requirement의 reason으로 사용하지 않는다. 양립 불가능한 Context 사이에서 closure를 생성하지 않는다. Unknown compatibility의 경로 export는 HOLD한다.

## 4. 정본 계약의 소유 위치와 대응

| 승인 source | 정본 소유 위치·보존 사항 |
| --- | --- |
| Proposal §2 / D1 | [Requirement Schema §3](../PREREQUISITE_REQUIREMENT_SCHEMA.md): source LO·partial/whole·direct inclusion·excludes·source 변경 영향 |
| Proposal §3 / D2 | Requirement Schema §4: 요구/만족/완료 분리·외부 취득 능력·개인 record 미지원 |
| Proposal §4 / D3 | Requirement Schema §5·§7: Context·Resource·provided/absent/unknown·조건부 replaces/residual/ref·OR-of-AND·target/key equality |
| Proposal §4 compatibility 및 §5 / D4 | [Dependency Schema §2–6](../OBJECTIVE_DEPENDENCY_SCHEMA.md): query/envelope/items·mode·selected_los·outside_selection·원본 복원·비필수 제외·compatibility·union gate·closure/export |
| Proposal §6 / D5 | Requirement Schema §6·§7: Mastery scale·ability별 이유·0/근거 부족 HOLD·Depth 분리·설계 판단 |
| Proposal §7 | Requirement Schema §2·§7: PR 문법/발급·미래 경로·closed fields·정확한 nested types/조건·provenance·배열/field 순서·JSONL |
| Proposal §9 | Requirement Schema §8: SAME/NEW PR·retired tombstone·terminal lifecycle·reference impact·Git history·admission/검증 분리 |
| Proposal §10 / Packet 정확 범위 | 이 ADR과 [LO Schema §11](../LEARNING_OBJECTIVE_SCHEMA.md#11-objective-dependency-and-prerequisite-requirement-boundary), [learning 안내](../learning/README.md), Project State |

Requirement Schema가 의미·record를, Dependency Schema가 파생 query·graph/export를 소유한다. LO Schema §11은 경계와 두 Schema 연결만 제공한다. 기존 LO record shape·identity·grounding·lifecycle·Mastery/Depth 및 다른 normative 절은 변경하지 않는다. Ontology v1.0 §2.2·5.6·13.1과 상위 Node Identity/Registry 계약은 유지한다. Ontology 개정·acyclicity 약화·Context 예외 도입은 없다.

계획을 실행 전 검토하여 기준점/승인 입력 확인 → 승인 계약의 직접 이관·대안의 ADR 분리 → 여섯 경로 최소 연결 → source fidelity·보호 bytes·링크/참조·diff 검증 → single Git writer의 정상 commit/non-force push → 실제 remote equality·clean 확인 → STOP으로 제한했다. 새로운 정책 선택이나 field/status 추가는 없다.

## 5. 정확한 변경 경로와 별도 admission 경계

이번 변경은 정확히 다음 여섯 경로다.

1. `PREREQUISITE_REQUIREMENT_SCHEMA.md` — 신규 정본
2. `OBJECTIVE_DEPENDENCY_SCHEMA.md` — 신규 파생 계약 정본
3. `decisions/0007-prerequisite-requirement-objective-dependency-schema-v0.1.md` — 이 결정 기록
4. `LEARNING_OBJECTIVE_SCHEMA.md` — §11만 최소 갱신
5. `learning/README.md` — 새 Schema 역할·미생성 데이터 경계 추가
6. `PROJECT_STATE.md` — 최신 완료 상태 추가·이전 상태 역사 보존

정본 데이터는 LO **817 active / 0 retired / LO0001–LO0817**, Concept504·Semantic Relations603 그대로다. PR Registry 없음 / PR ID 발급·예약0 / 관계 admission0 / Canonical Objective Dependency population 없음. 미래 `learning/prerequisite_requirements.jsonl`은 빈 파일도 생성하지 않는다. 별도 공식 Dependency/Skill/Context ID도 발급하지 않는다.

후속 concrete Requirement candidates는 승인 Schema 안의 구조·새 관계 의미 검토와 인간 exact admission set 승인을 거친 뒤 main 동기화·single writer allocation·검증·정상 remote 수용을 별도로 수행한다. Pilot required9·recommended/deepens14·미결4의 자동 정본화나 전체817 population은 없다. a-cache의 전체 준비 충분성은 미확보다. Entry Profile Registry·개인 학습 DB·Evidence Requirement·Mastery Evidence·Task Model·Exercise·Curriculum/Pathway·목차·본문·production graph engine·새 영구 validator는 생성하지 않는다.

## 6. 검증·Git 전달의 증거 경계

검증은 승인 source와 정본 대응, 여섯 경로 범위, 기존 정본·후보·역사 bytes, 로컬 Markdown 링크/절 참조, LO Schema §11의 경계 일관성, Registry/ID/admission 미실행과 `git diff --check`에 한정한다. 기존 VALIDATION의 표현 실험·LO Admission의 적격 validator 결과는 입력 불변을 확인하여 재사용한다. 의미 재감사나 새 실험을 하지 않는다.

2026-10-13 실제 문서 정본화 검증 결과:

- 승인 계약 이관13블록 exact 및 Proposal §7의 전체 field/type/조건/serialization 대응 PASS. D1–D5·OR-of-AND·자료3상태·부분/whole·Mastery/Depth·lifecycle/ID·projection envelope/선정 집합·union DAG gate를 원문과 대조했다. 새 미승인 의미 변경0이다.
- 허용 경로 exact6 PASS. 기존 tracked 보호 파일 **8120/8120 SHA-256 불변**; Ontology·Knowledge Registry/Graph·terminology·Frozen Proposal·Pilot·Schema 후보·검토/감사 근거 불변이다. LO Schema §11 밖 bytes, Project State 역사 전체와 Learning 기존 내용도 보존했다.
- 여섯 변경 문서의 로컬 Markdown 링크 **294/294**, fragments **6/6**, 문서 절 대응·UTF-8/LF/final newline 및 `git diff --check` PASS. 새 Schema2와 LO Schema §11의 단일 원천·부분 수행·Mastery/Depth·DAG 경계 일관성을 확인했다.
- LO817 active·0 retired·공식 ID 집합, nodes504, semantic_edges603의 count/hash PASS. SHA-256은 각각 `578b54496f4fd0ddbfa7c6e9abb5adf90bbba4fac4d65972340b1b663a68a8dc`, `15e5fc65cccceec1ac320ff4c2fe65fdc22d7a2a901e45581ffc5f54802cbf53`, `dc26a2e9e145f393050712a17ba522b5c9222af58fadb3cd20064f972183e95f`로 유지했다.
- 승인 입력6파일 baseline bytes와 REVIEW의 최종 Proposal·fixture identity 일치 PASS. 새 PR Registry·구체 PR ID·관계 데이터 없음 PASS. 임시 문서/무결성 검사만 repository 밖에서 수행했고 새 영구 검사 도구·의미 감사·데이터 검증 실험은 추가하지 않았다.

실제 commit SHA·non-force push·actual remote main 수용·local HEAD=origin/main=actual remote main·working tree clean은 실행 후 Git history와 최종 사용자 보고에서 확인한다. 미래 push 성공을 선기록하지 않는다. 완료 판정은 **SCHEMA-ONLY CANONICALIZATION PASS / NO DEPENDENCY ADMISSION**이며 완료 후 **STOP**한다.
