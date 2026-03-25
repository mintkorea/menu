import streamlit as st
import sqlite3
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# ----------------------
# DB
# ----------------------
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

# ----------------------
# 데이터 (전체 복구)
# ----------------------
data = [
    {"name":"박현욱","pos":"팀장","dept":"총무팀","ext":"0231478190","mobile":"01062450589","work":"부서업무 총괄"},
    {"name":"김종래","pos":"차장","dept":"총무팀","ext":"0231478191","mobile":"01090563701","work":"시설 관리"},
    {"name":"장영섭","pos":"차장","dept":"총무팀","ext":"0231478193","mobile":"01050720919","work":"예비군"},
    {"name":"주종호","pos":"과장","dept":"총무팀","ext":"0231478202","mobile":"01033241187","work":"보안"},
]

# ----------------------
# UI
# ----------------------
st.title("📞 성의교정 비상연락망")

search = st.text_input("검색")

if search:
    data = [x for x in data if search in str(x)]

# ----------------------
# HTML UI (핵심)
# ----------------------
html = """
<style>
.card {
 padding:12px;
 border-radius:12px;
 background:#f7f7f7;
 margin-bottom:8px;
}
.name {font-weight:bold;}
.work {font-size:0.8rem;color:#666;}
</style>

<script>
function callSelect(ext, mobile){
 let choice = confirm("확인 = 내선 / 취소 = 휴대폰");
 if(choice){
   window.location.href = "tel:" + ext;
 }else{
   window.location.href = "tel:" + mobile;
 }
}
</script>
"""

for c in data:
    html += f"""
<div class="card" onclick="callSelect('{c['ext']}','{c['mobile']}')">
 <div class="name">⭐ {c['name']} ({c['pos']})</div>
 <div class="work">{c['work']}</div>
</div>
"""

components.html(html, height=800, scrolling=True)
