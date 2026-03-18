import streamlit as st

st.set_page_config(layout="centered") # 모바일 세로 모드 최적화

# CSS를 활용해 이름 버튼을 작고 촘촘하게 배치
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 40px;
        font-size: 14px;
        margin-bottom: 2px;
        padding: 0;
    }
    .section-title { font-size: 12px; font-weight: bold; text-align: center; background: #eee; }
    </style>
""", unsafe_allow_html=True)

# 데이터 예시 (실제 전체 데이터를 이 리스트에 넣으면 됩니다)
def show_details(name, phone, birth, join_date):
    st.info(f"👤 **{name}**\n\n📞 연락처: {phone}\n\n🎂 생일: {birth}\n\n📅 입사일: {join_date}")
    st.markdown(f'<a href="tel:{phone.replace("-","")}" style="display:block; text-align:center; background:#007bff; color:white; padding:10px; border-radius:5px; text-decoration:none;">📞 즉시 전화걸기</a>', unsafe_allow_html=True)

# 1. 지휘부
col1, col2 = st.columns(2)
if col1.button("이규용 소장"): show_details("이규용 소장", "010-8883-6580", "1972.03.01", "-")
if col2.button("박상현 부소장"): show_details("박상현 부소장", "010-3193-4603", "1988.07.31", "-")

st.write("---")

# 2. 본문 (좌우 분할)
left, right = st.columns(2)

with left:
    st.markdown('<div class="section-title">🏥 회관/의산연</div>', unsafe_allow_html=True)
    if st.button("유정수 (반)"): show_details("유정수 반장", "010-5316-8065", "1970.09.25", "2020.09.01")
    st.caption("A조")
    c1, c2 = st.columns(2)
    if c1.button("배준용"): show_details("배준용 (A조장)", "010-4717-7065", "1969.12.24", "2022.07.26")
    if c2.button("이명구"): show_details("이명구", "010-8638-5819", "1964.09.15", "2025.03.21")
    # ... B조, C조 반복

with right:
    st.markdown('<div class="section-title">🏫 옴니버스</div>', unsafe_allow_html=True)
    if st.button("오제준 (반)"): show_details("오제준 반장", "010-3352-8933", "1970.03.29", "2022.05.18")
    st.caption("A조")
    if st.button("손병휘"): show_details("손병휘 (A조장)", "010-9966-2090", "1972.05.23", "2016.05.05")
    # ... B조, C조 반복
