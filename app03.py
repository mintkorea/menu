import streamlit as st
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import tempfile

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
# 3. 데이터 로드 (수정 완료 버전)
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
# 4. 전화번호 변환
# -----------------------------
def format_phone(ext):
    ext = str(ext).strip()

    if ext.startswith("*1"):
        number = ext.replace("*1", "").replace("-", "")
        return f"02-2258-{number}"
    else:
        return f"02-3147-{ext}"

df["전화"] = df["내선"].apply(format_phone)

# -----------------------------
# 5. 검색 / 필터
# -----------------------------
col1, col2 = st.columns([2,1])

with col1:
    keyword = st.text_input("🔍 검색 (이름/업무)")

with col2:
    dept_list = ["전체"] + sorted(df["부서"].dropna().unique().tolist())
    selected_dept = st.selectbox("부서 선택", dept_list)

filtered_df = df.copy()

if keyword:
    filtered_df = filtered_df[
        df["이름"].astype(str).str.contains(keyword, case=False, na=False) |
        df["업무"].astype(str).str.contains(keyword, case=False, na=False)
    ]

if selected_dept != "전체":
    filtered_df = filtered_df[filtered_df["부서"] == selected_dept]

# -----------------------------
# 6. 즐겨찾기
# -----------------------------
if "fav" not in st.session_state:
    st.session_state.fav = set()

# -----------------------------
# 7. 스타일 (모바일 + PDF 느낌)
# -----------------------------
st.markdown("""
<style>
.card {
    border-bottom: 1px solid #ddd;
    padding: 10px;
}
.name {
    font-weight: bold;
    font-size: 18px;
}
.meta {
    color: #666;
    font-size: 13px;
}
.phone {
    margin-top: 5px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 8. 출력
# -----------------------------
st.markdown("### 📋 연락처 목록")

for i, row in filtered_df.iterrows():

    is_fav = i in st.session_state.fav
    star = "⭐" if is_fav else "☆"

    col1, col2 = st.columns([10,1])

    with col1:
        st.markdown(f"""
        <div class="card">
            <div class="name">{row['이름']} ({row['직급']})</div>
            <div class="meta">{row['부서']} | {row['업무']}</div>
            <div class="phone">
                📞 <a href="tel:{row['전화']}">{row['전화']}</a> /
                📱 <a href="tel:{row['휴대폰']}">{row['휴대폰']}</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if st.button(star, key=f"fav_{i}"):
            if is_fav:
                st.session_state.fav.remove(i)
            else:
                st.session_state.fav.add(i)

# -----------------------------
# 9. PDF 생성
# -----------------------------
st.divider()
st.markdown("### 📄 PDF 다운로드")

if st.button("📄 PDF 생성"):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

    doc = SimpleDocTemplate(tmp.name)
    styles = getSampleStyleSheet()

    content = []

    for _, row in filtered_df.iterrows():
        text = f"""
        {row['이름']} ({row['직급']})<br/>
        {row['부서']} | {row['업무']}<br/>
        {row['전화']} / {row['휴대폰']}
        """
        content.append(Paragraph(text, styles["Normal"]))
        content.append(Spacer(1, 10))

    doc.build(content)

    with open(tmp.name, "rb") as f:
        st.download_button(
            "📥 PDF 다운로드",
            f,
            file_name="총무팀_비상연락망.pdf"
        )

# -----------------------------
# 10. 새로고침 버튼 (중요)
# -----------------------------
st.divider()

if st.button("🔄 데이터 새로고침"):
    st.cache_data.clear()
    st.rerun()
