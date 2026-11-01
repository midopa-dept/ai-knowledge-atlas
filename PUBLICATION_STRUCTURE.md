# AI Knowledge Book — 출판·학습 구조 정책

상태: **정본 — Part / Chapter Publication View 정책**

인간 승인: 2026-10-13 (Asia/Seoul). 승인 원문과 결정 근거는 [ADR 0008](decisions/0008-part-chapter-publication-structure.md)에 기록한다.

## 1. 목적과 권위

AI Knowledge Book은 **12개 Part 안의 60개 Chapter를 완결된 주요 학습 단위로 삼아 비선형으로 공부하는 교재**로 설계한다. 독자는 관련 지식을 Chapter 안에서 연결하여 학습한다. Concept 하나 또는 Learning Objective 하나를 완료할 때마다 다른 Chapter로 이동하는 구조를 기본으로 삼지 않는다.

이 문서는 이번 책의 Publication View 정책을 소유한다. 지식 분류, Concept의 의미, Learning Objective의 수행 계약과 실제 설명 위치는 구분한다.

| 관리 대상 | Authoritative source | 이 정책과의 관계 |
| --- | --- | --- |
| Level-1 grouping·Macro Area의 identity, 분류 의미와 소속 | [KNOWLEDGE_GRAPH_L1.md](KNOWLEDGE_GRAPH_L1.md) §3 | Part / Chapter가 참조하는 기존 분류 |
| Concept와 단일 `macro_area` home | [registry/nodes.jsonl](registry/nodes.jsonl), [Registry Schema](REGISTRY_SCHEMA.md) | 기본 Chapter 소속을 파생하는 원천 |
| Learning Objective와 Concept grounding | [learning/objectives.jsonl](learning/objectives.jsonl), [LO Schema](LEARNING_OBJECTIVE_SCHEMA.md) | Chapter의 수행·연습·평가 설계 기준 |
| Prerequisite Requirement와 Objective Dependency | [Requirement Schema](PREREQUISITE_REQUIREMENT_SCHEMA.md), [Dependency Schema](OBJECTIVE_DEPENDENCY_SCHEMA.md) | 근거·Context를 갖춘 선행 능력과 파생 관계의 계약 |
| 이번 책의 Part / Chapter 대응과 학습 원칙 | 이 문서 | 출판·교육 설계 정책 |

[Ontology v1.0](ONTOLOGY_V1.md)의 Knowledge / Learning / Exposition 분리와 단일 ontology·복수 Publication View 원칙을 따른다. 새 Knowledge node나 Ontology Layer를 만들지 않으며 Ontology v1.0을 수정하지 않는다. 이 문서에 12개 grouping과 60개 Area의 분류 목록·scope·소속을 별도 정본으로 복제하지 않는다.

## 2. Part와 Chapter의 대응

### 2.1 12개 grouping → 12개 Part

현재 [Level-1 Macro Areas](KNOWLEDGE_GRAPH_L1.md#3-level-1-macro-areas)의 12개 grouping 각각을 이번 책의 Part 하나에 대응시킨다. 기존 grouping의 identity·분류 의미·소속 Macro Area를 보존한다. Part는 출판상 계층이며 새로운 Knowledge Ontology node가 아니다.

Part 표기는 로마 숫자 **Ⅰ, Ⅱ, Ⅲ, Ⅳ, Ⅴ, Ⅵ, Ⅶ, Ⅷ, Ⅸ, Ⅹ, Ⅺ, Ⅻ**를 사용한다. 어느 grouping에 어느 로마 숫자를 배정할지는 후속 출판 순서 설계에서 결정한다. 현재 Level-1 문서의 grouping 순서는 탐색상의 기준이며 최종 출판·학습 순서가 아니다.

### 2.2 60개 Macro Area → 60개 Chapter

이번 책의 대응 정책은 **1 Macro Area → 1 Chapter**다. 현재 공식 Macro Area 60개 각각에 Chapter 하나를 계획하며, 그 Chapter는 해당 Area가 소속된 grouping에 대응하는 Part 안에 둔다. Chapter는 독자가 하나의 관련 지식 영역을 통합적으로 학습하는 주요 단위다. 단순한 Concept 목록이나 LO 목록으로 구성하지 않는다.

실제 Chapter 숫자 **1–60**과 최종 순서는 후속 출판 순서 설계에서 배정한다. Macro Area key, `K####`, `LO####`는 Chapter 번호로 재사용하거나 변경하지 않는다. Part / Chapter / Section의 출판상 위치·번호는 지식·수행 identity와 구분한다. 이번 정책은 새 `chapter_id` namespace나 Section identity·저장 Schema를 정의하지 않는다.

사용자의 “제10장 Transformer”, “10.1 Q/K/V”는 장·절 표기 형식을 설명하는 예시다. 실제 Transformer 장 번호나 Q/K/V 절 배정을 확정한 결정으로 해석하지 않는다.

## 3. Concept home과 실제 설명 위치

현재 active Concept 504개는 각각 공식 `macro_area` home 하나를 가진다. 기본 Chapter 소속은 다음 경로에서 파생한다.

```text
Concept K → registry/nodes.jsonl의 macro_area → 해당 Macro Area에 대응하는 Chapter
```

이 대응을 위해 Node Registry에 `chapter_id`를 추가하거나 Concept 504개의 Chapter 대응을 별도 정본 데이터로 중복 저장하지 않는다. Macro Area key의 분류 역할과 K의 stable identity도 그대로 유지한다.

각 Concept는 해당 Chapter에서 기본 설명 위치를 갖도록 후속 Exposition을 설계한다. **1 Concept = 1 Section** 규칙은 도입하지 않는다. 인접 Concept 여러 개를 한 절에서 함께 다루거나, 큰 Concept를 여러 소절에서 설명할 수 있다. 구체적인 절·소절 번호와 `primary_explanation` 위치는 아직 배정하지 않는다.

Concept의 canonical home은 하나여도 다른 Chapter에서 `review`, `application`, `re_entry` 등의 Occurrence를 가질 수 있다. 이런 재등장은 home 변경이나 Concept 복제의 이유가 아니다. 후반 AI 내용에서 수학 개념·수식이 다시 등장하면 최초 설명 위치를 명시적으로 역참조하고 필요에 따라 Re-entry Block을 제공한다.

## 4. Learning Objective와 Chapter

현재 active LO 817개는 Chapter 내부의 수행·연습·평가 설계 기준이다. LO는 독자가 무엇을 수행할 수 있어야 하는지를 정의하며, Concept와 실제 설명 위치를 대신하지 않는다. **1 Concept = 1 LO = 1 Section** 규칙은 도입하지 않는다.

현재 LO grounding은 Concept 504개 전체를 커버하며, 복수 Concept에 grounding된 LO는 31개다. Multi-Concept LO나 Chapter 간 통합 수행의 설명·연습·평가 위치는 후속 교육 설계에서 결정한다. 첫 Concept의 Chapter에 기계적으로 배정하거나 새 LO로 자동 분해하지 않는다. LO 번호와 grounding 배열 순서도 Chapter 학습 순서를 의미하지 않는다.

기존 LO statement·grounding·identity·lifecycle·observable performance 규칙을 변경하지 않는다. Mastery와 Target Depth는 별도 축이며 Chapter 정책 때문에 LO의 intrinsic field로 추가하지 않는다. Grounding은 직접적인 개념적 기반으로 유지하며 선행 능력이나 prerequisite를 자동 선언하지 않는다.

## 5. Chapter를 완결된 주요 학습 단위로 설계

독자는 Chapter 안에서 관련 지식을 체계적으로 연결하며 다음 기능을 이용할 수 있어야 한다. 각 기능의 실제 내용은 후속 집필·교육 설계에서 구체화한다.

| 단계 | Chapter가 갖추도록 설계할 기능 |
| --- | --- |
| 진입 | 필요한 능력 확인, 부족한 능력의 복습 위치 안내 |
| 통합 학습 | 관련 Concept의 체계적 설명과 수식·직관·메커니즘·구현 사례의 적절한 연결 |
| 연습 | Worked Example, 유제, 충분한 연습 |
| 진단과 복습 | 오류 진단, 피드백, 필요한 복습·Re-entry 안내 |
| 통합 확인 | Chapter 전체를 통합하는 연습·Checkpoint |
| 종료와 다음 선택 | 종료 시 기대하는 수행과 후속 Chapter 안내 |

Ontology v1.0의 Learning, Practice, Sequencing, Exposition, Curriculum Layer를 활용한다. `Module`, `Entry Profile`, `Exit Profile`, `Checkpoint`는 적절한 교육 설계 객체로 사용할 수 있지만, 지식 분류인 Macro Area를 Ontology상의 Module과 동일한 객체로 재정의하지 않는다. Chapter와 Module 사이의 구체적 교육 설계는 후속 단계로 남긴다.

Chapter 단위 학습에는 여러 독서 세션이 필요할 수 있다. 한 번 앉아서 모두 완료해야 한다는 시간 제한이 아니다. 모든 세부 LO의 개별 완료 기록을 다른 Chapter로 이동하는 무조건적 차단 조건으로 만들지 않는다.

본문을 읽었다는 사실은 Mastery의 증거가 아니다. Chapter 종료 판단에 사용할 실제 Evidence Requirement, 통합 Checkpoint, Entry / Exit Profile과 충족 판단은 아직 작성하지 않았다. 이 정책의 정본화가 Chapter의 학습 설계 완료나 학습효과 실증을 뜻하지 않는다.

## 6. 비선형 탐색과 그래프의 역할

### 독자의 학습 흐름

독자는 관심과 수준에 맞는 Chapter를 선택하고, 진입 능력을 확인한 뒤 관련 개념과 예제를 연결하여 학습한다. 연습·복습·통합 Checkpoint를 거쳐 다음 Chapter를 선택할 수 있도록 설계한다.

필요한 선수 능력이 이미 있으면 중복 학습을 강제하지 않는다. 부족하면 적절한 과거 Chapter의 절·소절이나 Re-entry Block으로 안내한다. 하나의 LO를 충족했다는 이유만으로 다른 Chapter로 즉시 이동시키지 않는다. 능력 보유와 특정 Chapter·LO의 이수 이력은 구분한다.

### 저자의 설계 기준

Concept Graph는 지식의 의미·연결 구조를, LO는 필요한 수행을, Prerequisite Requirement는 실제 선행 능력의 조건·Mastery·이유를 표현한다. 이를 Chapter 내부 설계와 Chapter 간 경로 설계에 활용한다.

Macro Area 소속이나 Knowledge Semantic Graph edge만으로 Chapter 간 필수 선수관계를 자동 추론하지 않는다. 모든 LO pair를 독자에게 노출하는 학습 경로로 만들지도 않는다. Chapter 간 추천 경로와 진입 조건은 실제 교육적 근거와 Context에 따라 후속 설계한다. 본권·해설서에는 목표 파악, 자기평가, 복습과 다음 선택에 필요한 정보를 독자에게 알맞게 제공한다.

기존 Requirement / Dependency Schema의 부분 능력·Context·자료·Mastery·OR-of-AND 의미와 보수적 required union DAG admission gate를 변경하지 않는다. Union graph는 cycle 검사용이며 독자의 필수 경로가 아니다. `recommended`·`deepens`를 필수 진입 차단으로 승격하지 않으며, unknown compatibility의 경로 export HOLD도 유지한다.

## 7. 이번 정본화의 경계와 후속 결정

이번에 확정한 것은 Part / Chapter 대응, Chapter 단위 통합 학습, 비선형 탐색과 설명·수행·지식 구조의 분리 원칙이다. 다음은 ChatGPT 메인 오케스트레이션에서 별도로 결정한다.

- Part의 로마 숫자 배정, Chapter 1–60의 최종 순서·번호와 구체적 목차
- Concept별 절·소절 번호와 Exposition / Occurrence 위치
- LO의 구체적 설명·연습·평가 배치와 Chapter 간 통합 수행 설계
- Chapter별 Entry / Exit Profile, Evidence Requirement와 통합 Checkpoint
- Chapter 간 선수관계·추천 경로·Re-entry의 구체적 설계
- 본권·해설서·Instructor's Guide 집필과 Problem Bank / Task Model 제작

기존 Concept·LO·Knowledge Graph·Schema와 후보 데이터는 이 작업으로 변경하지 않는다. 기존 선수관계 원본 23건 중 ready20 / HOLD3은 인간 admission approval 전 후보로 유지한다. 공식 PR ID 발급·예약, PR Registry 생성, ready20 admission, HOLD3 해결·승격을 수행하지 않는다. 새로운 Ontology v1.1도 제정하지 않는다.

## 8. 사람을 위한 안내의 유지

루트 [README](README.md)는 독자·기여자를 위한 프로젝트 소개와 현재 상태 요약이다. 상세 정책은 이 문서와 각 authoritative source에, 내부 진행 상태·historical checkpoint는 PROJECT_STATE.md에 둔다. 중요한 변경을 수행하는 동일한 작업에서 README 영향 여부를 확인하며, 지속 갱신 운영 규칙은 AGENTS.md에서 관리한다.

## 9. 번호 있는 Section과 출판 참조

2026-10-13의 후속 인간 결정은 [ADR 0012](decisions/0012-section-based-authoring-and-detailed-pilot.md)에 기록한다. Chapter는 완결된 주요 학습 단위이며, 그 안의 Section은 하나의 중요한 질문과 관련 기술을 충분히 설명하고 연습하는 독서 단위다. 각 Chapter를 교육적으로 의미 있는 번호 있는 Section으로 나눈다. 여러 Concept의 통합과 한 Concept의 여러 절에 걸친 설명을 허용하며 `1 Concept = 1 Section`, `1 LO = 1 Section` 규칙을 만들지 않는다. Section은 편집·학습 구조이며 새 Ontology node나 Knowledge identity가 아니다.

독자용 절 번호는 `장.절`, 정의·정리·예제·유제·연습문제·심화문제는 `장.절.유형별 순번`으로 표시한다. 각 유형의 카운터는 절마다 초기화하며 유형을 포함한 전체 명칭으로 식별한다. 증명은 해당 정리에 연결하고 형식을 채우기 위한 허위 정리를 만들지 않는다. 필요한 수식·그림·표에도 절에 종속된 번호를 제공할 수 있게 하되 일반 설명 소제목마다 숫자를 강제하지 않는다.

고정 내부 참조 표지와 독자용 번호를 구별한다. 번호를 원고와 해설에 중복 수동 입력하지 않고 조판에서 자동 생성하며, 장 번호 변경 시 절·객체·교차 참조를 함께 갱신한다. 내부 표지는 공식 Exercise·LO·Concept ID의 발급·변경이 아니다. 본권과 별도 해설서의 전체 명칭을 일치시킨다.

60개 Chapter의 최종 순서·번호와 구체적 목차는 미확정이다. Transformer 시제품의 임시 장 번호 10은 번호 체계 시연이며 정본 제10장 배정이 아니다. 이 원칙은 앞 절의 번호 유보를 해제하지 않는다.
