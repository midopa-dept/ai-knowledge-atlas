# ADR 0012 — 절 중심 교재 구조와 Transformer 첫 상세 절 시제품

상태: **인간의 명시적 결정 정본화 — 시제품의 인간 교육적 검토 대기**

결정일: 2026-10-13 (Asia/Seoul)

## 근거와 결정

인간 저자는 Transformer 전체 파일럿 v0.1의 설명이 과도하게 압축되어 있고 문제의 수와 세밀함이 부족하다고 평가했다. 기존 작성자 자체 검토의 `11/11 depth PASS`는 최종 교육적 승인이 아니다. 과거 ADR 0008–0011과 후보 bytes·승인 사실은 수정하지 않고 이번 후속 평가를 별도로 기록한다.

인간이 명시적으로 승인한 방향은 번호 있는 Section으로 Chapter를 나누기, 정의·정리·예제·유제·연습·심화의 유형별 절 종속 번호와 일관된 참조, 절별 능력 훈련을 위한 충분한 문제와 상세 해설, v0.1보다 훨씬 상세한 본문·중간 계산, 첫 한 절을 완성한 뒤 인간 평가 받기다. [출판 구조 §9](../PUBLICATION_STRUCTURE.md#9-번호-있는-section과-출판-참조), [집필 정책](../TEXTBOOK_AUTHORING_POLICY.md#절별-설명과-연습의-완결성)에 반영한다.

Chapter는 완결된 주요 학습 단위, Section은 중요한 질문과 기술을 충분히 배우고 연습하는 독서 단위다. Concept·LO와 일대일로 배정하지 않는다. Section은 기존 Publication View·Exposition의 편집 구조이며 새 Knowledge identity·Ontology node·Registry Schema를 만들지 않는다. 유형별 번호는 조판에서 생성하고 내부 참조 표지와 구분한다. 가정·정리·증명·직관·반례를 구별하며 실제 정리가 없으면 만들지 않는다.

## 이번 실행과 경계

0012 미사용과 신규 경로 충돌 없음을 확인했다. 시작 branch main, local HEAD=origin/main=actual remote main=`42e6017578d1ffaf9791d8d2bd353e0b3f74c836`, 작업 트리 clean이었다. 실제 원격은 DNS 제한 뒤 권한 적용 조회로 확인했다.

새 상세 절 후보에 Transformer 잠정 11절 구조와 K0302·LO0559의 첫 절 본문, 별도 해설, 문제 품질·깊이 검토, 코드·도해·A4 PDF를 제공한다. K0303의 scaled dot-product 공식·분산 도출은 다음 절의 집필 대상으로 남긴다. 독립 연습 18개 내외는 이번 실험의 목표이며 전권의 최적 문제 수나 고정 규칙이 아니다.

임시 장 번호 10은 조판 시연이다. 60개 Chapter 순서·정본 장 번호·최종 판형을 확정하지 않는다. 공식 Concept/LO/Exercise ID·선수관계 admission·기존 후보와 ADR은 불변이다. 설명·문항의 자체 검토와 독립 계산 검증은 인간 교육적 승인·실제 학습효과·Mastery의 증거가 아니다.

이번 종료 상태는 **절 중심 집필 정책 기록 — Transformer 첫 상세 절·연습 PDF 준비 / 인간 검토 대기**다. 전체 Transformer Chapter v0.2와 나머지 절을 완료 처리하지 않고, 종료 후 다른 절을 자동 집필하지 않는다.
