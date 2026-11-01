"""계산 경로·레이어 분리·한 요청·위치 회전·생성원 변경의 직접 제작 벡터 도해."""
from pathlib import Path
from html import escape
R = Path(__file__).resolve().parent
B, O, I = '#1d4ed8', '#b45309', '#172033'


def text(x, y, s, size=22, color=I):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">{escape(s)}</text>'


def box(x, y, w, h, lines, color=B):
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{"#eff6ff" if color == B else "#fff7ed"}" stroke="{color}" stroke-width="2"/>'
    for k, s in enumerate(lines): out += text(x+12, y+29+k*28, s, 21)
    return out


def arrow(x1, y1, x2, y2, color=B):
    return f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{color}" stroke-width="2.5" fill="none" marker-end="url(#{"b" if color == B else "o"})"/>'


def save(name, w, h, p):
    markers = ''.join(f'<marker id="{key}" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="{c}"/></marker>' for key,c in [('b',B),('o',O)])
    (R/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs>{markers}</defs><rect width="100%" height="100%" fill="white"/><g font-family="NanumGothic, sans-serif">'+''.join(p)+'</g></svg>\n')

p=[text(25,35,'새 입력 처리 전: 위치0/1은 이미 두 레이어를 통과했다.',26),
   box(25,75,350,68,['Cache 없음: [BOS, y1, y2]','모든 위치 h0, h1, h2 다시 입력']),
   box(485,75,350,68,['Cache 있음: 새 y2 한 행','위치2의 h = [1.2, 1]']),
   arrow(200,143,200,180),arrow(660,143,660,180),
   box(25,188,350,68,['레이어1: 세 행 N/Q/K/V','세 요청 Attention/Residual/FFN']),
   box(485,188,350,68,['레이어1: 새 행 N/Q/K/V','과거 K/V + 새 K/V로 한 요청']),
   arrow(200,256,200,293),arrow(660,256,660,293),
   box(25,301,350,68,['레이어2: 세 반환을 입력','과거 두 위치 계산도 반복']),
   box(485,301,350,68,['레이어2: 새 첫 반환 한 행','레이어2의 과거 K/V 재사용']),
   text(25,418,'고정 계약 아래 새 마지막 반환 대응: [2.647976, 0.243786]',24,O),
   text(25,458,'과거 계산 반복은 줄어도 새 Query의 세 Key 읽기는 남는다.',23)]
save('cache-repeat.svg',860,488,p)
p=[text(25,35,'레이어별 새 입력과 저장 항목의 출처',26),
   box(25,75,810,68,['Token y2, 원위치2: E=[1,1], P=[0.2,0]','초기 h=[1.2,1] → N(h)=[0.099504,-0.099504]']),
   arrow(430,143,430,179),
   box(25,187,350,96,['레이어1 past: 위치0/1','Head1 K: 0.447214,-0.410365','Head2 K: -0.447214,0.410365']),
   box(485,187,350,96,['레이어1 새 항목: 위치2','Head1 K/V: 0.099504/0.199007','Head2 K/V: -0.099504/-0.398015']),
   arrow(200,283,200,313),arrow(660,283,660,313),
   box(25,321,810,68,['각 Head Attention → C/W_O → 합 → N/FFN → 합','첫 반환 h_next = [1.520803,0.837181]'],O),
   arrow(430,389,430,423,O),
   box(25,431,810,42,['둘째 입력 N(h_next) = [0.323438,-0.323438]']),
   arrow(430,473,430,509),
   box(25,517,350,96,['레이어2 past: 위치0/1','Head1 K: 0.847402,-0.419787','Head2 K: -0.847402,0.419787']),
   box(485,517,350,96,['레이어2 새 항목: 위치2','Head1 K/V: 0.323438/0.646876','Head2 K/V: -0.323438/-1.293752']),
   arrow(200,613,200,645),arrow(660,613,660,645),
   box(25,653,810,68,['둘째 Attention/Residual/FFN → 최종 h=[2.647976,0.243786]','각 레이어·Head에 새 K/V 한 행 추가. 과거 행은 보존.'],O)]
save('cache-layers.svg',860,741,p)
p=[text(25,35,'레이어1 Head1: 요청 한 행, 제공 세 위치',26),
   box(25,75,810,42,['새 Q = 0.099504, 실제 요청 위치 = 2']),
   arrow(430,117,430,147),
   box(25,155,810,96,['K(0,1,2) = [0.447214,-0.410365,0.099504]','S = [0.044499,-0.040833,0.009901]','원위치 기준 허용 = [True,True,True]']),
   arrow(430,251,430,281),
   box(25,289,810,68,['Softmax(제공 위치 축) = [0.346717,0.318358,0.334926]','V(0,1,2) = [0.894427,-0.820729,0.199007]']),
   arrow(430,357,430,387),
   box(25,395,810,42,['세 비율 × 대응 세 V의 합 → Head 출력 0.115480'],O),
   text(25,482,'1 × 3 배열의 np.tril → [True,False,False]는 원위치2를 잃는다.',22,O)]
save('cache-head.svg',860,507,p)
p=[text(25,35,'회전 전 Key [1,0], 주파수 theta = pi/2',26)]
for i,(vec,desc) in enumerate([('[1,0]','위치0: 회전0'),('[0,1]','위치1: 반시계90도'),('[-1,0]','위치2: 반시계180도')]):
    x=25+i*285
    p+=[box(x,75,255,68,[desc,'회전 후 K = '+vec]),arrow(x+125,143,x+125,175),box(x,183,255,42,['V: 직접 회전 없음'],O)]
p += [text(25,276,'위치1 → 2: 회전 후 K는 새 좌표로 변환해야 한다.',24),
      box(25,310,810,96,['첫 Q/K 회전 변경 → 점수/집계 변경 가능','첫 Block 반환 → 둘째 N/투영 입력 변경 가능','따라서 상위 V는 다시 생성원을 확인한다.'],O),
      text(25,449,'회전 전 저장도 원위치와 바탕 표현의 유효성을 함께 보존한다.',23)]
save('cache-rope.svg',860,477,p)
p=[text(25,35,'첫 W_Q 변경이 상위 Cache에 도달하는 경로',26),
   box(25,75,350,68,['첫 입력 h → N1 → z','고정 z·W_K/W_V → 첫 K/V']),
   box(485,75,350,68,['첫 입력 h → N1 → z','바뀐 W_Q → 새 Query'],O),
   arrow(200,143,200,180),arrow(660,143,660,180,O),
   box(25,188,810,68,['같은 K/V라도 Query 변화 → 점수/비율/집계 변화 가능','위치0은 Key 하나라 비율1 유지. 여러 Key는 추가 확인.'],O),
   arrow(430,256,430,288,O),
   box(25,296,810,68,['C/W_O → Residual → N2/FFN → 첫 반환','첫 K/V 보존과 첫 반환 보존은 다른 판단'],O),
   arrow(430,364,430,398,O),
   box(25,406,810,68,['첫 반환 → 둘째 N1 → 둘째 Head별 K/V','변경이 전달된 위치마다 둘째 생성원을 확인한다.'],O),
   text(25,518,'Token 변경: 첫 K/V의 해당 위치 → 뒤 요청 집계 → 상위 입력',23)]
save('cache-dependency.svg',860,546,p)
print('Cache 벡터 도해5 생성')
