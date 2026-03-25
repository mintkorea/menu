import streamlit as st

st.set_page_config(page_title="성의교정 연락망", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
.card {
    background:#f8f9fb;
    padding:14px;
    border-radius:14px;
    margin-bottom:10px;
}

/* 한 줄 구조 핵심 */
.row {
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:10px;
}

/* 왼쪽 영역 */
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

/* 텍스트 */
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

/* 오른쪽 버튼 */
.right {
    display:flex;
    gap:6px;
    flex-shrink:0;
}

.tel-btn {
    padding:4px 8px;
    border-radius:8px;
    font-size:0.75rem;
    text-decoration:none;
    background:#e9ecef;
    color:#333;
}

/* 줄바꿈 방지 핵심 */
.name-wrap {
    white-space:nowrap;
    overflow:hidden;
    text-overflow:ellipsis;
}
</style>
""", unsafe_allow_html=True)

st.title("📞 성의교정 비상연락망")

# ---------------- 데이터 ----------------
data = [
    {"name":"박현욱","pos":"팀장","dept":"총무팀","ext":"02-3147-8190","mobile":"010-6245-0589","work":"부서업무 총괄"},
    {"name":"김종래","pos":"차장","dept":"총무팀","ext":"02-3147-8191","mobile":"010-9056-3701","work":"시설 관리"},
    {"name":"장영섭","pos":"차장","dept":"총무팀","ext":"02-3147-8193","mobile":"010-5072-0919","work":"예비군"},
]

# ---------------- 상태 ----------------
if "fav" not in st.session_state:
    st.session_state.fav = set()

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

    # 카드 시작
    st.markdown('<div class="card">', unsafe_allow_html=True)

    # ----------- 한 줄 (핵심) -----------
    st.markdown(f"""
    <div class="row">
        
        <div class="left">
            <div class="star">{star}</div>
            <div class="name-wrap">
                <div class="name">{c['name']}</div>
                <div class="sub">{c['pos']} · {c['dept']}</div>
            </div>
        </div>

        <div class="right">
            <a class="tel-btn" href="tel:{c['ext'].replace('-','')}">내선</a>
            <a class="tel-btn" href="tel:{c['mobile'].replace('-','')}">휴대폰</a>
        </div>

    </div>
    """, unsafe_allow_html=True)

    # ----------- 업무 -----------    
    st.markdown(f'<div class="work">{c["work"]}</div>', unsafe_allow_html=True)

    # ⭐ 즐겨찾기 버튼 (보이지 않게 위에 덮기)
    if st.button("⭐", key=f"fav{i}"):
        if is_fav:
            st.session_state.fav.remove(c["name"])
        else:
            st.session_state.fav.add(c["name"])
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
