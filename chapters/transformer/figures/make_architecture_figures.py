"""독자용 정보 접근·이동·두 출처·대안·누출 벡터 도해5."""
from pathlib import Path
from html import escape
R=Path(__file__).resolve().parent
B,O,I='#1d4ed8','#b45309','#172033'


def text(x,y,s,size=22,color=I):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">{escape(s)}</text>'


def box(x,y,w,h,lines,color=B):
    out=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{"#eff6ff" if color==B else "#fff7ed"}" stroke="{color}" stroke-width="2"/>'
    for k,s in enumerate(lines):out+=text(x+12,y+29+k*28,s,21)
    return out


def arrow(x1,y1,x2,y2,color=B):
    return f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{color}" stroke-width="2.5" fill="none" marker-end="url(#{"b" if color==B else "o"})"/>'


def save(name,w,h,p):
    markers=''.join(f'<marker id="{key}" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="{c}"/></marker>' for key,c in [('b',B),('o',O)])
    (R/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs>{markers}</defs><rect width="100%" height="100%" fill="white"/><g font-family="NanumGothic, sans-serif">'+''.join(p)+'</g></svg>\n')

p=[text(25,35,'같은 집합의 앞뒤 / 같은 집합의 현재·과거 / 별도 제공자',25)]
for off,name,grid,rows,cols in [(0,'Encoder Self',[[1]*3]*3,['x1','x2','x3'],['x1','x2','x3']),
                               (285,'Decoder Self',[[1,0,0],[1,1,0],[1,1,1]],['BOS','y1','y2'],['BOS','y1','y2']),
                               (570,'Decoder Cross',[[1]*3]*2,['BOS','y1'],['E1','E2','E3'])]:
    p.append(text(off+25,80,name,24))
    for j,s in enumerate(cols):p.append(text(off+85+j*60,118,s,18))
    for i,row in enumerate(grid):
        p.append(text(off+20,159+i*60,rows[i],18))
        for j,b in enumerate(row):
            p.append(f'<rect x="{off+75+j*60}" y="{135+i*60}" width="52" height="52" fill="{"#bfdbfe" if b else "#f1f5f9"}" stroke="#64748b"/>')
            p.append(text(off+94+j*60,169+i*60,str(b),23))
    p.append(text(off+25,355,f'{len(rows)}要求 × {len(cols)}提供'.replace('要求','요청').replace('提供','제공'),21))
p += [text(25,404,'1 / True = 허용   |   0 / False = 금지   |   패딩은 별도로 제외',23),text(25,444,'Cross의 원문 열 번호는 Decoder의 출력 시간이 아니다.',23,O)]
save('architectures-masks.svg',855,470,p)
p=[text(25,35,'입력은 알려진 토큰, Target는 다음 정답',26)]
for i,(inp,tar,allowed) in enumerate([('BOS','y1','BOS'),('y1','y2','BOS, y1'),('y2','y3','BOS, y1, y2')]):
    x=25+i*285
    p += [box(x,75,255,66,[f'입력 행 {i}: {inp}',f'허용: {allowed}']),arrow(x+125,141,x+125,177),
          box(x,185,255,70,[f'반환 행 {i}',f'Target: {tar}'],O)]
p += [text(25,305,'행1은 입력 y1을 읽고 y2를 예측한다.',24),text(25,343,'입력 행2의 y2 → 행1은 금지. 대각선 y1 → 행1은 허용.',22,O)]
save('architectures-shift.svg',860,375,p)
p=[text(25,35,'완성 원문3행과 생성 Prefix2행의 두 경로',26),
   box(25,75,350,70,['원문 Token → 내용 C + 위치 P','Encoder 입력 Z: 3 × 3']),arrow(200,145,200,180),
   box(25,188,350,70,['Bidirectional Self → 합/LN/FFN','Encoder 반환 E: 3 × 3']),arrow(200,258,200,295),
   box(25,303,350,70,['K = E W_K : 3 × 2','V = E W_V : 3 × 2']),
   box(485,75,350,70,['입력 [BOS, y1] → D: 2 × 3','Target [y1, y2]는 감독']),arrow(660,145,660,180),
   box(485,188,350,70,['Causal Self Q/K/V ← D','합/LN → H: 2 × 3']),arrow(660,258,660,295),
   box(485,303,350,70,['Q = H W_Q : 2 × 2','요청은 Decoder의 두 행']),
   arrow(200,373,200,420),arrow(660,373,660,420),
   box(25,428,810,70,['Cross S/A: 2 × 3 → O: 2 × 2 → M: 2 × 3','제공3행의 집계 → 요청2행으로 반환'],O),arrow(430,498,430,530),
   box(25,538,810,70,['H + M → LN → U → FFN → 합/LN → Y: 2 × 3','마지막 Y행의 Token 점수는 다음 y2를 예측한다.'],O)]
save('architectures-flow.svg',860,638,p)
p=[text(25,35,'조건부 생성: 둘 다 유효할 수 있지만 출처 경로는 다르다.',26),
   box(25,75,810,70,['Decoder-only: [지시, x1, x2, x3, SEP, BOS, y1]','하나의 스택: Self Q/K/V ← 같은 시퀀스']),arrow(430,145,430,175),
   box(25,183,810,65,['마지막 y1 요청은 앞의 조건 전체 + 출력 Prefix를 읽는다.','기본 Causal에서는 x1의 표현이 x2/x3를 읽지 못한다.'],O),
   box(25,303,350,70,['Encoder: [x1, x2, x3]','각 E행은 완성 조건 전체 접근']),
   box(485,303,350,70,['Decoder: [BOS, y1]','Self는 Causal Prefix 접근']),
   arrow(200,373,200,407),arrow(660,373,660,407),
   box(25,415,810,70,['Cross K/V ← E, Q ← Decoder Self 이후 H','Decoder 마지막 행에서 다음 Token 예측'],O),
   text(25,530,'같은 과제 수행 가능성은 같은 내부 표현/비용/성능의 보장이 아니다.',23)]
save('architectures-options.svg',860,557,p)
p=[text(25,35,'금지 열 차단 뒤에도 남을 수 있는 입력 생성 우회 경로',26),
   box(25,75,810,66,['미래 입력 D2 → 전체 평균(D0,D1,D2)','전체 평균을 초기 D0에 더하면 이미 미래를 포함한다.'],O),arrow(430,141,430,173,O),
   box(25,181,810,66,['오염된 초기 행0 → Q/K/V 또는 Residual 직접 경로','Causal Mask가 키 열2를 막아도 자기 행0의 오염은 남는다.'],O),arrow(430,247,430,277,O),
   box(25,285,810,42,['행별 후속 함수 → 예측 Y0에 금지 정보 도달 가능'],O),
   box(25,376,810,66,['다른 경로: 미래 원문2 → 전체 Encoder → E0','Cross가 E0만 읽어도 그 E0가 미래를 포함할 수 있다.'],O),
   text(25,490,'수정: 초기 표현/조건 제공자의 의존성부터 가용 정보 안으로 제한',23,B),
   text(25,530,'검사: 미래 변경 불변 + 허용 과거/조건 변경의 양성 대조',23,B)]
save('architectures-leak.svg',860,557,p)
print('접근·이동·두 경로·조건 대안·누출 도해5 생성')
