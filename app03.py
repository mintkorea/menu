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
# 5. 검색
# -----------------------------
keyword = st.text_input("🔍 검색")

if keyword:
    df = df[
        df["이름"].astype(str).str.contains(keyword, case=False, na=False) |
        df["업무"].astype(str).str.contains(keyword, case=False, na=False)
    ]

# -----------------------------
# 6. 출력
# -----------------------------
for _, row in df.iterrows():
    st.write(f"{row['이름']} ({row['직급']}) | {row['부서']} | {row['전화']}")

# -----------------------------
# 7. PDF (2단 컬럼)
# -----------------------------
st.divider()
st.markdown("### 📄 PDF 다운로드 (2단 보고서)")

if st.button("📄 PDF 생성"):

    try:
        pdfmetrics.registerFont(TTFont('KoreanFont', 'NanumGothic.ttf'))
    except:
        st.error("❌ NanumGothic.ttf 필요")
        st.stop()

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

    doc = SimpleDocTemplate(
        tmp.name,
        leftMargin=20,
        rightMargin=20,
        topMargin=20,
        bottomMargin=20
    )

    styles = getSampleStyleSheet()
    styles["Normal"].fontName = 'KoreanFont'
    styles["Normal"].fontSize = 8.5
    styles["Normal"].leading = 10

    # -----------------------------
    # 2단 컬럼 설정
    # -----------------------------
    frame1 = Frame(doc.leftMargin, doc.bottomMargin, (doc.width/2)-5, doc.height, id='col1')
    frame2 = Frame(doc.leftMargin + (doc.width/2)+5, doc.bottomMargin, (doc.width/2)-5, doc.height, id='col2')

    template = PageTemplate(id='TwoCol', frames=[frame1, frame2])
    doc.addPageTemplates([template])

    content = []

    # 제목
    content.append(Paragraph("<b>총무팀 비상연락망</b>", styles["Normal"]))
    content.append(Spacer(1, 8))

    df_sorted = df.sort_values(by=["부서", "이름"])
    groups = df_sorted.groupby("부서")

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
        st.download_button("📥 PDF 다운로드", f, file_name="비상연락망_2단보고.pdf")
