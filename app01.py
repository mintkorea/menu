import streamlit as st

# 기본 설정
st.set_page_config(page_title="연락망", layout="wide")

st.title("📞 성의교정 연락망")

# 데이터 (아주 간단)
contacts = [
    {"이름": "박현욱", "직급": "팀장", "부서": "총무", "전화": "010-6245-0589", "내선": "8190"},
    {"이름": "김종래", "직급": "차장", "부서": "총무", "전화": "010-9056-3701", "내선": "8191"},
    {"이름": "장영섭", "직급": "차장", "부서": "총무", "전화": "010-5072-0919", "내선": "8193"},
]

# 검색
search = st.text_input("🔍 이름 검색")

# 필터
if search:
    contacts = [c for c in contacts if search in c["이름"]]

# 출력 (HTML 없음 → 안정)
for c in contacts:
    st.write(f"이름: {c['이름']}")
    st.write(f"직급: {c['직급']} / 부서: {c['부서']}")
    st.write(f"전화: {c['전화']} / 내선: {c['내선']}")
    st.write("---")

if not contacts:
    st.write("검색 결과 없음")