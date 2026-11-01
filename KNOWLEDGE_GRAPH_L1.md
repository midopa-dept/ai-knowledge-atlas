Status: CANONICAL — Level-1 Macro Skeleton v0.2

# Level-1 AI Knowledge Graph

## 1. 문서 상태와 역할

이 문서는 AI Knowledge Book의 canonical Level-1 macro map이다. 주요 지식 영역과 연결을 제공하며 medium-resolution Node Registry와 atomic knowledge graph의 후속 설계 기준선이다. 현재 macro skeleton의 canonical 상태는 atomic graph의 동결을 뜻하지 않는다. 이 macro map은 registry, detailed prerequisite, Learning Objective graph를 정의하지 않는다. Stable node ID 운영 규칙은 별도 [NODE_IDENTITY.md](NODE_IDENTITY.md)에 정의한다.

동결된 [Ontology v1.0](ONTOLOGY_V1.md)을 따른다. Concept / Learning / Exposition을 분리하며, 대표 주제는 완성된 formal node가 아니다. 하나의 중심 질문으로 설명할 수 있는지, 독립 Learning Objective와 구체적 prerequisite를 지정할 수 있는지, downstream에서 독립적으로 재사용되는지를 기준으로 후속 node를 나눈다. Downstream dependency가 다르거나 별도 Learning Objective·Practice Bank가 필요하면 별도 Concept Node로 분리한다.

Publication Part/Volume/Chapter와 canonical knowledge structure는 동일하지 않다. 독자는 prerequisite와 cross-reference를 따라 비선형으로 이동하며, 교육자는 같은 graph로 Curriculum/Pathway를 구성할 수 있다. 후반에서 수학 개념·수식을 재사용하면 최초 설명 위치를 명시적으로 역참조하고 필요한 mathematics re-entry를 제공한다.

v0.1 A~Z와 v0.2의 대응, 설계 입력 provenance는 [Migration ADR](decisions/0001-macro-skeleton-v0.2.md)에 기록한다.

## 2. 식별자와 분류 원칙

Semantic macro-area key는 **v0.2에서의 canonical classification identifier**다. Immutable node identity가 아니며 향후 Level-1 revision에서 명시적인 migration을 통해 변경될 수 있다. 학습순서·prerequisite·책의 순서를 의미하지 않는다. Stable node identity는 `K####`이며 [Node Identity 운영 규칙](NODE_IDENTITY.md)을 따른다. 의미적 identity가 유지되는 macro classification 변경에는 같은 K를 유지한다.

예를 들어 향후 `K0347`이 `canonical_key: probability.conditional_distribution`, `macro_area: MATH-PROB`를 가질 수 있다. 이는 미래 구조의 설명용 예시일 뿐 실제 node 등록이나 schema 확정이 아니다. Canonical key와 macro classification도 immutable `K####` identity와 구분한다.

아래 12개 grouping은 탐색 편의이며 새로운 ontology 계층이 아니다. Domain은 분류·탐색 metadata이고 소속 자체는 prerequisite가 아니다. Classical AI의 historical/domain grouping은 AI-SEARCH·AI-KR·AI-PLANNING으로 보존한다. Statistical ML·RL·GEN·Perception의 독립 계보를 유지하며 전체 AI를 LLM 중심의 하위 분류로 재편하지 않는다.

## 3. Level-1 Macro Areas

### Mathematics — 14

#### MATH-FOUND — Mathematical Language & Proof

수학적 표현 언어와 기본 증명·반례를 다룬다. 극한의 계산은 MATH-CALC, 엄밀한 수렴은 MATH-ANALYSIS로 연결한다.

- **대표 주제:** sets and elements, variables and constants, functions, function composition, sequences, summation / product notation, exponentials, logarithms, limits, proof, counterexample.

#### MATH-DISCRETE — Discrete Mathematics

이산 객체의 구조와 조합적 사고를 다룬다. 알고리즘 구현·복잡도는 CS-COMP와 연결한다.

- **대표 주제:** logic, relations, combinatorics, counting, induction, recurrence relations, discrete graphs and trees.

#### MATH-LINALG — Linear Algebra & Euclidean Geometry

선형대수적 객체·연산과 유클리드 기하를 다룬다. PCA의 학습 방법은 ML-STAT에서 재사용한다.

- **대표 주제:** scalar, vector, matrix, transpose, dot product, norm, distance, similarity, matrix multiplication, linear transformation, linear independence, basis, dimension, rank, eigenvalues / eigenvectors, projection, matrix decomposition, PCA와의 연결.

#### MATH-CALC — Calculus

계산적·직관적 미적분과 다변수 미분을 다룬다. 엄밀한 기초는 MATH-ANALYSIS, 최적화는 MATH-OPT와 구분한다.

- **대표 주제:** limits, derivative, integral, partial derivative, gradient, chain rule, Jacobian, Hessian, multivariable calculus, backpropagation과의 연결.

#### MATH-ANALYSIS — Real Analysis

실수의 완비성, 엄밀한 극한·수렴과 함수열을 다룬다.

- **대표 주제:** completeness, rigorous limits, continuity, convergence, function sequences, pointwise and uniform convergence, rigorous differentiation and integration.

#### MATH-TOPOLOGY — Topology & Metric Spaces

거리공간과 위상공간의 구조를 다룬다. 측도론적 확률 전체의 일괄 prerequisite로 두지 않는다.

- **대표 주제:** metric spaces, open and closed sets, continuity, compactness, connectedness, completeness of metric spaces, topological spaces.

#### MATH-MEASURE — Measure Theory & Lebesgue Integration

측도·가측성과 Lebesgue 적분을 다룬다. 확률로의 적용과 측도론 자체를 구분한다.

- **대표 주제:** sigma-algebra, measure, measurability, Lebesgue integration, convergence of integrals, product measures.

#### MATH-DYNAMICS — Differential Equations & Dynamical Systems

미분방정식과 동역학계의 시간적 변화를 다룬다. 제어 설계는 CONTROL, 학습된 환경 dynamics는 WORLD와 연결한다.

- **대표 주제:** ordinary and partial differential equations, initial value problems, dynamical systems, equilibria, stability, continuous and discrete dynamics.

#### MATH-PROB — Probability Theory

확률공간, 확률변수·분포와 조건부 확률, 기댓값·수렴·극한정리를 다룬다. 확률과정은 MATH-STOCH로 구분한다.

- **Probability:** probability, random variable, joint distribution, conditional probability, conditional distribution, Bayes rule, independence, expectation, variance, covariance, common probability distributions.
- **대표 주제:** probability spaces, convergence of random variables, laws of large numbers, central limit theorem.

#### MATH-STOCH — Stochastic Processes

시간 등에 의해 색인된 확률적 과정과 그 성질을 다룬다. Stochastic Calculus는 Deep branch로 남긴다.

- **대표 주제:** stochastic processes, Markov chains/processes, martingales, Brownian motion.

#### MATH-STAT — Mathematical Statistics

표본으로부터의 추정·검정과 통계적 추론을 다룬다. 학습 문제의 정식화는 ML-STAT와 연결한다.

- **Statistics:** sampling, estimator, bias / variance, likelihood, maximum likelihood estimation, MAP / Bayesian inference, confidence interval, hypothesis testing.

#### MATH-INFO — Information Theory

정보량과 분포 간 관계를 다룬다.

- **Information Theory:** self-information, entropy, conditional entropy, cross-entropy, KL divergence, mutual information, information gain, information bottleneck.

#### MATH-OPT — Optimization

목적함수의 최적화, 제약과 최적화 알고리즘을 다룬다. 미분 계산 및 수치 오차와 구분한다.

- **대표 주제:** convexity, constrained optimization, Lagrange multiplier, gradient descent, stochastic gradient descent, momentum, adaptive optimization, numerical optimization.

#### MATH-NUM — Numerical Mathematics

수치적 근사, 오차·안정성과 계산 방법을 다룬다. 실행 자원·시스템 구조는 CS-SYSTEMS와 구분한다.

- **대표 주제:** floating-point arithmetic, numerical precision, approximation, conditioning, numerical stability, numerical linear algebra, numerical integration, numerical differential equations.

### Computing / Software Engineering — 3

#### CS-COMP — Algorithms, Data Structures & Computation

알고리즘·자료구조와 계산 복잡도의 기초를 다룬다.

- **대표 주제:** algorithms, computational complexity, recursion, dynamic programming, graph, tree, data structures.

#### CS-SYSTEMS — Computer Systems, Parallel & Distributed Computing

컴퓨터 구조, 메모리와 병렬·분산 계산을 다룬다. AI 학습·추론 특화 운용은 AI-SYSTEMS와 연결한다.

- **대표 주제:** parallelism, GPU computation, memory hierarchy, distributed computation, computer systems, synchronization, communication.

#### SE-FOUND — Software Engineering Foundations

요구사항에서 구현·검증·변경에 이르는 소프트웨어 공학 기초를 다룬다. HARNESS와 AGENTIC-SE가 이를 재사용한다.

- **대표 주제:** requirements / specification, architecture, modularity / interfaces, testing, CI, change management, formal methods / program verification의 deep branch.

### Classical AI / Decision / Control — 7

#### AI-SEARCH — Search, Constraint Solving & Game Search

상태공간에서의 탐색, 제약 해결과 게임 탐색을 다룬다.

- **대표 주제:** problem formulation, state space, BFS, DFS, uniform-cost search, A*, heuristic search, local search, tree search, constraint satisfaction problems, adversarial search, minimax, alpha-beta pruning, Monte Carlo Tree Search.

#### AI-KR — Logic, Knowledge Representation & Inference

논리, 지식 표현과 추론을 다룬다. 모델의 추론 동작을 다루는 MODEL-REASONING과 구분한다.

- **대표 주제:** propositional logic, first-order logic, inference, knowledge representation.

#### AI-PLANNING — Planning & Replanning

목표 달성을 위한 계획 구성과 상황 변화에 따른 재계획을 다룬다.

- **대표 주제:** classical planning, hierarchical planning, contingent planning, replanning.

#### AI-PROBMODELS — Probabilistic Models & State Estimation

확률모델을 통한 구조화된 추론과 상태 추정을 다룬다. Markov chain 자체는 MATH-STOCH, 의사결정 정식화는 AI-DECISION에 둔다.

- **Probabilistic modeling:** Bayesian networks, graphical models, temporal probabilistic models, HMM, Kalman filtering.
- **대표 주제:** state estimation, belief / state estimate.

#### AI-DECISION — Decision Theory & Sequential Decision Making

효용에 따른 선택과 순차적 의사결정 문제의 정식화를 다룬다. 학습 알고리즘은 RL과 구분한다.

- **Decision:** utility, decision theory, expected utility, value of information.
- **Sequential decision:** partial observability, MDP, POMDP.

#### CAUSAL — Causal Models & Causal Inference

인과모델, 개입과 인과 추론을 다룬다. 관측적 확률모델과 인과적 가정을 구분한다.

- **대표 주제:** causal graphs, structural causal models, intervention, confounding, identification, counterfactual reasoning.

#### CONTROL — Control Theory

동역학계의 피드백·안정성과 제어 설계를 다룬다. Control != RL이며 학습 기반 제어에서 연결할 수 있다.

- **대표 주제:** feedback control, state-space models, controllability, observability, stability, optimal control, model predictive control.

### Learning lineages — 9

#### ML-STAT — Statistical Machine Learning

학습 문제·일반화와 지도·비지도 학습 및 학습 이론을 독립 계보로 다룬다.

- **기초 learning framework:** learning problem, features, labels, train/validation/test split, loss, risk, generalization.
- **대표 supervised methods:** linear regression, logistic regression, perceptron, Naive Bayes, decision trees, ensembles, SVM, kernels, Gaussian processes.
- **Unsupervised / latent methods:** clustering, K-means, mixture models, EM, PCA, ICA, dimensionality reduction.
- **Learning theory:** empirical risk minimization, overfitting, regularization, PAC, VC dimension, distribution shift.

#### ML-DATA — Data & Learning Signals

데이터의 구성·품질·분포와 학습 신호를 다룬다.

- **대표 주제:** datasets, sampling, labeling, data quality, data leakage, contamination, class imbalance, long-tail distributions, augmentation, curriculum, sampling strategies, distribution shift, synthetic data, filtering, deduplication, data mixture, preference data, trajectory data.

#### DL — Neural Networks & Deep Learning

신경망의 구성·학습·안정성과 architecture 계열을 다룬다. Generic scaling은 신경망 크기·데이터·계산에 관한 범위이며 LLM scaling laws는 LLM에서 다룬다.

- **대표 주제:** perceptron, linear layer, activation, MLP, loss, backpropagation, optimization, initialization, exploding gradients, vanishing gradients, normalization, regularization, dropout, residual connections, representation learning, generic scaling.
- **Architecture families:** CNN, RNN, LSTM / GRU, GNN.
- **재사용:** autoencoder의 canonical home은 REP다. DL에서는 occurrence/cross-reference로 연결한다.

#### REP — Representation Learning & Self-Supervision

표현의 구조·기하, 자기지도 학습과 표현의 전이·재사용을 다룬다. Autoencoder의 canonical home이다.

- **대표 주제:** latent representation, embeddings, autoencoders, representation geometry, contrastive learning, metric learning, self-supervised learning, masked prediction, transfer learning, multi-task learning, few-shot representation, in-context representation.

#### GEN — Generative Models

생성모델의 여러 계열과 생성·샘플링을 다룬다. GEN != LLM이며 LLM으로 생성모델 전체를 대체하지 않는다.

- **대표 계열:** autoregressive models, latent-variable models, VAE, GAN, energy-based models, score-based models, diffusion, normalizing flow, flow matching.
- **주요 개념:** likelihood-based generation, sampling, latent space, score matching, denoising, guidance, conditional generation.

#### RL — Reinforcement Learning

정책·보상·가치를 통한 순차적 의사결정 학습을 독립 계보로 다룬다. RL != RLHF이며 RLHF·reasoning RL·tool-use RL은 후속 연결이다.

- **대표 주제:** sequential decision making, Markov property, MDP, state, action, reward, policy, trajectory, return, discount factor, Bellman equation, value function, Q function.
- **Algorithms:** dynamic programming, value iteration, policy iteration, Monte Carlo, temporal difference learning, SARSA, Q-learning, policy gradient, REINFORCE, actor-critic.
- **Broader RL:** exploration / exploitation, model-free RL, model-based RL, on-policy / off-policy, reward shaping, credit assignment, Deep RL, offline RL, imitation learning, hierarchical RL, multi-agent RL, POMDP.

#### SEQ — Sequential & Temporal Modeling

시퀀스와 시간적 의존성의 모델링을 다룬다. SEQ != Transformer이며 언어 외 시계열도 포함한다.

- **Sequence modeling:** N-gram, Markov sequence models, RNN, LSTM, encoder-decoder, seq2seq.
- **대표 주제:** temporal modeling, time series.

#### LANGUAGE — Language Representation, NLP & Language Modeling

언어 표현, NLP 과제와 언어 모델링을 다룬다. 대규모 모델의 구성·학습은 LLM과 연결한다.

- **Language:** tokenization, vocabulary, word representation, language modeling, machine translation.

#### AUDIO-SPEECH — Audio & Speech AI

오디오·음성의 표현과 처리를 다룬다. Analysis 계열 Fourier/Harmonic branch와 연결한다.

- **Audio / speech:** signals, spectrogram, ASR, TTS, audio representations.

### Foundation Models / Reasoning — 5

#### TRANSFORMER — Attention & Transformer

Attention 연산, 위치 표현과 Transformer 내부 구성을 다룬다.

- **Attention:** motivation, query, key, value, attention scores, softmax weights, scaled dot-product attention, self-attention, multi-head attention, cross-attention, causal masking.
- **Position:** positional representation, sinusoidal encoding, RoPE.
- **Transformer internals:** residual stream, LayerNorm, feed-forward network, Transformer block, encoder, decoder, encoder-decoder, KV cache, long-context / sparse attention.

#### FOUNDATION-MODELS — Foundation Models

여러 downstream 과제에 전이·적응하는 광범위한 사전학습 모델의 paradigm을 다룬다. Foundation Model != LLM이며 LLM보다 넓은 범위다.

- **대표 주제:** foundation models, pretraining, adaptation, transfer, modality-spanning model families.

#### LLM — Large Language Models

대규모 언어모델의 학습 목표·pretraining, 구성과 생성 방식을 다룬다. Foundation Models와 blanket requires로 연결하지 않는다.

- **대표 주제:** autoregressive factorization, next-token prediction, language-model objective, pretraining, dense Transformer models, Mixture of Experts, gating, LLM scaling laws.
- **Generation:** logits, softmax, decoding, temperature, top-k, top-p, beam search.
- **Serving-relevant concepts:** KV cache, batching.

#### POSTTRAIN — Post-training & Alignment

사전학습 이후 적응·정렬과 도구 사용 학습을 다룬다. AI-SAFETY의 위험 분석이나 RL 전체와 동일시하지 않는다.

- **Post-training:** supervised fine-tuning, instruction tuning, preference data, reward model, RLHF, PPO, DPO (direct preference optimization), rule-guided training, distillation.
- **Tools:** tool-use SFT, tool-use RL.

#### MODEL-REASONING — Model Reasoning & Test-Time Computation

모델의 reasoning traces, 추론 학습과 test-time computation을 다룬다. Classical AI의 논리적 inference/reasoning과 구분한다.

- **Reasoning:** chain-of-thought, self-consistency, process supervision, outcome supervision, verifiable reward, reasoning RL, inference-time compute, reasoning search, verifier-guided reasoning.
- **대표 주제:** reasoning traces, test-time computation.

### Perception / Environment — 4

#### VISION — Vision & Perceptual Learning

영상 표현과 지각 학습의 독립 계보를 다룬다.

- **Vision:** image representation, classical vision, CNN, detection, segmentation, Vision Transformer.

#### MULTIMODAL — Multimodal Learning & Models

여러 modality 간 표현·정렬과 결합 학습을 다룬다.

- **Multimodal:** cross-modal learning, contrastive image-text learning, vision encoder + language model, multimodal alignment, multimodal instruction tuning, multimodal LLM.

#### EMBODIED — Embodied AI & Robotics

환경과 상호작용하는 지각·행동 및 로보틱스를 다룬다.

- **Embodied:** perception-action loop, robot state/action, navigation, manipulation, vision-language-action models.

#### WORLD — World Models & Learned Environment Dynamics

학습된 환경 dynamics와 예측 모델을 다룬다. Embodied AI의 하위 영역으로 정의하지 않으며 GEN·RL·CONTROL·Planning·Video/Perception이 합류할 수 있다.

- **World models:** environment dynamics, latent world models, predictive models, video/world modeling, model-based planning.

### Knowledge / Context / State — 5

#### IR — Information Retrieval

관련 정보를 찾는 검색 문제를 다룬다. 생성과의 결합이나 invocation 노출 정책과 구분한다.

- **Information Retrieval:** sparse retrieval, dense retrieval, vector index, reranking.

#### RAG — Retrieval-Augmented Generation & Grounding

검색된 evidence를 generation과 결합하고 grounding하는 문제를 다룬다.

- **RAG:** chunking, retrieval, context assembly, grounding, RAG evaluation.

#### CONTEXT — Context Engineering

현재 model invocation/trajectory에 무엇을 노출할지 선택·구성·관리한다.

- **Context Engineering:** prompt, instruction hierarchy, context window, context selection, context pollution, lost-in-the-middle, progressive disclosure, context compression, compaction, retrieval.

#### MEMORY — Agent & Model Memory

모델과 Agent의 기억 유형·검색·통합을 다룬다. Memory != State, Observation != Memory를 유지한다.

- **Memory:** parametric memory, working memory, external memory, episodic memory, semantic memory, procedural memory.
- **대표 주제:** memory retrieval/consolidation.

#### LONG-STATE — Long-Horizon State & Execution Continuity

장기 실행의 상태 지속·일관성·인계·복구를 다룬다. Context != State이며 환경 상태·관측·belief와 기록된 canonical state를 구분한다.

- **State:** environment state, observation, belief / state estimate, persistent state, canonical state.
- **Long-horizon mechanisms:** checkpoint, handoff, task ledger, reconciliation, resume, recovery.
- **대표 주제:** idempotency.

### Agents — 2

#### AGENT — Agent Architecture & Tool Use

Model·tools·environment·control loop를 결합한 행동 시스템을 다룬다. Agent를 LLM의 하위개념으로 정의하지 않는다.

- **기본 구조:** model, tools, environment, control loop.
- **대표 주제:** agent loop, action, observation, tool calling, retrieval, planning, ReAct, plan-and-execute, task decomposition, reflection, self-correction, external feedback, replanning.
- **Agent families:** computer-use agents, browser agents, coding agents, research agents.

#### MULTIAGENT — Multi-Agent Systems

여러 Agent의 소통·조정·협력과 공동 계획·평가를 다룬다.

- **대표 주제:** roles, communication, coordination, cooperation, debate, peer review, shared memory, multi-agent planning, multi-agent evaluation, emergent failure modes.

### Engineering — 3

#### AI-SYSTEMS — AI Training & Inference Systems

AI 학습·추론의 실행 시스템과 성능·자원 trade-off를 다룬다.

- **Training systems:** GPU / accelerators, data parallelism, model parallelism, pipeline parallelism, tensor parallelism, mixed precision, checkpointing, distributed training.
- **Inference:** serving, batching, KV-cache management, quantization, pruning, distillation, speculative decoding, latency / throughput, memory / compute trade-offs.
- **대표 주제:** automatic differentiation, tensors.

#### HARNESS — Harness Engineering

Agent 실행을 뒷받침하는 인터페이스·환경·정책·검증과 engineering invariant를 다룬다. 소프트웨어 개발 이외의 Agent에도 적용할 수 있다.

- **Harness components:** context harness, tool interface, agent-computer interface, execution environment, planning policy, verification, persistent state, engineering invariant, guardrail, human escalation, observability, evaluation.
- **대표 Failure Modes:** context pollution, stale state, planning drift, hallucinated completion, regression, repeated action, architecture drift.
- **대표 mitigations:** preflight, replanning, tests, persistent state, checkpoint, lint, structural tests, risk-based escalation.

#### AGENTIC-SE — Agentic Software Engineering

Agent를 활용한 소프트웨어 요구사항·설계·구현·검증·변경 작업을 다룬다. Harness != Agentic SE이며 SE-FOUND와 HARNESS를 재사용한다.

- **대표 주제:** coding agents, specification-driven changes, repository context, implementation, code review, testing, CI, regression prevention, architecture consistency, change management.

### Measurement — 1

#### EVAL — Evaluation & Measurement

측정·평가의 방법과 불확실성 및 평가 실패 위험을 다룬다. 모델·LLM·Agent·Harness 모두에 cross-cutting하게 적용한다.

- **General evaluation:** metric, benchmark, dataset split, statistical uncertainty, confidence interval, paired evaluation, effect size, ablation, error analysis, measurement error.
- **AI/LLM evaluation:** LLM-as-judge, human evaluation, executable evaluation, trajectory evaluation, cost, latency.
- **Agent/Harness:** long-horizon evaluation, harness evaluation, verifier evaluation, intervention metrics.
- **Cross-cutting:** Goodhart's law, reward gaming, evaluation overfitting.

### Human Interaction — 1

#### HUMAN-AI — Human–AI Interaction & Collaborative Systems

사람과 AI의 상호작용·협업을 독립 cross-cutting 영역으로 다룬다. Agent 또는 Governance의 단순 하위영역으로 두지 않는다.

- **대표 주제:** mixed-initiative interaction, delegation, human-in-the-loop, trust/reliance calibration, human feedback, oversight interface, collaborative decision making.

### Trust / Society — 6

#### RELIABILITY — Reliability & Robustness

예측·행동의 신뢰성과 불확실성 및 조건 변화에 대한 견고성을 다룬다.

- **대표 주제:** calibration, uncertainty, robustness, adversarial robustness, distribution shift, hallucination.

#### INTERPRETABILITY — Interpretability & Mechanistic Analysis

모델의 설명·해석과 내부 메커니즘 분석을 독립 cross-cutting 영역으로 다룬다. Safety의 단순 하위도구로 두지 않는다.

- **대표 주제:** interpretability, explainability, mechanistic analysis, representations and circuits, intervention-based analysis.

#### AI-SAFETY — AI Safety & Alignment Risk

AI의 안전·정렬 위험과 실패를 다룬다. Post-training 기법 전체나 Security의 위협모델과 동일시하지 않는다.

- **대표 주제:** alignment, misuse, reward hacking, specification gaming, safety evaluation.

#### AI-SECURITY — AI / LLM / Agent Security

모델·LLM·Agent 및 실행 환경에 대한 보안 위협과 보호를 다룬다.

- **대표 주제:** prompt injection, tool security, sandboxing, permission boundaries, data exfiltration.

#### AI-PRIVACY — AI Privacy & Privacy-Preserving Learning

프라이버시 정의·위협과 프라이버시 보존 학습을 독립 cross-cutting 영역으로 다룬다. Security 또는 Governance 한쪽의 단순 하위영역으로 두지 않는다.

- **대표 주제:** privacy definitions/threat models, differential privacy, privacy-preserving learning, membership inference, model inversion, training-data exposure, data leakage, privacy–utility trade-off.

#### RESP-AI-GOV — Responsible AI, Accountability & Governance

AI의 공정성·책임과 조직·사회적 관리를 다룬다.

- **대표 주제:** fairness, human oversight, accountability, governance, documentation, risk management.

## 4. Boundary와 Cross-Domain Connections

Prerequisite DAG와 broader concept connection graph를 구분한다. 아래 화살표는 주요 연결·후보 dependency 또는 traversal이며 formal `requires` 선언이 아니다. Grouping, domain 소속, 목록 순서나 historical relation은 prerequisite를 자동 생성하지 않는다.

Ontology v1.0의 `requires`는 필수 이해 dependency, `recommended`는 권장 선행 학습, `deepens`는 심화 관계다. 후자의 두 관계를 required prerequisite로 취급하지 않는다. Required prerequisite를 확정할 때에는 **reason, required mastery, target Learning Objective 또는 target depth**를 갖추고 cycle을 만들지 않는다. 정밀한 dependency는 가능하면 Learning Objective 수준에서 정의한다.

일반 연결은 필요에 따라 `component_of`, `generalizes`, `specializes`, `mathematically_related`, `identity_or_decomposition`, `contrasts_with`, `applied_in`, `used_to_analyze`, `motivates`, `explains`, `historically_leads_to`로 구체화할 수 있다. History/philosophy를 별도의 강제 prerequisite continent로 만들지 않는다. Engineering에서는 `caused_by`, `manifested_as`, `detected_by`, `mitigated_by`, `enforced_by`를 사용할 수 있으나 여기서 detailed edge를 임의 등록하지 않는다.

### 수학과 medium/deep branch

MATH-CALC는 계산·직관, MATH-ANALYSIS는 완비성·엄밀한 극한·수렴·함수열, MATH-TOPOLOGY는 거리/위상 구조, MATH-MEASURE는 sigma-algebra·측도·가측성·Lebesgue 적분을 맡는다. MATH-PROB는 확률공간·분포·조건부 확률·기댓값·확률적 수렴과 극한정리, MATH-STOCH는 확률과정을 맡는다. 서로 연결하되 각 scope를 합치지 않는다.

Functional Analysis와 Differential Geometry / Manifolds는 deep medium branch로 남긴다. Fourier / Harmonic Analysis는 analysis 계열 medium/deep cross-domain branch이고, Stochastic Calculus는 MATH-STOCH의 Deep branch다. 이번에 이들을 별도 Level-1 area로 올리거나 실제 medium node로 등록하지 않는다. Topology 전체는 measure-theoretic probability의 blanket prerequisite가 아니며 필요한 objective-specific/deepening dependency로 연결한다.

Markov chain → MATH-STOCH, Bayesian Network / HMM / Kalman filtering → AI-PROBMODELS, MDP/POMDP의 decision problem formulation → AI-DECISION, Q-learning / policy gradient → RL로 home을 구분한다. RL에서 MDP/POMDP를 재사용해도 정식화와 학습 알고리즘을 하나의 node로 합치지 않는다.

### 설계 입력의 12개 경로와 반영 경계

다음 표는 사용자가 제공한 설계 세션의 stress-test 경로를 문서 구조에 반영한 기록이다. 그 세션의 exhaustive boundary review와 stress test 완료 보고는 canonicalization의 입력 근거이며, 이번 repository 작업에서 재실행하거나 실증한 결과가 아니다. 이번 validation은 명세·문서의 정적 대조다.

| 설계 검토 경로 | v0.2에 반영한 연결과 경계 |
| --- | --- |
| Classical AI → Agent | AI-SEARCH / AI-KR / AI-PLANNING → AGENT. Classical AI 계보를 유지하고 Search·Planning·Decision·RL·Tool Use·State·Model이 Agent에 여러 방식으로 합류한다. |
| LLM → Coding Agent → Harness → Agentic SE | LLM → AGENT의 coding agents → HARNESS → AGENTIC-SE. Agent 자체는 LLM 하위개념이 아니다. SE-FOUND → HARNESS, AGENT → HARNESS, HARNESS → AGENTIC-SE, SE-FOUND → AGENTIC-SE는 주요 연결·후보 dependency다. Harness != Agentic SE. |
| IR → RAG → Context → Agent | IR != RAG != Context. 검색 문제, evidence와 생성의 결합·grounding, 현재 invocation/trajectory에 노출할 정보 선택을 구분한다. MEMORY와 LONG-STATE도 연결하되 Memory != State, Context != State, Observation != Memory를 유지한다. |
| Vision → Multimodal → Embodied | VISION → MULTIMODAL → EMBODIED. Vision은 독립적인 지각 계보이며 모든 지각 학습에 언어나 LLM이 필요하다는 뜻이 아니다. |
| Dynamics + RL + Control + Generative Models → World Models | MATH-DYNAMICS + RL + CONTROL + GEN → WORLD. AI-PLANNING과 VISION의 video/perception도 연결한다. Control != RL이며 World Model은 Embodied의 하위영역이 아니다. |
| Foundation Models ↔ LLM | FOUNDATION-MODELS ↔ LLM. Foundation Model != LLM이며 더 넓은 paradigm과 언어모델을 구분한다. 둘 사이에 blanket requires를 선언하지 않는다. |
| Analysis → Measure → rigorous Probability | MATH-ANALYSIS → MATH-MEASURE → MATH-PROB / MATH-STOCH의 rigorous/deep 학습. Topology 전체를 blanket prerequisite로 만들지 않는다. |
| DL → Diffusion / Flow | DL → GEN의 diffusion / normalizing flow / flow matching. MATH-PROB·MATH-DYNAMICS·MATH-STOCH 등은 구체적 objective와 depth에 따라 연결한다. GEN != LLM을 유지한다. |
| Reliability / Safety / Security / Governance | RELIABILITY / AI-SAFETY / AI-SECURITY / RESP-AI-GOV의 신뢰성·정렬 위험·보안 위협·책임 범위를 구분한다. INTERPRETABILITY와 AI-PRIVACY는 이들을 가로지르는 독립 영역이다. |
| Human–AI → Harness | HUMAN-AI → HARNESS의 human escalation·oversight interface·feedback. 협업과 delegation을 Agent 또는 Governance만의 하위영역으로 축소하지 않는다. |
| Probability → Causal / Probabilistic Models | MATH-PROB → CAUSAL / AI-PROBMODELS. 인과적 개입·식별의 가정과 관측 분포에 대한 추론·상태 추정을 구분한다. |
| Analysis/Fourier → Audio/Speech | MATH-ANALYSIS 계열 Fourier / Harmonic Analysis medium/deep branch → AUDIO-SPEECH의 신호·spectrogram·표현. 별도 Fourier Level-1 area나 강제 Deep 진입 조건을 만들지 않는다. |

### Claim의 근거 수준

위 영역·scope·연결은 교재 구조에 관한 설계 결정이다. 이를 연구적 효과나 확립된 이론의 실증으로 해석하지 않는다. 특히 Harness-specific 개념이나 frontier 기법의 근거 수준은 Concept 전체가 아닌 개별 Claim에 부여한다. `foundational_theory`, `established_research`, `frontier_research`, `interpretive_framework`, `practical_heuristic`을 구분하고, interpretive framework·practical heuristic을 확립된 formal theory로 과장하지 않는다.

Factual/research claim은 가능한 한 claim 단위로 출처를 추적한다. 출처 유형과 Claim Status를 구분하며 `frontier_research` Claim에는 Ontology v1.0에 따른 `last_reviewed`가 필요하다. 이번 canonicalization은 검증하지 않은 연구 출처나 citation을 추가하지 않는다. 세부 Claim 정본화는 [출처 관리 원칙](references/README.md)을 따른다.

## 5. Cross-Cutting Hub 후보

다음 15개는 macro-level authoring/reference hub 후보이며 formal fixed ontology나 측정 완료된 centrality 순위가 아니다.

1. Function / Composition
2. Representation
3. Probability Distribution
4. Conditional Distribution
5. Expectation
6. Optimization
7. Convergence
8. Search / Planning
9. State / Observation / Belief
10. MDP / Sequential Decision
11. Feedback / Control
12. Attention
13. Transformer
14. External Evidence / Retrieval
15. Verification / Evaluation

슬래시로 묶인 표현은 참고 후보를 모은 것이며 서로 다른 Concept identity를 합친다는 뜻이 아니다. Topology와 Measure Theory가 중요한 Level-1 area라는 사실과 global hub centrality는 별개다. Downstream reuse/centrality는 향후 Practice Bank·review·re-entry의 우선 검토를 돕는 authoring signal이며, prerequisite나 교육적 우선순위를 자동 결정하지 않는다.

## 6. Representative Traversals

아래 다섯 경로는 독자·교육자가 사용할 수 있는 대표 macro traversal이다. 유일한 학습순서, 강제 선형 chain 또는 prerequisite graph 자체가 아니다. 실제 Pathway의 entry mastery와 objective/depth에 따라 조정한다.

### Modern AI Working

```text
Mathematical foundations
→ Statistical ML
→ Deep Learning
→ Sequence / Language
→ Transformer
→ LLM
→ Post-training / Model Reasoning
→ Agent
→ Harness
```

수학 기초는 MATH-FOUND·MATH-LINALG·MATH-CALC·MATH-PROB·MATH-STAT·MATH-INFO 등 필요한 Working 범위를 선택한다. Context·retrieval·memory·state와 verification, evaluation·safety·systems는 후반 작업에서 함께 연결한다. 모든 수학 Deep area를 이 경로의 일괄 진입 조건으로 두지 않는다.

### Decision / RL

```text
Probability
→ Decision / MDP
→ RL
→ Agent / Post-training / Model Reasoning
```

RL의 정책·보상·가치·계획은 독립 이론 계보다. RLHF, preference learning, reasoning RL, tool-use RL은 연결되는 응용이며 RL 전체를 대체하지 않는다.

### Mathematical Deep

```text
Calculus
→ Real Analysis
→ Measure Theory
→ rigorous Probability / Stochastic Processes
→ advanced ML / RL / Generative theory
```

Topology는 필요한 deep objective에서 연결하고 blanket prerequisite로 만들지 않는다. Functional Analysis·Differential Geometry·Fourier/Harmonic Analysis·Stochastic Calculus도 관련 medium/deep branch에서 선택한다.

### Perception / Embodied

```text
Deep Learning → Vision → Multimodal
RL + Control → Embodied → World Models
```

이는 지각·행동·환경 모델링을 둘러보는 복수 흐름이다. World Models의 GEN·RL·Control·Planning·Video 계보나 Embodied 밖 응용을 제한하지 않는다.

### Systems / Software

```text
CS Systems → AI Systems
Software Engineering → Harness → Agentic Software Engineering
```

CS-SYSTEMS의 계산 기반과 SE-FOUND의 소프트웨어 공학 기반을 구분한다. Harness로 진입할 때 AGENT와 HUMAN-AI, 실행 지속성이 필요한 경우 LONG-STATE도 연결한다.

## 7. 현재 해상도와 다음 단계

이번 canonicalization은 12개 탐색 grouping의 60개 semantic macro areas, boundary·주요 연결, 15개 hub 후보와 5개 대표 traversal 및 migration 기록을 확정한다. 설계 세션 검토와 이번 repository validation의 provenance는 [ADR](decisions/0001-macro-skeleton-v0.2.md)에서 구분한다.

이전의 “약 100~200개 medium-resolution node”는 이전 설계 단계의 규모 추정치일 뿐 후속 registry의 acceptance criterion이 아니다. 실제 node 수는 node cohesion(하나의 중심 질문), downstream dependency·독립 재사용, 독립 Learning Objective와 prerequisite 가능성, 별도 Practice Bank 필요성 등 Ontology v1.0의 분리 기준으로 재산정한다.

Macro Skeleton v0.2 canonicalization 당시에는 medium-resolution candidate 검토와 Registry admission을 별도 후속 단계로 남겼다. 현재 Medium Registry v1은 [registry/](registry/README.md)에 별도로 유지하며, schema는 [REGISTRY_SCHEMA.md](REGISTRY_SCHEMA.md), identity·allocation은 [NODE_IDENTITY.md](NODE_IDENTITY.md)를 따른다. Classification/tagging(예: core / branch)과 maturity/stability metadata의 미정 의미는 별도 검토하며, Ontology에 필요한 정의가 없다면 별도 canonicalization으로 해결한다. Curriculum-relative role을 Concept의 절대 속성으로 혼동하지 않는다.

Semantic edges, detailed prerequisite, Learning Objective graph, atomic concept expansion, Practice/Evidence mapping은 아직 수행하지 않았다. 이들을 이번 macro map의 목록이나 화살표로부터 자동 생성하지 않는다. 실제 진행 상태는 PROJECT_STATE.md에서 관리한다.
