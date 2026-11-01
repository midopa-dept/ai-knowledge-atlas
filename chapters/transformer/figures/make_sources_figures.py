"""10.4의 출처와 실제 집계를 직접 제작한 벡터 그림으로 표시한다."""
from html import escape
from pathlib import Path
ROOT = Path(__file__).resolve().parent
BLUE, ORANGE = '#1d4ed8', '#b45309'


def text(x, y, value, size=21, color='#172033', anchor='start'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{escape(value)}</text>'


def box(x, y, w, h, fill='#eff6ff', stroke=BLUE):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'


def arrow(x1, y1, x2, y2, color=BLUE):
    return f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{color}" stroke-width="2.5" marker-end="url(#{"orange" if color==ORANGE else "blue"})"/>'


def save(name, w, h, parts):
    markers = ''.join(f'<marker id="{name}" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="{color}"/></marker>' for name, color in [('blue', BLUE), ('orange', ORANGE)])
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs>{markers}</defs><rect width="100%" height="100%" fill="white"/><g font-family="NanumGothic, sans-serif">'+''.join(parts)+'</g></svg>'
    (ROOT/name).write_text(svg+'\n')


p = [text(20, 32, 'Self: 같은 X에서 요청·제공 → X의 위치로 반환', 25),
     box(20, 65, 155, 92), text(35, 98, 'X: 3 × 2'), text(35, 132, '세 위치'),
     box(230, 65, 205, 92), text(245, 98, '각각 투영'), text(245, 132, 'Q / K / V'),
     arrow(175, 110, 225, 110), arrow(435, 110, 480, 110),
     box(485, 65, 285, 92), text(500, 98, 'S / A: 3 × 3'), text(500, 132, '각 요청이 X의 값을 집계'),
     arrow(630, 157, 630, 195), box(230, 200, 540, 65),
     text(245, 240, 'O: 3 × 2  →  예시 X + O: 3 × 2'),
     text(20, 305, 'Cross: H가 요청, Z가 조건 제공 → H로 반환', 25),
     box(20, 340, 155, 76), text(35, 371, 'H: 2 × 3'), text(35, 401, '두 요청'),
     box(235, 340, 200, 76), text(250, 371, 'WQ: 3 × 2'), text(250, 401, 'Q: 2 × 2'),
     arrow(175, 378, 230, 378),
     box(20, 465, 155, 90, '#fff7ed', ORANGE), text(35, 499, 'Z: 3 × 2', color=ORANGE), text(35, 531, '세 제공 위치', color=ORANGE),
     box(235, 465, 200, 90, '#fff7ed', ORANGE), text(250, 499, 'WK / WV', color=ORANGE), text(250, 531, 'K / V: 3 × 2', color=ORANGE),
     arrow(175, 510, 230, 510, ORANGE),
     box(490, 340, 280, 105), text(505, 371, 'S / A: 2 × 3'), text(505, 401, 'O = AV: 2 × 2'), text(505, 431, '행은 H, 합하는 열은 Z', 19),
     arrow(435, 378, 485, 378), arrow(435, 505, 555, 450, ORANGE),
     arrow(635, 445, 635, 485), box(490, 490, 280, 65), text(505, 529, 'H + OR: 2 × 3'),
     text(20, 603, 'R: 2 × 3은 반환 폭을 맞춘다. Z의 새 표현은 직접 반환하지 않는다.', 20),
     text(20, 639, '접근 제약 B: Self는 X–X 쌍, Cross는 H–Z 쌍에 적용한다.', 20)]
save('sources-flow.svg', 800, 665, p)

p = [text(20, 32, 'Cross 요청0: h0 → q0 = [1, 0]', 25, BLUE),
     text(20, 70, 'Q의 출처 H, 비교 폭2: 내적을 √2로 나눈다.', 21),
     text(20, 112, 'Z의 제공 위치', 21, ORANGE)]
for j, (score, ratio, value, contrib) in enumerate([
        ('ln2', '2/5', '[2, 0]', '[4/5, 0]'),
        ('0', '1/5', '[0, 3]', '[0, 3/5]'),
        ('ln2', '2/5', '[2, 3]', '[4/5, 6/5]')]):
    x = 20+j*250
    p += [box(x, 135, 230, 105, '#fff7ed', ORANGE),
          text(x+15, 168, f'위치{j}: v{j} = {value}', 20, ORANGE),
          text(x+15, 200, f's0{j} = {score}', 21), text(x+15, 228, f'A0{j} = {ratio}', 21),
          arrow(x+110, 242, x+110, 275, ORANGE),
          box(x, 280, 230, 66, '#fff7ed', ORANGE), text(x+15, 321, contrib, 23, ORANGE)]
p += [text(20, 386, '허용 세 열의 지수 [2, 1, 2], 분모5 → 값별 기여를 더한다.', 22),
      arrow(385, 398, 385, 421, ORANGE),
      box(70, 425, 640, 80), text(90, 457, 'o0 = [8/5, 9/5] = [1.6, 1.8]', 25, BLUE),
      text(90, 488, '이 한 행은 Z의 위치가 아니라 H의 요청0으로 돌아간다.', 20, BLUE),
      text(20, 546, '다른 제공 위치1·2의 합 = [4/5, 9/5]', 22),
      text(20, 582, '예시 R 적용: o0 R = [8/5, 9/5, -1/5]', 22),
      text(20, 618, 'h0 + o0 R = [13/5, 9/5, 4/5]', 23, BLUE)]
save('sources-detail.svg', 790, 647, p)
print('10.4 전체·확대 도해2개 생성')
