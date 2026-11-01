"""Q/K 비교와 V 전달을 분리한 직접 제작 벡터 도해."""
from pathlib import Path

out = Path(__file__).resolve().parent / 'figures/qkv-roles.svg'
svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="540" viewBox="0 0 1100 540">
<defs><marker id="a" markerWidth="9" markerHeight="9" refX="8" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8" fill="none" stroke="#334155"/></marker></defs>
<rect width="1100" height="540" fill="white"/>
<g font-family="NanumGothic, sans-serif" fill="#172033" text-anchor="middle">
<text x="550" y="34" font-size="26">비교에서 비율을, 값에서 전달할 내용을 얻는다</text>
<g fill="#f4f7fb" stroke="#65748b" stroke-width="1.5">
<rect x="20" y="80" width="235" height="80" rx="6"/>
<rect x="300" y="80" width="340" height="80" rx="6"/>
<rect x="715" y="80" width="365" height="80" rx="6"/>
<rect x="275" y="250" width="390" height="90" rx="6"/>
<rect x="335" y="425" width="620" height="80" rx="6" fill="#eef4ed"/>
</g>
<g font-size="22">
<text x="137" y="110">받는 위치의 Q</text><text x="137" y="143">질의 q_1, q_2</text>
<text x="470" y="110">제공 위치의 K</text><text x="470" y="143">키 k_1, k_2, k_3</text>
<text x="897" y="110">같은 제공 위치의 V</text><text x="897" y="143">[2,0], [0,4], [2,4]</text>
<text x="470" y="280">비교 점수 → 행별 비율 A</text>
<text x="470" y="314">[0.2,0.6,0.2] / [0.2,0.2,0.6]</text>
<text x="645" y="455">같은 출처끼리 곱해 더하기 O = AV</text>
<text x="645" y="489">o_1 = [0.8,3.2] / o_2 = [1.6,3.2]</text>
</g>
<g fill="none" stroke="#334155" stroke-width="2" marker-end="url(#a)">
<path d="M137 160 L345 245"/><path d="M470 160 L470 245"/>
<path d="M470 340 L520 420"/><path d="M897 160 L897 420"/>
</g>
<text x="530" y="389" font-size="19">位置별 비율</text>
<text x="975" y="280" font-size="19">내용 전달</text>
<text x="897" y="360" font-size="18">키와 같은 행 순서</text>
</g></svg>'''
out.write_text(svg.replace('位置', '위치'))

# 예제의 실제 좌표를 같은 선형 축에 배치한다. 증명을 대신하는 자료가 아니다.
origin_x, origin_y, scale = 100, 410, 150
def point(x, y):
    return f'{origin_x + scale*x:g},{origin_y - scale*y:g}'

triangle = ' '.join(point(x,y) for x,y in [(0,0),(2,0),(0,2)])
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="490" viewBox="0 0 900 490"
data-origin="100,410" data-scale="150" data-inputs="0,0;2,0;0,2"
data-feasible="0.5,1" data-infeasible="1.5,1.5">
<defs><marker id="axis" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0 0 L6 3 L0 6" fill="none" stroke="#334155"/></marker></defs>
<rect width="900" height="490" fill="white"/>
<g font-family="NanumGothic, sans-serif" fill="#172033">
<text x="450" y="32" font-size="25" text-anchor="middle">좌표별 범위보다 작은 볼록결합의 영역</text>
<rect x="100" y="110" width="300" height="300" fill="#f5f7fa" stroke="#64748b" stroke-width="1.5" stroke-dasharray="6 5"/>
<polygon points="{triangle}" fill="#d6e9df" stroke="#27634e" stroke-width="2"/>
<g stroke="#334155" stroke-width="1.5" fill="none" marker-end="url(#axis)">
<path d="M70 410 L435 410"/><path d="M100 440 L100 70"/>
</g>
<g font-size="21">
<text x="437" y="418">x</text><text x="88" y="73">y</text>
<text x="83" y="432">0</text><text x="242" y="438">1</text><text x="393" y="438">2</text>
<text x="75" y="267">1</text><text x="75" y="117">2</text>
<text x="40" y="474">v₁=(0,0)</text><text x="313" y="474">v₂=(2,0)</text>
<text x="115" y="93">v₃=(0,2)</text>
</g>
<g stroke="#334155" stroke-width="1.5"><path d="M250 406 V414"/><path d="M96 260 H104"/></g>
<g fill="#27634e"><circle cx="100" cy="410" r="5"/><circle cx="400" cy="410" r="5"/><circle cx="100" cy="110" r="5"/></g>
<circle cx="175" cy="260" r="6" fill="#1457a6" data-value="0.5,1"/>
<text x="187" y="280" font-size="21" fill="#1457a6">(0.5, 1)</text>
<g stroke="#a53636" stroke-width="3" data-value="1.5,1.5"><path d="M318 178 L332 192 M318 192 L332 178"/></g>
<text x="328" y="165" font-size="21" fill="#a53636">(1.5, 1.5)</text>
<g font-size="21">
<rect x="477" y="87" width="395" height="102" rx="5" fill="#eaf3ed"/>
<text x="492" y="118">도달 가능한 영역: 삼각형 내부·경계</text>
<text x="492" y="151">x ≥ 0, y ≥ 0, x + y ≤ 2</text>
<text x="492" y="179" font-size="18">비음수 가중치의 합이 1인 집계</text>
<text x="492" y="223">점선 정사각형: 좌표별 범위</text>
<text x="492" y="253">0 ≤ x ≤ 2, 0 ≤ y ≤ 2</text>
<text x="492" y="310" fill="#1457a6">● (0.5, 1): 도달 가능</text>
<text x="492" y="340" font-size="19">비율 (0.25, 0.25, 0.5)</text>
<text x="492" y="391" fill="#a53636">× (1.5, 1.5): 도달 불가능</text>
<text x="492" y="421" font-size="19">x + y = 3 &gt; 2, 첫 비율이 -0.5</text>
</g>
</g></svg>'''
(out.parent / 'convex-region.svg').write_text(svg)
