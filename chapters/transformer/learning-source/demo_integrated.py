"""실제 학습·생성·대표 중간값을 JSON과 표준 출력으로 남긴다."""
import json
import platform
from pathlib import Path
import torch
from integrated_transformer import train, generate, EncoderDecoder


def serial(value):
    if isinstance(value, torch.Tensor):
        return value.tolist()
    if isinstance(value, dict):
        return {key: serial(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [serial(item) for item in value]
    return value


def run():
    model, learning = train()
    prefix = torch.tensor([[0, 1]], dtype=torch.long)
    generated, cache, history = generate(model, prefix)
    with torch.no_grad():
        logits, _, trace = model(torch.tensor([[0, 1, 2]]), trace=True)
        torch.manual_seed(23)
        conditional = EncoderDecoder().double().eval()
        cl, ct = conditional(torch.tensor([[0, 2, 1]]), prefix, trace=True)
    result = dict(environment=dict(python=platform.python_version(), torch=torch.__version__,
                                    device='cpu', dtype='float64', threads=1),
                  learning=learning, generated=generated, selection_history=history,
                  processed_tokens=cache.tokens, processed_positions=cache.positions,
                  decoder_trace=trace, encoder_decoder_trace=ct)
    root = Path(__file__).resolve().parent
    (root/'NUMERICAL_INTEGRATED.json').write_text(json.dumps(serial(result), ensure_ascii=False, indent=2)+'\n')
    print(f"CPU 학습 손실: {learning['initial_loss']:.9f} → {learning['final_loss']:.9f}")
    print(f"매개변수 갱신 L2: {learning['update_norm']:.9f}; Seed17; 80회")
    print('생성 시퀀스:', generated)
    print('마지막 처리 위치:', cache.positions.tolist(), '; 아직 처리하지 않은 선택:', generated[-1])
    print('위치2 Logit:', logits[0, -1].tolist())
    print('Encoder–Decoder 반환 shape:', list(cl.shape))


if __name__ == '__main__':
    run()
