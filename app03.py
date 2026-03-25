import streamlit as st
import sqlite3

st.set_page_config(page_title="성의교정 연락망", layout="wide")

# ----------------------------
# DB 초기화
# ----------------------------
conn = sqlite3.connect("fav.db", check_same_thread=False)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS fav (name TEXT PRIMARY KEY)")
conn.commit()

def is_fav(name):
    cur.execute("SELECT 1 FROM fav WHERE name=?", (name,))
    return cur.fetchone() is not None

def toggle_fav(name):
    if is_fav(name):
        cur.execute("DELETE FROM fav WHERE name=?", (name,))
    else:
        cur.execute("INSERT INTO fav VALUES (?)", (name,))
    conn.commit()

# ----------------------------
# CSS (카톡 스타일)
# ----------------------------
st.markdown("""
<style>
.chat-card {
    padding: 12px;
    border-radius: 16px;
    background: #f7f7f7;
    margin-bottom: 8px;
}

.name-row {
    display:flex;
    align-items:center;
    gap:6px;
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
    font-size:0.85rem;
    color:#888;
    margin-top:4px;
}

.call-btn {
    margin-top:8px;
    display:flex;
    gap:6px;
}

button[kind="secondary"] {
    border:none;
    background:transparent;
}
</style>
""", unsafe_allow_html=True)

st.title("📞 성의교정 비상연락망")

# ----------------------------
# 데이터
# ----------------------------
data = [
    {"name":"박현욱","pos":"팀장","dept":"총무팀","ext":"02-3147-8190","mobile":"010-6245-0589","work":"부서업무 총괄"},
    {"name":"김종래","pos":"차장","dept":"총무팀","ext":"02-3147-8191","mobile":"010-9056-3701","work":"시설 관리"},
]

# ----------------------------
# 검색
# ----------------------------
search = st.text_input("🔍 검색")

if search:
    data = [x for x in data if search in str(x)]

# ----------------------------
# 출력
# ----------------------------
for i, c in enumerate(data):

    fav = is_fav(c["name"])
    star = "★" if fav else "☆"

    with st.container():
        st.markdown('<div class="chat-card">', unsafe_allow_html=True)

        # ⭐ 이름줄
        st.markdown(f"""
<div class="name-row">
<span class="star">{star}</span>
<span class="name">{c["name"]}</span>
<span class="sub">{c["pos"]} ({c["dept"]})</span>
</div>
<div class="work">{c["work"]}</div>
""", unsafe_allow_html=True)

        # ⭐ 즐겨찾기 버튼
        if st.button("⭐", key=f"fav{i}"):
            toggle_fav(c["name"])
            st.rerun()

        # 📞 전화 선택 UI
        with st.expander("📞 전화하기"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button("내선", key=f"ext{i}"):
                    st.markdown(f"<a href='tel:{c['ext']}'></a>", unsafe_allow_html=True)

            with col2:
                if st.button("휴대폰", key=f"mob{i}"):
                    st.markdown(f"<a href='tel:{c['mobile']}'></a>", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
