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
    gap:10px;
}

.left {
    display:flex;
    align-items:center;
    gap:8px;
    flex:1;
    min-width:0;
}

.star {
    font-size:18px;
    color:#ffc107;
}

/* 한 줄 유지 */
.name-wrap {
    white-space:nowrap;
    overflow:hidden;
    text-overflow:ellipsis;
}

.name {
    font-weight:700;
    font-size:1rem;
}

.sub {
    font-size:0.8rem;
    color:#888;
    margin-left:4px;
}

.work {
    font-size:0.8rem;
    color:#888;
    margin-top:4px;
}

.right {
    display:flex;
    gap:6px;
    flex-shrink:0;
}

.tel-btn {
    padding:5px 9px;
    border-radius:8px;
    font-size:0.75rem;
    text-decoration:none;
    background:#e9ecef;
    color:#333;
}

/* ⭐ 버튼 스타일 */
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
    {"dept":"총무팀","name":"박현욱","pos":"팀장","ext":"02-3147-8190","mobile":"010-6245-0589","work":"부서업무 총괄"},
    {"dept":"총무팀","name":"김종래","pos":"차장","ext":"02-3147-8191","mobile":"010-9056-3701","work":"시설 및 자산관리"},
    {"dept":"총무팀","name":"장영섭","pos":"차장","ext":"02-3147-8193","mobile":"010-5072-0919","work":"예비군, 민방위"},
    {"dept":"총무팀","name":"주종호","pos":"과장","ext":"02-3147-8202","mobile":"010-3324-1187","work":"보안, 대관"},
    {"dept":"총무팀","name":"강은희","pos":"대리","ext":"02-3147-8206","mobile":"010-9127-1021","work":"문서배부, 행사"},
    {"dept":"총무팀","name":"김보라","pos":"선임","ext":"02-3147-8192","mobile":"010-8073-0527","work":"차량등록, 운영비"},
    {"dept":"총무팀","name":"노종현","pos":"책임","ext":"02-3147-8195","mobile":"010-9425-3109","work":"행사, 회의자료"},
    {"dept":"총무팀","name":"고규호","pos":"책임","ext":"02-3147-8196","mobile":"010-3381-8870","work":"캘린더, 인증평가"},
    {"dept":"총무팀","name":"김두리","pos":"사원","ext":"02-3147-8204","mobile":"010-9661-1257","work":"기숙사"},
    {"dept":"총무팀","name":"임세리","pos":"사원","ext":"02-3147-8197","mobile":"010-3281-1229","work":"우편, 정수기"},
    {"dept":"총무팀","name":"김종식","pos":"사원","ext":"-","mobile":"010-9256-6904","work":"업무지원"},

    {"dept":"안전관리","name":"윤호열","pos":"UM","ext":"02-3147-8199","mobile":"010-2623-7963","work":"소방/방재"},
    {"dept":"안전관리","name":"주상건","pos":"차장","ext":"02-2258-7135","mobile":"010-9496-6483","work":"시신기증"},
    {"dept":"안전관리","name":"곽정승","pos":"과장","ext":"02-3147-8194","mobile":"010-5218-6504","work":"사업계획"},
    {"dept":"안전관리","name":"박일용","pos":"과장","ext":"02-3147-8201","mobile":"010-6205-7751","work":"계약"},
    {"dept":"안전관리","name":"이경종","pos":"부장","ext":"02-3147-8203","mobile":"010-2623-7963","work":"교수업적"},
    {"dept":"안전관리","name":"김준석","pos":"과장","ext":"02-3147-8205","mobile":"010-9256-6904","work":"연구실 안전"},

    {"dept":"비서실","name":"이경자","pos":"부장","ext":"02-3147-8071","mobile":"010-6306-3652","work":"비서"},
    {"dept":"비서실","name":"이상희","pos":"과장","ext":"02-3147-8068","mobile":"010-3445-0623","work":"비서"},
    {"dept":"비서실","name":"박은영","pos":"과장","ext":"02-3147-8069","mobile":"010-5348-6849","work":"비서"},
]

# ---------------- 검색 ----------------
search = st.text_input("🔍 검색 (이름/부서/업무)")

filtered = data
if search:
    s = search.lower()
    filtered = [
        x for x in data
        if s in x["name"].lower()
        or s in x["dept"].lower()
        or s in x["work"].lower()
    ]

st.caption(f"{len(filtered)}명")

# ---------------- 출력 ----------------
for i, c in enumerate(filtered):

    is_fav = c["name"] in st.session_state.fav
    star = "★" if is_fav else "☆"

    st.markdown('<div class="card">', unsafe_allow_html=True)

    col1, col2 = st.columns([0.75, 0.25])

    with col1:
        c1, c2 = st.columns([0.08, 0.92])

        # ⭐ 즐겨찾기 버튼
        with c1:
            if st.button(star, key=f"fav{i}"):
                if is_fav:
                    st.session_state.fav.remove(c["name"])
                else:
                    st.session_state.fav.add(c["name"])
                st.rerun()

        with c2:
            st.markdown(f"""
            <div class="name-wrap">
                <span class="name">{c['name']}</span>
                <span class="sub">{c['pos']} · {c['dept']}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f'<div class="work">{c["work"]}</div>', unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        {"<a class='tel-btn' href='tel:"+c['ext'].replace('-','')+"'>내선</a>" if c['ext'] != "-" else ""}
        <a class="tel-btn" href="tel:{c['mobile'].replace('-','')}">휴대폰</a>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
