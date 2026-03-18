import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="보안팀 연락망", layout="wide")

# 1. HTML/CSS 직접 주입 (Streamlit 레이아웃 무시)
html_code = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    body { font-family: 'Malgun Gothic', sans-serif; margin: 0; padding: 10px; background-color: #f8f9fa; }
    .grid-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr); /* 무조건 4열 */
        gap: 8px;
    }
    .card {
        background: white;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 12px 2px;
        text-align: center;
        text-decoration: none;
        color: #333;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .card:active { background: #e9ecef; }
    .pos { font-size: 10px; color: #007bff; display: block; margin-bottom: 2px; }
    .name { font-size: 14px; font-weight: bold; display: block; }
    .section-title { 
        grid-column: span 4; 
        background: #007bff; color: white; 
        padding: 5px; font-size: 12px; border-radius: 4px; margin: 10px 0 5px 0;
        text-align: center;
    }
</style>
</head>
<body>

<div class="grid-container">
    <div class="section-title">🛡️ 지휘부 / 공통</div>
    <a href="tel:01053168065" class="card"><span class="pos">반장</span><span class="name">유정수</span></a>
    <a href="tel:01088836580" class="card"><span class="pos">소장</span><span class="name">이규용</span></a>
    <a href="tel:01031934603" class="card"><span class="pos">부소장</span><span class="name">박상현</span></a>
    <a href="tel:01033528933" class="card"><span class="pos">반장</span><span class="name">오제준</span></a>

    <div class="section-title">🏢 회관A / 🏫 옴니A</div>
    <a href="tel:01047177065" class="card"><span class="pos">A조장</span><span class="name">배준용</span></a>
    <a href="tel:01086385819" class="card"><span class="pos">A조원</span><span class="name">이명구</span></a>
    <a href="tel:01099662090" class="card"><span class="pos">A조장</span><span class="name">손병휘</span></a>
    <a href="tel:01025391799" class="card"><span class="pos">A조원</span><span class="name">권순호</span></a>

    <div class="section-title">🏢 회관B / 🏫 옴니B</div>
    <a href="tel:01082879895" class="card"><span class="pos">B조장</span><span class="name">심규천</span></a>
    <a href="tel:01077416732" class="card"><span class="pos">B조원</span><span class="name">임종현</span></a>
    <a href="tel:01089294294" class="card"><span class="pos">B조장</span><span class="name">황일범</span></a>
    <a href="tel:01099040247" class="card"><span class="pos">B조원</span><span class="name">이상길</span></a>
    
    </div>

</body>
</html>
"""

# 2. 컴포넌트로 실행 (가장 확실한 방법)
components.html(html_code, height=800, scrolling=True)
