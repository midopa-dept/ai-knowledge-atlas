"""직접 제작한10.5 벡터 도해. 본문의 수치·shape·변수와 대응한다."""
from html import escape
from pathlib import Path
ROOT=Path(__file__).resolve().parent
BLUE, ORANGE, INK='#1d4ed8','#b45309','#172033'


def text(x,y,value,size=23,color=INK):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">{escape(value)}</text>'


def box(x,y,w,h,color=BLUE):
    fill='#eff6ff' if color==BLUE else '#fff7ed'
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{color}" stroke-width="2"/>'


def arrow(x1,y1,x2,y2,color=BLUE):
    return f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{color}" stroke-width="2.5" marker-end="url(#{"blue" if color==BLUE else "orange"})"/>'


def save(name,w,h,parts):
    markers=''.join(f'<marker id="{name}" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="{color}"/></marker>' for name,color in [('blue',BLUE),('orange',ORANGE)])
    s=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs>{markers}</defs><rect width="100%" height="100%" fill="white"/><g font-family="NanumGothic, sans-serif">'+''.join(parts)+'</g></svg>'
    (ROOT/name).write_text(s+'\n')

p=[text(20,32,'같은 입력, 두 투영·집계, 하나의 최종 표현',26),
   box(205,60,430,70),text(225,90,'X (x): 3 × 2',25),text(225,118,'[[1,0], [0,1], [1,-1]]',23),
   arrow(330,130,205,182),arrow(510,130,640,182,ORANGE),
   box(20,187,375,180),text(38,220,'Head1: WQ / WK / WV',24,BLUE),
   text(38,252,'각 W: 2 × 1  →  Q/K/V: 3 × 1',21),
   text(38,284,'S / A: 3 × 3 (모든 열 허용)',21),
   text(38,316,'O1 = [7/5, 4/3, 7/5]^T',22),text(38,350,'trace: q, k, v, s, a, o',20),
   box(445,187,375,180,ORANGE),text(463,220,'Head2: 별도 WQ / WK / WV',23,ORANGE),
   text(463,252,'각 W: 2 × 1  →  Q/K/V: 3 × 1',21),
   text(463,284,'S / A: 3 × 3 (모든 열 허용)',21),
   text(463,316,'O2 = [-2/3, 20/13, -36/13]^T',21),text(463,350,'trace: q, k, v, s, a, o',20),
   arrow(205,367,320,420),arrow(640,367,520,420,ORANGE),
   box(145,425,550,77),text(162,459,'C (c): 3 × 2 = [O1 | O2]',25),text(162,489,'행은 같은 요청, 열은 Head별 값 좌표',22),
   arrow(420,502,420,535),box(145,540,550,77),
   text(162,573,'WO (wo): 2 × 2 = [[1,2],[-1,1]]',23),text(162,601,'Y (y) = C WO: 3 × 2',24),
   arrow(420,617,420,650),text(170,686,'세 요청의 표현 → 다음 Block 처리',24),
   text(20,730,'Cross: Q는 H, K/V는 Z. 출력 행은 H의 요청 위치다.',22)]
save('heads-flow.svg',840,758,p)

p=[text(20,32,'Head2의 요청1: 한 행 전체 계산',26),
   box(20,58,800,65,ORANGE),text(40,98,'x1 = [0,1] → q = 1   |   비교 폭 1, scale = 1',24),
   text(25,163,'제공 위치',23),text(220,163,'키 k',23),text(385,163,'점수 s',23),text(570,163,'값 v',23),
   text(25,208,'0: [1,0]',23),text(220,208,'0',23),text(385,208,'0',23),text(570,208,'-1',23),
   text(25,252,'1: [0,1]',23),text(220,252,'ln3',23),text(385,252,'ln3',23),text(570,252,'3',23),
   text(25,296,'2: [1,-1]',23),text(220,296,'-ln3',23),text(385,296,'-ln3',23),text(570,296,'-4',23),
   arrow(420,318,420,350,ORANGE),box(20,355,800,92,ORANGE),
   text(40,392,'모두 허용: exp(s) = [1, 3, 1/3]',24),
   text(40,428,'A2의 행1 = [3/13, 9/13, 1/13]',24),
   arrow(420,447,420,480,ORANGE),box(20,485,800,93,ORANGE),
   text(40,522,'값의 기여: -3/13 + 27/13 - 4/13',24),
   text(40,558,'O2의 행1 = 20/13  (3 × 1 출력의 한 행)',24),
   text(20,625,'s = QK^T / sqrt(1), a = 허용 열 Softmax, o = a @ v',22),
   text(20,667,'금지 열이 있으면 그 열은 지수·분모·집계에서 제외한다.',22)]
save('heads-detail.svg',840,695,p)

p=[text(20,32,'요청0: Concat은 좌표 보존, WO는 좌표 혼합',26),
   box(20,65,335,82),text(40,99,'Head1: o1 = 7/5',24,BLUE),text(40,133,'값 좌표 1개',22),
   box(485,65,335,82,ORANGE),text(505,99,'Head2: o2 = -2/3',24,ORANGE),text(505,133,'값 좌표 1개',22),
   arrow(187,147,322,196),arrow(652,147,520,196,ORANGE),
   box(150,202,540,70),text(175,244,'c0 = [7/5 | -2/3]  (1 × 2)',27),
   arrow(420,272,420,308),box(150,314,540,75),
   text(175,346,'wo의 첫 행: [1,2] ← Head1 좌표',22),
   text(175,377,'wo의 둘째 행: [-1,1] ← Head2 좌표',22),
   arrow(300,389,220,431),arrow(540,389,625,431,ORANGE),
   box(20,437,375,95),text(40,475,'첫 출력: 7/5 - (-2/3)',23),text(40,510,'= 31/15',25,BLUE),
   box(445,437,375,95,ORANGE),text(465,475,'둘째: 2(7/5) + (-2/3)',23),text(465,510,'= 32/15',25,ORANGE),
   text(20,583,'y0 = [31/15,32/15]  |  Y 전체: 3 × 2',25),
   text(20,629,'Head 순서를 바꾸면 대응하는 wo의 행도 함께 옮긴다.',22)]
save('heads-combine.svg',840,658,p)
print('전체·Head 확대·결합 도해3개 생성')
