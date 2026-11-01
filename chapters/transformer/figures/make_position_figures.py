"""10.6의 직접 제작 벡터 도해. 원 논문 그림을 복제하지 않는다."""
from html import escape
from pathlib import Path
ROOT=Path(__file__).resolve().parent
BLUE,ORANGE,INK='#1d4ed8','#b45309','#172033'


def text(x,y,value,size=22,color=INK):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">{escape(value)}</text>'


def box(x,y,w,h,color=BLUE):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{"#eff6ff" if color==BLUE else "#fff7ed"}" stroke="{color}" stroke-width="2"/>'


def arrow(x1,y1,x2,y2,color=BLUE):
    return f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{color}" stroke-width="2.5" marker-end="url(#{"blue" if color==BLUE else "orange"})"/>'


def save(name,w,h,parts):
    markers=''.join(f'<marker id="{name}" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="{color}"/></marker>' for name,color in [('blue',BLUE),('orange',ORANGE)])
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs>{markers}</defs><rect width="100%" height="100%" fill="white"/><g font-family="NanumGothic, sans-serif">'+''.join(parts)+'</g></svg>'
    (ROOT/name).write_text(svg+'\n')

p=[text(20,33,'위치 신호 없이 내용 행을 옮기면 출력도 따라간다',26),
   box(20,65,335,170),text(40,103,'원래 X = [[1,0],[2,0]]',23),
   text(40,143,'S = ln2 × [[1,2],[2,4]]',22),text(40,184,'O = [10/3, 18/5]^T',24),
   box(485,65,335,170,ORANGE),text(505,103,'PX = [[2,0],[1,0]]',23),
   text(505,143,"S' = ln2 × [[4,2],[2,1]]",22),text(505,184,"O' = [18/5, 10/3]^T",24),
   arrow(355,145,480,145,ORANGE),text(365,126,'교환',22),
   box(20,280,800,83),text(40,313,"Q'=PQ, K'=PK, V'=PV",23),
   text(40,345,"A'=P A P^T → O'=P O",24),
   text(20,405,'조건: 모든 열 허용 · 같은 위치별 투영 · 별도 위치 신호 없음',22)]
save('position-permutation.svg',840,435,p)

p=[text(20,33,'요청0: 같은 내용 점수에 상대 위치별 편향을 더한다',26),
   text(25,85,'키 위치',22),text(180,85,'delta = pQ-pK',22),text(435,85,'편향',22),text(640,85,'새 점수',22)]
for y,pos,delta,bias,score in [(132,'0','0','0','ln2'),(177,'1','-1','ln2','2 ln2'),(222,'2','-2','-ln2','0')]:
    p.extend([text(30,y,pos),text(245,y,delta),text(435,y,bias),text(640,y,score)])
p.extend([text(20,269,'원점수는 각 열 ln2, 요청 위치 pQ=0',23),
          arrow(420,282,420,315,ORANGE),box(20,322,800,93,ORANGE),
          text(40,360,'exp(S) = [2,4,1] → A = [2/7,4/7,1/7]',24),
          text(40,395,'O = (2/7)2 + (4/7)5 + (1/7)8 = 32/7',24),
          text(20,461,'편향은 scale 뒤 더한다. 음수 편향도 접근 금지는 아니다.',22)])
save('position-bias.svg',840,492,p)

p=[text(20,33,'같은 내용 q=k=[1,0], 요청 각도0과 키의 상대각',25)]
for cx,angle,label,dot,endpoint in [(145,0,'0도','1',(235,230)),(420,90,'90도','0',(420,140)),(695,180,'180도','-1',(605,230))]:
    cy=230
    p.extend([text(cx-60,88,'키 각도 '+label,23),
              f'<path d="M{cx-110},{cy} L{cx+110},{cy} M{cx},{cy+100} L{cx},{cy-110}" stroke="#94a3b8" stroke-width="1.4"/>',
              text(cx+102,cy+22,'x',18),text(cx+8,cy-101,'y',18),
              arrow(cx,cy,cx+90,cy,BLUE),arrow(cx,cy,*endpoint,ORANGE),
              text(cx-74,370,'내적 분자 = '+dot,22)])
    if angle:
        end=(cx,cy-60) if angle==90 else (cx-60,cy)
        p.append(f'<path d="M{cx+60},{cy} A60,60 0 0,0 {end[0]},{end[1]}" fill="none" stroke="{ORANGE}" stroke-width="2" marker-end="url(#orange)"/>')
p.extend([text(20,419,'파랑 q: [1,0] 고정 · 주황 k: 반시계 회전 (0도에서는 겹침)',22),
          text(20,458,'상대각 = 키 각도 - 요청 각도 = (pK-pQ) theta',23),
          text(20,500,'두 벡터의 길이는1로 유지되지만 서로 다른 회전은 내적을 바꾼다.',22)])
save('position-rotation.svg',840,532,p)

p=[text(20,33,'세 방식: 위치를 넣는 계산 지점이 다르다',26)]
for x,title,lines in [(20,'Absolute 가산',['X + E','↓ 투영 WQ/WK/WV','Q / K / V','↓ 내적 / sqrt(dk)','S']),
                      (295,'Relative Bias',['X → Q / K / V','↓ 내적 / sqrt(dk)','S0 + b(pQ-pK)','↓','S']),
                      (570,'RoPE',['X → Q / K / V','↓ Q/K에 위치 회전',"Q' / K'  (V 유지)",'↓ 내적 / sqrt(dk)','S'])]:
    p.extend([box(x,65,250,260,BLUE if x==20 else ORANGE),text(x+15,100,title,24)])
    for i,line in enumerate(lines):p.append(text(x+15,145+39*i,line,20))
p.extend([arrow(145,325,290,368),arrow(420,325,420,368,ORANGE),arrow(695,325,550,368,ORANGE),
          box(170,376,500,83),text(190,409,'S → 허용 열 Softmax → A → AV = O',23),
          text(190,442,'Mask는 별도 접근 관계, 값은 제공 행에 대응',21),
          text(20,506,'Absolute: V도 변할 수 있다 · Bias/RoPE: 국소 V는 그대로',22)])
save('position-paths.svg',840,536,p)
print('위치 도해4개 생성')
