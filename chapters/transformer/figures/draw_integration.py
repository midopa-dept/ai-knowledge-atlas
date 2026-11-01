"""직접 제작한 학습 도해. 논문 그림 복제가 아니라 본문의 계산 계약을 그린다."""
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parent


def diagram(name, title, boxes, arrows, notes):
    parts=['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="450" viewBox="0 0 900 450">',
           '<defs><marker id="arrow" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><path d="M0,0 L9,3.5 L0,7" fill="#445566"/></marker></defs>',
           '<rect width="900" height="450" fill="white"/>']
    def text(x,y,value,size=18):
        parts.append(f'<text x="{x}" y="{y}" font-family="NanumGothic" font-size="{size}" text-anchor="middle" fill="#152738">{escape(value)}</text>')
    text(450,33,title,22)
    for x,y,w,h,lines in boxes:
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#eff6ff" stroke="#7499ba" stroke-width="2"/>')
        for i,line in enumerate(lines):text(x+w/2,y+29+i*25,line)
    for x1,y1,x2,y2,label in arrows:
        parts.append(f'<path d="M{x1},{y1} L{x2},{y2}" stroke="#445566" stroke-width="2" fill="none" marker-end="url(#arrow)"/>')
        if label:text((x1+x2)/2,(y1+y2)/2-8,label,16)
    for i,line in enumerate(notes):text(450,398+i*25,line,17)
    parts.append('</svg>')
    (ROOT/name).write_text('\n'.join(parts)+'\n')


def run():
    diagram('integration-flow.svg','완성 조건과 출력 Prefix가 만나는 계산',
      [(20,80,200,80,['조건 ID [0,1,2]','Embedding + Position']),
       (310,80,210,80,['양방향 Self Block','Encoder E: 3×3']),
       (20,240,200,80,['출력 ID [BOS,A]','Embedding + Position']),
       (310,240,210,80,['Causal Self + 합/LN','요청 H: 2×3']),
       (650,220,220,100,['Cross + 합/LN + FFN','최종 Y: 2×3','Logit: 2×3 → 선택'])],
      [(220,120,310,120,''),(220,280,310,280,''),(520,280,650,280,'Q'),(520,120,730,220,'E에서 K/V')],
      ['Self의 Q/K/V는 같은 집합, Cross의 Q와 K/V는 다른 집합','조건의 뒤쪽은 이미 제공됨 / 출력의 미래는 금지됨'])
    diagram('integration-cache.svg','선택한 토큰과 처리한 위치를 구별하기',
      [(25,80,245,105,['Prefill: [0,1]','층1/2 각각 K/V','1×2Head×2위치×4']),
       (335,80,235,105,['마지막 Logit → 선택2','Cache는 아직 위치0·1','새 위치2는 처리 전']),
       (640,80,235,105,['입력2 + Position[2]','새 Q/K/V 계산','과거에 새 위치 Append']),
       (335,255,235,85,['첫 블록의 새 반환','둘째 레이어의 입력']),
       (640,255,235,85,['둘째 레이어 새 K/V','Logit → 다음 선택3'])],
      [(270,130,335,130,''),(570,130,640,130,''),(750,185,452,255,''),(570,300,640,300,'')],
      ['둘째 레이어는 첫 레이어 K/V를 복사하지 않음','Full/Incremental은 같은 Token·원위치·모델·Causal 조건에서 비교'])
    diagram('integration-efficiency.svg','비용을 줄이는 서로 다른 세 지점',
      [(25,90,250,190,['KV Cache','과거 표현/투영 재계산 감소','원 Full 계수 정의 유지','새 Query의 과거 읽기 유지']),
       (325,90,250,190,['Local Causal','허용15쌍 → 9쌍','먼 직접 연결6개 생략','남긴 열의 Softmax 재정규화']),
       (625,90,250,190,['별도 특징 Kernel','과거 제공 집합 유지','계수 정의 변경','직접 합 = S/z 인자 합'])],[],
      ['Full / Local / Kernel의 출력은 이 실험에서 서로 다름','좌표 곱셈 셈과 CPU/GPU 시간·모델 성능은 별도 검증'])


if __name__=='__main__':
    run()
