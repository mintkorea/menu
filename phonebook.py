import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="보안팀 통합 연락망", layout="wide")

# 1. 28명 전체 데이터 규격화 (수기 도면 기준)
# 각 조당 8명(2행)씩 배치되도록 리스트를 구성했습니다.
security_team = [
    # [지휘부] 4명 (1행)
    {"group": "top", "pos": "소장", "name": "이규용", "tel": "010-8883-6580", "birth": "1972.03.01", "entry": "-"},
    {"group": "top", "pos": "부소장", "name": "박상현", "tel": "010-3193-4603", "birth": "1988.07.31", "entry": "-"},
    {"group": "top", "pos": "반장", "name": "유정수", "tel": "010-5316-8065", "birth": "1970.09.25", "entry": "2020.09.01"},
    {"group": "top", "pos": "반장", "name": "오제준", "tel": "010-3352-8933", "birth": "-", "entry": "-"},
    
    # [A조] 8명 (2행)
    {"group": "a", "pos": "A장", "name": "배준용", "tel": "010-4717-7065", "birth": "1969.12.24", "entry": "2022.07.26"},
    {"group": "a", "pos": "A원", "name": "이명구", "tel": "010-8638-5819", "birth": "1964.09.15", "entry": "2025.03.21"},
    {"group": "a", "pos": "A원", "name": "김영중", "tel": "010-7726-5963", "birth": "1959.02.26", "entry": "2024.08.21"},
    {"group": "a", "pos": "A원", "name": "김삼동", "tel": "010-8081-XXXX", "birth": "-", "entry": "-"},
    {"group": "a", "pos": "A장", "name": "손병휘", "tel": "010-9966-2090", "birth": "-", "entry": "-"},
    {"group": "a", "pos": "A원", "name": "권순호", "tel": "010-2539-1799", "birth": "-", "entry": "-"},
    {"group": "a", "pos": "A원", "name": "김전식", "tel": "010-XXXX-XXXX", "birth": "-", "entry": "-"},
    {"group": "a", "pos": "A원", "name": "보안요원", "tel": "010-0000-0000", "birth": "-", "entry": "-"},
    
    # [B조] 8명 (2행)
    {"group": "b", "pos": "B장", "name": "심규천", "tel": "010-8287-9895", "birth": "-", "entry": "-"},
    {"group": "b", "pos": "B원", "name": "임종현", "tel": "010-7741-6732", "birth": "-", "entry": "-"},
    {"group": "b", "pos": "B원", "name": "황일범", "tel": "010-8929-4294", "birth": "-", "entry": "-"},
    {"group": "b", "pos": "B원", "name": "이상길", "tel": "010-9904-0247", "birth": "-", "entry": "-"},
    {"group": "b", "pos": "B원", "name": "요원1", "tel": "-", "birth": "-", "entry": "-"},
    {"group": "b", "pos": "B원", "name": "요원2", "tel": "-", "birth": "-", "entry": "-"},
    {"group": "b", "pos": "B원", "name": "요원3", "tel": "-", "birth": "-", "entry": "-"},
    {"group": "b", "pos": "B원", "name": "요원4", "tel": "-", "birth": "-", "entry": "-"},

    # [C조] 4명 (1행)
    {"group": "c", "pos": "C장", "name": "김태언", "tel": "010-XXXX-XXXX", "birth": "-", "entry": "1순위"},
    {"group": "c", "pos": "C원", "name": "이태원", "tel": "010-XXXX-XXXX", "birth": "-", "entry": "2순위"},
    {"group": "c", "pos": "C원", "name": "이정석", "tel": "010-XXXX-XXXX", "birth": "-", "entry": "3순위"},
    {"group": "c", "pos": "C원", "name": "보안요원", "tel": "-", "birth": "-", "entry": "-"},
    
    # [기숙사] 4명 (1행)
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
    body {{ font-family: sans-serif; margin: 0; padding: 10px; background-color: #fff; }}
    .grid-container {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 6px;
    }}
    .node {{
        height: 48px; border-radius: 8px; display: flex; flex-direction: column;
        align-items: center; justify-content: center; cursor: pointer;
        border: 1px solid rgba(0,0,0,0.1); box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
    /* 조별 색상 테마 */
    .top  {{ background-color: #f8f9fa; color: #495057; border-color: #dee2e6; }}
    .a    {{ background-color: #e7f5ff; color: #1971c2; border-color: #a5d8ff; }}
    .b    {{ background-color: #f3f0ff; color: #6f2dbd; border-color: #d0bfff; }}
    .c    {{ background-color: #fff4e6; color: #d9480f; border-color: #ffd8a8; }}
    .dorm {{ background-color: #ebfbee; color: #2b8a3e; border-color: #b2f2bb; }}
    
    .pos {{ font-size: 10px; opacity: 0.8; margin-bottom: 2px; }}
    .name {{ font-size: 15px; font-weight: bold; }}

    .info-panel {{
        grid-column: span 4; display: none;
        background: #fff; border: 2px solid #28a745; border-radius: 12px;
        padding: 15px; margin: 10px 0; text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.12);
    }}
    .call-btn {{
        display: block; background: #28a745; color: white;
        text-decoration: none; padding: 12px; border-radius: 8px;
        font-weight: bold; font-size: 17px; margin: 12px 0;
    }}
</style>
</head>
<body>

<div class="grid-container">
"""

for i, m in enumerate(security_team):
    html_code += f"""
    <div class="node {m['group']}" onclick="togglePanel('p{i//4}', '{m['name']}', '{m['pos']}', '{m['tel']}', '{m['birth']}', '{m['entry']}')">
        <span class="pos">{m['pos']}</span>
        <span class="name">{m['name']}</span>
    </div>
    """
    if (i + 1) % 4 == 0 or (i + 1) == len(security_team):
        html_code += f'<div id="p{i//4}" class="info-panel"></div>'

html_code += """
</div>

<script>
    let currentActive = null;
    function togglePanel(id, name, pos, tel, birth, entry) {
        const p = document.getElementById(id);
        if(currentActive && currentActive !== p) currentActive.style.display = 'none';

        if(p.style.display === 'block' && p.dataset.user === name) {
            p.style.display = 'none';
        } else {
            p.innerHTML = `
                <div style="font-size:20px; font-weight:bold;">${name} <small>(${pos})</small></div>
                <div style="margin: 10px 0; font-size:14px; color:#555;">
                    🎂 생일: ${birth} | 📅 입사: ${entry}
                </div>
                <a href="tel:${tel}" class="call-btn">📞 전화 연결</a>
                <div style="color:#999; font-size:12px;" onclick="this.parentElement.style.display='none'">닫기</div>
            `;
            p.style.display = 'block';
            p.dataset.user = name;
            currentActive = p;
            p.scrollIntoView({behavior:'smooth', block:'center'});
        }
    }
</script>
</body>
</html>
"""

components.html(html_code, height=1000, scrolling=True)
