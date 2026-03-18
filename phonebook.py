import streamlit as st

# 1. 화면 설정 및 데이터 초기화
if 'current_view' not in st.session_state:
    st.session_state.current_view = "성희회관"

# 성희회관 데이터 (사진 기반)
data_sunghee = [
    {"위치": "14층", "성명": "유순복", "연락처": "010-6370-0845", "비고": "B조(1직)"},
    {"위치": "13층", "성명": "박태연", "연락처": "010-5682-8927", "비고": "B조(1직)"},
    {"위치": "12층", "성명": "기성원", "연락처": "010-2618-9120", "비고": "A조(2직)"},
    {"위치": "11층", "성명": "김성순", "연락처": "010-4604-7608", "비고": "A조(3직)"},
    {"위치": "10층", "성명": "박현순", "연락처": "010-8714-7703", "비고": "B조(1직)"},
    {"위치": "반장", "성명": "허영찬", "연락처": "010-9894-3415", "비고": "A조 총괄"}
]

# 의산연 데이터 (사진 기반)
data_uisan = [
    {"위치": "8층", "성명": "안순재", "연락처": "010-9119-8879", "비고": "A조"},
    {"위치": "7층", "성명": "안순재", "연락처": "010-9119-8880", "비고": "A조"},
    {"위치": "6층", "성명": "장 성", "연락처": "010-8938-3988", "비고": "B조"},
    {"위치": "5층", "성명": "조미연", "연락처": "010-2252-2036", "비고": "A조"},
    {"위치": "별관 5층", "성명": "이선자", "연락처": "010-8210-7106", "비고": "A조"}
]

# 2. 스타일 설정 (모바일 최적화)
st.markdown("""
<style>
    /* 네비게이션 버튼 가로 정렬 */
    div[data-testid="stHorizontalBlock"] { display: flex !important; flex-wrap: nowrap !important; gap: 5px !important; }
    div[data-testid="column"] { min-width: 0px !important; flex: 1 !important; }
    
    /* 표 디자인 */
    .contact-table { width: 100%; border-collapse: collapse; font-size: 14px; margin-top: 10px; }
    .contact-table th { background-color: #f8f9fa; padding: 12px 5px; border-bottom: 2px solid #dee2e6; text-align: center; }
    .contact-table td { padding: 12px 5px; border-bottom: 1px solid #eee; text-align: center; }
    .tel-link { color: #007bff; text-decoration: none; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("🚨 보안비상연락망")

# 3. 네비게이션 버튼 (회관 / 의산연 순서)
col1, col2 = st.columns(2)
with col1:
    if st.button("🏢 성희회관", use_container_width=True):
        st.session_state.current_view = "성희회관"
with col2:
    if st.button("🔬 의산연", use_container_width=True):
        st.session_state.current_view = "의산연"

# 4. 표 생성 및 출력
view = st.session_state.current_view
target_data = data_sunghee if view == "성희회관" else data_uisan

st.subheader(f"📍 {view} 담당자 명단")

# HTML 문자열 생성
table_html = f"""
<table class="contact-table">
    <thead>
        <tr><th>위치</th><th>성명</th><th>연락처</th></tr>
    </thead>
    <tbody>
"""

for row in target_data:
    table_html += f"""
        <tr>
            <td><b>{row['위치']}</b></td>
            <td>{row['성명']}</td>
            <td><a href="tel:{row['연락처']}" class="tel-link">{row['연락처']}</a></td>
        </tr>
    """
table_html += "</tbody></table>"

# [핵심] 이 부분에서 반드시 unsafe_allow_html=True를 확인하세요!
st.markdown(table_html, unsafe_allow_html=True)
