"""직접 제작 벡터 도해4: 두 배치·행별 LN·FFN·대표 첫 위치 trace."""
from pathlib import Path
from html import escape
R=Path(__file__).resolve().parent
B,O,I='#1d4ed8','#b45309','#172033'


def text(x,y,s,size=22,color=I):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">{escape(s)}</text>'


def box(x,y,w,h,lines,color=B):
    p=[f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{"#eff6ff" if color==B else "#fff7ed"}" stroke="{color}" stroke-width="2"/>']
    for k,s in enumerate(lines): p.append(text(x+15,y+28+k*28,s,21))
    return ''.join(p)


def arrow(x1,y1,x2,y2,color=B):
    return f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{color}" stroke-width="2.4" marker-end="url(#{"b" if color==B else "o"})"/>'


def path(points,color=O):
    return f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="2.4" marker-end="url(#{"b" if color==B else "o"})"/>'


def save(name,w,h,p):
    markers=''.join(f'<marker id="{key}" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="{c}"/></marker>' for key,c in [('b',B),('o',O)])
    s=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs>{markers}</defs><rect width="100%" height="100%" fill="white"/><g font-family="NanumGothic, sans-serif">'+''.join(p)+'</g></svg>'
    (R/name).write_text(s+'\n')

p=[text(25,32,'하위 함수가 읽는 가지와 기존 표현을 잇는 경로',26)]
for off,pre in [(0,False),(430,True)]:
    p+=[text(off+25,72,'Pre-LN' if pre else 'Post-LN',25),
        box(off+105,92,290,40,['입력 X: n × d']),arrow(off+250,132,off+250,158)]
    if pre:
        p+=[box(off+105,165,290,68,['LN₁(X) → MHA','M: n × d']),
            path(f'{off+105},112 {off+45},112 {off+45},268 {off+105},268'),
            text(off+12,200,'X',24,O),arrow(off+250,233,off+250,248),
            box(off+105,252,290,40,['첫 합 U = X + M'],O),arrow(off+250,292,off+250,318),
            box(off+105,325,290,68,['LN₂(U) → FFN','F: n × d']),
            path(f'{off+105},272 {off+45},272 {off+45},428 {off+105},428'),
            text(off+12,360,'U',24,O),arrow(off+250,393,off+250,411),
            box(off+105,415,290,40,['반환 Y = U + F'],O),
            text(off+25,494,'추가 최종 LN은 이 Block에 없다.',20)]
    else:
        p+=[box(off+105,165,290,68,['MHA(X)','M: n × d']),
            path(f'{off+105},112 {off+45},112 {off+45},268 {off+105},268'),
            text(off+12,200,'X',24,O),arrow(off+250,233,off+250,248),
            box(off+105,252,290,40,['첫 합 R₁ = X + M'],O),arrow(off+250,292,off+250,313),
            box(off+105,320,290,40,['LN₁(R₁) → U']),arrow(off+250,360,off+250,378),
            box(off+105,385,290,40,['FFN(U) → F']),
            path(f'{off+105},340 {off+45},340 {off+45},460 {off+105},460'),
            text(off+12,404,'U',24,O),arrow(off+250,425,off+250,442),
            box(off+105,448,290,40,['둘째 합 R₂ = U + F'],O),arrow(off+250,488,off+250,508),
            box(off+105,515,290,40,['LN₂(R₂) → 반환 Y'])]
p+=[text(25,602,'파랑: 하위 연산/정규화    주황: 기존 표현과 반환의 Residual 합',22)]
save('block-paths.svg',850,625,p)
p=[text(25,35,'한 위치의 세 좌표: [1,3,5]',27),
   box(25,65,790,65,['μ = 3,  중심화: [-2,0,2]','σ² = (4 + 0 + 4) / 3 = 8/3']),arrow(420,130,420,157),
   box(25,165,790,65,['ε = 1/3 → 분모 sqrt(8/3 + 1/3) = sqrt(3)','z = [-2/sqrt(3), 0, 2/sqrt(3)]']),arrow(420,230,420,256),
   box(25,264,790,65,['γ = [2,1,0.5],  β = [1,-1,2]','LN = [1-4/sqrt(3), -1, 2+1/sqrt(3)]'],O),
   text(25,369,'이 통계에는 다른 위치/다른 Batch의 좌표가 들어오지 않는다.',23),
   text(25,405,'z 분산 = 8/9   |   γ/β 이후 평균은 약 0.089316',23)]
save('block-ln.svg',840,430,p)
p=[text(25,35,'동일 매개변수 · 다른 입력 · 위치별 계산',27)]
for y,x,z,h,f in [(65,'[1,-1,2]','[3,-2.5,-2,1.5]','[3,0,0,1.5]','[0.85,-0.2,-0.45]'),(225,'[-1,2,0]','[-1,2.5,3,-3.5]','[0,2.5,3,0]','[1.6,-0.45,1.55]')]:
    p += [box(25,y,790,112,[f'x = {x} → z = x W₁ + b₁ = {z}',f'ReLU(z) = {h}',f'f = h W₂ + b₂ = {f}'])]
p += [text(25,400,'각 행: 3 → 4 → 3 특징 폭. 두 행 사이에는 직접 화살표가 없다.',22),text(25,440,'Batch 벡터화도 마지막 특징 축만 변환한다.',23)]
save('block-ffn.svg',840,465,p)
p=[text(25,35,'대표 첫 요청: 동일한 X와 매개변수, 다른 함수 입력',26)]
for off,rows,color in [(0,[('MHA 입력','[1,0,2]'),('MHA 반환','[1.666667,0.5,1.166667]'),('첫 합 R₁','[2.666667,0.5,3.166667]'),('U = LN₁(R₁)','[0.478234,-1.386877,0.908644]'),('FFN 반환','[0.110883,-0.2,0.289117]'),('둘째 합 R₂','[0.589117,-1.586877,1.197761]'),('Y = LN₂(R₂)','[0.435550,-1.378506,0.942956]')],B),
                       (430,[('MHA 입력 LN₁(X)','[0,-1.215661,1.215661]'),('MHA 반환','[0.607831,-0.138808,0.746638]'),('U = X + M','[1.607831,-0.138808,2.746638]'),('FFN 입력 LN₂(U)','[0.170137,-1.296561,1.126423]'),('FFN 반환','[0.264931,-0.2,0.135069]'),('반환은 U에 더한다','Y = U + F'),('Y (추가 LN 없음)','[1.872762,-0.338808,2.881707]')],O)]:
    p.append(text(off+25,75,'Post-LN' if off==0 else 'Pre-LN',25,color))
    for i,(label,value) in enumerate(rows):
        y=95+i*88
        p.append(box(off+15,y,410,65,[label,value],color))
        if i<6: p.append(arrow(off+220,y+65,off+220,y+82,color))
p.append(text(25,743,'Pre의 FFN 입력 LN₂(U)는 합산 경로 U를 대체하지 않는다.',23))
save('block-trace.svg',860,765,p)
print('Block 경로·LN·FFN·대표 trace 도해4 생성')
