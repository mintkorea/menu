import streamlit as st
import pandas as pd
import tempfile

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame, PageTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

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
        return pd.read_csv(url)
    except:
        st.error("❌ 구글시트 불러오기 실패")
        return pd.DataFrame()

df = load_data()
if df.empty:
    st.stop()

# -----------------------------
# 4. 전화 변환
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

# 👉 정렬 추가 (가독성)
filtered_df = filtered_df.sort_values(by=["부서", "이름"])

# -----------------------------
# 6. 즐겨찾기
# -----------------------------
if "fav" not in st.session_state:
    st.session_state.fav = set()

show_fav = st.checkbox("⭐ 즐겨찾기만 보기")

if show_fav:
    filtered_df = filtered_df[filtered_df.index.isin(st.session_state.fav)]

# -----------------------------
# 7. 스타일 (모바일 최적)
# -----------------------------
st.markdown("""
<style>
.card {
    border-bottom: 1px solid #ddd;
    padding: 10px;
}

.name {
    font-weight: bold;
    font-size: 16px;
}

/* 줄바꿈 허용 */
.meta {
    color: #666;
    font-size: 13px;
    white-space: normal !important;
    word-break: keep-all;
}

.phone {
    margin-top: 5px;
    word-break: break-all;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 8. 출력 (핵심 개선)
# -----------------------------
st.markdown("### 📋 연락처 목록")

for i, row in filtered_df.iterrows():

    is_fav = i in st.session_state.fav
    star = "⭐" if is_fav else "☆"

    # ⭐ 클릭 영역 (작게)
    col_star, col_main = st.columns([1, 9])

    with col_star:
        if st.button(star, key=f"fav_{i}"):
            if is_fav:
                st.session_state.fav.remove(i)
            else:
                st.session_state.fav.add(i)

    with col_main:
        tel = row['전화']
        mobile = row['휴대폰']

        st.markdown(f"""
        <div class="card">
            <div class="name">{row['이름']} ({row['직급']})</div>
            <div class="meta">{row['부서']}</div>
            <div class="meta">{row['업무']}</div>
            <div class="phone">
                📞 <a href="tel:{tel}">{tel}</a> /
                📱 <a href="tel:{mobile}">{mobile}</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------
# 9. PDF (2단 보고서)
# -----------------------------
st.divider()
st.markdown("### 📄 PDF 다운로드")

if st.button("📄 PDF 생성"):

    try:
        pdfmetrics.registerFont(TTFont('KoreanFont', 'NanumGothic.ttf'))
    except:
        st.error("❌ NanumGothic.ttf 필요")
        st.stop()

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

    doc = SimpleDocTemplate(tmp.name, leftMargin=20, rightMargin=20, topMargin=20, bottomMargin=20)

    styles = getSampleStyleSheet()
    styles["Normal"].fontName = 'KoreanFont'
    styles["Normal"].fontSize = 8.5
    styles["Normal"].leading = 10

    # 2단 컬럼
    frame1 = Frame(doc.leftMargin, doc.bottomMargin, (doc.width/2)-5, doc.height, id='col1')
    frame2 = Frame(doc.leftMargin + (doc.width/2)+5, doc.bottomMargin, (doc.width/2)-5, doc.height, id='col2')

    doc.addPageTemplates([PageTemplate(id='TwoCol', frames=[frame1, frame2])])

    content = []

    content.append(Paragraph("<b>총무팀 비상연락망</b>", styles["Normal"]))
    content.append(Spacer(1, 8))

    groups = filtered_df.groupby("부서")

    for dept, group in groups:
        content.append(Paragraph(f"<b>{dept}</b>", styles["Normal"]))
        content.append(Spacer(1, 4))

        for _, row in group.iterrows():
            text = f"""
            <b>{row['이름']} ({row['직급']})</b><br/>
            {row['업무']}<br/>
            {row['전화']} / {row['휴대폰']}
            """
            content.append(Paragraph(text, styles["Normal"]))
            content.append(Spacer(1, 6))

    doc.build(content)

    with open(tmp.name, "rb") as f:
        st.download_button("📥 PDF 다운로드", f, file_name="비상연락망_보고서.pdf")

# -----------------------------
# 10. 새로고침
# -----------------------------
st.divider()

if st.button("🔄 데이터 새로고침"):
    st.cache_data.clear()
    st.rerun()
