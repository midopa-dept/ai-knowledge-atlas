# ADR 0010 — 인간 승인 집필 정책 결정 1–13 통합

상태: **인간 승인 결정의 정본 통합 — 기술적 문체와 PDF 시제품은 미승인·미제작**

결정일: 2026-10-13 (Asia/Seoul)

공식 소유 문서: [교재 집필 정책](../TEXTBOOK_AUTHORING_POLICY.md)

## 승인 근거와 통합 방식

사용자는 2026-10-13 새 실행 세션에서 ChatGPT 상위 오케스트레이션을 통해 순차 승인한 결정 1–13을 normative input으로 제공하며 추가 승인 없이 통합하도록 명시했다. 다음은 이번 요청의 직접 인용이다.

> 아래 13개 정책 결정은 전부 인간 저자가 승인했다. 추가 승인 없이 정확한 정본 통합을 수행하라.

이 ADR은 그 결정의 선택안·추가 조건과 실제 정본 조항을 추적한다. 이미 승인된 방향을 새로 설계하거나 같은 결정을 재질문하지 않았다. [ADR 0009](0009-textbook-authoring-policy.md)의 질문 중심 저술·자연스러운 한국어·충분한 설명·근거·계산기·코드·그림 원칙은 보존하고, 새로운 규범만 해당 주제에 통합했다. ADR 0009의 역사적 결정은 수정하지 않았다.

시작 branch는 `main`, local HEAD = origin/main = actual remote main = `4956aa3f240de04b30f6c7780e771bf22a426984`였다. Working tree clean과 ADR 0010 번호 미사용을 확인했다. Sandbox에서 DNS 조회가 실패한 뒤 권한 적용 `git ls-remote`로 실제 원격을 확인했다. 시작 시 기존 미반영 변경이나 기준점 이후 원격 변경은 없었다.

## 결정별 선택과 반영 위치

### D1 기본 독자 수준

**B안: 해당 분야를 처음 배우는 독자 중심.** 핵심 기술을 모른다고 가정하고 등장 이유부터 정의·직관·수학·원리·구현·한계·응용을 충분히 연결한다. 다른 Chapter의 기초를 전부 반복하지 않고 선수 능력을 짧은 Re-entry·안내로 제공한다. 이미 아는 독자에게 반복을 강제하지 않으며 설명 부족을 선수지식 부족으로 돌리지 않는다. 기존의 다양한 독자 범위 안에서 Chapter 설명의 기본 수준을 확정했다.

반영: [독자와 Chapter의 교육적 목표](../TEXTBOOK_AUTHORING_POLICY.md#독자와-chapter의-교육적-목표).

### D2 기술용어와 자연스러운 한국어

**B안: 자연스러운 한국어 설명 + 필요한 기술 원어 유지.** 번역된 기술용어는 독립 Chapter 첫 등장에 영어 원어를 반드시 병기한다. 문제와 의미부터 설명하고 어색한 직역을 피하며 반복 병기를 강제하지 않는다. 문맥상의 자연어 풀이와 정본 용어 변경은 구별한다. `prefix`를 기계적으로 모두 ‘접두’로 번역하지 않는다.

기존 용어 정책은 독립 unit의 first-use 경계는 이미 규정했지만 `ko`에서 영어 생략, 약어 full form 비강제를 허용했다. §8·§11에 Chapter의 번역 기술용어 첫 등장 규칙의 우선순위만 보강했다. Enum·record·LO statement는 변경하지 않았다. 특정 번역 변경은 별도 용어 검토와 admission이다.

반영: [한국어 문장과 문단](../TEXTBOOK_AUTHORING_POLICY.md#한국어-문장과-문단), [용어 정책 §8](../KOREAN_AUTHORING_TERMINOLOGY_POLICY.md#8-display-policies)·[§11](../KOREAN_AUTHORING_TERMINOLOGY_POLICY.md#11-first-use-acronym-and-notation-rules).

### D3 수학·기술적 설명의 깊이

**B안: 직관 → 단계적 수학 → 계산 → 구현 → 해석.** 핵심 정리의 엄밀한 증명과 필요한 derivation을 포기하지 않는다. 필요성·출발 문제·아이디어·식의 항·연산 이유·도출·가정·계산과 구현·전체 시스템으로의 결과 전달·한계를 설명하는 사고 기준이며 고정 서식은 아니다. 필수 도출·증명은 Working에서 완결한다. Definition / Assumption / Proposition·Theorem / Derivation / Proof / Counterexample / Intuitive interpretation을 구별한다. Overview / Working / Deep와 Mastery의 별도 축을 보존하고 새 `More Deeper` enum을 만들지 않는다.

반영: [설명의 깊이와 분량](../TEXTBOOK_AUTHORING_POLICY.md#설명의-깊이와-분량), [Working과 선택적 Deep의 배치](../TEXTBOOK_AUTHORING_POLICY.md#working과-선택적-deep의-배치).

### D4 Python과 실습 라이브러리

**A안: 공통적인 계층형 Python 실습 기반.** `uv`를 환경·의존성 관리 기본으로, NumPy·SciPy·scikit-learn·PyTorch를 분야별 기본 도구로, SymPy·Matplotlib을 필요에 따라 사용한다. 기존 PyTorch/TensorFlow 동등 선택에서 PyTorch를 딥러닝·Transformer·LLM 기본으로 구체화했다. TensorFlow 등은 특정 LO·사례에 적합한 이유가 있을 때 허용한다. 모든 도구의 일괄 사용·표준 라이브러리만 사용·Python 3.9 고정을 요구하지 않는다. 재현 환경·명확한 의존성·필요한 lockfile·실제 실행과 출력·가능한 CPU 기본 사례를 갖추며 불필요한 GPU·대형 모델·다운로드를 강제하지 않는다. 버전 검증과 환경 구현은 후속 Learning Source 제작이다.

반영: [계산기와 구현 도구](../TEXTBOOK_AUTHORING_POLICY.md#계산기와-구현-도구).

### D5 본문 코드·Chapter 부록·Learning Source

**B안: 핵심 코드는 본문, 완성된 실습은 Learning Source.** 추가 조건은 중요한 모델 전체 구현의 Chapter 종료부 부록 수록과 부분 인용의 정확한 원 파일 경로·시작/종료 라인 명시다. 고정 source revision 또는 출판 버전도 표시한다. 본문은 알고리즘·한국어 주석·입출력·shape·수식 대응·연산 이유를 충분히 설명하고 Learning Source는 실행 파일·추가 실험·환경·검증을 관리한다. 큰 보조 파일 전부의 인쇄는 요구하지 않지만 중요한 모델을 외부에서만 보게 하지 않는다. 독립 코드는 그대로 실행 가능해야 하고 발췌는 문맥을 제공한다. 최종 인쇄 라인을 고정하고 변경 시 본문·부록·소스 인용을 재검증한다. 정책의 경로/라인/revision 예시는 가상이며 실제 발급이 아니다.

반영: [Python 코드와 Learning Source](../TEXTBOOK_AUTHORING_POLICY.md#python-코드와-learning-source).

### D6 그림과 단계별 확대 도해

**B안: 이해에 도움이 되는 그림을 적극 사용.** 중요한 구조에는 단계별 확대 도해를 제공한다. 전체 → 구성요소 확대 → 계산·정보 흐름 → 수식·코드 → 전체로 돌아와 결과 전달을 연결한다. 그림 개수는 고정하지 않는다. 직접 제작·생성·적법한 재사용을 허용하며 정보 흐름·축·shape·화살표·명칭·본문 관계·제작 방법·출처·권한·인쇄 가독성을 확인하고 가능한 벡터 원본을 보존한다. 출처 표시와 재사용 권한 확인은 별개다.

반영: [그림과 시각 자료](../TEXTBOOK_AUTHORING_POLICY.md#그림과-시각-자료).

### D7 Chapter의 교육적 완결성

**B안: 대표 문제를 처음부터 끝까지 해결, 필요하면 C안처럼 추가 사례 제공.** Chapter 종류에 맞는 하나 이상의 대표 문제로 개념을 연결한다. 추가 사례는 새 조건·응용·한계·Chapter 연결을 드러내며 개수를 강제하지 않는다. 대표 문제 성공은 전체 Mastery가 아니며 공식 LO의 수행을 위한 충분한 연습·Checkpoint·필요한 변형 문제가 따로 필요하다. 다른 Chapter 전체를 무분별하게 반복하지 않는다.

반영: [대표 문제와 연습의 배치](../TEXTBOOK_AUTHORING_POLICY.md#대표-문제와-연습의-배치), [Chapter 사이의 설명 연결](../TEXTBOOK_AUTHORING_POLICY.md#chapter-사이의-설명-연결).

### D8 인쇄용 미주와 참고문헌

**B안: Chapter별 Endnotes + Bibliography.** 본문에 번호를 달고 Chapter 종료부에 미주·참고문헌을 모은다. 출처 외 역사·기술 보충도 가능하나 필수 설명을 미주로 보내지 않는다. 정확한 논문·절·그림·공식 locator와 인쇄본에서 찾을 서지정보를 제공하고 하이퍼링크에 의존하지 않는다. 디지털 내부 링크는 보조다. 조판 검증은 후속 PDF 시제품이며 이번에 대규모 bibliography Registry를 만들지 않는다.

반영: [인쇄용 미주와 참고문헌](../TEXTBOOK_AUTHORING_POLICY.md#인쇄용-미주와-참고문헌).

### D9 원고 형식과 PDF

**A안: Git Markdown 원본 + Pandoc·LaTeX PDF.** LuaLaTeX 또는 XeLaTeX와 템플릿은 시제품 검증 후 선택한다. 의미 있는 Chapter 초고·개정에는 검토용 PDF를 함께 제공한다. 수식·한국어와 수학 글꼴·그림과 확대 크기·Python 들여쓰기와 한국어 주석·미주와 참고문헌을 실제 페이지 렌더링으로 검토한다. Viewer의 LaTeX 문법 노출은 PDF로 해결한다. 이번에는 파이프라인이나 샘플을 만들지 않는다.

반영: [Markdown 원본과 검토용 PDF](../TEXTBOOK_AUTHORING_POLICY.md#markdown-원본과-검토용-pdf).

### D10 설명과 연습의 배치

**B안: 충분한 설명 + 짧은 이해 확인 + 절별 독립 연습.** 새 개념 설명 → 의미 있는 지점의 작은 질문/계산 → 논증·예제 전개 → 절 종료 독립 연습 → Chapter 통합 Checkpoint로 설계한다. 문단·수식마다 문제를 넣거나 증명 흐름을 끊지 않는다. 독자가 스스로 답할 기회를 제공하되 설명 없이 추측하게 하지 않는다. 기존 Practice / Sequencing 의미를 유지하며 문제 수를 고정하지 않는다.

반영: [대표 문제와 연습의 배치](../TEXTBOOK_AUTHORING_POLICY.md#대표-문제와-연습의-배치).

### D11 선택적 Deep 설명의 배치

**B안: 절별 선택적 Deep 블록.** 기본 설명 뒤 가까운 곳에서 일반 도출·추가 증명·가정 완화·반례·일반화·이론적 한계·확장 구현/분석을 선택적으로 제공한다. 매 절에 강제하지 않으며 길면 Chapter 종료부 심화 부록으로 분리한다. 필수 증명은 Working에 남기고 Deep를 건너뛰어도 기본 흐름이 완결되게 한다. 심화 코너의 출판용 이름은 미정이다.

반영: [Working과 선택적 Deep의 배치](../TEXTBOOK_AUTHORING_POLICY.md#working과-선택적-deep의-배치).

### D12 집필·검토 절차

**B안: 대표 기술 설명의 인간 검토 후 전체 Chapter 집필.** 어려운 설명·수식/도출·계산·한국어 주석 코드·그림/확대·전체로의 연결을 가능한 한 포함한 실제 샘플 → 읽을 수 있는 PDF와 인간 평가 → 승인 방향으로 전체 집필 → 수학·기술·Concept/LO·문항/해설·실행/소스·그림·인용·조판·교육적 완결성 검증의 네 단계다. 쉬운 도입부나 AI 자체 PASS로 문체 승인을 대체하지 않는다. 초기 대표 Chapter와 성격이 크게 다른 분야에서 기준을 세워 재사용하며 모든 60개 Chapter의 모든 절에 gate를 강제하지 않는다. 새 품질 문제는 필요한 범위만 추가 검토하고 실제 독자 경험·교육효과 미검증을 명시한다.

반영: [집필·검토 절차](../TEXTBOOK_AUTHORING_POLICY.md#집필검토-절차), [검토와 후보의 상태](../TEXTBOOK_AUTHORING_POLICY.md#검토와-후보의-상태).

### D13 Chapter 간 연결과 Re-entry

**B안: 필요한 순간에 부분 복습 + Chapter 끝의 다음 경로 안내.** 지금 필요한 이유·최소 기억·짧은 복습/확인·기존 Chapter·현재 계산으로의 복귀를 제공할 수 있다. 모든 개념에 Re-entry를 강제하지 않고 아는 독자는 건너뛰게 한다. Chapter 끝은 해결한 질문·남은 조건·이어지는 질문·권장 경로를 설명한다. 앞의 Knowledge Map·Curated Pathway는 별도 탐색 기능이다. 연결을 required prerequisite로 자동 승격하지 않으며 가상 Chapter/Section 번호를 발급하지 않는다. 실제 출판 번호·페이지 확정 후 역참조를 연결한다.

반영: [Chapter 사이의 설명 연결](../TEXTBOOK_AUTHORING_POLICY.md#chapter-사이의-설명-연결).

## 기존 정본과 승인 범위의 경계

[Ontology v1.0](../ONTOLOGY_V1.md)의 Knowledge / Learning / Exposition / Evidence / Practice / Publication 의미, Formal Object와 Practice 역할, Mastery / Target Depth의 분리를 보존한다. [출판 구조](../PUBLICATION_STRUCTURE.md)의 12 Part / 60 Chapter·Chapter 단위 통합 학습과 미배정 번호는 그대로다. Concept / LO Registry의 의미·수행·grounding, Requirement / Dependency Schema의 실제 능력·Context·자료·Mastery·관계는 이 정책의 설명 규칙으로 대체하지 않는다.

D2의 일반 first-use 조정과 D4의 framework 기본 선택은 추가 승인된 규범에 따른 명시적 구체화다. 승인 입력으로 해결할 수 없는 새 실질적 의미 충돌은 발견하지 않았다. 다음은 이번 인간 승인 사실에 포함하지 않는다.

- 특정 Python·패키지 버전과 공통 환경의 구현
- LaTeX 엔진·템플릿 최종 확정, 판형·글꼴·여백
- 특정 도해 스타일의 최종 출판 승인, Transformer 문체 샘플 최종 채택
- 공식 Chapter/Section 번호, 정식 문제은행·평가의 Mastery 판정
- 공식 PR admission과 선수관계 미결의 해결

## 별도 용어 검토

- **인간 피드백으로 등록한 미결:** `language_model.prefix_target_alignment`의 `접두 시퀀스–예측 대상 대응(prefix–target alignment)`이 부자연스럽다는 평가. Intended sense는 기존 위치별 입력 시퀀스·예측 대상 대응이다. [현재 record](../terminology/terms.jsonl), 관련 Concept label의 note와 공식 LO 사용처를 필요한 범위에서 대조하여 의미 충실도·구별·자연스러움을 검토한 뒤 별도 admission으로 처리한다. 이번에는 대체 번역을 확정하지 않았다.
- **일반 규칙과 record의 관계:** 실제 두 Registry의 display policy 집계를 확인했다. Concept labels는 `ko_en_first` 50 / `english` 4, general terms는 `ko_en_first` 385 / `english` 50 / `acronym` 2다. 현재 `ko`·`ko_acronym_first` record는 0이므로 D2 적용을 위한 개별 record 변경은 없었다. 향후 해당 record의 표시 지침이나 약어 full form source를 바꿔야 한다면 bounded review/admission으로 처리한다. 이 집계는 전체 의미감사가 아니다.

## 기존 문체 샘플의 현재 인간 평가

candidates/textbook-authoring-calibration-v0.1/PROSE_SAMPLE.md는 **NON-CANONICAL / HUMAN-REVIEWED / PROSE NOT APPROVED**다. 샘플 파일의 과거 ‘인간 저자 평가 전’ 문구는 당시 artifact의 상태로 보존하며 이 ADR과 현재 PROJECT_STATE가 이후 인간 평가를 기록한다.

사용자는 도입의 접근 방식과 Encoder–Decoder 도해 제작 방향을 긍정적으로 평가했다. 도입의 모든 문장이 완벽하거나 전체 문체가 승인된 것은 아니다. 특히 기술 설명은 매우 부자연스럽고 이해하기 어렵다고 평가하며 무리한 직역·압축적인 수식 설명·부자연스러운 문장을 지적했다. 공학용 계산기, 실용적인 Python 라이브러리, 한국어 주석 코드, PDF 검토를 요구했다. 정책 승인을 이 샘플의 문체 승인으로 확대하지 않는다. 이번 작업에서 샘플 bytes는 바꾸지 않았다. 독자 경험 측정·교육효과·Mastery 검증도 수행하지 않았다.

## 후속 인계와 이번 작업의 종료

다음 작업은 **TRANSFORMER — Reader-Approved Technical Prose Calibration + Print-Ready Review PDF Prototype**이다. 인간 피드백에 따라 분야 초심자를 위한 기술적 한국어를 다시 쓰고 필수 수학 도출·증명과 승인 용어를 보존한다. 실제 NumPy·PyTorch 등의 코드와 `uv` Learning Source 환경, 수식 대응·한국어 주석, 전체/확대 도해, 인쇄용 미주·참고문헌을 갖춘 Markdown을 작성한다. Pandoc·LaTeX로 PDF를 생성하고 실제 페이지를 검토하여 어려운 기술 설명을 인간 저자가 평가할 수 있게 제공한다. 문체를 먼저 인간이 확인한 뒤 전체 Chapter로 확장한다.

이번에는 기존 샘플 수정·Learning Source 환경 구축·PDF 제작·전체 Transformer v0.2 집필을 시작하지 않았다. Book Atlas·Blueprint·첫 원고·샘플·공식 데이터와 이전 ADR의 역사적 승인 기록을 보존했다. 새 Concept/LO/PR/Dependency/Exercise ID와 출판 번호는 발급하지 않았다.

검증은 정책 delta의 D1–D13·추가 조건·권위 경계·상태·링크·UTF-8·형식·허용 경로·Git bytes에 한정한다. 기존 KG·LO·Terminology admission·Pilot42 의미 재감사나 독립 AI review loop는 하지 않는다. 실제 결과는 PROJECT_STATE에 기록하고 최종 SHA·원격 수용·clean은 정상 commit/non-force push 후 Git history와 완료 보고로 확인한다. 전달 성공을 미리 기록하지 않는다.

완료 판정: **AUTHORING POLICY DECISIONS 1–13 CANONICALIZED — READER CALIBRATION PDF PENDING**. 이 판정은 Transformer 완성·문체 승인·PDF 출판·60개 Chapter 집필 준비 완료·교육효과나 Mastery 실증·선수관계 admission을 뜻하지 않는다. 전달 확인 후 종료한다.
