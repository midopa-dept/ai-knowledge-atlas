# 10.2절 실습

Python 3.12.2·NumPy 2.2.6·uv 0.13.0, CPU에서 실행했다. Python 3.12 환경을 사용한다. NumPy 외에 모델 다운로드·GPU·API 호출은 필요 없다.

저장소 루트에서:

```bash
cd chapters/transformer/learning-source
uv sync --locked
uv run --locked python demo_scoring.py
uv run --locked python verify_scoring.py
```

- `scoring.py`: 유한 실수·비차단 2차원 Q/K/V. D·S·A·O 반환. mask·batch·Head·dropout을 구현한 함수로 확대해 사용하지 않는다.
- `demo_scoring.py`: 두 질의/세 키/값의 본문 수치와 scale·큰 점수 비교. 실제 출력은 `EXPECTED_SCORING.txt`다.
- `solution_scoring.py`: 독립16의 기여 배열과 독립19의 요구 비 구성.
- `verify_scoring.py`: NumPy 행렬곱과 별도 70자리 Decimal 스칼라 연산 대조, 유한 부호 분포 완전열거, 조건 변형100회, 잘못된 입력10개 거부. 결과는 현재 작업 디렉터리의 `NUMERICAL_SCORING.json`에 기록한다. 증명은 본문과 해설에 있고 테스트로 대체하지 않는다.

source revision은 `scoring-source-v0.1`이며 각 실행 파일의 SHA-256은 상위 `source-manifest.json`에 고정했다. 인쇄 코드는 실제 파일에서 읽는다. 소스를 수정하면 revision·manifest·인쇄 범위·실행 출력·PDF를 함께 검토한다.

개발 호스트에서는 임시 uv 캐시와 기존 Python 경로를 지정해 환경을 만들었다. 새 환경에 동일 NumPy를 설치한 뒤 `uv run --offline --locked`로 실행했다. 이 설정은 독자에게 필요하지 않다.

## 10.3 Mask 실습

같은 Python3.12·NumPy2.2.6·uv.lock 환경에서 다음을 실행한다.

```bash
uv sync --locked
uv run --locked python demo_masking.py
uv run --locked python verify_masking.py
```

- `masking.py`: True=허용, 실제 원래 위치 비교와 Key padding, 허용 열만 정규화하는 `masked_softmax`, S/A/O 반환. 유효 빈행은 ValueError, 비활성 패딩 질의는 정규화 생략·A/O0. 모든 Q/K/V와 S는 유한해야 한다. 단일 시퀀스/Head·2차원 계약이며 batch·학습·dropout은 구현하지 않는다.
- `demo_masking.py`: 차단 전후·패딩·키 재배열·미래 변경을 출력한다. 실제 기대 출력은 `EXPECTED_MASKING.txt`.
- `solution_masking.py`: 누출 허용 쌍/누락 과거 쌍을 따로 진단하고 올바른 정책을 반환한다.
- `verify_masking.py`:70자리 Decimal 스칼라 기준20수치 사례, 실제 위치·패딩/재배열100변형, 미래 K/V 변화의 해당 행 exact 불변, 허용 과거 변화의 양성 대조, 잘못된 입력14거부와 비활성 빈행·극단 점수 계약. 결과는 `NUMERICAL_MASKING.json`.

10.2 소스/lockfile/revision은 보존한다. 새 코드는 `masking-source-v0.1`, 해시는 상위 `masking-source-manifest.json`에 고정한다. 10.3 인쇄 발췌와 전체 구현은 실제 파일의 줄을 읽는다. NumPy와 Decimal 기준 대조는 작성자 자체 검증이며 독립 AI 심사·인간 교육 승인·독자 실증이 아니다.

## 10.4 Self/Cross 입력 출처 실습

동일 uv lockfile·NumPy CPU 환경을 사용한다.

```bash
uv run --locked python demo_sources.py
uv run --locked python verify_sources.py
```

- `sources.py`: 유한2차원 투영, H→Q/Z→K,V 배정, 같은 X를 배정하는 Self 래퍼, 본문 실제 예제 입력과 R. 기존 `masking.py`를 수정 없이 재사용한다. 입력 배열을 직접 변경하지 않고 Q/K/V/S/A/O를 반환한다. 단일 Head·편향 없는 투영이며 batch·자동미분·학습·전체 Block은 구현하지 않는다.
- `demo_sources.py`: Self3위치·Cross2/3위치의 모든 중간값, X+O/H+OR, Z 변경과 열 차단을 출력한다. 실제 출력은 `EXPECTED_SOURCES.txt`다.
- `solution_sources.py`: 제공자만 변경하는 대조와 Z/Mask 열의 대응 순열이다.
- `verify_sources.py`:70자리 Decimal 스칼라 투영/점수/집계110사례, 길이/폭/Mask·Cross 양쪽 순열·Self 대응 순열100변형, Fraction 비율/합, 잘못된 입력12개 거부, 고정 값 기여·제공자 변경 양성 대조·차단 불변·중심차분의 두 미분 경로를 확인한다. 결과는 스크립트 옆 `NUMERICAL_SOURCES.json`에 기록한다.

새 revision은 `sources-source-v0.1`, 해시는 상위 `sources-source-manifest.json`이다. 이전 소스/revision/lockfile은 보존한다. shape 검사는 실제 출처의 정확성을 보장하지 않으므로 피연산자와 중간값도 확인한다. 검증 성공을 독자 학습효과나 독립 심사로 표시하지 않는다.

## 10.5 Multi-head Attention 실습

같은 Python3.12·NumPy2.2.6·uv.lock CPU 환경을 재사용한다.

```bash
uv run --locked python demo_heads.py
uv run --locked python verify_heads.py
```

- `heads.py`: Head별 독립 Q/K/V 투영→기존 `masked_attention`→좌표 축 Concat→W_O. 다른 Head별 비교/값 폭을 허용하고 각 Mask를 명시한다. Self는 같은 x를 H/Z에 배정하고 Cross는 별도 배열을 배정한다. 원입력을 직접 변경하지 않고 각 trace·C·Y를 반환한다. 배치·편향·dropout·학습·전체 Block은 생략했다.
- `demo_heads.py`: 대표 두 Head의 Q/K/V/D/S/A/O·shape·C/Y, Head만 교환한 오류, 대응 W_O까지 바꾼 보존, 두 Head의 Causal 결과를 출력한다. 실제 기대 출력은 `EXPECTED_HEADS.txt`다.
- `solution_heads.py`: 값 폭이 달라도 각 투영·Mask와 W_O의 대응 좌표 구간을 함께 옮긴다.
- `verify_heads.py`: NumPy 행렬곱/지수/Softmax를 호출하지 않는70자리 Decimal scalar reference로 명시5+생성100사례의 투영부터Y까지 대조한다. Fraction 대표 정답, 다른 비교 폭의 scaling·새 독립 문제·7/4폭 새 Cross 인터페이스·Head/요청/제공자 순열·블록 합 분해·상수V 동일 출력·공유 투영 오류·Concat/평균 반례·Mask 불변/양성 대조·14개 잘못된 입력 거부를 검증한다. 결과는 스크립트 옆 `NUMERICAL_HEADS.json`이다.

고정 revision은 `heads-source-v0.1`, 네 실행 파일의 SHA-256은 상위 `heads-source-manifest.json`에 있다. 실제 원본에서 본문/해설의 지정 라인을 인쇄한다. 이전 모든 소스/revision과 lockfile은 보존했다. 독립 scalar **계산 경로**는 독립 AI **심사자**와 다르며 실행 성공을 실제 학습효과로 바꾸지 않는다. Head의 이름·인공 좌표에 언어적 기능을 부여하지 않는다.

## 10.6 위치 표현 실습

기존 Python3.12.2·NumPy2.2.6·uv.lock CPU 환경을 그대로 사용한다.

```bash
uv run --locked python demo_position.py
uv run --locked python solution_position.py
uv run --locked python verify_position.py
```

- `position.py`: Sinusoidal 좌표·같은 폭의 위치 가산→Q/K/V·부호 delta=pQ-pK의 Bias·인접 좌표 쌍 RoPE·세 경로의 S/A/O. 기존 `sources.py`의 matrix/project와 `masking.py`의 score/허용 열 Softmax를 재사용한다. 전체 회전 폭은 짝수이며 실제 위치와 배열 행을 명시적으로 대응시킨다. 유한 CPU float64·단일 Head/시퀀스 계약이다. 안전한 교육용 위치 범위 절댓값2**31-1은 모델 일반 성질이 아니다.
- `demo_position.py`: 공통 기본 내용에서 세 경로의 실제 중간값·Sinusoidal 표·RoPE+Causal 출력을 보여 준다. 기대 출력은 `EXPECTED_POSITION.txt`다.
- `solution_position.py`: 원래 위치를 보존한 K/V 재배열과 순열로 기존 함수를 재사용하는 Split-half 구현이다.
- `verify_position.py`: NumPy 투영/Softmax와 별도70자리 Decimal scalar projection·exp·sqrt,75자리 Taylor sin/cos를 대조한다. 생성100사례마다 세 경로 S/A/O, 알려진90/180도 좌표·Fraction 정답·직교/길이·상대식·동시 이동·4차원·재배열·Split-half·Bias 부호/축·21입력 거부를 검사한다. 결과는 스크립트 옆 `NUMERICAL_POSITION.json`이다. rtol/atol3e-12의 유한 수치 시험은 본문 도출이나 증명을 대체하지 않는다.

고정 revision은 `position-source-v0.1`이고 실행4파일의 SHA-256은 상위 `position-source-manifest.json`에 있다. 인쇄 범위는 position.py86–111/1–111, solution_position.py1–15/18–28이며 실제 원본 줄을 읽는다. 대표 입력 생성 보조 함수는 Learning Source에 남긴다. 기존10.1–10.5 소스/revision·pyproject/lockfile은 불변이다. 독립 계산 경로를 독립 심사자로 표시하지 않는다. Context Length 성능·학습·Serving Cache·전체 Block을 검증한 프로그램으로 확대하지 않는다.

## 10.7 Transformer Block 실습

같은 Python3.12.2·NumPy2.2.6·uv.lock CPU 환경에서 이 디렉터리로 이동해 실행한다. GPU·모델/API·외부 데이터는 필요 없다.

```bash
uv run --locked python demo_block.py
uv run --locked python solution_block.py
uv run --locked python verify_block.py
```

- `block.py`: LN은 (..., d)의 마지막 특징 축을 keepdims=True/ddof=0으로 정규화한다. ε는 양의 유한 스칼라, γ/β는 폭d 벡터다. FFN은 (..., d)에 affine→ReLU→affine을 적용하고 중간 폭 d_ff에서 폭d로 돌아온다. Residual은 exact shape를 요구한다. Block은 단일 시퀀스(n,d)의 Post/Pre이며 `heads.py` MHA를 재사용한다. Head별 Mask(n,n)의 True는 허용, active(n)는 MHA 반환만0으로 한다. 패딩 최종0을 보장하지 않는다. 모든 입력/중간값은 유한 실수 float64이고 제자리 변경하지 않는다. Bias는 FFN에만 있고 Dropout·학습·Block Batch·Cross·별도 마지막 LN·Gated FFN은 지원하지 않는다. LN/FFN의 Batch 벡터화 지원과 Block Batch 미지원을 구별한다.
- `demo_block.py`: 대표 입력·매개변수와 두 순서의 Q/K/V/S/A/O/C/M, Residual, LN 통계, FFN Z/H/F, 최종 반환을 출력한다. `EXPECTED_BLOCK.txt`와 exact 비교한다.
- `solution_block.py`: 새 전체 Post 문제1·γ/β가 있는 새 두 순서 문제2·새 입력의 LN₂ 생략 오류 문제22를 계산한다. 기대 출력은 `EXPECTED_BLOCK_SOLUTIONS.txt`다.
- `reference_block.py`: NumPy 행렬 연산을 쓰지 않는 Decimal70 스칼라 투영/곱/exp/sqrt/LN/FFN으로 전 중간값을 다시 계산한다.
- `verify_block.py`: 명시4+생성100사례의 두 순서208경로를 rtol/atol4e-12로 대조한다. 폭/위치 수/Head/Mask/활성화/ε/γβ 변화, 분산0/폭1, 축·배치별 FFN,22개 거부 조건, 두 층 Causal 불변/전부 허용·입력 누출 양성 대조, 비제자리 계약을 검사한다. `NUMERICAL_BLOCK.json`에 결과를 기록한다. 유한 수치 시험과 본문 정확한 항등식/증명은 구별한다.

고정 revision은 `block-source-v0.1`, 실행5파일의 SHA-256은 상위 `block-source-manifest.json`이다. 인쇄는 block.py81–104 및1–136, solution_block.py41–57의 실제 줄을 읽는다. 기존10.1–10.6 소스/revision·pyproject/lockfile은 불변이다. PyTorch 비교·학습 성능 실험은 미실시다. 독립 계산 경로를 독립 심사자로 표시하지 않는다.

## 10.8 정보 요구와 Architecture 실습

기존 Python3.12.2·NumPy2.2.6·uv.lock CPU 환경에서 이 디렉터리로 이동해 실행한다.

```bash
uv run --locked python demo_architectures.py
uv run --locked python solution_architectures.py
uv run --locked python verify_architectures.py
```

- `architectures.py`: Boolean True=허용, 요청 행/제공 열의 전체 관계와 입력–Target 이동을 명시한다. `decoder_post`는 D(m,dD)와 E(n,dE), 서로 다른 Self/Cross 투영을 받아 Self→합/LN→Cross→합/LN→FFN→합/LN의 trace와 Y(m,dD)를 반환한다. 각 비교 폭dk는 Q/K에서 일치하며 값 폭dv를 W_O로 dD에 맞춘다. 기존 `block.py`·`heads.py`·`sources.py`·`masking.py`를 재사용한다. 유한 실수 float64 단일 시퀀스·한 Head Decoder이며 Batch·Dropout·학습·Cache·PyTorch 모델은 지원하지 않는다. Encoder 예제는 기존 Post Block의 한 Head 구성이다. Padding key와 비활성 Query를 구별하고 비활성 Attention 반환0을 Block 반환0으로 확대하지 않는다. 활성 빈행은 거부한다.
- `demo_architectures.py`: Encoder-only의 E/Readout, Decoder-only의 Causal 출력, 다른 폭/길이 Cross, 실제 원문→Encoder E→Decoder Self/Cross→Y→Token 점수의 모든 중간값을 출력한다. `EXPECTED_ARCHITECTURES.txt`와 exact 대조한다.
- `solution_architectures.py`: 독립 문제10/11의 새 Cross Q/K/V/S/A/O→Residual/LN과 잘못된 tril을 계산한다. `EXPECTED_ARCHITECTURE_SOLUTIONS.txt`가 실제 기대 출력이다.
- `reference_architectures.py`: NumPy 행렬 연산을 호출하지 않는 Decimal70 스칼라 Self/Cross/LN/FFN을 기존 독립 `reference_block.py`와 연결한다.
- `verify_architectures.py`: 생성100사례의 길이/폭/투영/FFN/γβ/Mask/active 전 중간값을 rtol/atol5e-12로 대조한다. Fraction·키 순열·미래 불변·과거/원문 변경 양성 대조·상수0 결함 거부·두 층·입력 오염·스트리밍 Encoder 간접 누출·패딩/비활성·21입력 거부·비제자리 계약을 검사한다. `ARCHITECTURE_CHECKS.json`과 `NUMERICAL_ARCHITECTURES.json`에 결과를 기록한다.

고정 revision은 `architectures-source-v0.1`이고5실행 파일의 SHA-256은 상위 `architectures-source-manifest.json`이다. 인쇄 범위는 architectures.py55–81/1–91 및 solution_architectures.py1–26의 실제 원본 줄이다. 기존10.1–10.7 소스/revision·pyproject/lockfile은 불변이다. 독립 계산 경로는 독립 심사자와 다르며 유한 입력 시험은 본문 귀납 증명·모든 모델 보장·실제 학습효과 실증을 대신하지 않는다.

## 10.9 두 레이어 KV Cache 실습

같은 Python3.12.2·NumPy2.2.6·기존 uv.lock CPU 환경에서 이 디렉터리로 이동해 실행한다.

```bash
uv run --locked python demo_cache.py
uv run --locked python solution_cache.py
uv run --locked python verify_cache.py
```

- `kv_cache.py`: 행별 Pre-LN 두 레이어, Head별 폭·Q/K/V·원위치 Mask·RoPE Q/K 회전·Attention·Concat/W_O·Residual·N/F를 명시한다. `full_prefix`는 전행, `incremental`은 새행만 순차 계산한다. Cache의 Layer/Head/원위치·K/V 및 model/Token/position/policy/valid 계약과 seal을 확인한다. 계약 변화의 보수적 거부는 항목 전체가 수학적으로 무효라는 판정이 아니다. 항목별 유효성은 별도 생성원 분석으로 판단한다. 유한 float64 단일 시퀀스 inference이며 GPU·Batch Serving·훈련·Dropout API·Paging·성능 최적화는 제공하지 않는다. 패딩 Key와 비활성 Query를 구별하고 활성 빈행은 거부한다.
- `cache_validity.py`: 대표 두 레이어의 변경별 Layer/Head/position/K/V 생성원을 추적한다. 재사용·재계산·추가 확인을 구별한다. 모든 Decoder에 통하는 자동 의존 분석기가 아니며 원고의 조건과 예외를 따른다.
- `demo_cache.py`: 원설계의 대표 Full2/Full3·두 레이어 증분·과거 Cache·최종 점수 및 RoPE를 출력한다. `NUMERICAL_CACHE.json`과 `EXPECTED_CACHE.txt`를 생성/대조한다.
- `solution_cache.py`: 유제 새 입력과 독립8의 다른 Prefix/원위치/투영/Head 폭/FFN·γ를 계산한다. `CACHE_SOLUTIONS.json`·`EXPECTED_CACHE_SOLUTIONS.txt`를 제공한다.
- `reference_cache.py`: NumPy 투영/Attention/LN/FFN 함수를 사용하지 않는 Decimal70 스칼라 구현이다. RoPE 삼각함수는 Decimal π로 ±π 각도 축약 후 Taylor 계산한다.
- `verify_cache.py`: 명시3+생성100사례의 전 중간값 Full/Incremental/Decimal·과거 값 보존·변경10안·15거부·원위치/Mask/Head/Layer·허용 과거 반응·정밀도/Dropout/seq정규화 반례·RoPE 원위치1000을 검사한다. `CACHE_CHECKS.json`에 실제 결과와 항목 유효성 표를 기록한다. 미래 불변과 허용 과거 변경 반응을 함께 확인한다.

고정 revision은 `cache-source-v0.1`이며6실행 파일의 SHA-256과 인쇄 범위는 상위 `cache-source-manifest.json`이다. 인쇄는 kv_cache.py55–85/solution_cache.py1–19 원본과 대조한다. `norm`/`feed`의 좁은 함수 인터페이스를 Working 지원으로 사용할 수 있으나 `layer` 전체 호출로 과제의 새 투영/출처 연결을 대신하지 않는다. 기존10.1–10.8 소스·pyproject·uv.lock은 보존했다. 독립 수치 기준·별도 기술 심사·귀납 증명·독자 실증을 구별한다.

## 10.10 비용·연결·Kernel 실습

기존 Python3.12.2·NumPy2.2.6·uv.lock CPU 환경을 사용한다. 이 디렉터리에서 실행한다.

```bash
uv run --locked python demo_efficient.py
uv run --locked python solution_efficient.py
uv run --locked python verify_efficient.py
```

- `efficient.py`: 원위치1부터/배열0부터, True=허용. Full Causal·현재 포함 Local·Causal Global·허용 쌍별 Softmax·층별 초기 의존 집합·특징 내적/직접 합·S/z 재배치·현재 포함 Prefix와 비용 셈을 제공한다. 투영/특징 생성·출력 변환·FFN 비용은 제외한다. 실제 시간/GPU 측정은 없다.
- `reference_efficient.py`: NumPy 행렬곱과 분리한 Decimal70 스칼라 Softmax, Fraction 특징 직접 합, 시간 확장 그래프 경로 열거 기준이다. 별도 계산 경로는 별도 심사자와 다르다.
- `demo_efficient.py`: 본문10/7쌍·세 단계·Global11쌍·Kernel3·Softmax3.732992·전Prefix 상태·미래40/과거10 변경 대조. `NUMERICAL_EFFICIENT.json`과 `EXPECTED_EFFICIENT.txt`에 실제 값을 남긴다.
- `solution_efficient.py`: 다른 Query/Key 특징·Value폭2의 직접/인자/Prefix 계산. `EXPECTED_EFFICIENT_SOLUTIONS.txt`와 대조한다.
- `verify_efficient.py`: 생성120사례의 점수/계수/출력·Fraction/상태 모든 좌표·세층 경로 열거·Key 재배열/원위치·비제자리·미래 불변/과거 대조·잘못된Global 두층누출·24거부 조건을 검사한다. 결과는 `EFFICIENT_CHECKS.json`이다.

특징은 이 구현에서 좌표별 비음수로 제한한다(가중치 비음수의 충분조건). 분모0과 비유한 결과는 거부한다. 원위치는 signed int64 범위의 양의 정수이며 unsigned 입력은 검사 뒤 안전하게 변환한다. 큰 유한 실수도 중간 누적에서 범위를 넘을 수 있어 모든 실수의 수치 안정성을 보장하지 않는다. 관찰용 Dense Mask·가중치 반환과 모든 Prefix 상태 목록을 저장하므로 학습 코드 전체를 실제 최소메모리 Sparse/스트리밍 구현이라고 보고하지 않는다. 현재 상태만 보존하는 이론적 크기는 별도다.

source revision `efficient-source-v0.1`의 bytes·인쇄 범위는 상위 `efficient-source-manifest.json`으로 고정한다. 도해는 `../figures/make_efficient.py`로 재생성한다. 기존10.1–10.9 소스·lockfile은 보존했다. 독립 기술 심사는 별도 기록을 따르며 인간 최종 편집 승인·실제 학습효과 실증과 구별한다.

## 10.11 전체 모델·학습·생성

기존 Full Pilot의 Python3.12.2·PyTorch2.2.2·NumPy1.26.4 lockfile을 재사용하며 옛 decoder.py는 수정하지 않았다. 새 소스는 이 디렉터리에 있다. CPU float64·Seed17·1스레드, 외부 모델/데이터/API/GPU가 필요 없다. 최초 환경 구성에는 의존성 설치가 필요하다. 저장소 루트에서:

```bash
uv run --locked --directory chapters/transformer/torch-env python ../learning-source/demo_integrated.py
uv run --locked --directory chapters/transformer/torch-env python ../learning-source/verify_integrated.py
uv run --locked --directory chapters/transformer/torch-env python ../learning-source/flagship_integrated.py
uv run --locked --directory chapters/transformer/torch-env python ../learning-source/compare_integrated.py
uv run --locked --directory chapters/transformer/torch-env python ../learning-source/solution_integrated.py
```

`integrated_transformer.py`는 직접 Q/K/V·Mask·Head 결합·출력 투영·Pre-LN/Residual/FFN·2층 Decoder·별도 Encoder–Decoder·Loss/Adam/학습·생성·레이어 Cache를 구현한다. 기본 Decoder에는 Padding/RoPE/Local을 넣지 않았다. `demo_integrated.py`는 실제 학습/생성/Trace, `verify_integrated.py`는398 중간 Tensor·별도 SDPA/스칼라·정보 접근·Cache 생성원 시험, `flagship_integrated.py`는 작은 Post-LN 두 단계 생성, `compare_integrated.py`는 동일 학습 Head의 Full/Local/별도 특징Kernel, `solution_integrated.py`는 새 통합 문제의 계산 자료다. JSON은 모두 실제 실행 관찰이며 단순 기대값이 아니다. source revision과6파일 해시는 `../integrated-source-manifest.json`, 상세 조건·한계·환경은 개발 저장소의 검증 기록에 있다(공개하지 않음).
