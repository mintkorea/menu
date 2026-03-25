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
    position:relative;
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
}

.star {
    font-size:18px;
    color:#ffc107;
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

/* ⭐ 버튼 숨기기 (핵심) */
button[kind="secondary"] {
    position:absolute;
    left:14px;
    top:14px;
    width:20px;
    height:20px;
    opacity:0;
    z-index:10;
}
</style>
""", unsafe_allow_html=True)

st.title("📞 성의교정 비상연락망")

# ---------------- 데이터 ----------------
data = [
    {"dept":"총무팀","name":"박현욱","pos":"팀장","ext":"02-3147-8190","mobile":"010-6245-0589","work":"부서업무 총괄"},
    {"dept":"총무팀","name":"김종래","pos":"차장","ext":"02-3147-8191","mobile":"010-9056-3701","work":"시설 관리"},
    {"dept":"총무팀","name":"장영섭","pos":"차장","ext":"02-3147-8193","mobile":"010-5072-0919","work":"예비군"},
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

    # ⭐ UI (보이는 별)
    st.markdown(f"""<div class="row">

<div class="left">
    <span class="star">{star}</span>
    <div>
        <div class="name">{c['name']}</div>
        <div class="sub">{c['pos']} · {c['dept']}</div>
    </div>
</div>

<div class="right">
    <a class="tel-btn" href="tel:{c['ext'].replace('-','')}">내선</a>
    <a class="tel-btn" href="tel:{c['mobile'].replace('-','')}">휴대폰</a>
</div>

</div>""", unsafe_allow_html=True)

    # ⭐ 실제 클릭 영역 (투명 버튼)
    if st.button("⭐", key=f"fav{i}"):
        if is_fav:
            st.session_state.fav.remove(c["name"])
        else:
            st.session_state.fav.add(c["name"])
        st.rerun()

    st.markdown(f'<div class="work">{c["work"]}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
