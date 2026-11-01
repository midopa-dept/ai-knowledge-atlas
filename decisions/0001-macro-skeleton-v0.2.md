# ADR 0001 — Macro Skeleton v0.2 Canonicalization

Status: ACCEPTED — 2026-09-10

## Context

v0.1의 A~Z는 macro 영역을 찾기 위한 authoring aid였다. 여러 수학·AI·engineering 영역이 합쳐져 있어 후속 registry 설계에서 scope와 dependency를 구별하기 위한 Level-1 revision이 필요했다. 이번 변경은 동결된 [Ontology v1.0](../ONTOLOGY_V1.md)을 적용한 macro classification revision이며 Ontology 변경이 아니다.

이전 canonical graph는 v0.1 checkpoint `6396e61344531dbad0b7d34081b4b3bff97d4fdf`(비공개 개발 저장소)로 보존한다. 이번 작업의 시작 HEAD는 `13f83daeb46f4540531eb4d4caf374970e934fda`다.

### 설계 입력 provenance

입력은 사용자가 제공한 “AI Knowledge Book — Macro Skeleton v0.2 Canonicalization” 설계 계약이다. 보관 위치는 Codex 계획 세션의 최초 사용자 메시지(2026-09-10)다. 현재 실행 세션의 승인된 계획 및 추가 세 조건을 함께 적용했다.

사용자는 별도 설계 세션에서 v0.2 redesign, exhaustive boundary review와 12개 stress-test 경로 검토가 완료됐다고 보고했다. 이 완료 보고는 canonicalization의 입력 근거다. 이번 repository 작업이 해당 검토를 재실행·실증했거나 그 효과를 연구적으로 입증했다는 뜻이 아니다. 설계 경로와 그에 대응하는 경계는 [현재 macro map](../KNOWLEDGE_GRAPH_L1.md)에 보존한다. 확인하지 않은 연구 출처를 이 보고의 근거로 추가하지 않는다.

## Decision

- [Macro Skeleton v0.2](../KNOWLEDGE_GRAPH_L1.md)의 60개 semantic macro-area key를 v0.2의 canonical classification identifier로 채택한다. 12개 grouping은 탐색 편의이며 새로운 ontology 계층이 아니다.
- Macro key는 immutable node identity가 아니며 후속 Level-1 revision에서 migration으로 변경 가능하다. 향후 stable node identity는 `K####`로 설계하며 classification 변경에도 유지하는 방향이다. 이번에는 node registry나 schema를 만들지 않는다.
- Macro area membership ≠ prerequisite ≠ publication order다. Concept / Learning / Exposition 분리, reason·mastery·target objective/depth를 갖춘 prerequisite와 DAG, broader concept connection graph의 구분을 유지한다.
- Classical AI·Statistical ML·RL·GEN·Perception의 독립 계보를 보존한다. Classical AI는 AI-SEARCH·AI-KR·AI-PLANNING의 historical/domain grouping으로 유지한다. Agent를 LLM 하위로, World Models를 Embodied 하위로 정의하지 않는다.
- 수학의 계산·엄밀성·구조·측도·확률·확률과정 경계를 분리한다. Functional Analysis, Differential Geometry / Manifolds, Fourier / Harmonic Analysis, Stochastic Calculus는 medium/deep branch로 남긴다.
- Software Engineering·Control·Human–AI·Privacy를 복원 또는 분리하고 Interpretability를 독립 cross-cutting 영역으로 유지한다. Autoencoder의 home은 REP이며 DL에서 재사용한다. DL generic scaling과 LLM scaling laws를 구분한다.
- 기존 hub 목록과 단일 중심 spine을 15개 authoring/reference hub 후보, 5개 비강제 traversal로 대체한다. Hub는 측정 완료된 centrality 순위가 아니며 연결은 formal requires를 자동 선언하지 않는다.
- 이전 “약 100~200개 medium-resolution node”는 historical 규모 추정치로만 보존하며 acceptance criterion으로 사용하지 않는다. 실제 수량은 Ontology v1.0의 node cohesion, downstream dependency·독립 재사용, 독립 Learning Objective·prerequisite 가능성, 별도 Practice Bank 필요성에 따라 재산정한다.
- `ONTOLOGY_V1.md`를 수정하지 않는다. Claim-level provenance, mathematics re-entry와 publication/knowledge structure 분리를 보존한다.

### v0.1 → v0.2 migration

아래는 이전 macro 영역의 주된 이동·분할과 복원 범위다. 일대일 node identity 매핑이나 모든 주제의 배타적 소속 표가 아니다. 기존 지식을 삭제하는 migration이 아니며 기존 대표 주제는 새 scope·대표 주제·cross-reference에 유지한다.

| v0.1 | 기존 영역 | v0.2 destination keys |
| --- | --- | --- |
| A | Mathematical Language / Foundations | `MATH-FOUND`, `MATH-DISCRETE` |
| B | Linear Algebra / Geometry | `MATH-LINALG` |
| C | Calculus / Optimization | `MATH-CALC`, `MATH-OPT` |
| D | Probability / Statistics / Information Theory | `MATH-PROB`, `MATH-STAT`, `MATH-INFO` |
| E | Computer Science / Computation | `CS-COMP`, `CS-SYSTEMS`, `SE-FOUND` |
| F | Classical AI / Search / Logic / Planning | `AI-SEARCH`, `AI-KR`, `AI-PLANNING` |
| G | Uncertainty / Decision / Control | `AI-PROBMODELS`, `AI-DECISION`, `CAUSAL`, `CONTROL` |
| H | Statistical Machine Learning | `ML-STAT` |
| I | Data / Learning Signals | `ML-DATA` |
| J | Neural Networks / Deep Learning | `DL` |
| K | Representation Learning / Self-Supervision | `REP` |
| L | Generative Models | `GEN` |
| M | Reinforcement Learning / Control | `RL` |
| N | Sequence / Language / Speech | `SEQ`, `LANGUAGE`, `AUDIO-SPEECH` |
| O | Attention / Transformer | `TRANSFORMER` |
| P | Foundation Models / Large Language Models | `FOUNDATION-MODELS`, `LLM` |
| Q | Post-training / Alignment / Reasoning | `POSTTRAIN`, `MODEL-REASONING` |
| R | Perception / Multimodal / Embodied AI / World Models | `VISION`, `MULTIMODAL`, `EMBODIED`, `WORLD` |
| S | Retrieval / Context / External Knowledge | `IR`, `RAG`, `CONTEXT` |
| T | Memory / Long-Horizon State | `MEMORY`, `LONG-STATE` |
| U | Agents | `AGENT` |
| V | Multi-Agent Systems | `MULTIAGENT` |
| W | AI Systems / Compute | `AI-SYSTEMS` |
| X | Harness Engineering / Agentic Software Engineering | `HARNESS`, `AGENTIC-SE` |
| Y | Evaluation / Measurement | `EVAL` |
| Z | Reliability / Safety / Security / Society | `RELIABILITY`, `INTERPRETABILITY`, `AI-SAFETY`, `AI-SECURITY`, `AI-PRIVACY`, `RESP-AI-GOV` |

새 mathematical areas로 MATH-ANALYSIS, MATH-TOPOLOGY, MATH-MEASURE, MATH-DYNAMICS, MATH-STOCH, MATH-NUM을 명시하고 HUMAN-AI를 추가한다. MATH-DISCRETE는 A의 일부 기반을 이어받으며 독립 scope를 갖는다. SE-FOUND·CAUSAL·CONTROL 등의 destination은 기존 영역에 모두 충분히 기술되어 있었다는 주장이 아니라 분리·복원할 범위도 포함한다.

세부 cross-reference로 J의 autoencoder는 REP(K의 successor)에 home을 두고 DL에서 재사용한다. C의 엄밀성·수치 기초는 MATH-ANALYSIS·MATH-NUM, E의 numerical precision은 MATH-NUM, automatic differentiation·tensors는 AI-SYSTEMS에 연결한다. G의 Markov 관련 기반은 MATH-STOCH, M의 제어 측면은 CONTROL과 연결한다. Z의 human oversight는 RESP-AI-GOV와 HUMAN-AI, X의 실행 상태·검증은 LONG-STATE·EVAL에서도 재사용한다. 이들은 주된 migration 표를 보완하며 기존 주제를 소거하지 않는다.

## Rationale

Semantic key는 알파벳 위치보다 영역의 의미와 scope를 직접 드러낸다. Revision 가능한 분류와 stable node identity를 분리하면 macro 구조의 변경이 개별 지식 단위의 identity 변경으로 전파되는 것을 피할 수 있다.

수학의 계산적 Working 진입과 엄밀한 Deep 학습을 구분하면 topology 전체나 측도론을 모든 AI 학습의 blanket prerequisite로 만드는 것을 피하면서 심화 기반을 보존할 수 있다. Concept 분리는 고정 node 수를 맞추기보다 실제 downstream dependency와 독립 학습목표를 따라야 한다.

Classical AI·RL·GEN·Perception은 독립된 계보와 진입 경로를 갖도록 구성한다. Software Engineering 기반을 따로 두어 HARNESS와 AGENTIC-SE가 이를 재사용하게 하고, Control과 RL의 서로 다른 scope를 보존한다. Human–AI·Privacy·Interpretability는 여러 시스템과 학습 영역을 가로지르므로 한 응용이나 Governance/Safety에만 종속시키지 않는다.

설계 입력의 12개 경로는 이러한 경계를 선택한 근거로 사용했다. 이는 교재 분류의 설계 판단이며 보편적인 교육 법칙이나 기법의 효과 검증이 아니다.

## Consequences

Canonical Level-1 기준은 v0.2이고 A~Z는 위 migration과 historical checkpoint로 추적한다. 기존 출판 순서나 immutable node 체계를 확정하지 않는다. 후속 revision도 분류 변경을 조용히 덮어쓰지 않고 migration으로 추적해야 한다.

다음 단계는 60개 영역을 기준으로 medium-resolution registry를 재설계하고 node scope·canonical key·macro classification·stable K####와 주요 relation 후보를 구체화하는 것이다. Detailed prerequisite와 Learning Objective graph, atomic expansion, Practice/Evidence mapping은 후속 작업이다. Classification/tagging과 maturity/stability metadata의 미정 의미도 별도 검토한다.

### 이번 repository validation의 범위

이번 구현 validation은 key/name 60개와 grouping별 수량·중복, A~Z 26개 migration destination의 유효성, 기존 대표 주제와 요청된 boundary·branch·hub·traversal의 문서 반영, Markdown 링크·fragment, 상태 기록, whitespace와 변경 파일 범위의 정적 대조다. 시작 HEAD 대비 Ontology의 byte 동일성과 diff 부재도 확인한다. 임시 검증 script만 사용하며 영구 validation 파일이나 pipeline은 추가하지 않는다.

2026-09-10 정적 대조 결과: 설계 입력과 60개 key/name의 정확한 일치·중복 없음, grouping별 14+3+7+9+5+4+5+2+3+1+1+6, A~Z migration 26행의 유효한 destination, hub 15개·traversal 5개·설계 경로 12개의 문서 반영을 확인했다. 기존 대표 주제를 쉼표로 분리한 508개 항목의 문자열 보존을 검사하고 이동 scope와 경계는 본문 검토로 보완했다. 이는 topic coverage 보조 검사이며 508개 Concept Node를 정의한 것이 아니다. 상대 Markdown 링크 18개와 Git object 기준 historical checkpoint 링크 1개를 확인했으며 fragment 링크는 없었다. `git diff --check`와 네 파일 변경 범위 검사를 통과했다. `ONTOLOGY_V1.md`는 시작 HEAD와 byte 단위로 동일하고 SHA-256은 `58fc5ba1a2bdd5d31b66a018afd99b52c23bbc4f7e7fb7d4f576c9af7b37fcfd`다.

설계 세션의 exhaustive review나 stress-test를 재실행했다고 보고하지 않는다. 이번 산출물은 KNOWLEDGE_GRAPH_L1.md, PROJECT_STATE.md, decisions/README.md와 이 ADR의 네 파일로 한정한다. 세부 연구 Claim 검증과 registry 설계는 이번 validation의 범위 밖이다.
