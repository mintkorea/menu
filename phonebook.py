import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="보안 통합 연락망", layout="wide")

html_code = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
    body { font-family: sans-serif; margin: 0; padding: 5px; background-color: #fff; }
    .grid-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 3px;
    }
    .node {
        height: 38px; border-radius: 4px; display: flex; flex-direction: column;
        align-items: center; justify-content: center; cursor: pointer;
        border: 1px solid rgba(0,0,0,0.1);
    }
    /* 조별 배경색 구분 */
    .group-top { background-color: #f1f3f5; } /* 지휘부: 연회색 */
    .group-a   { background-color: #e7f5ff; } /* A조: 연파랑 */
    .group-b   { background-color: #f3f0ff; } /* B조: 연보라 */
    .group-c   { background-color: #fff4e6; } /* C조: 연주황 */
    
    .node .pos { font-size: 8px; color: #666; line-height: 1; }
    .node .name { font-size: 12px; font-weight: bold; }

    /* 클릭 시 나타나는 정보창 (해당 줄 전체 너비 차지) */
    .info-panel {
        grid-column: span 4; display: none;
        background: #f8f9fa; border: 2px solid #28a745; border-radius: 8px;
        padding: 12px; margin: 5px 0; text-align: center;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
    }
    .call-btn {
        display: inline-block; background: #28a745; color: white;
        text-decoration: none; padding: 10px 20px; border-radius: 5px;
        font-weight: bold; font-size: 15px; margin-top: 8px;
    }
</style>
</head>
<body>

<div class="grid-container">
    <div class="node group-top" onclick="toggle('p1', '유정수', '반장', '010-5316-8065')"><span class="pos">반장</span><span class="name">유정수</span></div>
    <div class="node group-top" onclick="toggle('p1', '이규용', '소장', '010-8883-6580')"><span class="pos">소장</span><span class="name">이규용</span></div>
    <div class="node group-top" onclick="toggle('p1', '박상현', '부소장', '010-3193-4603')"><span class="pos">부소</span><span class="name">박상현</span></div>
    <div class="node group-top" onclick="toggle('p1', '오제준', '반장', '010-3352-8933')"><span class="pos">반장</span><span class="name">오제준</span></div>
    <div id="p1" class="info-panel"></div>

    <div class="node group-a" onclick="toggle('p2', '배준용', 'A조장', '010-4717-7065')"><span class="pos">A장</span><span class="name">배준용</span></div>
    <div class="node group-a" onclick="toggle('p2', '이명구', 'A조원', '010-8638-5819')"><span class="pos">A원</span><span class="name">이명구</span></div>
    <div class="node group-a" onclick="toggle('p2', '손병휘', 'A조장', '010-9966-2090')"><span class="pos">A장</span><span class="name">손병휘</span></div>
    <div class="node group-a" onclick="toggle('p2', '권순호', 'A조원', '010-2539-1799')"><span class="pos">A원</span><span class="name">권순호</span></div>
    <div id="p2" class="info-panel"></div>

    <div class="node group-b" onclick="toggle('p3', '심규천', 'B조장', '010-8287-9895')"><span class="pos">B장</span><span class="name">심규천</span></div>
    <div class="node group-b" onclick="toggle('p3', '임종현', 'B조원', '010-7741-6732')"><span class="pos">B원</span><span class="name">임종현</span></div>
    <div class="node group-b" onclick="toggle('p3', '황일범', 'B조장', '010-8929-4294')"><span class="pos">B장</span><span class="name">황일범</span></div>
    <div class="node group-b" onclick="toggle('p3', '이상길', 'B조원', '010-9904-0247')"><span class="pos">B원</span><span class="name">이상길</span></div>
    <div id="p3" class="info-panel"></div>
</div>

<script>
    let lastPanel = null;
    function toggle(panelId, name, pos, tel) {
        const panel = document.getElementById(panelId);
        
        // 다른 패널이 열려있으면 닫기
        if(lastPanel && lastPanel !== panel) lastPanel.style.display = 'none';

        if (panel.style.display === 'block' && panel.dataset.current === name) {
            panel.style.display = 'none';
        } else {
            panel.innerHTML = `
                <div style="font-size:16px; font-weight:bold;">${name} <span style="font-size:12px; font-weight:normal; color:#666;">| ${pos}</span></div>
                <a href="tel:${tel.replace(/-/g,'')}" class="call-btn">📞 ${tel} 연결</a>
                <div style="margin-top:8px; font-size:11px; color:#999;" onclick="this.parentElement.style.display='none'">창 닫기 ✖</div>
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

components.html(html_code, height=650, scrolling=True)
