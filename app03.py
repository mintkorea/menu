import streamlit as st
import pandas as pd

# -----------------------------
# 1. 기본 설정
# -----------------------------
st.set_page_config(page_title="비상연락망", layout="wide")

st.title("📞 총무팀 비상연락망")

# -----------------------------
# 2. 구글시트 설정
# -----------------------------
SHEET_ID = "1sGpEFXLNsZm76lRPuyS4vLGmTQGkAYtNHt1f03mx0h0"
SHEET_NAME = "Sheet1"

# -----------------------------
# 3. 데이터 로드
# -----------------------------
@st.cache_data(ttl=60)
def load_data():
    try:
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
        df = pd.read_csv(url)
        return df
    except:
        st.error("❌ 구글시트 불러오기 실패 (공유 설정 확인)")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

# -----------------------------
# 4. 검색
# -----------------------------
keyword = st.text_input("🔍 검색 (이름/업무)")

if keyword:
    df = df[
        df["이름"].astype(str).str.contains(keyword, case=False, na=False) |
        df["업무"].astype(str).str.contains(keyword, case=False, na=False)
    ]

# -----------------------------
# 5. 출력 (모바일 최적)
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
# 6. HTML → PDF 기능
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

st.download_button(
    "📥 HTML 다운로드 (PDF 변환용)",
    html,
    file_name="비상연락망.html",
    mime="text/html"
)

# -----------------------------
# 7. 새로고침 버튼
# -----------------------------
st.divider()

if st.button("🔄 데이터 새로고침"):
    st.cache_data.clear()
    st.rerun()