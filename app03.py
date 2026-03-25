import streamlit as st

st.set_page_config(page_title="성의교정 연락망", layout="wide")

# ---------------- 상태 관리 ----------------
if "fav" not in st.session_state:
    st.session_state.fav = set()

# ---------------- 디자인 (CSS) ----------------
st.markdown("""
<style>
    .block-container { padding-top: 1rem; }
    
    /* 카드 전체 레이아웃 */
    .contact-card {
        background: #ffffff;
        padding: 12px;
        border-radius: 12px;
        margin-bottom: 10px;
        border: 1px solid #eee;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }

    /* 이름+별표+직함 한 줄 정렬 */
    .header-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100%;
    }

    .name-section {
        display: flex;
        align-items: center;
        gap: 8px; /* 별표와 이름 사이 간격 */
    }

    .name-text { font-weight: 700; font-size: 1.05rem; color: #111; }
    .sub-text { font-size: 0.85rem; color: #777; }
    .work-text { font-size: 0.85rem; color: #888; margin: 4px 0 0 32px; }

    /* 버튼 그룹 (내선, 휴대폰) */
    .btn-group { display: flex; gap: 6px; }
    .tel-link {
        padding: 4px 10px;
        background: #f0f2f6;
        border-radius: 6px;
        font-size: 0.8rem;
        text-decoration: none !important;
        color: #333 !important;
        font-weight: 500;
    }

    /* ⭐ 버튼 투명화 및 정렬 */
    .stButton > button {
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
        color: #ffc107 !important;
        font-size: 20px !important;
        line-height: 1;
    }
</style>
""", unsafe_allow_html=True)

st.title("📞 성의교정 비상연락망")

# ---------------- 데이터 ----------------
data = [
    {"dept":"총무팀","name":"박현욱","pos":"팀장","ext":"02-3147-8190","mobile":"010-6245-0589","work":"부서업무 총괄"},
    {"dept":"총무팀","name":"김종래","pos":"차장","ext":"02-3147-8191","mobile":"010-9056-3701","work":"시설 및 자산관리"},
    {"dept":"총무팀","name":"장영섭","pos":"차장","ext":"02-3147-8193","mobile":"010-5072-0919","work":"예비군, 민방위"},
    {"dept":"총무팀","name":"주종호","pos":"과장","ext":"02-3147-8202","mobile":"010-3324-1187","work":"보안, 대관"},
    {"dept":"총무팀","name":"강은희","pos":"대리","ext":"02-3147-8206","mobile":"010-9127-1021","work":"문서배부, 행사"},
    {"dept":"총무팀","name":"김보라","pos":"선임","ext":"02-3147-8192","mobile":"010-8073-0527","work":"차량등록, 운영비"},
    {"dept":"총무팀","name":"노종현","pos":"책임","ext":"02-3147-8195","mobile":"010-9425-3109","work":"행사, 회의자료"},
    {"dept":"총무팀","name":"고규호","pos":"책임","ext":"02-3147-8196","mobile":"010-3381-8870","work":"캘린더, 인증평가"},
    {"dept":"총무팀","name":"김두리","pos":"사원","ext":"02-3147-8204","mobile":"010-9661-1257","work":"기숙사 사감"},
    {"dept":"총무팀","name":"임세리","pos":"사원","ext":"02-3147-8197","mobile":"010-3281-1229","work":"우편, 정수기"},
    {"dept":"총무팀","name":"김종식","pos":"사원","ext":"-","mobile":"010-9256-6904","work":"업무지원"},
    {"dept":"안전관리","name":"윤호열","pos":"UM","ext":"02-3147-8199","mobile":"010-2623-7963","work":"소방/방재"},
    {"dept":"안전관리","name":"주상건","pos":"차장","ext":"02-2258-7135","mobile":"010-9496-6483","work":"시신기증"},
    {"dept":"안전관리","name":"곽정승","pos":"과장","ext":"02-3147-8194","mobile":"010-5218-6504","work":"사업계획, 예산"},
    {"dept":"안전관리","name":"박일용","pos":"과장","ext":"02-3147-8201","mobile":"010-6205-7751","work":"계약, 사인물"},
    {"dept":"안전관리","name":"이경종","pos":"부장","ext":"02-3147-8203","mobile":"010-2623-7963","work":"교수업적평가"},
    {"dept":"안전관리","name":"김준석","pos":"과장","ext":"02-3147-8205","mobile":"010-9256-6904","work":"연구실 안전"},
    {"dept":"비서실","name":"이경자","pos":"부장","ext":"02-3147-8071","mobile":"010-6306-3652","work":"부총장 비서"},
    {"dept":"비서실","name":"이상희","pos":"과장","ext":"02-3147-8068","mobile":"010-3445-0623","work":"사무처장 비서"},
    {"dept":"비서실","name":"박은영","pos":"과장","ext":"02-3147-8069","mobile":"010-5348-6849","work":"의대학장 비서"},
]

# ---------------- 검색 및 필터 ----------------
c1, c2 = st.columns([3, 1])
with c1:
    search = st.text_input("🔍 이름/부서/업무 검색")
with c2:
    show_fav = st.checkbox("⭐ 즐겨찾기")

filtered = data
if search:
    s = search.lower()
    filtered = [x for x in filtered if any(s in str(v).lower() for v in x.values())]
if show_fav:
    filtered = [x for x in filtered if x["name"] in st.session_state.fav]

st.caption(f"검색 결과: {len(filtered)}명")

# ---------------- 리스트 출력 ----------------
for i, c in enumerate(filtered):
    is_f = c["name"] in st.session_state.fav
    star_icon = "★" if is_f else "☆"
    
    # 카드 시작
    st.markdown('<div class="contact-card">', unsafe_allow_html=True)
    
    # 헤더 행 (별표 + 이름 + 버튼들)
    h_col1, h_col2 = st.columns([0.7, 0.3])
    
    with h_col1:
        # 별표 버튼과 이름을 가로로 밀착 배치하기 위한 내부 컬럼
        inner_c1, inner_c2 = st.columns([0.12, 0.88])
        with inner_c1:
            if st.button(star_icon, key=f"f_{i}"):
                if is_f: st.session_state.fav.remove(c["name"])
                else: st.session_state.fav.add(c["name"])
                st.rerun()
        with inner_c2:
            st.markdown(f'<div class="name-text">{c["name"]} <span class="sub-text">{c["pos"]} · {c["dept"]}</span></div>', unsafe_allow_html=True)
            
    with h_col2:
        ext_link = f"tel:{c['ext'].replace('-', '')}"
        mob_link = f"tel:{c['mobile'].replace('-', '')}"
        st.markdown(f"""
            <div class="btn-group">
                {"<a href='"+ext_link+"' class='tel-link'>내선</a>" if c['ext'] != "-" else ""}
                <a href="{mob_link}" class="tel-link">휴대폰</a>
            </div>
        """, unsafe_allow_html=True)

    # 하단 업무 내용
    st.markdown(f'<div class="work-text">{c["work"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
