import streamlit as st

st.set_page_config(page_title="성의교정 연락망", layout="wide")

# ---------------- 1. CSS 디자인 (가로 고정 핵심) ----------------
st.markdown("""
<style>
    /* 전체 여백 조절 */
    .block-container { padding-top: 1rem; }

    /* 카드 스타일 */
    .contact-card {
        background: #ffffff;
        padding: 12px;
        border-radius: 12px;
        margin-bottom: 10px;
        border: 1px solid #eee;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }

    /* ⭐ 별표와 이름을 무조건 한 줄에 가로로 배치 */
    .header-row {
        display: flex;
        align-items: center; /* 세로 중앙 정렬 */
        gap: 8px; /* 별표와 이름 사이 간격 */
        width: 100%;
        margin-bottom: 4px;
    }

    .name-text { font-weight: 700; font-size: 1.05rem; color: #111; margin: 0; }
    .sub-text { font-size: 0.85rem; color: #777; margin-left: 4px; }
    .work-text { font-size: 0.85rem; color: #888; margin: 2px 0 0 32px; line-height: 1.3; }

    /* 버튼 그룹 */
    .btn-group { display: flex; gap: 6px; margin-top: 10px; }
    .tel-link {
        flex: 1;
        text-align: center;
        padding: 8px 0;
        background: #f0f2f6;
        border-radius: 6px;
        font-size: 0.85rem;
        text-decoration: none !important;
        color: #333 !important;
        font-weight: 500;
        border: 1px solid #ddd;
    }
    .mob-link { background: #007bff; color: white !important; border: none; }

    /* ⭐ 스트림릿 버튼 스타일 제거 (별표 전용) */
    .stButton > button {
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
        color: #ffc107 !important;
        font-size: 22px !important;
        width: 24px !important;
        height: 24px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("📞 성의교정 비상연락망")

# ---------------- 2. 데이터 (이미지 텍스트 반영) ----------------
data = [
    {"dept":"총무팀","name":"박현욱","pos":"팀장","ext":"02-3147-8190","mobile":"010-6245-0589","work":"부서업무 총괄"},
    {"dept":"총무팀","name":"김종래","pos":"차장","ext":"02-3147-8191","mobile":"010-9056-3701","work":"시설 및 자산관리 (대학본관, 의산연, 성의회관 등)"},
    {"dept":"총무팀","name":"장영섭","pos":"차장","ext":"02-3147-8193","mobile":"010-5072-0919","work":"예비군대대장, 민방위, 병무행정, 행사, ITC"},
    {"dept":"총무팀","name":"주종호","pos":"과장","ext":"02-3147-8202","mobile":"010-3324-1187","work":"보안, 미화, 대관, 게스트하우스"},
    {"dept":"안전관리","name":"윤호열","pos":"UM","ext":"02-3147-8199","mobile":"010-2623-7963","work":"소방/방재 인증평가, 시설관리 (옴니버스파크 등)"},
    {"dept":"안전관리","name":"주상건","pos":"차장","ext":"02-2258-7135","mobile":"010-9496-6483","work":"시신기증 업무"},
]

if "fav" not in st.session_state:
    st.session_state.fav = set()

search = st.text_input("🔍 이름/부서/업무 검색")

# ---------------- 3. 출력 (Flexbox 구조) ----------------
for i, c in enumerate(data):
    if search and not any(search.lower() in str(v).lower() for v in c.values()):
        continue
        
    is_f = c["name"] in st.session_state.fav
    star = "★" if is_f else "☆"
    
    # 카드 시작
    st.markdown('<div class="contact-card">', unsafe_allow_html=True)
    
    # [헤더 구역] 별표와 이름을 강제로 가로 배치
    col_btn, col_info = st.columns([0.1, 0.9])
    with col_btn:
        if st.button(star, key=f"f_{i}"):
            if is_f: st.session_state.fav.remove(c["name"])
            else: st.session_state.fav.add(c["name"])
            st.rerun()
    with col_info:
        # 이 구역 안에서 이름과 직함을 다시 가로로 배치
        st.markdown(f'<div class="header-row"><span class="name-text">{c["name"]}</span><span class="sub-text">{c["pos"]} · {c["dept"]}</span></div>', unsafe_allow_html=True)

    # 업무 내용
    st.markdown(f'<div class="work-text">{c["work"]}</div>', unsafe_allow_html=True)

    # 버튼들
    ext_link = f"tel:{c['ext'].replace('-', '')}"
    mob_link = f"tel:{c['mobile'].replace('-', '')}"
    st.markdown(f"""
        <div class="btn-group">
            {"<a href='"+ext_link+"' class='tel-link'>내선 연결</a>" if c['ext'] != "-" else ""}
            <a href="{mob_link}" class="tel-link mob-link">휴대폰 연결</a>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
