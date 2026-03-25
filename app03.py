import streamlit as st
import json

# ----------------------------
# 1. 기본 설정
# ----------------------------
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# ----------------------------
# 2. CSS (끝판왕 UI)
# ----------------------------
st.markdown("""
<style>
.block-container { padding-top: 10px; }

.contact-card {
    padding: 14px;
    border-radius: 14px;
    background: #ffffff;
    margin-bottom: 10px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

.name-row {
    display: flex;
    align-items: center;
    gap: 6px;
    flex-wrap: nowrap;
}

.star {
    font-size: 18px;
    cursor: pointer;
    color: #ffc107;
}

.name-text {
    font-size: 1.05rem;
    font-weight: 700;
}

.pos-text {
    font-size: 0.8rem;
    color: #666;
}

.work-text {
    font-size: 0.85rem;
    color: #888;
    margin-top: 4px;
}

.right-box {
    text-align: right;
}

.ext-btn {
    display: block;
    font-size: 0.95rem;
    font-weight: bold;
    color: #007bff;
    text-decoration: none;
}

.mobile-btn {
    display: block;
    font-size: 0.8rem;
    color: #999;
    text-decoration: none;
}

/* 버튼 숨김 */
button[kind="secondary"] {
    padding: 0;
    border: none;
    background: transparent;
}

</style>
""", unsafe_allow_html=True)

st.title("📞 성의교정 비상연락망")

# ----------------------------
# 3. 데이터
# ----------------------------
@st.cache_data
def get_data():
    return [
        {"dept":"총무팀","name":"박현욱","pos":"팀장","ext":"02-3147-8190","mobile":"010-6245-0589","work":"부서업무 총괄"},
        {"dept":"총무팀","name":"김종래","pos":"차장","ext":"02-3147-8191","mobile":"010-9056-3701","work":"시설 및 자산관리"},
        {"dept":"총무팀","name":"장영섭","pos":"차장","ext":"02-3147-8193","mobile":"010-5072-0919","work":"예비군, 민방위"},
        {"dept":"총무팀","name":"주종호","pos":"과장","ext":"02-3147-8202","mobile":"010-3324-1187","work":"보안, 대관"},
        {"dept":"안전관리","name":"주상건","pos":"차장","ext":"02-2258-7135","mobile":"010-9496-6483","work":"시신기증"},
        {"dept":"비서실","name":"이경자","pos":"부장","ext":"02-3147-8071","mobile":"010-6306-3652","work":"비서"},
    ]

data = get_data()

# ----------------------------
# 4. 즐겨찾기 (브라우저 저장)
# ----------------------------
if "favorites" not in st.session_state:
    st.session_state.favorites = set()

# ----------------------------
# 5. 검색 UI
# ----------------------------
c1, c2 = st.columns([3,1])

with c1:
    search = st.text_input("🔍 검색", placeholder="이름, 부서, 업무")

with c2:
    only_fav = st.checkbox("⭐ 즐겨찾기")

# ----------------------------
# 6. 필터
# ----------------------------
filtered = data

if search:
    s = search.lower()
    filtered = [x for x in filtered if s in str(x).lower()]

if only_fav:
    filtered = [x for x in filtered if x['name'] in st.session_state.favorites]

st.caption(f"{len(filtered)}명")

# ----------------------------
# 7. 카드 출력 (핵심)
# ----------------------------
for i, c in enumerate(filtered):

    is_fav = c["name"] in st.session_state.favorites
    star = "★" if is_fav else "☆"

    ext = c["ext"].replace("-", "")
    mobile = c["mobile"].replace("-", "")

    ext_link = f"tel:{ext}" if ext.isdigit() else ""
    mobile_link = f"tel:{mobile}"

    col1, col2 = st.columns([0.72, 0.28])

    with col1:
        st.markdown(f"""
        <div class="contact-card">
            <div class="name-row">
                <span class="star">{star}</span>
                <span class="name-text">{c["name"]}</span>
                <span class="pos-text">{c["pos"]} ({c["dept"]})</span>
            </div>
            <div class="work-text">{c["work"]}</div>
        """, unsafe_allow_html=True)

        # ⭐ 클릭 처리
        if st.button("", key=f"fav{i}"):
            if is_fav:
                st.session_state.favorites.remove(c["name"])
            else:
                st.session_state.favorites.add(c["name"])
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="contact-card right-box">

            {"<a class='ext-btn' href='"+ext_link+"'>" if ext_link else ""}
            {c["ext"]}
            {"</a>" if ext_link else ""}

            <a class="mobile-btn" href="{mobile_link}">
            {c["mobile"]}
            </a>

        </div>
        """, unsafe_allow_html=True)
