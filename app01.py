import streamlit as st
import pandas as pd

st.set_page_config(page_title="비상연락망", layout="wide")

st.title("📞 총무팀 비상연락망")

# -----------------------------
# 구글시트 설정
# -----------------------------
SHEET_ID = "1sGpEFXLNsZm76lRPuyS4vLGmTQGkAYtNHt1f03mx0h0"
SHEET_NAME = "Sheet1"

@st.cache_data(ttl=60)
def load_data():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
    return pd.read_csv(url)

df = load_data()

# -----------------------------
# 검색
# -----------------------------
keyword = st.text_input("🔍 검색")

if keyword:
    df = df[
        df["이름"].astype(str).str.contains(keyword, case=False, na=False) |
        df["업무"].astype(str).str.contains(keyword, case=False, na=False)
    ]

# -----------------------------
# 출력
# -----------------------------
for _, row in df.iterrows():
    tel = str(row["휴대폰"]).replace("-", "")

    st.markdown(f"""
    ### {row['이름']} ({row['직급']})
    - 📞 [{row['휴대폰']}](tel:{tel})
    - 🏢 {row['부서']}
    - 💼 {row['업무']}
    - ☎ {row['내선']}
    """)

# -----------------------------
# HTML 다운로드 (PDF 대체)
# -----------------------------
st.divider()
st.markdown("### 📄 PDF 저장")

html = "<h2>비상연락망</h2>"

for _, row in df.iterrows():
    html += f"""
    <p>
    <b>{row['이름']} ({row['직급']})</b><br>
    {row['부서']} | {row['업무']}<br>
    {row['휴대폰']} / {row['내선']}
    </p>
    """

st.download_button("📥 HTML 다운로드", html, file_name="contacts.html")
