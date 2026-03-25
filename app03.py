import streamlit as st

st.set_page_config(page_title="성의교정 연락망", layout="wide")

# ---------------- 상태 ----------------
if "fav" not in st.session_state:
    st.session_state.fav = set()

# ---------------- 즐겨찾기 클릭 처리 ----------------
query = st.query_params

if "fav" in query:
    name = query["fav"]

    if name in st.session_state.fav:
        st.session_state.fav.remove(name)
    else:
        st.session_state.fav.add(name)

    st.query_params.clear()
    st.rerun()

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
</style>
""", unsafe_allow_html=True)

st.title("📞 성의교정 비상연락망")

# ---------------- 데이터 ----------------
def get_data():
    return [
        {"dept":"총무팀","name":"박현욱","pos":"팀장","ext":"02-3147-8190","mobile":"010-6245-0589","work":"부서업무 총괄"},
        {"dept":"총무팀","name":"김종래","pos":"차장","ext":"02-3147-8191","mobile":"010-9056-3701","work":"시설 및 자산관리"},
        {"dept":"총무팀","name":"장영섭","pos":"차장","ext":"02-3147-8193","mobile":"010-5072-0919","work":"예비군, 민방위"},
        {"dept":"총무팀","name":"주종호","pos":"과장","ext":"02-3147-8202","mobile":"010-3324-1187","work":"보안, 대관"},
        {"dept":"총무팀","name":"강은희","pos":"대리","ext":"02-3147-8206","mobile":"010-9127-1021","work":"문서배부, 행사"},
        {"dept":"총무팀","name":"김보라","pos":"선임","ext":"02-3147-8192","mobile":"010-8073-0527","work":"차량등록, 운영비"},
        {"dept":"안전관리","name":"주상건","pos":"차장","ext":"02-2258-7135","mobile":"010-9496-6483","work":"시신기증"},
        {"dept":"비서실","name":"이경자","pos":"부장","ext":"02-3147-8071","mobile":"010-6306-3652","work":"비서"},
    ]

data = get_data()

# ---------------- 검색 ----------------
search = st.text_input("🔍 검색 (이름/부서/업무)")

filtered = data
if search:
    s = search.lower()
    filtered = [x for x in data if s in str(x).lower()]

st.caption(f"{len(filtered)}명")

# ---------------- 출력 ----------------
for c in filtered:

    is_fav = c["name"] in st.session_state.fav
    star = "★" if is_fav else "☆"

    st.markdown('<div class="card">', unsafe_allow_html=True)

    html = f"""<div class="row">

<div class="left">
    <a href="?fav={c['name']}" style="text-decoration:none;">
        <span class="star">{star}</span>
    </a>
    <div class="name-wrap">
        <div class="name">{c['name']}</div>
        <div class="sub">{c['pos']} · {c['dept']}</div>
    </div>
</div>

<div class="right">
    <a class="tel-btn" href="tel:{c['ext'].replace('-','')}">내선</a>
    <a class="tel-btn" href="tel:{c['mobile'].replace('-','')}">휴대폰</a>
</div>

</div>"""

    st.markdown(html, unsafe_allow_html=True)

    st.markdown(f'<div class="work">{c["work"]}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
