import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="보안팀 통합 연락망", layout="wide")

# 데이터 정의 (기존 대화 내용 기반 추출 및 예시 포함)
# 실제 데이터로 아래 리스트를 보완하여 사용하세요.
staff_data = [
    {"group": "top", "pos": "소장", "name": "이규용", "tel": "010-8883-6580", "birth": "1972.03.01", "entry": "-"},
    {"group": "top", "pos": "부소장", "name": "박상현", "tel": "010-3193-4603", "birth": "1988.07.31", "entry": "-"},
    {"group": "top", "pos": "반장", "name": "유정수", "tel": "010-5316-8065", "birth": "1970.09.25", "entry": "2020.09.01"},
    {"group": "top", "pos": "반장", "name": "오제준", "tel": "010-3352-8933", "birth": "-", "entry": "-"},
    
    {"group": "a", "pos": "A장", "name": "배준용", "tel": "010-4717-7065", "birth": "1969.12.24", "entry": "2022.07.26"},
    {"group": "a", "pos": "A원", "name": "이명구", "tel": "010-8638-5819", "birth": "1964.09.15", "entry": "2025.03.21"},
    {"group": "a", "pos": "A장", "name": "손병휘", "tel": "010-9966-2090", "birth": "-", "entry": "-"},
    {"group": "a", "pos": "A원", "name": "권순호", "tel": "010-2539-1799", "birth": "-", "entry": "-"},
    
    {"group": "b", "pos": "B장", "name": "심규천", "tel": "010-8287-9895", "birth": "-", "entry": "-"},
    {"group": "b", "pos": "B원", "name": "임종현", "tel": "010-7741-6732", "birth": "-", "entry": "-"},
    {"group": "b", "pos": "B장", "name": "황일범", "tel": "010-8929-4294", "birth": "-", "entry": "-"},
    {"group": "b", "pos": "B원", "name": "이상길", "tel": "010-9904-0247", "birth": "-", "entry": "-"},
    
    {"group": "c", "pos": "C장", "name": "김태언", "tel": "010-XXXX-XXXX", "birth": "-", "entry": "1순위"},
    {"group": "c", "pos": "C원", "name": "이태원", "tel": "010-XXXX-XXXX", "birth": "-", "entry": "2순위"},
    {"group": "c", "pos": "C원", "name": "이정석", "tel": "010-XXXX-XXXX", "birth": "-", "entry": "3순위"},
    # ... 나머지 인원 추가 가능
]

html_code = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
    body {{ font-family: sans-serif; margin: 0; padding: 5px; background-color: #fff; }}
    .grid-container {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 3px;
    }}
    .node {{
        height: 40px; border-radius: 4px; display: flex; flex-direction: column;
        align-items: center; justify-content: center; cursor: pointer;
        border: 1px solid rgba(0,0,0,0.08); transition: 0.2s;
    }}
    .node:active {{ transform: scale(0.95); opacity: 0.7; }}
    
    /* 조별 색상 구분 */
    .top {{ background-color: #f1f3f5; color: #495057; }} /* 지휘부: 회색 */
    .a   {{ background-color: #e7f5ff; color: #1971c2; }} /* A조: 파랑 */
    .b   {{ background-color: #f3f0ff; color: #6f2dbd; }} /* B조: 보라 */
    .c   {{ background-color: #fff4e6; color: #d9480f; }} /* C조: 주황 */
    
    .node .pos {{ font-size: 8px; font-weight: normal; margin-bottom: 1px; opacity: 0.8; }}
    .node .name {{ font-size: 13px; font-weight: bold; }}

    .info-panel {{
        grid-column: span 4; display: none;
        background: #f8f9fa; border: 2px solid #28a745; border-radius: 10px;
        padding: 15px; margin: 5px 0; text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }}
    .call-btn {{
        display: block; background: #28a745; color: white;
        text-decoration: none; padding: 12px; border-radius: 8px;
        font-weight: bold; font-size: 16px; margin: 10px 0;
    }}
    .extra-info {{ font-size: 13px; color: #555; line-height: 1.6; border-top: 1px solid #eee; pt: 8px; }}
</style>
</head>
<body>

<div class="grid-container">
"""

# HTML에 노드 추가 (4개 단위로 패널 자동 삽입)
for i, member in enumerate(staff_data):
    html_code += f"""
    <div class="node {member['group']}" onclick="toggle('p{i//4}', '{member['name']}', '{member['pos']}', '{member['tel']}', '{member['birth']}', '{member['entry']}')">
        <span class="pos">{member['pos']}</span>
        <span class="name">{member['name']}</span>
    </div>
    """
    # 4개마다 또는 마지막에 정보 패널 삽입
    if (i + 1) % 4 == 0 or (i + 1) == len(staff_data):
        html_code += f'<div id="p{i//4}" class="info-panel"></div>'

html_code += """
</div>

<script>
    let lastPanel = null;
    function toggle(panelId, name, pos, tel, birth, entry) {
        const panel = document.getElementById(panelId);
        if(lastPanel && lastPanel !== panel) lastPanel.style.display = 'none';

        if (panel.style.display === 'block' && panel.dataset.current === name) {
            panel.style.display = 'none';
        } else {
            panel.innerHTML = `
                <div style="font-size:18px; font-weight:bold; margin-bottom:5px;">${name} <small style="color:#666;">(${pos})</small></div>
                <div class="extra-info">
                    🎂 생일: <b>${birth}</b><br>
                    📅 입사: <b>${entry}</b>
                </div>
                <a href="tel:${tel.replace(/-/g,'')}" class="call-btn">📞 전화 연결 (${tel})</a>
                <div style="font-size:12px; color:#999; text-decoration:underline;" onclick="this.parentElement.style.display='none'">닫기</div>
            `;
            panel.style.display = 'block';
            panel.dataset.current = name;
            lastPanel = panel;
        }
    }
</script>

</body>
</html>
"""

components.html(html_code, height=800, scrolling=True)
