import streamlit as st

st.set_page_config(layout="wide")

st.title("📞 성의교정 비상연락망")

data = [
    {"name":"박현욱","pos":"팀장","dept":"총무팀","ext":"02-3147-8190","mobile":"010-6245-0589","work":"부서업무 총괄"},
    {"name":"김종래","pos":"차장","dept":"총무팀","ext":"02-3147-8191","mobile":"010-9056-3701","work":"시설관리"},
]

# CSS 안정형
st.markdown("""
<style>
.card {
 padding:12px;
 border-radius:12px;
 background:#f9f9f9;
 margin-bottom:10px;
}

.name-row {
 display:flex;
 align-items:center;
 gap:6px;
}

.name {
 font-weight:bold;
}

.work {
 font-size:0.8rem;
 color:#666;
}

.tel {
 margin-top:6px;
 display:flex;
 gap:10px;
}

a {
 text-decoration:none;
 color:blue;
}
</style>
""", unsafe_allow_html=True)

for i, c in enumerate(data):
    st.markdown(f"""
<div class="card">
 <div class="name-row">
   ⭐ <span class="name">{c['name']}</span>
   <span>({c['pos']})</span>
 </div>
 <div class="work">{c['work']}</div>
 <div class="tel">
   <a href="tel:{c['ext']}">내선</a>
   <a href="tel:{c['mobile']}">휴대폰</a>
 </div>
</div>
""", unsafe_allow_html=True)
