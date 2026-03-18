import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="보안 통합 연락망", layout="wide")

# 데이터 구성 (수기 도면의 좌우 배치 로직 적용)
# 순서: [왼쪽1, 왼쪽2, 오른쪽1, 오른쪽2] 순으로 한 행이 구성됨
security_data = [
    # 1행: 지휘부 (반장-소장-부소장-반장 배치)
    {"group": "top", "pos": "반장(회관)", "name": "유정수", "tel": "010-5316-8065", "birth": "1970.09.25", "entry": "2020.09.01"},
    {"group": "top", "pos": "소장", "name": "이규용", "tel": "010-8883-6580", "birth": "1972.03.01", "entry": "-"},
    {"group": "top", "pos": "부소장", "name": "박상현", "tel": "010-3193-4603", "birth": "1988.07.31", "entry": "-"},
    {"group": "top", "pos": "반장(옴니)", "name": "오제준", "tel": "010-3352-8933", "birth": "-", "entry": "-"},
    
    # 2~3행: A조 (좌: 회관A / 우: 옴니A)
    {"group": "a", "pos": "A장(회관)", "name": "배준용", "tel": "010-4717-7065", "birth": "1969.12.24", "entry": "2022.07.26"},
    {"group": "a", "pos": "A원(회관)", "name": "이명구", "tel": "010-8638-5819", "birth": "1964.09.15", "entry": "2025.03.21"},
    {"group": "a", "pos": "A장(옴니)", "name": "손병휘", "tel": "010-9966-2090", "birth": "-", "entry": "-"},
    {"group": "a", "pos": "A원(옴니)", "name": "권순호", "tel": "010-2539-1799", "birth": "-", "entry": "-"},
    {"group": "a", "pos": "A원(회관)", "name": "김영중", "tel": "010-7726-5963", "birth": "1959.02.26", "entry": "2024.08.21"},
    {"group": "a", "pos": "A원(회관)", "name": "김삼동", "tel": "010-8081-XXXX", "birth": "-", "entry": "-"},
    {"group": "a", "pos": "A원(옴니)", "name": "김전식", "tel": "-", "birth": "-", "entry": "-"},
    {"group": "a", "pos": "A원(옴니)", "name": "-", "tel": "-", "birth": "-", "entry": "-"},

    # 4~5행: B조 (좌: 회관B / 우: 옴니B)
    {"group": "b", "pos": "B장(회관)", "name": "심규천", "tel": "010-8287-9895", "birth": "-", "entry": "-"},
    {"group": "b", "pos": "B원(회관)", "name": "임종현", "tel": "010-7741-6732", "birth": "-", "entry": "-"},
    {"group": "b", "pos": "B장(옴니)", "name": "황일범", "tel": "010-8929-4294", "birth": "-", "entry": "-"},
    {"group": "b", "pos": "B원(옴니)", "name": "이상길", "tel": "010-9904-0247", "birth": "-", "entry": "-"},
    {"group": "b", "pos": "B원(회관)", "name": "요원1", "tel": "-", "birth": "-", "entry": "-"},
    {"group": "b", "pos": "B원(회관)", "name": "요원2", "tel": "-", "birth": "-", "entry": "-"},
    {"group": "b", "pos": "B원(옴니)", "name": "요원3", "tel": "-", "birth": "-", "entry": "-"},
    {"group": "b", "pos": "B원(옴니)", "name": "-", "tel": "-", "birth": "-", "entry": "-"},

    # 6행: C조 (좌: 회관C / 우: 옴니C)
    {"group": "c", "pos": "C장(회관)", "name": "김태언", "tel": "-", "birth": "-", "entry": "1순위"},
    {"group": "c", "pos": "C원(회관)", "name": "이태원", "tel": "-", "birth": "-", "entry": "2순위"},
    {"group": "c", "pos": "C원(옴니)", "name": "이정석", "tel": "-", "birth": "-", "entry": "3순위"},
    {"group": "c", "pos": "C원(옴니)", "name": "-", "tel": "-", "birth": "-", "entry": "-"},

    # 7행: 기숙사
    {"group": "dorm", "pos": "기숙사", "name": "요원A", "tel": "-", "birth": "-", "entry": "-"},
    {"group": "dorm", "pos": "기숙사", "name": "요원B", "tel": "-", "birth": "-", "entry": "-"},
    {"group": "dorm", "pos": "기숙사", "name": "요원C", "tel": "-", "birth": "-", "entry": "-"},
    {"group": "dorm", "pos": "기숙사", "name": "요원D", "tel": "-", "birth": "-", "entry": "-"},
]

html_code = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
    body {{ font-family: sans-serif; margin: 0; padding: 5px; }}
    .main-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 4px; padding-bottom: 60px; }}
    .node {{
        height: 42px; border-radius: 5px; display: flex; flex-direction: column;
        align-items: center; justify-content: center; border: 1px solid #ddd;
    }}
    /* 구역 구분선 (가운데 세로선 효과) */
    .node:nth-child(4n-2) {{ border-right: 2px solid #aaa; }} 
    
    .top {{ background-color: #f1f3f5; color: #333; }}
    .a   {{ background-color: #e7f5ff; color: #007bff; }}
    .b   {{ background-color: #f3f0ff; color: #845ef7; }}
    .c   {{ background-color: #fff4e6; color: #fd7e14; }}
    .dorm {{ background-color: #ebfbee; color: #2b8a3e; }}
    
    .pos {{ font-size: 8px; opacity: 0.7; }}
    .name {{ font-size: 13px; font-weight: bold; }}

    .info-panel {{
        grid-column: span 4; display: none; background: #fff; border: 2px solid #28a745;
        border-radius: 10px; padding: 10px; margin: 5px 0; text-align: center;
    }}
    .footer-bar {{
        position: fixed; bottom: 0; left: 0; width: 100%; background: #eee;
        display: flex; height: 50px; border-top: 1px solid #ccc;
    }}
    .footer-item {{ flex: 1; display: flex; align-items: center; justify-content: center; font-size: 12px; border-right: 1px solid #ddd; }}
</style>
</head>
<body>
<div class="main-grid">
"""

for i, m in enumerate(security_data):
    html_code += f"""
    <div class="node {m['group']}" onclick="show('p{i//4}', '{m['name']}', '{m['pos']}', '{m['tel']}', '{m['birth']}', '{m['entry']}')">
        <span class="pos">{m['pos']}</span>
        <span class="name">{m['name']}</span>
    </div>
    """
    if (i + 1) % 4 == 0:
        html_code += f'<div id="p{i//4}" class="info-panel"></div>'

html_code += """
</div>
<div class="footer-bar">
    <div class="footer-item">회관</div><div class="footer-item">의산연</div>
    <div class="footer-item">옴니</div><div class="footer-item">기숙사</div>
</div>
<script>
    function show(id, n, p, t, b, e) {
        const el = document.getElementById(id);
        if(n === '-') return;
        el.innerHTML = `<b>${n}</b> (${p})<br>🎂 ${b} | 📅 ${e}<br>
                        <a href="tel:${t}" style="display:block; background:#28a745; color:#fff; padding:8px; margin-top:5px; border-radius:5px; text-decoration:none;">📞 전화걸기</a>`;
        el.style.display = el.style.display === 'block' ? 'none' : 'block';
    }
</script>
</body></html>
"""

components.html(html_code, height=900, scrolling=True)
