import streamlit as st

st.set_page_config(page_title="보안 비상연락망", layout="wide")

# CSS: 모바일 2열 강제 고정 및 깔끔한 버튼 디자인
st.markdown("""
    <style>
    .stButton>button {
        width: 100%; height: 35px; font-size: 13px; margin-bottom: 2px;
        padding: 0; border: 1px solid #ddd; background-color: #fdfdfd;
    }
    .info-display {
        background-color: #e7f3ff; padding: 12px; border-radius: 8px;
        border: 1px solid #b3d7ff; margin-bottom: 15px; position: sticky; top: 10px; z-index: 999;
    }
    .call-btn {
        display: inline-block; background: #007bff; color: white;
        padding: 8px 15px; border-radius: 5px; text-decoration: none; font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 1. 상태 관리: 현재 선택된 사람의 정보만 저장
if 'selected_member' not in st.session_state:
    st.session_state.selected_member = None

def select_member(name, role, phone, birth, join):
    st.session_state.selected_member = {
        "name": name, "role": role, "phone": phone, "birth": birth, "join": join
    }

# 2. [상단 고정] 선택된 사람의 정보창 (누를 때마다 여기서 내용만 바뀜)
if st.session_state.selected_member:
    m = st.session_state.selected_member
    st.markdown(f"""
        <div class="info-display">
            <b>{m['name']} ({m['role']})</b><br>
            🎂 생일: {m['birth']} | 📅 입사: {m['join']}<br>
            📞 {m['phone']} &nbsp;&nbsp; <a href="tel:{m['phone'].replace('-','')}" class="call-btn">전화걸기</a>
        </div>
    """, unsafe_allow_html=True)
else:
    st.info("이름을 클릭하면 상세 정보와 전화 버튼이 나타납니다.")

# 3. 본문: 모바일 2열 강제 유지
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("🏢 **회관/의산연**")
    if st.button("유정수(반)"): select_member("유정수", "반장", "010-5316-8065", "1970.09.25", "2020.09.01")
    st.caption("A조")
    if st.button("배준용(장)"): select_member("배준용", "A조장", "010-4717-7065", "1969.12.24", "2022.07.26")
    if st.button("이명구"): select_member("이명구", "A조원", "010-8638-5819", "1964.09.15", "2025.03.21")
    if st.button("김영중"): select_member("김영중", "A조원", "010-7726-5963", "1959.02.26", "2024.08.21")
    if st.button("김삼동"): select_member("김삼동", "A조원", "010-2345-8081", "1967.02.01", "2025.05.02")

with col_right:
    st.markdown("🏫 **옴니버스**")
    if st.button("오제준(반)"): select_member("오제준", "반장", "010-3352-8933", "1970.03.29", "2022.05.18")
    st.caption("A조")
    if st.button("손병휘(장)"): select_member("손병휘", "A조장", "010-9966-2090", "1972.05.23", "2016.05.05")
    if st.button("권순호"): select_member("권순호", "A조원", "010-2539-1799", "1980.12.14", "2026.02.11")
    if st.button("김전식"): select_member("김전식", "A조원", "010-3277-0808", "1966.07.23", "2025.02.10")

# 하단 기숙사 등 추가...
