"""입력에서 Logit까지 관찰하는 작은 CPU Transformer. Dropout은 생략한다."""
from dataclasses import dataclass
import math
import torch
from torch import nn


def snapshot(items):
    """관찰값은 계산 그래프와 분리한다. 학습 경로 자체는 분리하지 않는다."""
    return {key: value.detach().clone() for key, value in items.items()}


@dataclass(frozen=True)
class Cache:
    """고정 모델·연속 원위치·패딩 없는 처리 입력만 보유하는 추론 상태."""
    layers: tuple
    positions: torch.Tensor
    tokens: torch.Tensor
    owner: int
    versions: tuple


class Attention(nn.Module):
    def __init__(self, width, heads):
        super().__init__()
        if width < 1 or heads < 1 or width % heads:
            raise ValueError("모델 폭은 양의 Head 수로 나누어져야 한다")
        self.heads, self.dk = heads, width // heads
        self.q = nn.Linear(width, width, bias=False)
        self.k = nn.Linear(width, width, bias=False)
        self.v = nn.Linear(width, width, bias=False)
        self.out = nn.Linear(width, width, bias=False)

    def split(self, x):
        # 좌표를 Head별로 나누고 위치 축 앞에 Head 축을 둔다.
        b, n, _ = x.shape
        return x.reshape(b, n, self.heads, self.dk).transpose(1, 2)

    def forward(self, receiver, provider, allowed, past=None, trace=False):
        # Self는 두 출처가 같고 Cross는 받는 표현과 제공 표현이 다르다.
        q = self.split(self.q(receiver))
        new_k, new_v = self.split(self.k(provider)), self.split(self.v(provider))
        k, v = new_k, new_v
        if past is not None:
            k = torch.cat((past[0], new_k), dim=2)
            v = torch.cat((past[1], new_v), dim=2)
        if allowed.dtype != torch.bool or allowed.shape != (q.shape[0], q.shape[2], k.shape[2]):
            raise ValueError("허용표는 (batch,요청 수,전체 제공 수)의 Boolean이어야 한다")
        if not allowed.any(-1).all():
            raise ValueError("모든 요청에는 적어도 하나의 허용 Key가 필요하다")
        scores = q @ k.transpose(-1, -2) / math.sqrt(self.dk)
        masked = scores.masked_fill(~allowed[:, None, :, :], -torch.inf)
        weights = torch.softmax(masked, dim=-1)  # Key 위치끼리 정규화한다.
        heads = weights @ v
        b, _, n, _ = heads.shape
        joined = heads.transpose(1, 2).contiguous().reshape(b, n, -1)
        mixed = self.out(joined)
        observed = snapshot(dict(q=q, new_k=new_k, new_v=new_v, k=k, v=v,
                                 scores=scores, allowed=allowed, weights=weights,
                                 heads=heads, joined=joined, mixed=mixed)) if trace else {}
        return mixed, (k, v), observed


class FeedForward(nn.Module):
    def __init__(self, width):
        super().__init__()
        self.first = nn.Linear(width, 2 * width)
        self.second = nn.Linear(2 * width, width)

    def forward(self, x, trace=False):
        linear = self.first(x)
        activated = torch.relu(linear)
        returned = self.second(activated)
        return returned, snapshot(dict(linear=linear, activated=activated,
                                       returned=returned)) if trace else {}


class Block(nn.Module):
    """Pre-LN Self Block. 반환을 정규화하지 않고 다음 레이어로 전달한다."""
    def __init__(self, width, heads):
        super().__init__()
        self.n1, self.n2 = nn.LayerNorm(width), nn.LayerNorm(width)
        self.attention = Attention(width, heads)
        self.ffn = FeedForward(width)

    def forward(self, h, allowed, past=None, trace=False):
        z = self.n1(h)
        mixed, kv, att = self.attention(z, z, allowed, past, trace)
        r = h + mixed
        u = self.n2(r)
        f, ft = self.ffn(u, trace)
        returned = r + f
        observed = snapshot(dict(input=h, z=z, r=r, u=u, f=f,
                                 returned=returned)) if trace else {}
        if trace:
            observed.update(attention=att, ffn=ft)
        return returned, kv, observed


class Decoder(nn.Module):
    """학습 가능한 Absolute Position·2레이어를 기본값으로 쓰는 Decoder-only."""
    def __init__(self, vocabulary=4, width=8, heads=2, layers=2, limit=32):
        super().__init__()
        if layers < 1 or limit < 1:
            raise ValueError("레이어 수와 위치표 길이는 양수여야 한다")
        self.token = nn.Embedding(vocabulary, width)
        self.position = nn.Embedding(limit, width)
        self.blocks = nn.ModuleList([Block(width, heads) for _ in range(layers)])
        self.final_norm = nn.LayerNorm(width)
        self.vocab = nn.Linear(width, vocabulary, bias=False)

    def versions(self):
        # 일반적인 Optimizer/in-place 변경을 검출한다. .data 우회 변경은 금지한다.
        return tuple(p._version for p in self.parameters())

    def forward(self, tokens, past=None, use_cache=False, trace=False):
        if tokens.dtype != torch.long or tokens.ndim != 2 or min(tokens.shape) < 1:
            raise ValueError("입력은 비어 있지 않은 (batch,위치) Long Token ID여야 한다")
        if past is not None and not use_cache:
            raise ValueError("과거 상태를 읽는 호출은 새 Cache도 반환해야 한다")
        if use_cache and (self.training or torch.is_grad_enabled()):
            raise ValueError("Cache는 eval·no_grad 추론에서만 사용한다")
        b, n = tokens.shape
        start = 0
        if past is not None:
            if past.owner != id(self) or past.versions != self.versions():
                raise ValueError("다른 모델 또는 변경된 매개변수의 Cache다")
            start = past.tokens.shape[1]
            expected_positions = torch.arange(start, device=tokens.device)
            if (past.tokens.shape[0] != b or len(past.layers) != len(self.blocks)
                    or not torch.equal(past.positions, expected_positions)):
                raise ValueError("Cache의 batch·레이어·원위치 계약이 다르다")
            for block, (k, v) in zip(self.blocks, past.layers):
                expected = (b, block.attention.heads, start, block.attention.dk)
                if k.shape != expected or v.shape != expected:
                    raise ValueError("레이어별 Cache shape가 다르다")
        if start + n > self.position.num_embeddings:
            raise ValueError("학습 가능한 위치표 범위를 벗어났다")
        positions = torch.arange(start, start + n, device=tokens.device)
        key_positions = torch.arange(start + n, device=tokens.device)
        allowed = (key_positions[None, :] <= positions[:, None]).expand(b, -1, -1)
        embedding = self.token(tokens)
        positional = self.position(positions)[None, :, :].expand(b, -1, -1)
        h = embedding + positional
        initial = h
        kvs, traces = [], []
        for index, block in enumerate(self.blocks):
            old = None if past is None else past.layers[index]
            h, kv, observed = block(h, allowed, old, trace)
            kvs.append(tuple(x.detach().clone() for x in kv) if use_cache else kv)
            traces.append(observed)
        final = self.final_norm(h)  # Block 반환 이후 스택 마지막에서 한 번 더 정규화한다.
        logits = self.vocab(final)
        cache = None
        if use_cache:
            processed = tokens if past is None else torch.cat((past.tokens, tokens), dim=1)
            cache = Cache(tuple(kvs), key_positions.clone(), processed.clone(),
                          id(self), self.versions())
        observed = snapshot(dict(embedding=embedding, position=positional, initial=initial,
                                 returned=h, final=final, logits=logits)) if trace else {}
        if trace:
            observed['blocks'] = traces
        return logits, cache, observed


class EncoderDecoder(nn.Module):
    """출처가 분리된 작은 Pre-LN Encoder–Decoder. 원 논문 재현은 아니다."""
    def __init__(self, vocabulary=4, width=8, heads=2, limit=32):
        super().__init__()
        self.token = nn.Embedding(vocabulary, width)
        self.position = nn.Embedding(limit, width)
        self.encoder = Block(width, heads)
        self.self_attention = Attention(width, heads)
        self.self_norm = nn.LayerNorm(width)
        self.cross = Attention(width, heads)
        self.cross_norm = nn.LayerNorm(width)
        self.ffn_norm = nn.LayerNorm(width)
        self.ffn = FeedForward(width)
        self.vocab = nn.Linear(width, vocabulary, bias=False)

    def forward(self, source, prefix, source_valid=None, trace=False):
        b, n = source.shape
        m = prefix.shape[1]
        if source_valid is None:
            source_valid = torch.ones_like(source, dtype=torch.bool)
        if source_valid.dtype != torch.bool or source_valid.shape != source.shape:
            raise ValueError("원문 유효 키는 같은 shape의 Boolean이어야 한다")
        z = self.token(source) + self.position(torch.arange(n))[None, :, :]
        d = self.token(prefix) + self.position(torch.arange(m))[None, :, :]
        enc_allowed = source_valid[:, None, :].expand(b, n, n)
        e, _, et = self.encoder(z, enc_allowed, trace=trace)
        self_allowed = torch.ones(m, m, dtype=torch.bool).tril().expand(b, m, m)
        # Decoder는 Self→Cross→FFN 각각의 앞에서 정규화한다.
        q_source = self.self_norm(d)
        mixed, _, st = self.self_attention(q_source, q_source, self_allowed, trace=trace)
        h = d + mixed
        cross_q = self.cross_norm(h)
        cm, _, ct = self.cross(cross_q, e, source_valid[:, None, :].expand(b, m, n), trace=trace)
        r = h + cm
        u = self.ffn_norm(r)
        f, ft = self.ffn(u, trace)
        y = r + f
        logits = self.vocab(y)
        observed = snapshot(dict(z=z, d=d, e=e, h=h, cross_q=cross_q, r=r,
                                 u=u, f=f, y=y, logits=logits)) if trace else {}
        if trace:
            observed.update(encoder=et, self_attention=st, cross_attention=ct, ffn=ft)
        return logits, observed


def dataset():
    """길이9의 네 주기열을 한 칸 이동해 입력8개와 Target8개로 만든다."""
    sequences = torch.tensor([[(start + j) % 4 for j in range(9)]
                              for start in range(4)], dtype=torch.long)
    return sequences[:, :-1], sequences[:, 1:]


def train(steps=80, seed=17):
    torch.manual_seed(seed)
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    model = Decoder().double()  # CPU float64로 학습과 비교의 정밀도를 같게 한다.
    inputs, targets = dataset()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.015)
    before = torch.cat([p.detach().reshape(-1) for p in model.parameters()]).clone()
    losses = []
    model.train()
    with torch.no_grad():
        initial = nn.functional.cross_entropy(model(inputs)[0].reshape(-1, 4), targets.reshape(-1)).item()
    for _ in range(steps):
        logits, _, _ = model(inputs)
        loss = nn.functional.cross_entropy(logits.reshape(-1, 4), targets.reshape(-1))
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        losses.append(loss.item())
    model.eval()
    with torch.no_grad():
        final_logits, _, _ = model(inputs)
        final = nn.functional.cross_entropy(final_logits.reshape(-1, 4), targets.reshape(-1)).item()
    after = torch.cat([p.detach().reshape(-1) for p in model.parameters()])
    return model, dict(seed=seed, steps=steps, initial_loss=initial, final_loss=final,
                       update_norm=(after-before).norm().item(), losses=losses,
                       training_prediction=final_logits.argmax(-1).tolist())


@torch.no_grad()
def generate(model, prefix, count=6):
    """선택만 한 마지막 토큰과 Cache에 처리된 토큰을 구별한다."""
    if type(count) is not int or count < 1 or prefix.shape[0] != 1:
        raise ValueError("생성은 batch1과 양의 정수 선택 횟수를 사용한다")
    model.eval()
    logits, cache, _ = model(prefix, use_cache=True)
    sequence = prefix[0].tolist()
    history = []
    for step in range(count):
        chosen = logits[:, -1].argmax(-1)[:, None]
        sequence.append(chosen.item())
        history.append(dict(chosen=chosen.item(), processed_positions=cache.positions.tolist()))
        # 마지막 선택 토큰은 아직 처리하지 않아 반환 Cache에 없다.
        if step + 1 < count:
            logits, cache, _ = model(chosen, past=cache, use_cache=True)
    return sequence, cache, history
