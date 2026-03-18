import streamlit as st

# 1. 모바일 최적화 설정
st.set_page_config(page_title="통합 비상연락망", layout="wide")

# 폰트 크기 및 버튼 스타일 조정 (모바일 한 화면에 많이 담기 위함)
st.markdown("""
    <style>
    [data-testid="stVerticalBlock"] { gap: 0.5rem; }
    .stButton>button { width: 100%; padding: 0.2rem; font-size: 0.8rem; }
    .contact-box { border: 1px solid #e6e9ef; padding: 5px; border-radius: 5px; background-color: #f8f9fa; margin-bottom: 5px; }
    .name-text { font-weight: bold; font-size: 0.9rem; }
    .phone-text { color: #007bff; font-size: 0.85rem; text-decoration: none; }
    </style>
    """, unsafe_allow_html=True)

# 2. 상단 고정: 소장/부소장
col_top1, col_top2 = st.columns(2)
with col_top1:
    st.markdown('<div class="contact-box">👑 <b>소장</b> 이규용<br><a class="phone-text" href="tel:01088836580">010-8883-6580</a></div>', unsafe_allow_html=True)
with col_top2:
    st.markdown('<div class="contact-box">🥈 <b>부소장</b> 박상현<br><a class="phone-text" href="tel:01031934603">010-3193-4603</a></div>', unsafe_allow_html=True)

# 3. 중앙: 보안팀 (좌: 회관/의산연 | 우: 옴니버스)
st.divider()
col_sec1, col_sec2 = st.columns(2)

with col_sec1:
    st.subheader("🏥 회관/의산연")
    st.caption("반장: 유정수 010-5316-8065")
    
    # A조 (회관2 + 의산연2)
    with st.expander("🅰️ A조 (4명)", expanded=True):
        st.markdown("""
        - 배준용(장) <a class="phone-text" href="tel:01047177065">010-4717-7065</a>
        - 이명구 <a class="phone-text" href="tel:01086385819">010-8638-5819</a>
        - 김영중 <a class="phone-text" href="tel:01077265963">010-7726-5963</a>
        - 김삼동 <a class="phone-text" href="tel:01023458081">010-2345-8081</a>
        """, unsafe_allow_html=True)
        
    # B조/C조 동일 구조... (내용 생략 가능하나 구조 유지)

with col_sec2:
    st.subheader("🏫 옴니버스")
    st.caption("반장: 오제준 010-3352-8933")
    
    # A조 (옴니3)
    with st.expander("🅰️ A조 (3명)", expanded=True):
        st.markdown("""
        - 손병휘(장) <a class="phone-text" href="tel:01099662090">010-9966-2090</a>
        - 권순호 <a class="phone-text" href="tel:01025391799">010-2539-1799</a>
        - 김진식 <a class="phone-text" href="tel:01032770808">010-3277-0808</a>
        """, unsafe_allow_html=True)

# 4. 하단: 기숙사 & 미화팀
st.divider()
st.subheader("🏠 성의기숙사")
st.markdown("이강택(반장) / 유시균 / 이상현")

# 미화팀은 탭으로 분리하여 화면 복잡도 감소
tab_h, tab_u = st.tabs(["🧹 성의회관 미화", "🧪 의산연 미화"])
with tab_h:
    st.write("14층 유순복 | 13층 박태연 | 12층 기성원 ...") # 데이터 반복문 처리 가능
