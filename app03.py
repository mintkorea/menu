import streamlit as st

st.set_page_config(page_title="성의교정 연락망", layout="wide")

st.title("📞 성의교정 비상연락망")

# ----------------------
# 데이터 (전체 넣으세요)
# ----------------------
data = [
    {"name":"박현욱","pos":"팀장","dept":"총무팀","ext":"02-3147-8190","mobile":"010-6245-0589","work":"부서업무 총괄"},
    {"name":"김종래","pos":"차장","dept":"총무팀","ext":"02-3147-8191","mobile":"010-9056-3701","work":"시설 관리"},
    {"name":"장영섭","pos":"차장","dept":"총무팀","ext":"02-3147-8193","mobile":"010-5072-0919","work":"예비군"},
    {"name":"주종호","pos":"과장","dept":"총무팀","ext":"02-3147-8202","mobile":"010-3324-1187","work":"보안"},
]

# ----------------------
# 상태
# ----------------------
if "fav" not in st.session_state:
    st.session_state.fav = set()

# ----------------------
# 검색
# ----------------------
search = st.text_input("🔍 검색 (이름/부서/업무)")

filtered = data
if search:
    s = search.lower()
    filtered = [x for x in data if s in str(x).lower()]

st.caption(f"{len(filtered)}명")

# ----------------------
# 출력
# ----------------------
for i, c in enumerate(filtered):

    is_fav = c["name"] in st.session_state.fav
    star = "★" if is_fav else "☆"

    with st.container():
        col1, col2 = st.columns([0.75, 0.25])

        # ---------------- 좌측 ----------------
        with col1:
            # ⭐ 즐겨찾기 + 이름
            c1, c2 = st.columns([0.08, 0.92])

            with c1:
                if st.button(star, key=f"fav{i}"):
                    if is_fav:
                        st.session_state.fav.remove(c["name"])
                    else:
                        st.session_state.fav.add(c["name"])
                    st.rerun()

            with c2:
                st.markdown(f"**{c['name']}** ({c['pos']} / {c['dept']})")

            st.caption(c["work"])

        # ---------------- 우측 ----------------
        with col2:
            # 📞 내선 / 휴대폰 선택 (링크 확실히 보이게)
            st.markdown(f"""
            📞 **전화**
            
            - [내선 {c['ext']}](tel:{c['ext'].replace('-', '')})
            - [휴대폰 {c['mobile']}](tel:{c['mobile'].replace('-', '')})
            """)

    st.divider()
