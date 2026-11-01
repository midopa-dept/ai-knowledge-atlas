# AI Knowledge Atlas

한국어 · [English](README.en.md)

수학의 기초에서 AI·LLM·Agent·Harness Engineering까지를 하나의 비선형 한국어 교재로 엮으려는 프로젝트(AI Knowledge Book)의 **지식 구조와 첫 Chapter**를 공개한 저장소입니다. 교재 전체는 비공개 저장소에서 계속 쓰고 있습니다.

이 저장소에는 세 가지가 있습니다.

1. **지식 그래프와 학습목표.** Concept 504개, 의미 관계 603개, Learning Objective 817개, 한국어 용어 491개(일반 용어 437·개념 표기 54)와 이를 정의하는 schema·정책·결정 기록입니다.
2. **결정적 validator와 test.** 위 데이터가 schema를 지키는지 검사하는 Python 표준 라이브러리 도구 4개와 test 159개입니다.
3. **Transformer 장(검토 후보).** 11절로 된 「Attention과 Transformer」 본권(241쪽)과 별도 상세 해설(114쪽)의 PDF와 Markdown 원고, CPU에서 돌아가는 실습 코드입니다.

## 왜 지식 구조부터 만들었나

60개 Chapter짜리 책을 여러 세션에 걸쳐 쓰면, 같은 개념이 장마다 다른 이름으로 나오거나 선수지식이 빠진 채로 설명이 이어지기 쉽습니다. 그래서 원고보다 먼저 다음을 정했습니다.

- **안정된 node identity.** 개념마다 `K0001` 같은 ID와 `canonical_key`, 범위(scope)·포함/제외 경계를 둡니다. ID는 다시 쓰지 않고, 폐기·병합도 기록으로 남깁니다([NODE_IDENTITY.md](NODE_IDENTITY.md)).
- **관계의 종류를 좁게.** 개념 사이 관계는 정해진 의미 관계만 씁니다. 그래프 연결만으로 학습 순서를 정하지 않습니다([SEMANTIC_EDGE_SCHEMA.md](SEMANTIC_EDGE_SCHEMA.md)).
- **학습목표를 개념과 분리.** Learning Objective는 "학습 뒤 무엇을 할 수 있는가"를 정의하고 개념에 grounding으로 연결합니다. 504개 개념이 모두 하나 이상의 학습목표로 덮입니다([LEARNING_OBJECTIVE_SCHEMA.md](LEARNING_OBJECTIVE_SCHEMA.md)).
- **선수관계는 별도 계약.** 선행 능력의 조건·숙달 수준·이유를 담는 schema만 정본으로 정했습니다. 실제 선수관계 데이터는 아직 하나도 승인하지 않았습니다([PREREQUISITE_REQUIREMENT_SCHEMA.md](PREREQUISITE_REQUIREMENT_SCHEMA.md)).
- **영어 의미와 한국어 표기 분리.** 개념의 정본 의미는 영어로 두고, 교재에 쓸 한국어 용어는 별도 정책과 데이터로 관리합니다([KOREAN_AUTHORING_TERMINOLOGY_POLICY.md](KOREAN_AUTHORING_TERMINOLOGY_POLICY.md)).
- **외부 지식이 근거.** 기술적 설명은 외부 논문·전문 서적·공식 문서에 근거합니다. 이 저장소의 Registry나 Ontology는 집필 범위를 관리하는 기준일 뿐 기술적 사실의 증거로 인용하지 않습니다([TEXTBOOK_AUTHORING_POLICY.md](TEXTBOOK_AUTHORING_POLICY.md), [ADR 0014](decisions/0014-external-knowledge-authority-and-anti-self-reference.md)).

## 구성

| 경로 | 내용 |
| --- | --- |
| [ONTOLOGY_V1.md](ONTOLOGY_V1.md) | 개념·관계·학습목표 등 기본 대상의 정의(동결) |
| [KNOWLEDGE_GRAPH_L1.md](KNOWLEDGE_GRAPH_L1.md) | 12개 탐색 grouping과 60개 Macro Area |
| [NODE_IDENTITY.md](NODE_IDENTITY.md) · [REGISTRY_SCHEMA.md](REGISTRY_SCHEMA.md) · [SEMANTIC_EDGE_SCHEMA.md](SEMANTIC_EDGE_SCHEMA.md) | 개념 ID와 수명주기, Registry 레코드, 의미 관계 |
| [LEARNING_OBJECTIVE_SCHEMA.md](LEARNING_OBJECTIVE_SCHEMA.md) · [PREREQUISITE_REQUIREMENT_SCHEMA.md](PREREQUISITE_REQUIREMENT_SCHEMA.md) · [OBJECTIVE_DEPENDENCY_SCHEMA.md](OBJECTIVE_DEPENDENCY_SCHEMA.md) | 학습목표, 선수 요구, 목표 사이 의존 |
| [PUBLICATION_STRUCTURE.md](PUBLICATION_STRUCTURE.md) · [TEXTBOOK_AUTHORING_POLICY.md](TEXTBOOK_AUTHORING_POLICY.md) · [KOREAN_AUTHORING_TERMINOLOGY_POLICY.md](KOREAN_AUTHORING_TERMINOLOGY_POLICY.md) | 12 Part / 60 Chapter 구조, 질문 중심 집필 정책, 한국어 용어 정책 |
| [decisions/](decisions/README.md) | 위 정본을 정한 결정 기록 0001~0014 |
| [registry/](registry/README.md) | `nodes.jsonl`(Concept 504), `semantic_edges.jsonl`(관계 603) |
| [learning/](learning/README.md) | `objectives.jsonl`(Learning Objective 817) |
| [terminology/](terminology/README.md) | 한국어 용어 437개, 개념 표기 54개 |
| [references/](references/README.md) | 참고문헌 정책. `bibliography.bib`는 아직 비어 있고, Transformer 장의 참고문헌은 원고 안에 있습니다 |
| `scripts/` · `tests/` | validator 4개와 test |
| [chapters/transformer/](chapters/transformer/README.md) | Transformer 장 원고·PDF·그림·실습 |

## 검사 실행

Python 3 표준 라이브러리만 씁니다(Python 3.15에서 확인). validator는 `git` 명령과 Git 이력을 쓰므로, 얕지 않은(shallow가 아닌) clone 폴더에서 실행합니다.

```bash
python3 scripts/validate_registry.py
python3 scripts/validate_semantic_edges.py
python3 scripts/validate_learning_objectives.py
python3 scripts/validate_terminology.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

검사 통과는 데이터가 schema와 참조 규칙을 지킨다는 뜻입니다. 개념 정의나 학습목표 문장이 교육적으로 옳다는 뜻은 아닙니다.

## 현재 상태와 한계

- 지식 구조(Concept·관계·학습목표·용어)는 정본으로 등록했습니다. Part 순서, Chapter 1~60 번호, 절 구성은 아직 정하지 않았습니다. 데이터의 나열 순서와 ID 번호는 학습 순서가 아닙니다.
- 선수관계(Prerequisite Requirement) 데이터는 0건입니다. schema만 정본입니다.
- Transformer 장은 독립 기술·교육·지면 검토와 교정 재심사를 마친 **검토 후보**입니다. 저자의 최종 편집·출판 승인과 실제 독자의 학습효과 검증은 하지 않았습니다.
- 이 저장소는 비공개 개발 저장소의 한 시점(2026-10-16)에서 뽑은 사본입니다. 문서가 가리키던 비공개 후보·작업 기록은 옮기지 않았습니다. 그런 링크는 글자만 남겼고, 본문에 나오는 `candidates/…` 경로는 개발 저장소 안의 위치입니다.

## 라이선스

- **코드**(`scripts/`, `tests/`, `chapters/transformer/` 아래의 `.py` 파일과 실습 환경 설정): [MIT License](LICENSE)
- **그 밖의 내용**(문서·원고·PDF·그림·데이터): [CC BY-NC-SA 4.0](LICENSE-CONTENT.md)

자세한 경계는 [LICENSE-CONTENT.md](LICENSE-CONTENT.md)에 있습니다.
