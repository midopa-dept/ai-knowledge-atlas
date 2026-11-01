"""10.3 계산에서 직접 제작한 벡터 도해. 논문 그림을 복제하지 않는다."""
from html import escape
from pathlib import Path
root = Path(__file__).resolve().parent


def text(x, y, value, size=19, color='#1f2937', anchor='start'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{escape(value)}</text>'


def box(x, y, w, h, color='#f8fafc'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{color}" stroke="#64748b"/>'


def arrow(x1, y1, x2, y2, color='#475569'):
    return f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{color}" stroke-width="2" fill="none" marker-end="url(#arrow)"/>'


def save(name, w, h, parts):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="context-stroke"/></marker></defs><rect width="100%" height="100%" fill="white"/><g font-family="NanumGothic, sans-serif">' + ''.join(parts) + '</g></svg>'
    (root/name).write_text(svg+'\n')


p=[text(20,30,'점수와 권한을 따로 구성한 뒤 허용 위치만 집계한다',23),
   box(20,65,310,85,'#eff6ff'),text(35,94,'Q: 3 × 1     K: 3 × 1'),text(35,124,'S의 각 행 = [0, ln2, ln3]'),
   box(380,65,340,85,'#ecfdf5'),text(395,94,'원래 위치 + 실제 키 여부'),text(395,124,'B: 3 × 3,  True = 허용'),
   arrow(180,151,270,208),arrow(550,151,480,208),
   box(100,210,520,135,'#ecfdf5'),text(115,239,'각 질의의 허용 열만 Softmax'),
   text(115,270,'J0 = {0}       → A0 = [1, 0, 0]'),
   text(115,300,'J1 = {0, 1}   → A1 = [1/3, 2/3, 0]'),
   text(115,330,'J2 = {0, 1, 2} → A2 = [1/6, 1/3, 1/2]'),
   box(20,395,210,65),text(35,424,'V: 3 × 2'),text(35,448,'값의 출처는 K와 대응'),
   arrow(230,426,300,426),arrow(410,345,410,395),
   box(300,395,420,100,'#eff6ff'),text(315,423,'O = AV: 3 × 2'),text(315,452,'[2,0], [2/3,4], [19/3,8]'),text(315,480,'다음 위치의 예측 계산으로 전달'),
   text(20,535,'입력 BOS / y1 / y2    →    예측 대상 y1 / y2 / y3',20),
   text(20,572,'빈 유효 행: 오류     패딩 질의: 정규화 생략·출력0',19)]
save('masking-flow.svg',750,595,p)

p=[text(20,30,'질의 행1: 입력 y1로 대상 y2를 예측한다',23),
   text(270,69,'키 배열 열 j',20)]
for j,(pos,token) in enumerate([(2,'y2'),(0,'BOS'),(1,'y1')]):
    x=270+135*j
    p += [text(x+48,100,f'열{j}',18,anchor='middle'),text(x+48,130,f'원래 위치{pos}',18,anchor='middle'),text(x+48,158,token,19,anchor='middle')]
for i,row in enumerate([[0,1,0],[0,1,1],[1,1,1]]):
    y=182+76*i
    p += [text(20,y+24,f'질의 행{i}',18),text(20,y+50,f'원래 위치{i} → 대상{i+1}',17)]
    for j,b in enumerate(row):
        x=270+135*j
        p += [box(x,y,96,56,'#d1fae5' if b else '#f1f5f9'),text(x+48,y+36,str(b),24,anchor='middle')]
p += [text(20,445,'행1의 잘못된 tril: [1, 1, 0]',20,'#b91c1c'),
      text(20,477,'열0 (위치2·정답) → 출력 → y2 예측: 누출',19,'#b91c1c'),
      text(20,511,'수정: [0, 1, 1]  →  미래 열0 차단·과거 열2 복구',19,'#047857'),
      text(20,545,'열0/1/2의 V도 위치2/0/1에 맞춰 함께 옮긴다.',18),
      text(20,579,'초록1 = 허용, 회색0 = 차단. 표는 수정 후 전체 Mask다.',18)]
save('masking-grid.svg',720,602,p)
print('10.3 직접 제작한 벡터 도해2개 생성')
