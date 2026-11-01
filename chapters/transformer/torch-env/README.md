# PyTorch 실습 환경

10.11절 통합 실습(`../learning-source/demo_integrated.py` 등)이 쓰는 고정 환경입니다. `pyproject.toml`과 `uv.lock`만 있고 코드는 `../learning-source/`에 있습니다. NumPy 1.26.4와 PyTorch 2.2.2를 쓰고 CPU에서 실행합니다. Linux x86_64에서는 잠금 파일에 따라 CUDA용 PyTorch와 `nvidia-*` 휠(수 GB)이 설치됩니다.

```bash
uv run --locked --directory chapters/transformer/torch-env python ../learning-source/demo_integrated.py
```

원래는 이 장의 이전 전체 파일럿 실습 폴더에 있던 환경이라 `pyproject.toml`의 이름이 `transformer-full-pilot`입니다.
