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
# 검색 / 필터
# -----------------------------
keyword = st.text_input("🔍 검색 (이름/업무)")

if keyword:
    df = df[
        df["이름"].astype(str).str.contains(keyword, case=False, na=False) |
        df["업무"].astype(str).str.contains(keyword, case=False, na=False)
    ]

# -----------------------------
# 화면 출력
# -----------------------------
st.markdown("### 📋 연락처 목록")

for _, row in df.iterrows():
    tel = str(row["휴대폰"]).replace("-", "")

    st.markdown(f"""
    <div style="padding:10px;border-bottom:1px solid #ddd;">
        <b style="font-size:18px;">{row['이름']} ({row['직급']})</b><br>
        <span style="color:#666;">{row['부서']} | {row['업무']}</span><br>
        📞 <a href="tel:{tel}">{row['휴대폰']}</a> /
        ☎ {row['내선']}
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# PDF용 HTML 생성
# -----------------------------
st.divider()
st.markdown("### 📄 PDF 저장")

html = """
<html>
<head>
<meta charset="utf-8">
<style>
body { font-family: Arial; }
.card {
    border-bottom:1px solid #ccc;
    padding:10px;
}
.name {
    font-size:18px;
    font-weight:bold;
}
.meta {
    color:#555;
    font-size:13px;
}
</style>
</head>
<body>
<h2>총무팀 비상연락망</h2>
"""

for _, row in df.iterrows():
    html += f"""
    <div class="card">
        <div class="name">{row['이름']} ({row['직급']})</div>
        <div class="meta">{row['부서']} | {row['업무']}</div>
        <div>{row['휴대폰']} / {row['내선']}</div>
    </div>
    """

html += "</body></html>"

# 다운로드 버튼
st.download_button(
    "📥 HTML 다운로드 (PDF 변환용)",
    html,
    file_name="비상연락망.html",
    mime="text/html"
)