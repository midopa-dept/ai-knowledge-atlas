# ADR 0008 — Part / Chapter 출판·학습 구조와 README 관리 정책 정본화

상태: **인간 승인에 따른 정본 결정**

승인일: 2026-10-13 (Asia/Seoul)

적용 문서: [PUBLICATION_STRUCTURE.md](../PUBLICATION_STRUCTURE.md)

## 배경

기존 지식 분류는 12개 Level-1 grouping과 60개 Macro Area다. Concept 504개와 LO 817개는 등록되어 있지만, 독자가 이 지식을 어떤 단위로 연결하여 학습할지는 출판·교육 설계 정책으로 명시할 필요가 있었다. 루트 README에는 초기 구축 단계, issued LO 0, 과거 정본화 자리 안내가 남아 있어 실제 프로젝트 상태와 독자의 학습 방식이 충분히 드러나지 않았다.

작업 시작 시 branch는 `main`, local HEAD = origin/main = actual remote main은 `cd91ca607dde0a8c595d7bc30b309b48427d8ebb`였으며 working tree는 clean이었다. ADR 0008과 신규 출판 정책 경로에 충돌이 없음을 확인했다.

## 인간 승인 근거

사용자가 2026-10-13 (Asia/Seoul) ChatGPT 메인 오케스트레이션 채팅에서 명시한 원문을 이 세션에 전달했으며, 다음 발언을 인간 결정의 근거로 기록한다.

> 대분류 12개짜리는 분류 체계 남겨두고 이걸 로마자 구분으로 각각을 하나의 큰 대륙이라 두고, macro area 60개짜리를 원래 이야기한게 맞다. 그러면 504개 concept가 각 chapter에 들어가는거지.
>
> 이를테면 만약에, 10장이 transformer면, 10.1장 q/k/v 이런 식이라는거지(예시에 불과함).

이어 사용자가 명시적으로 요청했다.

> 그래. 이 목표도 정본에 반영할 수 있도록 하자. 그리고 이런 것들이 리드미에 제대로 반영 안 되어있음. 리드미는 사람이 읽기 좋은 형식으로(ai 참고용 아님) 작성해놓고 계속 갱신하도록 하자.

본 작업 지시는 Part Ⅰ–Ⅻ 표기, 1 Macro Area → 1 Chapter, Chapter 기본 학습 단위, 데이터·Ontology 불변, 번호·세부 설계 유보와 README 유지관리 정책까지 명시적으로 승인했다. “10장이 transformer”, “10.1장 q/k/v”는 형식 예시이며 실제 번호·절 배정 승인이 아니다. 기존 ready20 선수관계 후보의 admission 승인으로 확대 해석하지 않는다.

## 결정

1. 기존 12개 grouping을 보존하고 이번 책의 Part 12개에 각각 대응시킨다. 로마 숫자 Ⅰ–Ⅻ를 사용하되 최종 배정 순서는 유보한다.
2. 기존 Macro Area 60개 각각에 Chapter 하나를 대응시킨다. Chapter 1–60의 최종 순서·번호는 후속 설계에서 배정한다.
3. Concept의 기본 Chapter 소속은 공식 단일 `macro_area` home에서 파생한다. `chapter_id`를 Registry에 추가하거나 504개 대응을 별도 정본으로 저장하지 않는다.
4. Chapter를 완결된 주요 학습 단위로 삼아 진입 확인, 설명·예제·연습·복습·통합 Checkpoint, 기대 수행과 다음 선택 안내를 연결하도록 설계한다. 여러 독서 세션에 걸친 학습이 가능하며 모든 세부 LO 완료를 무조건적인 이동 차단으로 만들지 않는다.
5. Concept / LO / Section 사이의 일대일 규칙을 만들지 않는다. Multi-Concept LO는 첫 Concept의 Chapter로 자동 배정하거나 분해하지 않는다. Home과 다른 Chapter의 Occurrence를 구별한다.
6. 필요한 능력이 이미 있으면 중복 학습을 강제하지 않고, 부족하면 절·소절 또는 Re-entry로 돌아가도록 설계한다. Macro 소속·Semantic edge에서 필수 선수관계를 자동 추론하거나 모든 LO pair를 독자 경로로 노출하지 않는다.
7. [PUBLICATION_STRUCTURE.md](../PUBLICATION_STRUCTURE.md)를 이번 책의 Publication View 정책 정본으로 신설한다. 지식 분류·Concept·LO 데이터의 기존 authoritative source는 유지한다.
8. [README.md](../README.md)를 독자·기여자를 위한 소개 문서로 재작성하고, AGENTS.md에 지속 갱신 운영 규칙을 둔다. PROJECT.md는 핵심 원칙과 정책 링크를 반영하고, PROJECT_STATE.md는 새 현재 상태와 과거 checkpoint를 구별한다.

## 선택 이유와 대안

Chapter 안에서 관련 지식을 연결하는 독서 단위와 Concept·LO 수준의 정밀한 저술·교육 설계 단위를 함께 유지하기 위한 결정이다. 12개 기존 분류와 60개 Area를 재편하지 않고 출판 구조에 대응시키면 승인된 지식 범위를 그대로 활용할 수 있다.

Concept 또는 LO마다 독서 단위를 나누는 방식은 이번에 승인된 Chapter 단위 통합 학습과 맞지 않는다. Macro Area를 Module과 동일시하는 방식은 지식 분류와 instructional package를 혼합한다. Chapter 대응 데이터를 중복 저장하는 방식은 단일 home 원천과 별도로 동기화할 계약을 늘린다. 따라서 기존 원천에서 소속을 파생하고 설명·연습 위치는 별도 후속 설계로 남긴다.

Chapter 단위 원칙만으로 교육 설계가 완성되지는 않는다. 여러 Concept·LO를 어떻게 연결하고 어떤 통합 수행으로 점검할지 정하는 작업이 필요하다. 이 결정은 인간이 승인한 설계 정책이며 실제 학습효과나 학습자 Mastery를 실증한 결과가 아니다.

## Ontology와 기존 계약의 관계

[Ontology v1.0](../ONTOLOGY_V1.md) §2.1·2.5·9·11·12의 Knowledge / Learning / Exposition 분리와 Publication View를 적용한다. Part / Chapter는 새 Knowledge node나 Layer가 아니며 Macro Area는 Module로 재정의하지 않는다. Module, Entry / Exit Profile, Checkpoint 등은 기존 Layer에서 적절히 활용하는 후속 설계 객체다.

LO의 수행·grounding·identity·Mastery / Target Depth 경계는 [LO Schema](../LEARNING_OBJECTIVE_SCHEMA.md)를 유지한다. [Requirement Schema](../PREREQUISITE_REQUIREMENT_SCHEMA.md)와 [Dependency Schema](../OBJECTIVE_DEPENDENCY_SCHEMA.md)의 부분 능력·Context·OR-of-AND·능력별 Mastery·보수적 required union DAG gate·unknown compatibility HOLD를 변경하지 않는다. Chapter 종료 판단의 Evidence Requirement와 통합 Checkpoint도 후속 단계다.

## README 지속 갱신 정책

승인된 운영 정책은 다음과 같으며 실제 작업 규칙은 AGENTS.md의 “README 유지관리”에서 관리한다.

- 목적·범위·책의 구조·학습 방식·출판 계획이 실질적으로 바뀌면 동일 작업에서 해당 설명을 갱신한다.
- 주요 Registry population이나 큰 설계 단계 완료 시 공개적인 현재 상태 요약을 확인하고 필요한 경우 갱신한다.
- 사람을 위한 요약으로 유지하며 상세 규칙·증거·해시·Git 이력은 복제하지 않고 authoritative 문서로 연결한다.
- 작은 내부 변경에는 불필요한 README churn을 만들지 않으며 모든 commit마다 수정하지 않는다.
- Historical checkpoint와 과거 승인 사실을 소급 변경하지 않는다.
- 완료 보고에는 README 갱신 여부를 포함한다.

## 후속 미결 범위

인간이 승인한 것은 위 정책과 이번 여섯 경로의 문서 변경이다. 이 작성자는 새 장 번호·학습 경로·교육 객체를 결정하지 않았다. 아래 목록은 후속 작업의 범위이며 이번 완료나 자동 실행을 뜻하지 않는다.

- Part·Chapter의 실제 번호·최종 순서와 구체적 목차
- Concept의 절·소절 번호, primary explanation과 review / application / re-entry 위치
- LO별 Exposition / Exercise / Assessment 배치 및 Chapter 간 통합 수행
- Chapter별 Entry / Exit Profile, Evidence Requirement, 통합 Checkpoint와 종료 판단
- Chapter 간 선수관계·추천 경로와 독자용 Re-entry 안내
- ready20의 별도 인간 admission 판단, HOLD3의 별도 해결 판단
- Task Model / Problem Bank와 본권·해설서·Instructor's Guide 집필

이번 정책 때문에 새로운 PR ID를 발급·예약하거나 공식 Registry를 만들지 않는다. Ontology v1.1, 기존 Concept·LO의 의미 재감사, 관계 population, 독립 AI review loop 또는 대규모 validator도 추가하지 않는다.

## 검증과 전달 경계

검증은 현재 분류 수·단일 home·LO grounding coverage, 문서 계약의 정적 대조, 링크·Markdown·허용 diff와 보호 파일 불변성에 한정한다. 결과는 PROJECT_STATE.md의 이 정책 checkpoint에 기록한다. 기존 후보의 판단·파일럿·의미 감사를 재실행하지 않는다.

정상 commit과 non-force push 후 실제 local HEAD = origin/main = actual remote main 및 clean 상태를 직접 확인한다. 실행 전 push 성공이나 최종 commit SHA를 문서에 선기록하지 않는다. Git 전달 결과는 실제 Git history와 완료 보고로 확인하며 후속 설계는 메인 오케스트레이션의 별도 결정으로 남긴다.
