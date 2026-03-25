import streamlit as st

st.set_page_config(page_title="성의교정 연락망", layout="wide")

# ---------------- 상태 ----------------
if "fav" not in st.session_state:
    st.session_state.fav = set()

# ---------------- CSS ----------------
st.markdown("""
<style>
.card {
    background:#f8f9fb;
    padding:14px;
    border-radius:14px;
    margin-bottom:10px;
    box-shadow:0 2px 6px rgba(0,0,0,0.05);
}

.row {
    display:flex;
    justify-content:space-between;
    align-items:center;
}

.left {
    display:flex;
    align-items:center;
    gap:8px;
}

.name {
    font-weight:700;
}

.sub {
    font-size:0.8rem;
    color:#666;
}

.work {
    font-size:0.8rem;
    color:#888;
    margin-top:4px;
}

.right {
    display:flex;
    gap:6px;
}

.tel-btn {
    padding:5px 9px;
    border-radius:8px;
    font-size:0.75rem;
    text-decoration:none;
    background:#e9ecef;
    color:#333;
}

/* ⭐ 버튼을 별처럼 */
button[kind="secondary"] {
    border:none !important;
    background:transparent !important;
    font-size:18px !important;
    padding:0 !important;
    margin-right:4px;
}
</style>
""", unsafe_allow_html=True)

st.title("📞 성의교정 비상연락망")

# ---------------- 데이터 ----------------
data = [
    # ---------------- 총무팀 ----------------
    {"dept":"총무팀","name":"박현욱","pos":"팀장","ext":"02-3147-8190","mobile":"010-6245-0589","work":"부서업무 총괄"},
    {"dept":"총무팀","name":"김종래","pos":"차장","ext":"02-3147-8191","mobile":"010-9056-3701","work":"시설 및 자산관리(대학본관, 의산연, 성의회관 등)"},
    {"dept":"총무팀","name":"장영섭","pos":"차장","ext":"02-3147-8193","mobile":"010-5072-0919","work":"예비군대대장, 민방위, 병무행정, 행사, ITC, 기타서무"},
    {"dept":"총무팀","name":"주종호","pos":"과장","ext":"02-3147-8202","mobile":"010-3324-1187","work":"보안, 미화, 대관, 게스트하우스, 인체유래물은행"},
    {"dept":"총무팀","name":"강은희","pos":"대리","ext":"02-3147-8206","mobile":"010-9127-1021","work":"의료원 직인/문서배부, 월례조회, 행사, 회의"},
    {"dept":"총무팀","name":"김보라","pos":"선임","ext":"02-3147-8192","mobile":"010-8073-0527","work":"명예교수실 점검 및 관리, 차량등록, 부서운영비"},
    {"dept":"총무팀","name":"노종현","pos":"책임","ext":"02-3147-8195","mobile":"010-9425-3109","work":"행사, 회의자료취합, 단위기관장회의, 예비군대대"},
    {"dept":"총무팀","name":"고규호","pos":"책임","ext":"02-3147-8196","mobile":"010-3381-8870","work":"캘린더/다이어리, 인증평가, 대학정보공시, 안전점검"},
    {"dept":"총무팀","name":"김두리","pos":"사원","ext":"02-3147-8204","mobile":"010-9661-1257","work":"성의기숙사 사감"},
    {"dept":"총무팀","name":"임세리","pos":"사원","ext":"02-3147-8197","mobile":"010-3281-1229","work":"우편, 물품/비품청구, 정수기관리, 정보보호"},
    {"dept":"총무팀","name":"김종식","pos":"사원","ext":"-","mobile":"010-9256-6904","work":"업무지원"},

    # ---------------- 안전관리 ----------------
    {"dept":"안전관리","name":"윤호열","pos":"UM","ext":"02-3147-8199","mobile":"010-2623-7963","work":"소방/방재 인증평가, 시설관리(옴니버스파크 등)"},
    {"dept":"안전관리","name":"주상건","pos":"차장","ext":"02-2258-7135","mobile":"010-9496-6483","work":"시신기증 업무"},
    {"dept":"안전관리","name":"곽정승","pos":"과장","ext":"02-3147-8194","mobile":"010-5218-6504","work":"사업계획, 예산, 주차/차량관리"},
    {"dept":"안전관리","name":"박일용","pos":"과장","ext":"02-3147-8201","mobile":"010-6205-7751","work":"계약(임대차, 용역 등), 사인물관리, 교원기숙사"},
    {"dept":"안전관리","name":"이경종","pos":"부장","ext":"02-3147-8203","mobile":"010-2623-7963","work":"교수업적평가, 문서분배, 그룹웨어 ITC"},
    {"dept":"안전관리","name":"김준석","pos":"과장","ext":"02-3147-8205","mobile":"010-9256-6904","work":"연구실 안전관리, 출입증등록, 기타서무"},

    # ---------------- 비서실 ----------------
    {"dept":"비서실","name":"이경자","pos":"부장","ext":"02-3147-8071","mobile":"010-6306-3652","work":"의무부총장, 기획조정실장 비서"},
    {"dept":"비서실","name":"이상희","pos":"과장","ext":"02-3147-8068","mobile":"010-3445-0623","work":"영성구현실장, 사무처장 비서"},
    {"dept":"비서실","name":"박은영","pos":"과장","ext":"02-3147-8069","mobile":"010-5348-6849","work":"의과대학장 비서"},

    # ---------------- 의산연별관 ----------------
    {"dept":"의산연별관","name":"주용덕","pos":"보안","ext":"별관","mobile":"010-2021-9541","work":"의산연 별관 보안"},
    {"dept":"의산연별관","name":"김승배","pos":"보안","ext":"별관","mobile":"010-8704-2591","work":"의산연 별관 보안"},
    {"dept":"의산연별관","name":"안정진","pos":"보안","ext":"별관","mobile":"010-4925-2926","work":"의산연 별관 보안"},

    # ---------------- 협력업체 ----------------
    {"dept":"협력업체","name":"신성휴","pos":"소장","ext":"-","mobile":"010-7161-2201","work":"미화 협력업체 총괄"},
    {"dept":"협력업체","name":"이규용","pos":"소장","ext":"8300","mobile":"010-8883-6580","work":"보안 협력업체 총괄"},
]

# ---------------- 검색 ----------------
search = st.text_input("🔍 검색")

filtered = data
if search:
    s = search.lower()
    filtered = [x for x in data if s in str(x).lower()]

# ---------------- 출력 ----------------
for i, c in enumerate(filtered):

    is_fav = c["name"] in st.session_state.fav
    star = "★" if is_fav else "☆"

    st.markdown('<div class="card">', unsafe_allow_html=True)

    col1, col2 = st.columns([0.7, 0.3])

    with col1:
        c1, c2 = st.columns([0.1, 0.9])

        # ⭐ 진짜 버튼
        with c1:
            if st.button(star, key=f"fav{i}"):
                if is_fav:
                    st.session_state.fav.remove(c["name"])
                else:
                    st.session_state.fav.add(c["name"])
                st.rerun()

        with c2:
            st.markdown(f"**{c['name']}**")
            st.caption(f"{c['pos']} · {c['dept']}")

        st.markdown(f'<div class="work">{c["work"]}</div>', unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <a class="tel-btn" href="tel:{c['ext'].replace('-','')}">내선</a>
        <a class="tel-btn" href="tel:{c['mobile'].replace('-','')}">휴대폰</a>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
