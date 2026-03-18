import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="보안팀 비상연락망", layout="wide")

# 1. 보안팀 전체 데이터 구성 (명단 기반)
# 실제 데이터 중 확인된 내용을 넣었으며, 부족한 부분은 형식에 맞춰 채워 넣으시면 됩니다.
security_team = [
    # 지휘부 (Grey)
    {"group": "top", "pos": "소장", "name": "이규용", "tel": "010-8883-6580", "birth": "1972.03.01", "entry": "-"},
    {"group": "top", "pos": "부소장", "name": "박상현", "tel": "010-3193-4603", "birth": "1988.07.31", "entry": "-"},
    {"group": "top", "pos": "반장", "name": "유정수", "tel": "010-5316-8065", "birth": "1970.09.25", "entry": "2020.09.01"},
    {"group": "top", "pos": "반장", "name": "오제준", "tel": "010-3352-8933", "birth": "-", "entry": "-"},
    
    # A조 (Blue)
    {"group": "a", "pos": "A장", "name": "배준용", "tel": "010-4717-7065", "birth": "1969.12.24", "entry": "2022.07.26"},
    {"group": "a", "pos": "A원", "name": "이명구", "tel": "010-8638-5819", "birth": "1964.09.15", "entry": "2025.03.21"},
    {"group": "a", "pos": "A장", "name": "손병휘", "tel": "010-9966-2090", "birth": "-", "entry": "-"},
    {"group": "a", "pos": "A원", "name": "권순호", "tel": "010-2539-1799", "birth": "-", "entry": "-"},
    
    # B조 (Purple)
    {"group": "b", "pos": "B장", "name": "심규천", "tel": "010-8287-9895", "birth": "-", "entry": "-"},
    {"group": "b", "pos": "B원", "name": "임종현", "tel": "010-7741-6732", "birth": "-", "entry": "-"},
    {"group": "b", "pos": "B장", "name": "황일범", "tel": "010-8929-4294", "birth": "-", "entry": "-"},
    {"group": "b", "pos": "B원", "name": "이상길", "tel": "010-9904-0247", "birth": "-", "entry": "-"},

    # C조 (Orange)
    {"group": "c", "pos": "C장", "name": "김태언", "tel": "010-XXXX-XXXX", "birth": "-", "entry": "1순위"},
    {"group": "c", "pos": "C원", "name": "이태원", "tel": "010-XXXX-XXXX", "birth": "-", "entry": "2순위"},
    {"group": "c", "pos": "C원", "name": "이정석", "tel": "010-XXXX-XXXX", "birth": "-", "entry": "3순위"},
    {"group": "c", "pos": "C원", "name": "보안요원", "tel": "010-0000-0000", "birth": "-", "entry": "-"},
    
    # 추가 인원 (28명까지 동일한 형식으로 반복)
]

# 2. 고밀도 그리드 HTML/JS
html_code = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
    body {{ font-family: 'Malgun Gothic', sans-serif; margin: 0; padding: 10px; background-color: #fff; }}
    .grid-container {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 5px;
    }}
    .node {{
        height: 45px; border-radius: 6px; display: flex; flex-direction: column;
        align-items: center; justify-content: center; cursor: pointer;
        border: 1px solid rgba(0,0,0,0.1); box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }}
    /* 조별 테두리 및 텍스트 색상 구분 */
    .top {{ background-color: #f8f9fa; border-color: #dee2e6; color: #495057; }}
    .a   {{ background-color: #e7f5ff; border-color: #a5d8ff; color: #1971c2; }}
    .b   {{ background-color: #f3f0ff; border-color: #d0bfff; color: #6f2dbd; }}
    .c   {{ background-color: #fff4e6; border-color: #ffd8a8; color: #d9480f; }}
    
    .node .pos {{ font-size: 9px; margin-bottom: 2px; }}
    .node .name {{ font-size: 14px; font-weight: bold; }}

    /* 상세 정보 패널 (아코디언 방식) */
    .info-panel {{
        grid-column: span 4; display: none;
        background: white; border: 2px solid #28a745; border-radius: 12px;
        padding: 15px; margin: 8px 0; text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}
    .call-btn {{
        display: block; background: #28a745; color: white;
        text-decoration: none; padding: 12px; border-radius: 8px;
        font-weight: bold; font-size: 17px; margin: 12px 0;
    }}
    .details {{ font-size: 14px; color: #444; line-height: 1.8; }}
    .close-txt {{ color: #999; font-size: 12px; text-decoration: underline; cursor: pointer; }}
</style>
</head>
<body>

<div class="grid-container">
"""

# 인원 배치 및 패널 생성 (4인당 1개 패널 할당)
for i, m in enumerate(security_team):
    html_code += f"""
    <div class="node {m['group']}" onclick="openDetail('p{i//4}', '{m['name']}', '{m['pos']}', '{m['tel']}', '{m['birth']}', '{m['entry']}')">
        <span class="pos">{m['pos']}</span>
        <span class="name">{m['name']}</span>
    </div>
    """
    if (i + 1) % 4 == 0 or (i + 1) == len(security_team):
        html_code += f'<div id="p{i//4}" class="info-panel"></div>'

html_code += """
</div>

<script>
    let activePanel = null;
    function openDetail(id, name, pos, tel, birth, entry) {
        const panel = document.getElementById(id);
        if(activePanel && activePanel !== panel) activePanel.style.display = 'none';

        panel.innerHTML = `
            <div style="font-size:20px; font-weight:bold; margin-bottom:10px;">${name} <span style="font-size:14px; font-weight:normal;">(${pos})</span></div>
            <div class="details">
                🎂 생일: <b>${birth}</b><br>
                📅 입사: <b>${entry}</b>
            </div>
            <a href="tel:${tel.replace(/-/g,'')}" class="call-btn">📞 전화 연결 (${tel})</a>
            <div class="close-txt" onclick="this.parentElement.style.display='none'">닫기</div>
        `;
        panel.style.display = 'block';
        activePanel = panel;
        
        // 클릭 위치로 부드럽게 스크롤
        panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
</script>

</body>
</html>
"""

# 컴포넌트 출력
components.html(html_code, height=900, scrolling=True)
