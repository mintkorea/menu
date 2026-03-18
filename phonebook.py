import streamlit as st
import streamlit.components.v1 as components

# 1. 상태 관리 및 데이터 설정
if 'current_view' not in st.session_state:
    st.session_state.current_view = "성희회관"

# 성희회관 데이터
data_sunghee = [
    {"위치": "14층", "성명": "유순복", "연락처": "010-6370-0845"},
    {"위치": "13층", "성명": "박태연", "연락처": "010-5682-8927"},
    {"위치": "12층", "성명": "기성원", "연락처": "010-2618-9120"},
    {"위치": "11층", "성명": "김성순", "연락처": "010-4604-7608"},
    {"위치": "10층", "성명": "박현순", "연락처": "010-8714-7703"},
    {"위치": "반장", "성명": "허영찬", "연락처": "010-9894-3415"}
]

# 의산연 데이터
data_uisan = [
    {"위치": "8층", "성명": "안순재", "연락처": "010-9119-8879"},
    {"위치": "7층", "성명": "안순재", "연락처": "010-9119-8880"},
    {"위치": "6층", "성명": "장 성", "연락처": "010-8938-3988"},
    {"위치": "5층", "성명": "조미연", "연락처": "010-2252-2036"},
    {"위치": "별관 5층", "성명": "이선자", "연락처": "010-8210-7106"}
]

st.title("🚨 보안비상연락망")

# 2. 네비게이션 버튼
col1, col2 = st.columns(2)
with col1:
    if st.button("🏢 성희회관", use_container_width=True):
        st.session_state.current_view = "성희회관"
with col2:
    if st.button("🔬 의산연", use_container_width=True):
        st.session_state.current_view = "의산연"

# 3. HTML 표 생성
view = st.session_state.current_view
target_data = data_sunghee if view == "성희회관" else data_uisan

# 스타일과 표를 하나의 문자열로 합침
html_string = f"""
<div style="font-family: sans-serif;">
    <h3 style="color: #333;">📍 {view} 담당자 명단</h3>
    <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 16px;">
        <thead>
            <tr style="background-color: #f8f9fa; border-bottom: 2px solid #dee2e6;">
                <th style="padding: 12px; text-align: center;">위치</th>
                <th style="padding: 12px; text-align: center;">성명</th>
                <th style="padding: 12px; text-align: center;">연락처</th>
            </tr>
        </thead>
        <tbody>
"""

for row in target_data:
    html_string += f"""
        <tr style="border-bottom: 1px solid #eee;">
            <td style="padding: 12px; text-align: center;"><b>{row['위치']}</b></td>
            <td style="padding: 12px; text-align: center;">{row['성명']}</td>
            <td style="padding: 12px; text-align: center;">
                <a href="tel:{row['연락처']}" style="color: #007bff; text-decoration: none; font-weight: bold;">{row['연락처']}</a>
            </td>
        </tr>
    """

html_string += "</tbody></table></div>"

# 4. [핵심] st.markdown 대신 components.html 사용
# height는 명단 길이에 따라 조절 가능합니다.
components.html(html_string, height=500, scrolling=True)
