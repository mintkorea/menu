import streamlit as st

st.set_page_config(page_title="보안 비상연락망", layout="wide")

# CSS: 모바일에서도 무조건 2열 유지 및 상단 고정 정보창
st.markdown("""
    <style>
    /* 상단 정보창 고정 */
    .fixed-info {
        position: sticky; top: 0; z-index: 1000;
        background-color: #e8f4ff; padding: 10px;
        border-bottom: 2px solid #007bff; margin-bottom: 15px;
    }
    /* 강제 2열 레이아웃 (핵심) */
    .flex-container {
        display: flex; flex-direction: row !important; 
        width: 100%; gap: 5px;
    }
    .flex-col {
        flex: 1; min-width: 0; /* 모바일에서도 반반 유지 */
    }
    /* 리스트 버튼 스타일 */
    .name-card {
        display: block; width: 100%; background: #ffffff;
        border: 1px solid #ddd; padding: 10px 5px; margin-bottom: 4px;
        text-align: center; font-size: 14px; border-radius: 4px;
        cursor: pointer; color: black; text-decoration: none;
    }
    </style>
""", unsafe_allow_html=True)

# 데이터 클릭 상태 관리
if 'm' not in st.session_state:
    st.session_state.m = None

def select(n, r, p, b, j):
    st.session_state.m = {"n": n, "r": r, "p": p, "b": b, "j": j}

# 1. 상단 정보창 (하나만 노출)
if st.session_state.m:
    m = st.session_state.m
    st.markdown(f"""
        <div class="fixed-info">
            <b style="font-size:16px;">{m['n']} ({m['r']})</b><br>
            <span style="font-size:13px;">🎂 {m['b']} | 📅 {m['j']}</span><br>
            <a href="tel:{m['p'].replace('-','')}" style="display:block; background:#007bff; color:white; text-align:center; padding:8px; border-radius:5px; text-decoration:none; margin-top:5px; font-weight:bold;">📞 즉시 전화걸기</a>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown('<div class="fixed-info">이름을 클릭하면 정보가 나타납니다.</div>', unsafe_allow_html=True)

# 2. 본문 (강제 좌우 2열)
st.markdown('<div class="flex-container">', unsafe_allow_html=True)

# --- 왼쪽: 회관/의산연 ---
with st.container():
    st.write("🏢 **회관/의산연**")
    # Streamlit 버튼은 세로로 쌓이므로, HTML 링크/버튼 형태로 구현 필요
    if st.button("유정수(반)"): select("유정수", "보안반장", "010-5316-8065", "1970.09.25", "2020.09.01")
    st.caption("A조")
    if st.button("배준용(장)"): select("배준용", "보안조장", "010-4717-7065", "1969.12.24", "2022.07.26")
    if st.button("이명구"): select("이명구", "보안조원", "010-8638-5819", "1964.09.15", "2025.03.21")
    if st.button("김영중"): select("김영중", "보안조원", "010-7726-5963", "1959.02.26", "2024.08.21")
    if st.button("김삼동"): select("김삼동", "보안조원", "010-2345-8081", "1967.02.01", "2025.05.02")

# --- 오른쪽: 옴니버스 ---
with st.container():
    st.write("🏫 **옴니버스**")
    if st.button("오제준(반)"): select("오제준", "보안반장", "010-3352-8933", "1970.03.29", "2022.05.18")
    st.caption("A조")
    if st.button("손병휘(장)"): select("손병휘", "보안조장", "010-9966-2090", "1972.05.23", "2016.05.05")
    if st.button("권순호"): select("권순호", "보안조원", "010-2539-1799", "1980.12.14", "2026.02.11")
    if st.button("김전식"): select("김전식", "보안조원", "010-3277-0808", "1966.07.23", "2025.02.10")

st.markdown('</div>', unsafe_allow_html=True)
