# 첫 상세 절의 실행 실습

본문의 가중 집계만 다룬다. NumPy2.2.6·Python3.12 계열을 `uv.lock`에 고정했다. 실제 검증은 Python3.12.2 CPU에서 수행했다. 기존 v0.3의 NumPy 고정 환경을 출발점으로 이름·설명을 새 후보에 맞추었으며, PyTorch 모델 학습이나 scaled dot-product는 이번 실습에 포함하지 않는다. 최신 버전 추천이 아니다.

```bash
cd chapters/transformer/section-10-1/learning-source
uv sync --locked
uv run python demo.py
uv run python verify.py
```

- `aggregate.py`: 교육용 비음수 점수 행합 규칙·가중 집계·출처별 기여·비율 이동·대응 순열. 전체72줄을 본문 부록에 수록한다.
- `demo.py`: 본문의 두 요청. 예상 출력은 `EXPECTED_OUTPUT.txt`다.
- `solution_code.py`: 독립연습12의 한 구현.14줄을 별도 해설에 실제 소스로 수록한다.
- `verify.py`: NumPy 배열 연산을 쓰지 않는 `Fraction` 스칼라 기준, 별도로 적은 예상값24사례, 증명 조건100변형·거부7조건, 오류 구현의 반례. 출력은 `NUMERICAL_OUTPUT.json`에 남긴다.

소스 표지는 `section-source-v0.1`이며 인쇄 파일의 SHA-256과 범위는 후보 루트 `source-manifest.json`에서 검사한다. 공식 Exercise ID가 아니다. Python 코드 인덱스는0부터 시작하고 수학의 위치 인덱스는1부터 시작한다. 행합·비음수의 코드 검사는 부동소수점 허용오차를 사용하지만 수학적 정리의 가정은 정확한 조건이다. 출력 재현은 독자의 언어 의미 이해나 Mastery 실증이 아니다.

개발 호스트에서는 기존 uv 캐시와 기존 Python 경로로 새 환경을 오프라인 생성했다. 이 설정은 독자에게 필요하지 않다. NumPy 외 GPU·대형 모델·데이터 다운로드는 필요하지 않다.
