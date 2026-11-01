Status: FROZEN — Ontology v1.0

# AI Knowledge Book — Ontology v1.0

## 1. 목적

Ontology v1.0은 수학의 기초부터 현대 AI, LLM, Agent, Harness Engineering까지 다루는 하나의 거대한 비선형 교재를 일관되게 설계하기 위한 canonical ontology다. 다음 두 사용자를 동시에 지원한다.

- **학습자:** 지식 지도와 상호참조를 이용해 자신의 수준과 관심에 따라 학습 경로를 스스로 선택한다.
- **교육자:** 동일한 지식 구조에서 목표, 대상, 시간에 맞는 교육과정을 설계한다.

책의 물리적 목차나 Part/Volume 구조는 canonical knowledge structure가 아니다. 실제 지식 구조는 ontology와 knowledge graph가 결정한다.

## 2. 핵심 원칙

### 2.1 Knowledge / Learning / Exposition 분리

개념 자체, 학습목표, 책에서의 실제 설명 위치를 구분한다.

### 2.2 No prerequisite without a reason

`requires` 관계는 관습적 교육순서가 아니라 실제 이해에 필요한 경우에만 사용한다. 정밀한 prerequisite는 가능하면 Concept 수준이 아니라 Learning Objective 수준에서 정의한다.

각 required prerequisite에는 최소한 다음 정보가 있어야 한다.

- 필요한 Mastery 수준
- 어떤 target objective/depth에 필요한지
- 필요한 이유

### 2.3 Reading is not mastery

본문을 읽었다는 사실을 학습 완료의 증거로 취급하지 않는다. Learning Objective는 observable performance로 정의하고, 문제·설명·전이·설계를 통해 mastery evidence를 요구한다.

### 2.4 Self-contained learner principle

Instructor's Guide가 없어도 본권과 해설서만으로 완전한 독학이 가능해야 한다. 다음 과정에 필요한 정보가 Instructor's Guide에만 존재해서는 안 된다.

- 선수지식 확인
- 개념 학습
- 연습
- 자신의 이해 확인
- 틀린 경우 복습 위치 찾기
- 다음 경로 선택

### 2.5 Single ontology, multiple publication views

Canonical ontology는 하나이며 본권, 해설서, Instructor's Guide는 서로 다른 projection이다. 각 출판물의 구성은 12절에서 정의한다.

### 2.6 Claim-level epistemic provenance

근거 수준은 Concept 전체가 아니라 개별 Claim에 부여한다. Claim Status는 10.2절의 다섯 범주를 구분하며, 사실적·연구적 주장은 가능한 한 출처와 연결한다.

### 2.7 Mathematics re-entry

후반 AI 내용에서 앞서 배운 수학 개념이나 수식이 다시 등장하면 최초 설명 위치를 명시적으로 역참조한다. 오랜 간격 뒤 재등장하는 핵심 개념에는 Re-entry Block을 사용할 수 있다.

## 3. Knowledge Layer

### 3.1 Concept

Concept는 재사용 가능한 지식 단위다.

| 구분 | 값 |
| --- | --- |
| 대표 type | `concept`, `operation`, `mechanism`, `method`, `system`, `phenomenon`, `engineering_pattern` |
| 역할 | `atomic`, `bridge`, `integration` |

Concept의 분리 기준은 다음과 같다.

- 하나의 중심 질문으로 설명 가능한가
- 독립적인 Learning Objective를 만들 수 있는가
- 구체적인 prerequisite를 지정할 수 있는가
- downstream에서 독립적으로 재사용되는가

Downstream dependency가 명확히 달라지거나 별도의 Learning Objective·Practice Bank가 필요하면 별도 Concept Node로 분리한다.

### 3.2 Formal Object

Formal Object는 수학적 형식 객체로, 다음을 포함한다.

- definition
- axiom / assumption
- identity
- proposition
- theorem
- lemma
- corollary
- proof
- derivation
- counterexample

Proof, derivation, intuitive interpretation을 구분한다.

### 3.3 Engineering Invariant

Agent/Harness/시스템 설계에서 지속적으로 유지하거나 기계적으로 검사하려는 조건이다. 예를 들면 dependency boundary, regression-free state, schema constraint가 있다.

### 3.4 Failure Mode

시스템이나 학습에서 관찰되는 구체적인 실패 양식이다. 주요 관계는 `caused_by`, `manifested_as`, `detected_by`, `mitigated_by`다.

### 3.5 Trade-off

단일 정답이 아니라 조건에 따라 선택이 달라지는 설계관계다. 최소한 다음을 표현한다.

- options
- decision factors
- benefits
- costs
- failure conditions

### 3.6 Misconception

반복적으로 등장하고 진단·교정할 가치가 있는 대표 오개념이다. 관계는 `addressed_by`, `elicited_by`, `diagnosed_by`, `repaired_by`다.

### 3.7 Notation

책 전체에서 수학적 기호의 의미와 최초 등장 위치, 재사용 위치를 관리한다. 오랜 간격 뒤 다시 등장하면 local refresh를 제공할 수 있다.

### 3.8 Entity / Role

파일·문서·관측값 등의 객체 자체와 특정 시스템에서 수행하는 역할을 구분한다. 예를 들어 하나의 파일은 persistent artifact이면서, 모델에게 읽히는 순간 context source 역할도 할 수 있다.

### 3.9 Domain / Terminology / Scope metadata

Domain은 Concept의 분류 및 탐색을 위한 metadata다. Domain 소속 자체는 prerequisite를 의미하지 않으며, prerequisite는 `requires` 등 명시적 dependency로만 표현한다.

Alias / terminology management를 통해 동일 Concept의 약어, 역사적 명칭, 분야별 다른 명칭 등을 관리할 수 있어야 한다. Scope metadata에는 설명 범위와 intended scope를 기록하여, 너무 큰 Concept가 의도하지 않게 과도한 내용을 끌어들이지 않도록 한다.

## 4. Knowledge Relations

| 관계 분류 | 관계 |
| --- | --- |
| Learning-order relations | `requires`, `recommended`, `deepens` |
| General knowledge relations | `component_of`, `generalizes`, `specializes`, `mathematically_related`, `identity_or_decomposition`, `contrasts_with`, `applied_in`, `used_to_analyze`, `motivates`, `explains`, `historically_leads_to` |
| Engineering relations | `caused_by`, `manifested_as`, `detected_by`, `mitigated_by`, `enforced_by` |

Prerequisite DAG와 general concept connection graph를 논리적으로 구분한다.

`requires`는 이해에 필요한 필수 dependency, `recommended`는 필수는 아니지만 권장되는 선행 학습, `deepens`는 이해를 심화하는 관계다. `recommended`와 `deepens`를 required prerequisite로 취급하지 않는다.

## 5. Learning Layer

### 5.1 Learning Objective

Concept를 안다는 추상적 표현 대신 학습자가 무엇을 수행할 수 있어야 하는지를 정의한다. 좋은 objective는 observable action을 사용한다.

- **나쁜 예:** Entropy를 이해한다.
- **좋은 예:** 주어진 이산 확률분포의 entropy를 계산하고 값의 차이를 설명할 수 있다.

### 5.2 Objective Dependency

한 Learning Objective가 다른 objective를 가능하게 하는 관계다. 정밀한 curriculum dependency의 중심은 Concept Graph가 아니라 Objective Graph다.

### 5.3 Mastery

일반적인 수행 수준을 다음 5단계로 사용한다.

| 단계 | Mastery |
| --- | --- |
| 0 | Unfamiliar |
| 1 | Recognition |
| 2 | Operational |
| 3 | Conceptual |
| 4 | Derivational / Transfer |

### 5.4 Target Depth

책의 설명 깊이는 Mastery와 별도 축으로 둔다.

- Overview
- Working
- Deep

Mastery와 Target Depth는 동일한 개념이 아니다.

### 5.5 Terminal / Enabling role

Terminal objective와 enabling objective는 objective의 절대 속성이 아니라 특정 Curriculum/Pathway 안에서의 역할이다.

### 5.6 Prerequisite Requirement

Prerequisite Requirement는 Learning Layer의 first-class object다. 정밀한 prerequisite는 가능하면 Concept 수준이 아니라 Learning Objective 수준에 연결한다. 각 required prerequisite는 2.2절에 따라 최소한 target Learning Objective 또는 target depth, required mastery, reason을 가진다.

## 6. Evidence / Assessment Layer

### 6.1 Evidence Requirement

학습자가 objective를 달성했다고 판단하기 위해 어떤 observable performance가 필요한지 정의한다. 구조는 다음과 같다.

Learning Objective → Evidence Requirement → Task Model → Exercise Instances

개별 Exercise Instance 하나의 정답 여부만으로 mastery 전체를 증명했다고 보지 않는다. 중요한 Learning Objective는 필요에 따라 서로 다른 Task Model 또는 evidence form을 통해 복수의 evidence를 확보한다.

Q-matrix/coverage mapping은 Exercise와 Learning Objective/skill의 coverage를 추적하는 authoring/instructor 도구로 사용할 수 있다.

### 6.2 Task Model

개별 문제가 아니라 문제 family의 구조를 정의한다. 문제 수가 많아져도 objective coverage, variation, evidence coverage를 유지하기 위한 객체다.

### 6.3 Answer Mode

다음 유형을 지원한다.

- `closed`
- `bounded`
- `rubric_based`
- `open`

### 6.4 Rubric

정답 하나가 없는 설계·비교·연구 문제를 평가하기 위한 optional first-class object다.

## 7. Practice Layer

### 7.1 Learning Activity

Learning Activity의 사고 유형(type)과 학습 역할(role)은 서로 독립이다.

| 구분 | 값 |
| --- | --- |
| type | `retrieval`, `calculation`, `explanation`, `comparison`, `derivation`, `transfer`, `debugging`, `synthesis`, `design`, `research` |
| role | `worked_example`, `completion_problem`, `guided_practice`, `paired_practice`, `independent_practice`, `checkpoint`, `challenge`, `research_problem` |

Learning Activity 또는 Exercise Instance는 필요에 따라 다음 metadata를 가질 수 있다.

- `difficulty`
- `scaffolding_level`
- `transfer_distance` (7.3절)
- `retrieval_mode`: `open_book`, `closed_book`
- structural family / Task Model
- misconception targets
- `builds_on`

### 7.2 Worked Example / 유제

Worked Example은 본권에서 문제와 풀이를 함께 보여주는 exposition의 일부다. Worked Example과 그에 대응하는 paired/guided practice는 같은 structural family 또는 Task Model을 공유할 수 있으며, 다음과 같이 guidance를 점차 제거할 수 있다.

worked example → paired practice → guided practice → independent practice → transfer

### 7.3 Transfer distance

- `near_copy`
- `near_transfer`
- `far_transfer`

### 7.4 Practice Bank

핵심 개념에는 충분히 큰 문제은행을 제공한다. 문제 수는 고정하지 않으며, practice demand는 다음 요소에 따라 달라질 수 있다.

- procedural complexity
- reuse frequency
- misconception risk
- transfer importance

중요한 Concept의 초기 설계 시 다음 수량을 저자용 starting heuristic의 예로 참고할 수 있다.

| 활동 | 초기 설계 참고 수량 |
| --- | --- |
| worked examples | 2–3 |
| paired/guided practice | 2–4 |
| completion | 1–3 |
| independent practice | 4–10+ |
| comparison/debugging | 1–3 |
| near transfer | 2–4 |
| far transfer | 1–3 |
| checkpoint | 2–4 |
| later review | 2–4+ |

이 숫자들은 연구적으로 최적화된 상수가 아니라, Concept별 procedural complexity, reuse frequency, misconception risk, transfer importance에 따라 달라지는 practical authoring heuristic이다. 고정된 문제 수를 요구하지 않는다.

### 7.5 Essential Set

Practice Bank 중 ★ Essential 문제를 별도로 선정한다. Essential Set은 단순히 좋은 문제 몇 개가 아니라 최소한의 문제 수로 핵심 Learning Objective와 Evidence Requirement를 충분히 덮도록 설계한다. 교육자는 이를 최소 필수 과제로 사용할 수 있다.

### 7.6 문제 우선순위

필요에 따라 다음과 같이 표현할 수 있다.

- ★ Essential
- ● Recommended
- ○ Additional
- ◆ Challenge

Challenge는 표시 기호뿐 아니라 Practice Layer에서 사용할 수 있는 명시적인 practice object/role이다. Learning Activity의 `challenge` role로 표현할 수 있으며, `research_problem`과 동일한 의미로 합치지 않는다.

### 7.7 Checkpoint

Practice는 능력을 형성하고, Checkpoint는 능력이 형성됐는지를 빠르게 표본검사한다. 이처럼 Practice와 Assessment를 구분한다.

Checkpoint는 다음 용도 등에 사용할 수 있다.

- 다음 큰 개념 진입 전 prerequisite diagnostic
- 단원 종료 mastery check

### 7.8 Solution

상세 문제 해설은 별도 해설서에 제공한다. Solution에는 필요에 따라 다음을 포함한다.

- 정답
- 풀이 전략
- 단계별 풀이
- 흔한 오류
- remediation
- alternative solution
- forward connection

Worked Example의 풀이는 예외적으로 본권 inline에 포함한다.

## 8. Sequencing Layer

### 8.1 Instructional Sequence

여러 Learning Activity의 교수적 순서를 하나의 설계단위로 표현한다. 대표 progression은 다음과 같다.

concept explanation → worked example → guided/paired practice → completion → independent practice → transfer → checkpoint

Sequencing 설계는 worked examples, guidance fading, retrieval practice, spacing, interleaving, self-explanation, example variation, formative assessment, misconception repair, cognitive load control을 지원한다. 이들은 모든 경우에 강제되는 단일 교수법이 아니라 sequencing을 설계하기 위한 지원 원칙이다.

### 8.2 Review Plan

개념 학습은 첫 설명에서 끝나지 않으며, 책 전체에서 의도적으로 다시 회수한다. Review는 acquisition → conceptual understanding → transfer 방향으로 발전할 수 있으며, 뒤로 갈수록 transfer distance를 증가시킬 수 있다. 단순 반복이 아니라 다음처럼 evidence 수준을 높일 수 있다.

- calculation
- explanation
- discrimination
- application
- transfer
- synthesis

### 8.3 Structural Lag

정적인 책에서는 spacing을 고정된 날짜가 아니라 structural lag로 표현하며, 실제 시간 간격을 강제하지 않는다. 다음과 같이 내용상 거리를 표현할 수 있다.

- `local`
- `same_chapter`
- `later_chapter`
- `later_part`
- `remote`

### 8.4 Re-entry Block

오래전에 배운 개념이 뒤에서 다시 필요할 때 제공한다. 구성은 다음과 같다.

- 처음 배운 위치
- 이번에 왜 필요한지
- 최소한 기억해야 할 내용
- 짧은 cold-retrieval 문제
- 막힐 경우 돌아갈 위치

### 8.5 Interleaved Set

유사 개념을 구분하고 적절한 개념을 선택하게 하기 위해 여러 Concept의 문제를 섞을 수 있다.

### 8.6 Remediation Rule

오답 또는 Misconception에 따라 학습자가 어디를 복습하고 어떤 문제를 추가로 풀어야 하는지 정의한다.

### 8.7 Reuse / centrality as authoring signals

Concept의 downstream reuse나 graph centrality는 더 많은 practice, 더 강한 review, 더 적극적인 re-entry가 필요한 후보를 찾기 위한 derived authoring signal로 사용할 수 있다. 이는 7.4절의 practice demand 등을 검토하는 데 도움을 주지만, 보편적인 교육 법칙이나 자동 결정 규칙은 아니다.

## 9. Exposition Layer

### 9.1 Exposition

실제 책에서 개념을 설명하는 단위다.

### 9.2 Occurrence

Concept 자체와 책에서의 등장 위치를 분리한다. Occurrence role의 예는 다음과 같다.

- `primary_explanation`
- `review`
- `application`
- `deep_dive`
- `re_entry`

핵심 Concept은 primary explanation 위치가 명확해야 한다.

### 9.3 Cross-reference

선수지식, 수학 복습, 후속 응용 등을 책 안에서 연결한다.

Exposition과 Learning Activity 사이에는 `motivates_exposition`, `embedded_in`, `practices_after`, `assesses_after`, `reviews_later` role을 표현할 수 있다. Concept/Exposition의 위치 관계에는 `introduced_at`, `reviewed_at`, `reused_in`을 지원한다. 이러한 관계를 표현하더라도 Concept와 Occurrence는 서로 다른 객체다.

## 10. Epistemic Layer

### 10.1 Claim

책의 사실적·연구적·해석적 주장을 가능한 한 claim 단위로 관리한다.

### 10.2 Claim Status

- `foundational_theory`
- `established_research`
- `frontier_research`
- `interpretive_framework`
- `practical_heuristic`

`interpretive_framework`와 `practical_heuristic`을 실제 학계의 확립된 formal theory인 것처럼 표현해서는 안 된다. 특히 수학적 비유나 다른 분야의 formalism을 AI/Harness에 적용할 때는 실제 연구에서 사용되는 formalization인지, 이 책의 interpretive framework인지 claim의 근거 수준과 출처를 통해 구분할 수 있어야 한다.

### 10.3 Evidence Source

출처 유형을 구분할 수 있다. 예는 다음과 같다.

- `textbook`
- `primary_paper`
- `survey`
- `systematic_review`
- `meta_analysis`
- `official_documentation`
- `official_engineering_report`
- `benchmark`
- `empirical_case_study`
- `preprint`

### 10.4 Citation Status

- `verified`
- `needs_source`
- `source_under_review`

출판 시 factual/research claim에 `needs_source`가 남지 않도록 한다.

### 10.5 Temporal Validity

최신 AI 영역의 정보에는 필요에 따라 다음 등을 기록한다.

- `first_verified`
- `last_reviewed`
- `valid_as_of`
- `observed_at`
- `superseded_by`

### 10.6 Conditional Authority

어떤 source가 authoritative한지는 질문/목적에 조건부일 수 있다.

## 11. Curriculum Layer

### 11.1 Curated Pathway

독자 또는 교육자를 위해 저자가 책 안에 제시하는 정적인 추천 경로다. 자동 개인화 시스템을 의미하지 않는다.

예:

- Transformer 빠른 경로
- LLM 수학 경로
- Coding Agent 경로
- Harness Engineering 경로

### 11.2 Module

관련 Learning Objectives, Exposition, Practice, Assessment를 묶는 instructional unit/package다. Module은 knowledge Domain과 동일한 개념이 아니다.

### 11.3 Entry Profile

해당 Pathway/Module 진입에 필요한 assumed mastery와 checkpoint다.

### 11.4 Exit Profile

종료 시 달성해야 하는 terminal objectives와 evidence다.

### 11.5 Curriculum-relative roles

다음은 Concept의 절대 속성이 아니라 Curriculum 내부 역할이다.

- terminal / enabling
- core / recommended / enrichment
- full / review / reference / omit

Objective의 terminal/enabling 역할 역시 5.5절과 같이 특정 Curriculum/Pathway에 상대적이다.

### 11.6 Constructive alignment

Learning Objective의 observable verb ↔ 실제 Practice Activity ↔ Assessment / Evidence Requirement는 서로 정렬되어야 한다. 예를 들어 objective가 “비교한다”인데 계산 문제만 제공하는 식의 불일치를 피한다.

## 12. Publication Model

하나의 canonical ontology에서 publication view만 분리한다. 아래 표는 각 출판물의 대표 구성이며, ontology object의 배타적인 출판 위치나 visibility를 지정하지 않는다.

| 출판물 | 포함 내용 |
| --- | --- |
| 본권 | 설명, 수식, Worked Example + 풀이, 유제, Practice Bank, ★ Essential, Checkpoint, 누적복습, Challenge / Research Problem, 학습자용 remediation 및 cross-reference |
| 해설서 | 상세 정답, 풀이, 흔한 오류, remediation, alternative solution, concept connection |
| Instructor's Guide | Objective structure, Evidence Requirements, Task Models, Essential 선정 근거, coverage/Q-matrix 정보, rubric, misconception diagnosis, curriculum examples, instructional rationale, remediation strategy |

Instructor's Guide에만 존재하는 정보가 학습자의 정상적 독학에 필수여서는 안 된다.

### 12.1 Publication visibility / projection rule

- 지원하는 visibility metadata는 `learner`, `solution`, `instructor`, `authoring_only`다. Visibility는 ontology object type과 일대일 대응하지 않으며, object의 종류만으로 publication visibility를 결정하지 않는다.
- 가능하면 object 전체보다 field-level visibility를 우선한다. 동일한 canonical object를 각 출판물의 독자와 목적에 맞게 선택·요약·표현할 수 있으며, 서로 다른 field 또는 projection이 여러 출판물에서 다르게 노출될 수 있다.
- Learner-facing 핵심 정보가 `instructor` 또는 `authoring_only`에만 존재해서는 안 된다.
- Learning Objective, Evidence Requirement, Task Model, Rubric, Misconception, Remediation Rule 등도 Instructor's Guide 전용 객체가 아니다. 학습자의 목표 파악, 연습, 자기평가, 오개념 진단, 복습 및 다음 경로 선택에 필요한 내용은 본권 또는 해설서에 학습자용으로 제공한다.
- 특히 정답 하나가 없는 문제의 자기평가에 필요한 평가기준이나 rubric은 본권 또는 해설서에서 확인할 수 있어야 한다. 모든 내부 설계 정보나 메타데이터를 그대로 노출할 필요는 없다.
- Instructor's Guide는 동일한 canonical object의 상세 설계 구조, 선정 근거, coverage 분석, 교수 전략 및 교육과정 예시를 교육자용으로 제공한다.
- 각 projection은 canonical 의미와 일관되어야 하며, 본권과 해설서를 합친 학습자용 projection은 13.7절의 Learner Closure를 충족해야 한다.

## 13. Ontology Consistency Rules

다음은 ontology가 지켜야 할 최소 invariant다.

### 13.1 Knowledge

- Required prerequisite relation은 cycle을 만들지 않아야 한다.
- Required prerequisite에는 reason이 있어야 한다. 필요한 Mastery와 target objective/depth도 2.2절에 따라 명시한다.

### 13.2 Learning

- Working/Deep 핵심 Concept에는 measurable Learning Objective가 있어야 한다.
- Objective는 observable action을 사용한다.

### 13.3 Evidence

- 중요한 objective에는 Evidence Requirement가 있어야 한다.
- Evidence Requirement를 elicitation하는 Task Model이 있어야 한다.

### 13.4 Practice

- 핵심 Working 수준 objective에는 충분한 Practice Bank가 있어야 한다.
- 주요 procedural concept은 worked example과 독립연습을 갖는 것을 원칙으로 한다.
- Essential Set은 핵심 objective/evidence coverage를 충족해야 한다.

### 13.5 Exposition

- 핵심 Concept에는 명확한 primary explanation 위치가 있어야 한다.
- 후반에서 재등장하는 foundational concept은 필요에 따라 review/re-entry를 제공한다.

### 13.6 Epistemic

- Factual/research claim에는 가능한 한 evidence source를 연결한다.
- Frontier research는 최신성 검토가 가능하도록 temporal metadata를 갖는다.
- `frontier_research` 상태의 Claim은 최신성 추적을 위해 `last_reviewed`를 가져야 한다.

### 13.7 Learner Closure

모든 learner-facing 핵심 objective에 대해 본권과 해설서 내에서 다음 loop가 닫혀 있어야 한다.

Exposition → Practice → Check → Feedback → Remediation → Continue

## 14. 상태 및 버전 관리

Ontology v1.0은 합의된 canonical specification으로 동결되어 있다. v1.0 이후 변경은 기존 의미를 조용히 덮어쓰지 않는다. 구조 변경이 필요하면 별도 결정과 버전 변경을 거친다.
