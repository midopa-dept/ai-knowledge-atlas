"""본문의 작은 행렬과 합 축을 직접 제작한 SVG로 그린다."""
from html import escape
from pathlib import Path
root=Path(__file__).resolve().parent


def text(x,y,label,size=19,color='#1f2937',anchor='start'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{escape(label)}</text>'


def box(x,y,w,h,fill='#f1f5f9'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="#64748b"/>'


def save(name,w,h,parts):
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="100%" height="100%" fill="white"/><g font-family="NanumGothic, sans-serif">'+''.join(parts)+'</g></svg>'
    (root/name).write_text(svg+'\n')


parts=[text(30,30,'같은 비교 좌표를 곱하고 더한다',23),box(30,60,270,105),
       text(46,90,'둘째 질의 q = [0, 1]'),text(46,120,'셋째 키 k = [1, 1]'),
       text(46,148,'0 × 1 + 1 × 1 = 1'),text(332,124,'→',35),
       text(450,62,'제공 위치 j',18),text(469,91,'1',18,anchor='middle'),text(551,91,'2',18,anchor='middle'),text(633,91,'3',18,anchor='middle')]
for i,row in enumerate([[1,0,1],[0,1,1]]):
    parts.append(text(360,140+i*68,f'질의 {i+1}',17))
    for j,value in enumerate(row):
        x=435+82*j; y=108+68*i
        parts += [box(x,y,68,52,'#dbeafe' if (i,j)==(1,2) else '#f8fafc'),text(x+34,y+34,str(value),22,anchor='middle')]
parts += [text(30,270,'Q: 2 × 2    K: 3 × 2    K^T: 2 × 3    D: 2 × 3',20),
          text(30,307,'한 셀은 한 질의·키의 점수다. 값 좌표는 아직 사용하지 않는다.',18)]
save('dot-grid.svg',720,330,parts)

parts=[text(25,30,'비교에서 집계까지 — 같은 두 질의와 세 제공 위치',23)]
rows=[('D = QK^T','[1, 0, 1]','[0, 1, 1]','2 × 3'),
      ('S = D / √2','[0.707, 0, 0.707]','[0, 0.707, 0.707]','2 × 3'),
      ('A = 행별 Softmax','[0.401, 0.198, 0.401]','[0.198, 0.401, 0.401]','2 × 3'),
      ('O = AV','[1.604, 2.396]','[1.198, 3.209]','2 × 2')]
for i,(label,r1,r2,shape) in enumerate(rows):
    y=58+i*107
    parts += [box(25,y,680,84,'#eff6ff' if i==2 else '#f8fafc'),text(42,y+27,label,20),
              text(305,y+27,r1,18),text(305,y+57,r2,18),text(42,y+57,shape,17)]
    if i<3: parts.append(text(365,y+105,'↓',25,anchor='middle'))
parts += [text(25,506,'V = [[2, 0], [0, 4], [2, 4]]   (3 × 2)',20),
          text(25,541,'QK^T: 비교 좌표 합     AV: 제공 위치의 기여 합',19)]
save('scoring-flow.svg',730,565,parts)
print('직접 제작한 벡터 도해2개 생성')
