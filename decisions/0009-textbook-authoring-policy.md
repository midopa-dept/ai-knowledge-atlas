# ADR 0009 — 근원적 질문 중심 집필 정책 정본화

상태: **사용자의 명시적 요청에 따른 정본 결정**

결정일: 2026-10-13 (Asia/Seoul)

공식 소유 문서: [TEXTBOOK_AUTHORING_POLICY.md](../TEXTBOOK_AUTHORING_POLICY.md)

## 배경과 요청 근거

TRANSFORMER의 첫 설계와 첫 원고 v0.1은 이미 후보로 존재한다. 계산·LO 정렬의 준비 상태와 독자가 질문을 풀어 가는 설명의 충분함은 별개로 검토해야 한다. 사용자는 이전 v0.2 단순 편집 프롬프트를 실행하지 않았다고 명시했고, 첫 원고를 보존한 채 전체 60개 Chapter의 집필 원칙을 공식화하고 실제 한국어 샘플을 준비하도록 요청했다.

이번 세션에서 사용자가 명시한 원문은 다음과 같다.

> 이 책은 독자가 근원적인 질문을 해소할 수 있도록 돕는 교재다.
>
> 이번에는 전체 Chapter를 즉시 재작성하지 않는다. 먼저 전체 60개 Chapter에 적용할 저술 원칙과 실제 문체 샘플을 준비한다.
>
> 집필 원칙의 공식 소유 문서로 다음을 신설한다. "TEXTBOOK_AUTHORING_POLICY.md"

이는 집필 정책 정본화와 지정 경로의 후보 작성·문서 반영·정상 commit 및 non-force push를 승인한 작업 요청이다. 샘플의 실제 문체가 이미 채택되었다는 승인으로 확대하지 않는다.

시작 branch는 `main`, local HEAD = origin/main = actual remote main = `a160f4de53efb5f871a46436dd315cffffbf0724`, working tree clean이었다. 권한 적용 실제 원격 조회로 확인했으며 ADR 0009의 번호 충돌은 없었다. 변경 전 계획과 권위 대조는 작업 계획에 기록한다.

## 결정

1. Chapter의 최상위 목적을 근원적 질문의 해소로 삼는다. 문제·이전 접근·새 아이디어·작동·수학·적용·조건·한계·발전·Chapter 연결을 사고의 기준으로 사용하되 매 절의 기계적 서식으로 강제하지 않는다.
2. 자연스러운 한국어 문단과 중간 사고 단계를 확보한다. 공식 LO는 수행 정렬의 기준으로 유지하고 그 문체를 본문에 기계적으로 복제하지 않는다. 단어 금지·문장 길이·분량으로 품질을 대신하지 않는다.
3. 설명 깊이와 분량은 질문·메커니즘·가정·실패·대안·후속 연결에 따라 정한다. 기존 초고의 절·문자·문항 수나 LO coverage를 충분함의 자동 판정으로 사용하지 않는다.
4. 원 논문·수학적 도출·후속 연구·현대 구현·저자 비유·경험칙을 구분하고 Ontology의 Claim 수준·출처·시간 유효성을 적용한다. 특정 논문의 전체 해설·실험 재현을 집필 목표로 강제하지 않는다.
5. Chapter 간 연결과 짧은 Re-entry를 제공하되 다른 Chapter의 고유 범위를 보존한다. 연결을 필수 선수관계로 자동 변환하거나 가상 절 번호를 발급하지 않는다.
6. 계산기와 실행 가능한 한국어 주석 Python 코드를 교육 목적에 맞게 사용한다. 손계산과 도구 계산을 구분하고, framework 선택 근거·입출력·축·환경·가정·실행 확인·본문과 Learning Source의 대응을 기록한다.
7. 그림의 설명 목적·과학적 정확성·제작 방식·출처·재사용 권한을 각각 확인한다. 원본 또는 재생성 소스를 보존한다.
8. 새 집필 정책을 정본으로 신설하고 PROJECT·AGENTS에 최소 반영한다. README에는 독자용 저술 철학과 새 milestone을, PROJECT_STATE에는 후보 준비와 남은 인간 판단을 기록한다.
9. 새 샘플은 `candidates/textbook-authoring-calibration-v0.1/`에만 작성한다. 전체 TRANSFORMER 재작성과 인간의 최종 문체 채택은 아직 시작·완료한 것으로 기록하지 않는다.

## 선택 이유와 정책의 경계

기존 초고를 표면적으로 다듬는 것만으로는 문제에서 메커니즘과 모델 전체로 이어지는 설명 방식을 검토하기 어렵다. 새 샘플은 질문의 출발과 계산의 의미, 계산 뒤 결과의 전달을 실제 문단으로 읽어 볼 수 있게 한다. 기존 원고를 보존하면 비교와 후속 인간 판단의 기준을 잃지 않는다.

기술용어와 문단 저술을 한 정책으로 합치지 않는다. [기존 한국어 용어 정책](../KOREAN_AUTHORING_TERMINOLOGY_POLICY.md)은 표기·첫 등장·기호·sense·정본 용어 Registry의 권위를 유지한다. 새 정책은 설명의 전개와 출판 표현을 관리하며 용어 부재를 새 정본 번역으로 채우지 않는다.

Ontology §2.1·2.3·2.5·2.6·2.7, §5–6·9–10·12–13을 적용한다. 질문은 편집상 설명의 중심이며 Concept identity, LO 수행, Evidence / Task / Exercise 객체를 대체하지 않는다. 12 Part / 60 Chapter, 단일 Concept home, Mastery와 Depth 구별, 독학 loop와 required prerequisite 계약은 그대로다. 새 공식 Chapter / Section / PR / Exercise ID와 정본 자료 Schema를 만들지 않는다.

## 보존·검증·전달

허용 변경은 새 정책·이 ADR·PROJECT·AGENTS·README·PROJECT_STATE와 새 후보 경로다. 기존 v0.1 원고·Blueprint·Book Atlas·Concept·LO·PR 후보·Schema·용어·ready20/HOLD3는 불변 보존한다. 기존 KG와 LO의 의미 재감사는 수행하지 않는다.

새 산출물의 문단·정책 적합성·수식·실행·도해·링크·허용 변경과 보호 파일의 bytes 대조 결과는 검증 기록에 둔다. 별도 독립 AI 검토는 실시하지 않으며 자체 검토를 독립 검토 PASS로 보고하지 않는다. 인간은 샘플을 직접 읽고 자연스러움·설명 속도·깊이·도구 부담을 최종 판단한다.

정책과 샘플의 준비 판정은 **TEXTBOOK AUTHORING POLICY CANONICALIZED — KOREAN PROSE CALIBRATION SAMPLE PREPARED**다. 이는 출판 완료·문체 채택·교육 효과·Chapter Mastery의 실증이 아니다. 정상 commit·non-force push 후 실제 Git 상태는 완료 보고와 Git history로 확인하며 실행 전 원격 수용을 선기록하지 않는다. 완료 후 종료한다.
