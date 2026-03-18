import streamlit as st

# 1. 화면 설정
st.set_page_config(page_title="보안 비상연락망", layout="wide")

# 2. 강제 2열 레이아웃 및 디자인 CSS
st.markdown("""
    <style>
    /* 모바일 강제 2열 Flexbox */
    .row-container {
        display: flex;
        flex-wrap: nowrap;
        width: 100%;
        gap: 10px;
    }
    .col-half {
        flex: 1;
        min-width: 0; /* 너비 고정 */
    }
    /* 버튼 스타일 최적화 */
    .stButton>button {
        width: 100%; height: 38px; font-size: 13px;
        margin-bottom: 4px; padding: 0; border: 1px solid #ddd;
    }
    /* 상단 고정 정보창 */
    .info-display {
        background-color: #eef6ff; padding: 15px; border-radius: 10px;
        border: 2px solid #3b82f6; margin-bottom: 20px;
        position: sticky; top: 10px; z-index: 1000;
    }
    .call-btn {
        display: block; width: 100%; background: #2563eb; color: white !important;
        text-align: center; padding: 10px; border-radius: 6px;
        text-decoration: none; font-weight: bold; margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 상태 관리 (선택된 인원 정보)
if 'person' not in st.session_state:
    st.session_state.person = None

def set_info(name, role, phone, birth, join):
    st.session_state.person = {"name": name, "role": role, "phone": phone, "birth": birth, "join": join}

# 4. 상단 고정 정보창 (누를 때마다 내용만 바뀜)
if st.session_state.person:
    p = st.session_state.person
    st.markdown(f"""
        <div class="info-display">
            <h3 style='margin:0; font-size:18px;'>👤 {p['name']} ({p['role']})</h3>
            <p style='margin:5px 0; font-size:14px;'>🎂 {p['birth']} | 📅 {p['join']}</p>
            <p style='margin:5px 0; font-weight:bold; color:#2563eb;'>📞 {p['phone']}</p>
            <a href="tel:{p['phone'].replace('-','')}" class="call-btn">즉시 전화걸기</a>
        </div>
    """, unsafe_allow_html=True)
else:
    st.info("이름을 클릭하면 상단에 상세 정보가 나타납니다.")

# 5. 본문: 강제 2열 레이아웃
# HTML을 직접 열고 닫는 방식으로 Streamlit 버튼을 배치합니다.
st.markdown('<div class="row-container">', unsafe_allow_html=True)

# --- 좌측 열 (회관 / 의산연) ---
st.markdown('<div class="col-half">', unsafe_allow_html=True)
st.subheader("🏢 회관/의산연")
if st.button("유정수(반)", key="sec_1"): set_info("유정수", "보안반장", "010-5316-8065", "1970.09.25", "2020.09.01")
st.caption("A조")
if st.button("배준용(장)", key="sec_2"): set_info("배준용", "보안조장", "010-4717-7065", "1969.12.24", "2022.07.26")
if st.button("이명구", key="sec_3"): set_info("이명구", "보안조원", "010-8638-5819", "1964.09.15", "2025.03.21")
if st.button("김영중", key="sec_4"): set_info("김영중", "보안조원", "010-7726-5963", "1959.02.26", "2024.08.21")
if st.button("김삼동", key="sec_5"): set_info("김삼동", "보안조원", "010-2345-8081", "1967.02.01", "2025.05.02")
st.caption("B조")
if st.button("심규천(장)", key="sec_6"): set_info("심규천", "보안조장", "010-8287-9895", "1967.04.10", "2024.11.11")
if st.button("임종현", key="sec_7"): set_info("임종현", "보안조원", "010-7741-6732", "1968.01.18", "2021.08.10")
# C조 등 추가 가능
st.markdown('</div>', unsafe_allow_html=True)

# --- 우측 열 (옴니버스) ---
st.markdown('<div class="col-half">', unsafe_allow_html=True)
st.subheader("🏫 옴니버스")
if st.button("오제준(반)", key="sec_8"): set_info("오제준", "보안반장", "010-3352-8933", "1970.03.29", "2022.05.18")
st.caption("A조")
if st.button("손병휘(장)", key="sec_9"): set_info("손병휘", "보안조장", "010-9966-2090", "1972.05.23", "2016.05.05")
if st.button("권순호", key="sec_10"): set_info("권순호", "보안조원", "010-2539-1799", "1980.12.14", "2026.02.11")
if st.button("김전식", key="sec_11"): set_info("김전식", "보안조원", "010-3277-0808", "1966.07.23", "2025.02.10")
st.caption("B조")
if st.button("황일범(장)", key="sec_12"): set_info("황일범", "보안조장", "010-8929-4294", "1969.05.30", "2022.04.01")
if st.button("이상길", key="sec_13"): set_info("이상길", "보안조원", "010-9904-0247", "1978.07.13", "2024.09.11")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) # row-container 닫기
