Status: CANONICAL — Korean Authoring & Terminology Policy v0.1

# Korean Authoring & Terminology Policy

## 1. Purpose and authority

한국어 저술의 terminology drift를 막고 semantic fidelity, terminological consistency, reader usability를 함께 보존한다. 번역률을 높이는 것이 목적이 아니다. 이 문서는 authoring/publication terminology의 authority이며 기존 영어 canonical semantics를 번역하거나 대체하지 않는다.

[Ontology v1.0](ONTOLOGY_V1.md)의 Knowledge / Learning / Exposition 분리, §3.9 terminology metadata, §3.7 Notation, §12 publication projection을 따른다. [Node Identity](NODE_IDENTITY.md), [Registry Schema](REGISTRY_SCHEMA.md), [Semantic Edge Schema](SEMANTIC_EDGE_SCHEMA.md), [Learning Objective Schema](LEARNING_OBJECTIVE_SCHEMA.md)의 identity·semantic·record 규칙은 그대로 적용한다. Terminology로 semantic conflict를 해결하지 않으며 필요한 의미 정의는 별도 canonicalization에서 해결한다.

결정 배경은 [ADR 0006](decisions/0006-korean-authoring-terminology-policy-v0.1.md), canonical storage는 [terminology/README](terminology/README.md), 진행 상태는 PROJECT_STATE를 참조한다. Policy v0.1 canonicalization 당시에는 **policy/schema only — terminology canonical entries 0 / official LO issued 0**이었다. 현재 Korean Terminology v1은 T4-B 입고 후 Concept labels 54 / general terms 437 / total 491이며, 이 상태는 검증된 admission commit의 canonical remote `main` non-force fast-forward 수용 시점부터 적용한다. Official LO issued는 0이다. 아래 모든 번역·표시·record 예시는 **ILLUSTRATIVE / NOT APPROVED TERMINOLOGY**이며 preferred term 승인, glossary, pilot freeze 또는 admission이 아니다.

## 2. Korean publication language

AI Knowledge Book의 학습자 대상 서술, 설명, Learning Objective, 문제, 해설 및 기타 publication-facing prose의 기본 저술 언어는 **한국어**다. 본권·해설서·Instructor's Guide의 publication prose에도 이 원칙을 적용한다.

Source code, identifiers, canonical keys, K / LO IDs, API names, protocol literals, mathematical notation, standard abbreviations 및 번역보다 원어 사용이 더 정확하고 명확한 고유 기술명은 유지할 수 있다. 기술용어는 해당 entry의 display policy를 따른다. 내부 architecture/schema 문서나 historical artifacts의 언어까지 일괄 한국어화하지 않는다.

## 3. English semantic authority

[Node Registry](registry/nodes.jsonl)의 K identity, `canonical_key`, English Concept title, scope, boundary와 [Semantic Graph](registry/semantic_edges.jsonl)의 semantic edges가 계속 semantic authority다. 한국어 label은 이 의미의 publication 표현이다. Label 변경만으로 K identity 변경, rename, split, merge, retirement 또는 issuance가 발생하지 않는다.

예를 들어 K0498의 canonical title `Model Checking`은 유지하고, publication label은 별도 terminology registry에서 조회한다. `모델 검사`라는 예시는 policy canonicalization 당시 승인된 것은 아니며 현재 승인 여부는 exact canonical entry로 판단한다. English title/key/scope/boundary, semantic edges, historical proposals/audits를 한국어로 덮어쓰지 않는다. Title을 소문자로 표시하는 등 occurrence typography는 semantic source 수정이 아니지만 고유명사·API·약어의 대소문자는 보존한다.

## 4. Terminology layer separation and resolution precedence

Concept-backed label과 general technical term은 별도 storage를 사용하되 하나의 publication terminology authority를 구성한다. 먼저 occurrence가 가리키는 K 또는 technical sense를 확인한다. 영어 surface string만으로 matching하지 않는다.

1. Canonical terminology registry의 **exact applicable entry**를 적용한다. K를 가리키면 `concept_labels.jsonl`의 해당 K entry, 비-Concept sense이면 `terms.jsonl`의 해당 `term_key` entry다.
2. Concept-backed preferred Korean label을 사용할 수 있는 occurrence에서는 해당 K label/display policy를 적용한다. 이는 1번과 별도 중복 registry가 아니라 Concept lookup의 명시적 fallback이다. 다른 sense의 general-term entry는 K label을 override하지 못한다.
3. 동일 sense에 대한 repository의 **approved terminology precedent**를 확인한다. 승인 결정의 path/commit과 적용 범위를 추적할 수 있어야 한다. Historical draft, 단순 반복 사용, 이 문서의 예시는 승인 근거가 아니다.
4. Established Korean academic/technical usage를 근거와 함께 검토한다.
5. 적절한 한국어 용례를 확정하기 어렵다면 English retention을 우선한다.
6. 필요한 임시 authoring candidate는 review 대상으로 수집한다.

1–2의 canonical entry가 있으면 worker가 새 번역을 만들거나 하위 근거로 바꿀 수 없다. 3–6은 canonical entry 자동 생성 절차가 아니며 중요한 반복 용어는 §12의 review를 거친다. Exact entries의 충돌이나 의미 판별 불가는 임의 우선 선택으로 숨기지 않고 terminology review로 보낸다. Worker-local spontaneous translation의 **조용한 canonical 확정은 금지**하며 명시적으로 provisional인 후보 제안은 허용한다.

## 5. Concept-backed labels

Canonical path: `terminology/concept_labels.jsonl`. Identity는 기존 K인 `concept_id`이며 별도 terminology ID를 발급하지 않는다. K당 하나의 current record를 둔다. English title, canonical key, scope, boundary, macro area는 중복 저장하지 않고 K를 통해 Registry에서 조회한다.

기존 K가 표현하는 의미를 general-term record로 다시 정의하지 않는다. 한 K의 분야별 별칭이 필요하더라도 worker가 두 번째 canonical preferred label을 만들지 않는다. Sense가 canonical Concept boundary를 넘는다면 별도 semantic review가 먼저다.

## 6. General technical terms

Canonical path: `terminology/terms.jsonl`. 독립 Medium Concept K가 아니지만 반복되는 기술용어를 관리한다. 예시 유형은 proof obligation, path condition, runtime, rollout, checkpoint, trace, acceptance condition이다. 실제 K 존재 여부와 scope는 pilot에서 current Registry로 확인하며 이 목록으로 non-Concept 판정을 확정하지 않는다. Glossary를 위해 K node를 억지로 만들지 않는다.

`term_key`는 sense를 구분하는 stable authoring key다. K, LO 또는 Ontology object identity가 아니며 issuance/non-reuse semantics를 자동 상속하지 않는다. Domain/sense namespace를 포함한 ASCII full-match `[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)+`를 사용한다. 예: `formal_methods.proof_obligation`. 같은 English surface라도 다른 sense이면 별도 key와 `context_note`로 구분한다. Key 변경 시 authoring references를 점검하고 Git 변경 기록에 이유를 남기되 K/LO allocation·tombstone 규칙을 적용하지 않는다.

## 7. Translation strategies

| Strategy | 선택 기준 |
| --- | --- |
| Established Korean term | 안정적인 한국어 학술·교육 용례를 확인했을 때 |
| Korean preferred + English first-use | 한국어 표현이 적절하고 원문 검색·문헌 연결에 병기가 도움이 될 때 |
| English retained | 원어가 의미·검색 가능성·실무 명료성을 더 잘 보존할 때 |
| Acronym retained | 약어 자체의 사용이 적절하고 원문과의 연결을 보존할 때 |
| Project-preferred editorial translation | 용례가 불안정하거나 경쟁 번역 중 repository가 근거를 밝혀 선택할 때 |

Strategy는 선택 이유이고 display policy는 실제 표시 동작이다. 별도 strategy field를 중복 저장하지 않고 근거는 review 기록에 둔다. 영어라는 이유만으로 순한국어 대응어를 만들거나 비표준 직역을 강제하지 않는다. 사람 이름, 알고리즘명, architecture명 등 named methods/proper nouns도 term별 결정이며 일괄 음역·한글화하지 않는다.

## 8. Display policies

Enum은 `ko`, `ko_en_first`, `english`, `acronym`, `ko_acronym_first`의 다섯 값이다. 다음 예시는 표시 동작 설명일 뿐 용어 승인 목록이 아니다.

| Value | 첫 등장 | 이후 | 필요한 표시 값 |
| --- | --- | --- | --- |
| `ko` | 고윳값 | 고윳값 | `preferred_ko` |
| `ko_en_first` | 모델 검사(model checking) | 모델 검사 | `preferred_ko` + English source |
| `english` | Transformer | Transformer | English source |
| `acronym` | LLM | LLM | `acronym` |
| `ko_acronym_first` | 검색 증강 생성(RAG) | RAG | `preferred_ko` + `acronym` |

위 표의 기본 표시 동작과 별도로, 독립 Chapter에서 번역된 기술용어를 사용할 때는 §11의 영어 원어 첫 등장 병기 규칙을 적용한다. 이 규칙은 기존 enum이나 특정 record의 `preferred_ko`·`display_policy`를 변경하지 않는다.

English source는 Concept에서 Registry의 English title, general term에서 `english`다. 예시의 lowercase parenthetical은 일반명사 typography이며 고유 기술명에는 적용하지 않는다. English/acronym retention을 위해 불필요한 한국어 label을 생성하지 않는다. Enum은 출판 위치·등장 이력이나 번역의 학술적 확립 여부를 표현하지 않는다.

## 9. Preferred and avoided forms

`preferred_ko`는 해당 의미의 승인된 한국어 표기다. `avoid_ko`는 실제 semantic collision 또는 drift 위험이 있는 번역어만 기록한다. 취향에 따른 포괄적 금지 목록으로 사용하지 않는다. 예를 들어 model checking의 `모델 검사` / avoid `모델 검증` 조합은 검토 가능한 설명용 후보이며 policy canonicalization 당시 freeze하지 않았다.

Avoid의 이유와 혼동되는 sense/K를 Concept의 `note` 또는 general term의 `context_note`에 기록한다. Avoid는 해당 sense의 publication 표기에 적용하며 다른 의미의 정당한 용례나 원문 인용까지 전역 금지하지 않는다. Preferred/avoid 변경은 근거·충돌·사용처 review를 거친 repository 변경으로 관리한다.

## 10. Distinction preservation and collision handling

Readability만으로 서로 다른 의미를 합치지 않는다. 필수 검토 구별은 verification / validation, specification / requirement, state / context / memory, proof / derivation, model checking / formal verification, evaluation / testing, constraint / requirement, execution / inference 및 grounding과 alignment의 서로 다른 technical senses다.

Pilot/admission audit는 두 files를 함께 조회하고 Concept의 English title을 K로 join하여 다음을 확인한다.

- English → multiple Korean forms: 동일 의미의 영어가 여러 preferred forms로 drift하는지 확인한다. 동일 surface의 다른 senses는 근거를 남겨 구분한다.
- Multiple English Concepts/terms → same Korean form: 서로 다른 의미가 같은 preferred 표기로 collapse되는지 확인한다. Acronym/English 유지 항목도 실제 렌더링되는 surface의 충돌을 확인한다.

동일 한국어 surface 자체가 자동 오류는 아니다. 혼동 가능성이 있으면 qualifier 추가, 영어 병기 또는 다른 preferred term을 검토하고 허용/수정 이유·적용 범위를 기록한다. `ko` policy에서 지속적인 disambiguation이 필요하면 worker가 임의 병기를 고착시키지 말고 label/policy revision을 검토한다. 문자열 검사만으로 의미 구별이 보존됨을 증명하지 않는다.

## 11. First-use, acronym and notation rules

First-use는 기본적으로 각 독립적으로 읽는 chapter 또는 publication unit의 최초 등장에 적용한다. Authoring artifact는 그 unit 경계를 명시한다. 별도로 열람하는 LO 목록·문제 세트도 독립 unit일 수 있다. 매 문장·모든 section마다 병기를 강제하지 않는다.

2026-10-13 인간 승인 [집필 결정 D2](decisions/0010-authoring-policy-human-decisions-1-13.md#d2-기술용어와-자연스러운-한국어)에 따라 **번역된 기술용어는 각 독립 Chapter의 첫 등장에 영어 원어를 반드시 병기**한다. Chapter에서는 이 규칙이 §8의 `ko` 첫 등장 영어 생략과 아래 약어 규칙의 full form 비강제보다 우선한다. `ko_acronym_first`에서도 번역 기술용어를 쓰면 영어 원어와 약어를 함께 식별할 수 있게 한다. 원어·약어만 유지하는 표기에 새 한국어 번역을 강제하거나 모든 절에서 다시 병기하지 않는다.

영어 원어는 승인된 English source에서 취한다. Source가 약어뿐이거나 정확한 full form을 확인할 수 없으면 추측하지 않고 bounded terminology review로 남긴다. 특정 record의 표기·표시 지침 변경은 별도 review/admission에서 처리하며 기존 record와 공식 LO 원문을 소급 수정하지 않는다.

Section 간 재진입, 긴 간격, Re-entry Block 또는 고위험 ambiguous term에서는 같은 승인 표기로 원어를 다시 보여줄 수 있다. 반복 병기는 학습·검색·문헌 접근의 필요로 판단하고 새로운 번역을 만들지 않는다.

약어는 term별 policy가 authority다. `acronym`은 첫 등장부터 약어, `ko_acronym_first`는 첫 등장에 한국어와 약어, 이후 약어다. English full form은 기본적으로 강제하지 않는다. 필요한 경우 승인된 `note`/`context_note`에 first-use full-form 표시 지침을 기록한다. Full form은 English source에서 취하고 그 source가 약어 또는 다른 title이면 추측하여 확장하지 말고 review한다. Full form 병기를 위한 별도 enum/field는 만들지 않는다.

수학 기호·공식·영어 variable·standard notation은 한국어 문장에 맞춰 임의 rename하지 않는다. 예를 들어 entropy 설명 언어가 달라져도 `H(X)`는 보존한다. Notation의 의미와 재사용은 Ontology의 Notation Layer에서 관리하고 terminology record로 중복하지 않는다.

## 12. Unknown-term workflow

중요한 반복 용어가 없거나 sense가 불분명하면 먼저 K/term lookup과 approved precedent를 확인한다. 해결되지 않으면 authoring draft에 provisional marker 또는 연결된 review entry를 남긴다. Review에는 English surface, K 또는 intended sense/context, 발생 위치, 임시 표기/retention, 후보·혼동 위험, 확인한 근거와 unresolved 판단을 담는다. 이 정보는 authoring review artifact이며 canonical record에 provisional/status fields를 추가하지 않는다.

Terminology review에서 semantic fidelity → consistency → reader usability 순으로 검토하고, 선택 이유·collision disposition·승인 근거를 기록한 뒤 별도 admission에서 registry에 반영한다. Draft의 provisional marker는 publication freeze 전에 해소한다. Worker는 임시 표기를 조용히 canonical로 승격할 수 없다. 사소한 일반 영어 표현까지 등록하지 않으며 recurring technical sense와 의미 혼동 위험을 기준으로 수집한다. Canonical semantics 자체에 정의가 없으면 번역 결정으로 보충하지 않고 별도 canonicalization으로 보낸다.

## 13. Korean Learning Objective authoring

향후 canonical Learning Objective의 `statement` 기본 언어는 **한국어**다. 수학 기호, canonical abbreviations, approved English-retained terms, code/API identifiers는 유지할 수 있다. Worker는 이 policy와 applicable terminology authority를 읽고 작성한다.

[LO Schema](LEARNING_OBJECTIVE_SCHEMA.md)의 observable performance, 수행 대상·핵심 조건, grounding, granularity 및 identity continuity 규칙을 그대로 적용한다. “이해한다/안다”만으로 수행을 대신하지 않는다. 한국어화가 action, performance object, 핵심 조건·범위 또는 Concept 구별을 바꾸지 않았는지 semantic-equivalence audit로 확인한다. 이 정책은 LO record schema, K grounding 또는 LO issuance 규칙을 변경하지 않는다.

## 14. Terminology provenance

Terminology choice의 근거 종류는 established Korean academic usage, established Korean industry usage, original English retained, project editorial preference로 구분한다. 검토 기록에서 각 K/term_key에 연결해 선택 이유와 출처를 추적한다. Canonical record는 작게 유지하고 provenance 종류·source 목록·review 결과는 별도 pilot/admission review artifact에 둔다.

향후 pilot에서는 국내 대학 교재/강의의 안정적 용례, 국가·학회·표준기관 용어, 널리 쓰이는 한국어 기술문서, 원저자의 공식 용어가 중요한 경우 원문을 사용할 수 있다. 실제 확인한 source와 확인하지 않은 후보를 구별하고 용례를 확인하지 않은 번역을 “확립됨”이라고 보고하지 않는다. Popularity vote가 의미 충실도를 대체하지 않는다.

이는 editorial terminology provenance이며 Ontology의 scientific Claim Status와 다르다. 번역 선택이나 terminology review PASS는 학습효과의 실증이 아니다. 이 checkpoint에서는 외부 용례 연구를 수행하거나 예시의 established status를 판정하지 않는다.

## 15. Registry schema

Policy v0.1 canonicalization 당시 아래 schema만 확정하고 두 JSONL은 **empty file도 생성하지 않았다**. 현재 canonical data는 `terminology/concept_labels.jsonl`과 `terminology/terms.jsonl`에 저장한다. Unknown fields와 `null`은 금지한다. 모든 문자열은 non-empty, 앞뒤 공백 없는 UTF-8 text다.

| Field | Concept label | General term | Contract |
| --- | --- | --- | --- |
| `concept_id` | 필수 | 금지 | Current active Concept K, Registry syntax/padding, K당 unique |
| `term_key` | 금지 | 필수 | §6 syntax, file 내 unique authoring sense key |
| `english` | 금지 | 필수 | 해당 sense의 English term; 같은 surface의 다른 senses 허용 |
| `preferred_ko` | 조건부 | 조건부 | `ko`, `ko_en_first`, `ko_acronym_first`에 필수; `english`, `acronym`에는 생략 |
| `display_policy` | 필수 | 필수 | §8 enum |
| `acronym` | 조건부 | 조건부 | `acronym`, `ko_acronym_first`에 필수; 나머지에는 생략 |
| `avoid_ko` | optional | optional | 중복 없는 non-empty string array; preferred와 같은 값 금지 |
| `note` | optional | 금지 | Concept의 혼동/avoid 이유 또는 full-form 표시 지침 |
| `context_note` | 금지 | optional | General sense 구분, 혼동/avoid 이유 또는 full-form 표시 지침 |

`avoid_ko`를 사용하면 해당 note에 구체적 위험 이유가 있어야 한다. General `english` surface가 복수 senses에 반복되면 `context_note`가 필수다. `note`/`context_note`로 English title/key/scope/boundary/macro를 복제하거나 새로운 Concept 의미를 정의하지 않는다. `acronym`은 title에서 약어를 추측하지 않고 표시할 literal을 결정하기 위해 양쪽 schema에 필요한 최소 조건부 field다. `preferred_ko`는 original English-retention entry에서 가짜 번역을 강제하지 않도록 조건부다.

설명용 record — **NOT APPROVED / NOT ADMITTED**:

```json
{"concept_id":"K0498","preferred_ko":"모델 검사","display_policy":"ko_en_first"}
```

```json
{"term_key":"formal_methods.proof_obligation","english":"proof obligation","preferred_ko":"증명 의무","display_policy":"ko_en_first"}
```

Canonical serialization은 UTF-8/no BOM/LF/final newline, physical line당 compact standard JSON object 하나, readable Unicode 유지다. Blank lines, comments, duplicate members, NaN/Infinity, trailing commas는 금지한다. Concept records는 numeric K ascending, general terms는 ASCII `term_key` ascending으로 정렬한다. Field order는 Concept에서 `concept_id → preferred_ko → display_policy → acronym → avoid_ko → note`, general에서 `term_key → english → preferred_ko → display_policy → acronym → avoid_ko → context_note`이며 존재하는 field만 쓴다. `avoid_ko`는 Unicode code-point ascending으로 정렬한다.

Schema/entry revision은 Git history로 관리하며 per-record version, terminology ID, Claim Status, K/LO lifecycle fields를 추가하지 않는다. K retirement/의미 변경이 발생하면 연결 label과 current publication references를 audit하고 historical 상태는 Git으로 보존한다. K successor로 label을 자동 이전하지 않는다. Admission은 schema/reference/serialization 검사와 editorial sense/collision/provenance review를 모두 요구한다. Permanent terminology validator는 policy canonicalization 당시 만들지 않았으며 현재 `scripts/validate_terminology.py`에서 구조 규칙을 검사한다.

## 16. Pilot and admission boundary

기존 English LO Pilot 29개와 L1/L2/L3/L4 artifacts는 byte-identical로 보존한다. 이들은 **pre-admission semantic reference pilot**이다. L4 structural/schema stress test PASS는 repository audit 결과이고 external/design granularity review PASS는 **policy canonicalization checkpoint에서 사용자가 제공한 외부 설계 검토 결과**다. 외부 검토를 이번 작업에서 재실행했다고 보고하지 않는다. **Korean publication-language validation은 아직 수행하지 않았다.** English 29개 unchanged final freeze는 수행하지 않으며 오류 artifact로 삭제하지 않는다.

Policy canonicalization 당시 다음 별도 checkpoint는 **Korean Terminology Pilot v0.1**이었다. 당시 권장 범위는 30–60 high-risk terms였으며 아래 모든 stress families를 포함하고 29개 LO 한국어 변환에 필요한 용어를 우선하도록 계획했다. 아래 목록은 sense review coverage 요구이며 번역 목록이나 확정 K/non-K mapping이 아니다. 중복 surface는 서로 다른 sense 검토를 생략할 근거가 아니다.

| Family | Mandatory review terms |
| --- | --- |
| Mathematics | proof, derivation, expectation, likelihood, entropy |
| Software Engineering | requirement, specification, verification, validation, testing, acceptance condition |
| Formal Methods | formal verification, formal specification, model checking, proof obligation, invariant, refinement, satisfiability, validity, path condition |
| ML / LLM | objective, loss, inference, representation, alignment, token, context, decoding |
| Agent / Harness | state, execution state, memory, context, harness, verification gate, constraint, execution, handoff, tool call |
| Evaluation | evaluation, evaluator, measurement, validity, benchmark, coverage |
| Safety / Security | behavior specification, prompt injection, trust boundary |

Pilot는 applicable K/sense mapping, provenance, display/first-use/avoid, 양방향 collision과 mandatory distinctions를 검토한다. Freeze와 canonical terminology admission은 구별하며 candidate 승인·검증·명시적 admission 없이 canonical JSONL로 승격하지 않는다. 한국어 LO 변환에 필요한 용어는 approved authority 또는 해결된 review 근거를 갖춰야 한다.

Canonical terminology v1 admission 이후 후속 순서는 **English LO Pilot 29개를 별도 Korean LO Pilot으로 변환 → fresh semantic-equivalence audit → Korean publication-language validation → Korean LO Pilot final freeze → full LO population orchestration design**이다. Population과 LO admission은 후속 승인 절차이며 pilot freeze가 issuance를 뜻하지 않는다.

Policy/schema canonicalization 당시에는 504 Concept titles/scopes/boundaries나 29 objectives를 번역하지 않았고 terminology entries·official LO를 생성하지 않았다. 이후 terminology pilot v0.2의 승인된 146개 records를 별도 admission으로 materialize했다. 이 admission에서도 English Registry semantics와 29 objectives는 보존하며 official LO는 0, `learning/objectives.jsonl`은 absent다. Korean LO 변환은 후속 작업이다.
