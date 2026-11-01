# ADR 0006 — Korean Authoring & Terminology Policy v0.1

Status: ACCEPTED — 2026-09-13

## Context

Baseline은 `a745edeffc1b56d497e283997406863a8ac0ad63` (`docs: checkpoint learning objective pilot v0.1`)이다. Preflight에서 clean `main`, local HEAD = origin/main = actual remote main = baseline을 확인했다. Knowledge Registry는 504 active / 0 retired, Semantic Graph는 603 assertions, official LO issued는 0이며 `learning/objectives.jsonl`은 없다.

설계 입력은 사용자가 제공한 Korean Authoring & Canonical Terminology Policy v0.1 checkpoint 명세다. 기존 English LO Pilot 29개는 L4 PASS이며 external/design granularity review PASS는 **사용자 제공 외부 설계 검토 provenance**다. 이번 repository 작업에서 외부 검토를 재실행하지 않았다. Korean publication-language validation은 미수행이며 English pilot의 unchanged final freeze는 의도적으로 보류한다.

[Ontology v1.0](../ONTOLOGY_V1.md)의 §3.9 terminology metadata와 §12 publication projection은 별도 publication terminology layer를 허용한다. 기존 [LO Schema](../LEARNING_OBJECTIVE_SCHEMA.md)의 statement·grounding·observable performance·identity 규칙과 새 한국어 authoring rule 사이에 semantic conflict는 발견하지 않았다. 이 결정은 policy/schema canonicalization이며 실제 용례의 학술적 확립 여부나 학습효과를 검증한 연구 결과가 아니다.

## Decision

- [KOREAN_AUTHORING_TERMINOLOGY_POLICY.md](../KOREAN_AUTHORING_TERMINOLOGY_POLICY.md)를 **CANONICAL — Korean Authoring & Terminology Policy v0.1**로 채택한다. Publication prose와 향후 LO statement의 기본 언어는 한국어다.
- English canonical K identity/key/title/scope/boundary와 semantic edges는 semantic authority로 유지한다. 한국어 표기는 authoring/publication layer이며 semantic source를 overwrite하지 않는다.
- Future Concept labels는 `terminology/concept_labels.jsonl`에서 기존 K로 참조한다. General technical terms는 `terminology/terms.jsonl`에서 sense별 `term_key`로 관리한다. Term key는 Knowledge identity가 아니며 K/LO issuance·non-reuse 규칙을 상속하지 않는다.
- Display enum은 `ko`, `ko_en_first`, `english`, `acronym`, `ko_acronym_first`다. Korean label은 해당 세 Korean policies에만, literal acronym은 두 acronym policies에만 필수다. Note fields와 avoid forms는 혼동 방지·sense 구별·full-form 표시 지침에 필요한 경우만 허용한다.
- Exact applicable entry를 먼저 조회한다. Concept occurrence는 K label, 비-Concept sense는 term entry를 적용하며 일반 용어가 K label을 override하지 못한다. Approved precedent → established usage → English retention → provisional candidate/review의 fallback은 자동 canonical 승격이 아니다.
- Worker-local spontaneous translation의 조용한 canonical 확정은 금지한다. Unknown recurring terms는 위치·sense·후보·근거·위험을 review로 수집하고 publication freeze 전에 해소한다.
- [terminology/README](../terminology/README.md)는 schema/policy-only 상태를 알린다. Population은 0이며 두 JSONL은 empty file도 생성하지 않는다.
- English Pilot 29개와 모든 L1/L2/L3/L4 artifacts는 byte-identical인 **pre-admission semantic reference pilot**으로 보존한다. Korean Terminology Pilot → terminology review/freeze → 별도 Korean LO conversion → semantic-equivalence audit → Korean LO final freeze → full LO population orchestration을 후속 순서로 둔다.

## Rationale and alternatives rejected

### Why English canonical semantics remain untouched

이미 발급된 K와 그 scope/boundary/edges는 의미 구별의 기준이다. 영어 semantic fields를 한국어로 일괄 교체하면 표현 선택과 semantic revision을 혼동하고 기존 audit의 대조 기반을 잃는다. Korean label 변경은 K identity 변경이 아니므로 semantic fields의 in-place translation과 bilingual 중복 fields 추가를 기각한다.

### Why Korean terminology is separate

한국어 출판은 동일 의미를 학습자에게 표현하는 선택이다. Knowledge Registry에 language/display/translation provenance를 넣는 대안은 semantic data와 publication policy를 결합한다. 별도 layer는 현재 Ontology와 schema bytes를 보존하면서 approved terminology를 공유하게 한다.

### Why Concept labels and general terms differ

Concept-backed label은 K를 통해 의미가 결정된다. General term까지 K로 발급하면 반복되는 기술 표현을 Medium Concepts로 부풀리게 된다. 반대로 K label에 별도 terminology identity를 발급하면 두 identity를 동기화해야 한다. 두 files와 sense별 authoring key를 채택하고 K/LO lifecycle을 일반 용어에 복제하지 않는다.

### Why worker-local translation is disallowed

각 worker의 자연스러운 문장 선택만으로는 verification/validation 같은 구별과 일관된 병기를 보장할 수 없다. 자유 번역 후 문자열만 통일하는 대안은 이미 collapse된 sense를 놓칠 수 있다. Applicable entry 우선 적용과 provisional review를 통해 번역 제안은 허용하되 조용한 canonical 확정은 막는다.

### Why English terms and acronyms can remain untranslated

원어·약어는 의미 정확성과 검색·문헌 연결에 유리할 수 있다. 일괄 한국어화는 이 연결을 손상할 수 있어 term별 display policy를 둔다. 모든 record에 `preferred_ko`를 필수로 하는 대안은 retained terms에 가짜 번역을 요구하므로 기각한다. `acronym` literal은 English title만으로 정확히 유도할 수 없어 양쪽 schema에 조건부로 허용한다. Full-form 전용 enum/field는 추가하지 않고 필요시 승인된 note와 English source를 사용한다.

### Why preferred/avoid forms and collision review are useful

Preferred만으로는 혼동을 일으킨 경쟁 번역어와 배제 이유를 잃는다. Avoid는 실제 충돌 위험에 한정하고 note에 이유를 요구한다. 동일 한국어 표기를 무조건 금지하는 대안도 다의어의 정당한 사용을 막으므로 기각한다. 양방향 collision review와 qualifier/병기/표기 변경을 의미에 따라 판단한다. Policy 예시를 승인 용어로 취급하는 대안은 schema-only 경계를 침범하므로 기각한다.

### Why terminology pilot precedes Korean LO conversion

English pilot의 structural/granularity PASS는 한국어 표현에서의 의미 구별을 확인한 결과가 아니다. 먼저 30–60 high-risk terms와 mandatory families를 검토해야 29개 LO의 action/object/조건·grounding을 보존하는 한국어화를 평가할 수 있다. English pilot을 unchanged final publication pilot으로 freeze하거나 504 Concepts/29 LOs를 지금 번역하는 대안은 기각한다.

## Consequences

한국어 저술 worker는 policy와 applicable entries, 그 의미의 canonical K를 확인해야 한다. Unknown-term review와 collision/provenance 관리 비용이 추가되며 registry가 비어 있는 동안 문서 예시를 승인된 glossary로 사용할 수 없다. 실용성과 의미 구별의 trade-off는 후속 pilot에서 근거와 함께 결정한다.

Provenance는 K/term_key에 연결되는 후속 review/admission artifacts에서 추적하며 scientific Claim Status와 구별한다. First-use는 독립 publication unit 기준이고 re-entry 병기를 허용한다. Mathematical notation, code/API identifiers와 proper-name literals는 해당 authority를 유지한다.

변경 범위는 새 policy, 이 ADR, terminology README 및 PROJECT.md, PROJECT_STATE.md, root README, decisions README, learning README의 **8개 파일**이다. Learning README는 기존 영어 pilot의 상태·다음 절차만 명확히 한다. 모든 다른 tracked bytes는 보존한다. Ontology/LO Schema/Node Identity/Registry Schema/Semantic Edge Schema/Macro Skeleton, Node Registry, Semantic Graph 및 existing pilot artifacts를 수정하지 않는다. Terminology entries 0 / official LO 0, next K0505 유지. 이번 checkpoint 완료 뒤 멈춘다.

## Validation

기존 Registry/Semantic-edge validators, existing 117 tests, baseline 대비 모든 비대상 tracked bytes, 504 active / 0 retired 및 603 assertions, pilot 29개, 금지 JSONL 부재, Markdown links/fragments, git diff --check와 8-file boundary를 검증한다. Schema/display/precedence·provenance·pilot 경계의 문서 정합성을 함께 검토한다. 이는 policy/schema 검증이며 실제 terminology choice의 freeze 또는 한국어 LO semantic-equivalence 검증이 아니다. 수행 결과는 검증 후 아래에 기록한다. Committed-revision 검증 및 최종 commit/remote/tree 상태는 완료 보고에서 별도로 확인한다.

### Repository validation — 2026-09-13

- Working-tree Registry validator PASS: 504 active / 0 retired, identity/history 보존. Semantic-edge validator PASS: 603 assertions와 valid endpoints/order/cycles.
- Existing full test suite **117/117 PASS**. 새 tests나 permanent terminology/LO validator는 생성하지 않았다.
- Baseline 대비 모든 비대상 tracked files **83개 byte-identical**. 보호 canonical 문서·두 Registry JSONLs, English Pilot 29개 및 L1/L2/L3/L4 전체 artifacts를 포함한다. K issuance 변경 없음, next K0505 유지.
- 상대 Markdown links **315개**, 그중 fragment **1개 PASS**. 계획된 **8개 파일**만 변경; 모든 변경 문서 UTF-8/no BOM/LF/final newline/whitespace 검사 및 `git diff --check` PASS.
- Canonical terminology entries **0**; `terminology/concept_labels.jsonl`, `terminology/terms.jsonl` absent. Official LO issued **0**; `learning/objectives.jsonl` absent.
- Editorial architecture review: 다섯 display policies의 조건부 label/acronym 요구, K 대 general-sense lookup 우선순위, unknown-term workflow, preferred/avoid와 collision, provenance/Claim Status 분리, illustrative-only 예시, mandatory future stress families 및 English pilot 보존/한국어 freeze 연기 상태가 정책·ADR·안내 문서 간 일치함을 확인했다. 실제 번역 선택·용례 조사·terminology pilot·한국어 LO 변환은 수행하지 않았다.
