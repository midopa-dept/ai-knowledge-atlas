# 제10장. Attention과 Transformer (검토 후보)

[저장소 README](../../README.md)

Attention의 가중 집계에서 출발해 점수 계산, Mask, Self/Cross Attention, Multi-Head, 위치 표현, Transformer 블록, Encoder·Decoder 구조, KV Cache, Efficient Attention을 거쳐 작은 Transformer 전체 구현까지 이어지는 11절짜리 장입니다. 장 번호 10은 조판용이며 책의 최종 장 번호가 아닙니다.

**상태:** 절별 독립 기술·교육 검토, 전 지면 검토, 교정 재심사를 마친 검토 후보입니다. 저자의 최종 편집·출판 승인과 실제 독자의 학습효과 검증은 하지 않았습니다.

## 읽는 법

| 파일 | 내용 |
| --- | --- |
| [CHAPTER.pdf](CHAPTER.pdf) | 본권 241쪽. 이론·도출·예제·유제·독립 연습·심화 문제·Checkpoint·미주·참고문헌 |
| [SOLUTIONS.pdf](SOLUTIONS.pdf) | 별도 상세 해설 114쪽 |
| [CHAPTER.md](CHAPTER.md) · [SOLUTIONS.md](SOLUTIONS.md) | 위 PDF의 pandoc 원고 |

**읽기용은 PDF입니다.** Markdown은 pandoc + XeLaTeX 빌드용 원고라서 GitHub 화면에서는 일부가 다르게 보입니다.

- 인쇄용 코드 블록은 비어 있습니다. 빌드할 때 `source`·`source-start`·`source-end` 속성이 가리키는 실습 파일의 줄을 읽어 채웁니다.
- `{#sec-…}` 같은 pandoc 속성과 교차 참조가 그대로 보입니다.

PDF는 비공개 개발 저장소에서 2026-10-15(KST)에 빌드했습니다. 빌드 스크립트와 조판 설정은 옮기지 않았습니다. 이 저장소에 맞춰 원고의 경로 표기(그림·실습 위치)를 바꿨기 때문에, PDF 본문의 실행 명령에 나오는 `candidates/…` 경로는 아래 표의 위치로 읽어야 합니다.

| PDF의 경로 | 이 저장소 |
| --- | --- |
| `candidates/transformer-section-series-v0.1/learning-source` | [learning-source/](learning-source/README.md) |
| `candidates/transformer-detailed-section-pilot-v0.1/learning-source` | [section-10-1/learning-source/](section-10-1/learning-source/README.md) |
| `candidates/chapter-transformer-pilot-v0.1/learning-source`(PyTorch 환경) | [torch-env/](torch-env/README.md) |

## 실습

[uv](https://docs.astral.sh/uv/)와 Python 3.12가 필요합니다. 모든 실습은 CPU에서 돌고, 데이터셋·모델 다운로드·상용 API는 필요하지 않습니다. 단, Linux x86_64에서는 `torch-env/uv.lock`에 따라 CUDA용 PyTorch와 `nvidia-*` 휠(수 GB)이 함께 설치됩니다.

```bash
cd chapters/transformer/learning-source
uv run --locked python demo_scoring.py
uv run --locked python verify_scoring.py
```

10.2~10.10절 실습은 `learning-source/`의 NumPy 환경에서, 10.1절은 `section-10-1/learning-source/`에서 돌립니다. 10.11절 전체 모델(CPU 학습·생성)은 PyTorch 환경을 씁니다.

```bash
uv run --locked --directory chapters/transformer/torch-env python ../learning-source/demo_integrated.py
uv run --locked --directory chapters/transformer/torch-env python ../learning-source/verify_integrated.py
```

절별 파일 설명과 기대 출력은 [learning-source/README.md](learning-source/README.md)에 있습니다. `verify_*.py`는 `learning-source/`(10.1절은 `section-10-1/learning-source/`)의 결과 JSON을 다시 씁니다.

2026-11-02에 이 저장소의 사본으로 다시 돌린 결과(macOS, Apple Silicon)는 다음과 같습니다.

- `verify_*.py` 11개가 모두 정상 종료했습니다(10.2~10.10절 9개, 10.11절 1개, 10.1절 1개).
- 데모 11개 중 8개는 출력이 `EXPECTED_*`와 바이트 단위로 같았습니다.
- `demo_cache.py`·`demo_efficient.py`는 부동소수점 마지막 자리만 달랐습니다.
- `demo_integrated.py`는 학습 손실과 logit이 1e-7 수준에서 달랐습니다.

원고가 밝히듯이 운영체제·PyTorch 빌드·BLAS가 다르면 마지막 자리가 달라질 수 있습니다. 검증 스크립트는 허용오차로 비교합니다.

## 그림

`figures/`의 SVG·PDF는 같은 폴더의 `make_*.py`로 직접 그렸습니다. 10.1절 그림은 `section-10-1/figures/`에 있습니다. 그중 `qkv-roles`·`convex-region`은 `section-10-1/make_figures.py`로 그렸고, `translation-overview`·`weighted-retrieval`은 개발 저장소에서 앞서 직접 만든 그림을 옮긴 것이라 생성 스크립트가 없습니다.

## 라이선스

원고·PDF·그림은 [CC BY-NC-SA 4.0](../../LICENSE-CONTENT.md), `.py` 코드와 실습 환경 설정은 [MIT](../../LICENSE)입니다.
