import streamlit as st
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import tempfile

# -----------------------------
# 1. 설정
# -----------------------------
st.set_page_config(page_title="비상연락망", layout="wide")

st.title("📞 총무팀 비상연락망")

# 👉 구글시트 ID 입력
SHEET_ID = "여기에_시트ID"
SHEET_NAME = "Sheet1"

# -----------------------------
# 2. 데이터 로드 (구글시트)
# -----------------------------
@st.cache_data(ttl=60)
def load_data():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
    df = pd.read_csv(url)
    return df

df = load_data()

# -----------------------------
# 3. 전화번호 변환
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
# 4. 검색 / 필터
# -----------------------------
col1, col2 = st.columns([2,1])

with col1:
    keyword = st.text_input("🔍 검색 (이름/업무)")

with col2:
    dept_list = ["전체"] + sorted(df["부서"].dropna().unique().tolist())
    selected_dept = st.selectbox("부서", dept_list)

filtered_df = df.copy()

if keyword:
    filtered_df = filtered_df[
        df["이름"].str.contains(keyword, case=False, na=False) |
        df["업무"].str.contains(keyword, case=False, na=False)
    ]

if selected_dept != "전체":
    filtered_df = filtered_df[filtered_df["부서"] == selected_dept]

# -----------------------------
# 5. 즐겨찾기
# -----------------------------
if "fav" not in st.session_state:
    st.session_state.fav = set()

# -----------------------------
# 6. UI 스타일
# -----------------------------
st.markdown("""
<style>
.card {
    border-bottom: 1px solid #ddd;
    padding: 10px;
}
.name {font-weight:bold; font-size:18px;}
.meta {color:#666; font-size:13px;}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 7. 출력
# -----------------------------
st.markdown("### 📋 연락처")

for i, row in filtered_df.iterrows():

    is_fav = i in st.session_state.fav
    star = "⭐" if is_fav else "☆"

    col1, col2 = st.columns([10,1])

    with col1:
        st.markdown(f"""
        <div class="card">
        <div class="name">{row['이름']} ({row['직급']})</div>
        <div class="meta">{row['부서']} | {row['업무']}</div>
        <div>
        📞 <a href="tel:{row['전화']}">{row['전화']}</a> /
        📱 <a href="tel:{row['휴대폰']}">{row['휴대폰']}</a>
        </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if st.button(star, key=i):
            if is_fav:
                st.session_state.fav.remove(i)
            else:
                st.session_state.fav.add(i)

# -----------------------------
# 8. PDF 생성
# -----------------------------
st.divider()
st.markdown("### 📄 PDF 다운로드")

if st.button("PDF 생성"):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

    doc = SimpleDocTemplate(tmp.name)
    styles = getSampleStyleSheet()

    content = []

    for _, row in filtered_df.iterrows():
        text = f"{row['이름']} ({row['직급']})<br/>{row['부서']} | {row['업무']}<br/>{row['전화']} / {row['휴대폰']}"
        content.append(Paragraph(text, styles["Normal"]))
        content.append(Spacer(1, 10))

    doc.build(content)

    with open(tmp.name, "rb") as f:
        st.download_button("📥 다운로드", f, file_name="contacts.pdf")
