"""본문의 실제 Mask·층 경로·shape로 직접 제작한 SVG. 논문 도해를 복제하지 않는다."""
from pathlib import Path
import sys
from html import escape
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'learning-source'))
from efficient import causal_mask, local_global_mask
ROOT=Path(__file__).resolve().parent
BLUE='#2463a6'; ORANGE='#b94f1b'; INK='#172b40'; LIGHT='#eaf2fb'


def start(height):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="920" height="{height}" viewBox="0 0 920 {height}">',
            '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="context-stroke"/></marker></defs>',
            '<rect width="100%" height="100%" fill="white"/>',
            '<g font-family="NanumGothic, sans-serif" fill="#172b40" font-size="19">']


def text(s,x,y,label,size=19,color=INK,anchor='middle'):
    s.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{escape(label)}</text>')


def line(s,x1,y1,x2,y2,color=BLUE,width=2):
    s.append(f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{color}" stroke-width="{width}" marker-end="url(#arrow)"/>')


def box(s,x,y,w,h,labels,color=BLUE):
    s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{LIGHT}" stroke="{color}" stroke-width="2"/>')
    for t,label in enumerate(labels): text(s,x+w/2,y+30+t*28,label)


def node(s,x,y,label,color=BLUE):
    s.append(f'<circle cx="{x}" cy="{y}" r="18" fill="white" stroke="{color}" stroke-width="2"/>')
    text(s,x,y+6,str(label),17)


def save(s,name):
    (ROOT/name).write_text('\n'.join(s+['</g></svg>'])+'\n')


s=start(385)
for offset,label,b in [(75,'Full Causal: 10쌍',causal_mask([1,2,3,4],[1,2,3,4])),(535,'Local w=2: 7쌍',causal_mask([1,2,3,4],[1,2,3,4],2))]:
    text(s,offset+150,29,label,22)
    text(s,offset+150,55,'제공 j (열)',17)
    text(s,offset-35,162,'요청 i',16)
    for j in range(4): text(s,offset+80+j*45,78,str(j+1),16)
    for i in range(4):
        text(s,offset+42,110+i*45,str(i+1),16)
        for j in range(4):
            x,y=offset+58+j*45,86+i*45
            s.append(f'<rect x="{x}" y="{y}" width="43" height="43" fill="{BLUE if b[i,j] else "#edf0f3"}"/>')
            text(s,x+21,y+28,'1' if b[i,j] else '0',18,'white' if b[i,j] else '#647080')
    text(s,offset+150,300,'자기 연결 포함 / 정보는 제공→요청',17)
    line(s,offset+70,343,offset+250,343)
    text(s,offset+60,368,'1',16); text(s,offset+260,368,'4' if offset==75 else '2',16)
    text(s,offset+155,333,'직접 연결 예',16)
save(s,'efficient-mask.svg')

s=start(385)
xs=[95,335,575,815]; ys=[90,157,224,291]
for l,x in enumerate(xs): text(s,x,38,'초기 입력' if l==0 else f'{l}층 뒤',20)
for l in range(3):
    for i in range(4):
        for j in range(max(0,i-1),i+1):
            active=(j==l and i==l+1)
            line(s,xs[l]+20,ys[j],xs[l+1]-20,ys[i],ORANGE if active else '#aebccd',4 if active else 1.5)
for l,x in enumerate(xs):
    for i,y in enumerate(ys): node(s,x,y,i+1,ORANGE if i==l else BLUE)
text(s,460,350,'초기1 → 1층2 → 2층3 → 3층4 : 최소3단계',21,ORANGE)
text(s,460,378,'모든 Edge는 이전 층 → 다음 층. 옅은 선도 합법적인 연결이다.',17)
save(s,'efficient-layers.svg')

s=start(345); b=local_global_mask(); xs=[90,275,460,645,830]
text(s,460,27,'Causal Local + 중계3: 자기5쌍 + 아래6쌍 = 11쌍',21)
for i in range(5):
    for j in range(i):
        if b[i,j]:
            h=35+(i-j)*24
            color=ORANGE if j==2 or i==2 else BLUE
            s.append(f'<path d="M {xs[j]+12} 140 C {xs[j]+25} {140-h}, {xs[i]-25} {140-h}, {xs[i]-12} 140" fill="none" stroke="{color}" stroke-width="2.5" marker-end="url(#arrow)"/>')
for i,x in enumerate(xs): node(s,x,150,i+1,ORANGE if i==2 else BLUE)
text(s,460,194,'자기 Edge는 모두 포함. 중계3은 제공1·2·3만 읽는다.',17)
box(s,65,235,210,67,['초기 위치1'])
box(s,355,235,210,67,['1층 위치3'])
box(s,645,235,210,67,['2층 위치5'])
line(s,275,268,355,268,ORANGE,3);line(s,565,268,645,268,ORANGE,3)
text(s,460,331,'초기1의 정보는 중계를 거쳐 두 층에 도달할 수 있다.',17)
save(s,'efficient-global.svg')

s=start(360)
text(s,225,32,'직접 쌍별 Kernel',22);text(s,685,32,'같은 Kernel의 인자 분해',22)
box(s,55,65,340,90,['Q 특징 n×r / K 특징 n×r','W = ΦQ ΦK^T : n×n'])
box(s,55,200,340,120,['분모: 각 W 행의 합','분자: WV : n×d_v','같은 행 분모로 나누기'])
line(s,225,155,225,200)
box(s,515,65,340,90,['K 특징과 V를 먼저 결합','S = ΦK^T V : r×d_v'])
box(s,515,200,340,120,['z = 제공 특징의 합 : r','분자 ΦQ S / 분모 ΦQ z','반환 n×d_v'])
line(s,685,155,685,200)
text(s,460,348,'정확한 재배치는 이 특징 Kernel에 대한 등식이다.',18,ORANGE)
save(s,'efficient-factor.svg')

s=start(320)
box(s,30,40,240,92,['이전 상태 S_(i-1), z_(i-1)','현재까지 읽은 이전 항들'])
box(s,365,40,250,92,['현재 Key 특징 / Value','외적 r×d_v / 특징 r'])
box(s,300,175,320,95,['S_i, z_i에 현재 항 추가','제공 범위는1…i'])
line(s,150,132,335,175);line(s,490,132,490,175)
box(s,710,175,180,95,['현재 Query 특징','출력 o_i'])
line(s,620,215,710,215)
text(s,800,143,'현재 입력에서 생성',16)
text(s,460,304,'갱신 → 현재 요청 적용 → 다음 시점에 상태 전달',19,ORANGE)
save(s,'efficient-prefix.svg')

s=start(300)
text(s,460,29,'앞 요청 i=2: 합의 끝이 다르면 정보 접근도 다르다.',22)
for i,x in enumerate([110,285,460,635]): box(s,x,64,135,65,[f'위치{i+1}'])
box(s,120,200,250,65,['Prefix S₂,z₂: 제공1·2'])
box(s,550,200,270,65,['전체 S₄,z₄: 제공1·2·3·4'])
for x in [177,352]: line(s,x,129,245,200)
for x in [177,352,527,702]: line(s,x,129,685,200,ORANGE if x>400 else BLUE)
text(s,460,292,'오른쪽 상태에는 앞 요청의 미래3·4가 이미 들어 있다.',18,ORANGE)
save(s,'efficient-global-prefix.svg')

s=start(325)
for x,title,labels in [(25,'KV Cache',['과거 Q/K/V·Block 계산','과거 K/V 생성 재사용','새 Query의 과거 읽기는 남음']),
                        (330,'Sparse',['직접 제공 집합 J_i','선택한 Edge만 비교·집계','생략된 직접 연결 / 새 분모']),
                        (635,'Kernel',['특징 기반 가중합 정의','S,z로 제공 정보를 누적','같은 Kernel 재배치 / 대체 계수'])]:
    text(s,x+130,38,title,23)
    box(s,x,80,260,145,labels)
    text(s,x+130,258,'절감 지점과 보장 조건을 확인',16)
text(s,460,304,'Exact Kernel은 원 Dense 연산을 유지하는 구현 최적화다.',20,ORANGE)
save(s,'efficient-savings.svg')
print('실제 Mask와 shape에서 도해7개 생성 완료')
