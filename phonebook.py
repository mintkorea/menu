import streamlit as st

# 1. 상태 관리 및 데이터 설정
if 'current_building' not in st.session_state:
    st.session_state.current_building = "성희회관"

# 성희회관 데이터 (보내주신 사진 기반 일부)
data_sunghee = [
    {"위치": "14층", "성명": "유순복", "연락처": "010-6370-0845", "조": "B조(1직)"},
    {"위치": "13층", "성명": "박태연", "연락처": "010-5682-8927", "조": "B조(1직)"},
    {"위치": "12층", "성명": "기성원", "연락처": "010-2618-9120", "조": "A조(2직)"},
    {"위치": "11층", "성명": "김성순", "연락처": "010-4604-7608", "조": "A조(3직)"},
    {"위치": "반장", "성명": "허영찬", "연락처": "010-9894-3415", "조": "A조"}
]

# 의산연 데이터 (보내주신 사진 기반 일부)
data_uisan = [
    {"위치": "8층", "성명": "안순재", "연락처": "010-9119-8879", "조": "A조"},
    {"위치": "7층", "성명": "안순재", "연락처": "010-9119-8880", "조": "A조"},
    {"위치": "6층", "성명": "장 성", "연락처": "010-8938-3988", "조": "B조"},
    {"위치": "별관 5층", "성명": "이선자", "연락처": "010-8210-7106", "조": "A조"},
    {"위치": "별관 1,2층", "성명": "정혜숙", "연락처": "010-9130-0652", "조": "B조"}
]

# 2. 모바일 최적화 및 표 스타일 CSS
st.markdown("""
<style>
    .block-container { padding: 1rem 0.5rem !important; }
    /* 네비게이션 버튼 가로 정렬 */
    div[data-testid="stHorizontalBlock"] { display: flex !important; flex-wrap: nowrap !important; gap: 5px !important; }
    div[data-testid="column"] { min-width: 0px !important; flex: 1 !important; }
    
    /* 표 디자인 */
    .contact-table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 14px; }
    .contact-table th { background-color: #f1f3f5; padding: 12px 5px; border-bottom: 2px solid #dee2e6; text-align: center; }
    .contact-table td { padding: 12px 5px; border-bottom: 1px solid #eee; text-align: center; }
    .tel-link { color: #007bff; text-decoration: none; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("🚨 보안비상연락망")

# 3. 네비게이션 버튼 (보안 연락망 하부 배치)
col1, col2 = st.columns(2)
with col1:
    if st.button("🏢 성희회관", use_container_width=True):
        st.session_state.current_building = "성희회관"
with col2:
    if st.button("🔬 의산연", use_container_width=True):
        st.session_state.current_building = "의산연"

# 4. 선택된 건물의 표 렌더링 (핵심 해결책)
current = st.session_state.current_building
target_data = data_sunghee if current == "성희회관" else data_uisan

st.markdown(f"### 📍 {current} 담당자 명단")

# HTML 표 작성
html_code = f"""
<table class="contact-table">
    <thead>
        <tr><th>위치</th><th>성명</th><th>연락처</th></tr>
    </thead>
    <tbody>
"""

for item in target_data:
    html_code += f"""
        <tr>
            <td><b>{item['위치']}</b></td>
            <td>{item['성명']}</td>
            <td><a href="tel:{item['연락처']}" class="tel-link">{item['연락처']}</a></td>
        </tr>
    """

html_code += "</tbody></table>"

# [중요] unsafe_allow_html=True를 설정해야 표가 정상적으로 보입니다.
st.markdown(html_code, unsafe_allow_html=True)
