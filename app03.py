import streamlit as st
import pandas as pd
import tempfile

# PDF 관련 라이브러리
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame, PageTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# -----------------------------
# 1. 기본 설정 및 모바일 최적화 CSS
# -----------------------------
st.set_page_config(page_title="비상연락망", layout="wide")

st.markdown("""
<style>
    /* 1. 모바일에서 컬럼이 아래로 떨어지는 현상 방지 */
    [data-testid="column"] {
        width: fit-content !important;
        flex: unset !important;
        min-width: unset !important;
    }
    
    /* 2. 별표 버튼 자체의 스타일 (투명하고 작게) */
    div[data-testid="stButton"] > button {
        border: none !important;
        background: transparent !important;
        padding: 0px !important;
        margin: 0px !important;
        line-height: 1 !important;
        color: #ffc107 !important;
        font-size: 22px !important; /* 별 크기 조정 */
        box-shadow: none !important;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* 3. 이름과 직급 텍스트 스타일 */
    .name-label {
        font-weight: bold;
        font-size: 17px;
        color: #333;
        display: inline-block;
        margin-top: 2px; /* 별표와 높이 맞춤 */
    }

    /* 4. 카드 하단 정보 (부서, 연락처) */
    .contact-info-box {
        border-bottom: 1px solid #f0f0f0;
        padding-bottom: 12px;
        margin-bottom: 10px;
        margin-left: 5px;
    }

    .meta-text {
        color: #666;
        font-size: 13px;
        margin: 4px 0;
    }

    .phone-link {
        font-size: 14px;
        text-decoration: none;
        color: #007bff;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

st.title("📞 총무팀 비상연락망")

# -----------------------------
# 2. 데이터 로드 (구글시트)
# -----------------------------
SHEET_ID = "1sGpEFXLNsZm76lRPuyS4vLGmTQGkAYtNHt1f03mx0h0"
SHEET_NAME = "Sheet1"

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
# 3. 데이터 전처리
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
# 4. 검색 및 필터 UI
# -----------------------------
col_search, col_dept = st.columns([2, 1])

with col_search:
    keyword = st.text_input("🔍 이름/업무 검색")

with col_dept:
    dept_list = ["전체"] + sorted(df["부서"].dropna().unique().tolist())
    selected_dept = st.selectbox("부서 필터", dept_list)

filtered_df = df.copy()

if keyword:
    filtered_df = filtered_df[
        df["이름"].astype(str).str.contains(keyword, case=False, na=False) |
        df["업무"].astype(str).str.contains(keyword, case=False, na=False)
    ]

if selected_dept != "전체":
    filtered_df = filtered_df[filtered_df["부서"] == selected_dept]

filtered_df = filtered_df.sort_values(by=["부서", "이름"])

# -----------------------------
# 5. 즐겨찾기 상태 관리
# -----------------------------
if "fav" not in st.session_state:
    st.session_state.fav = set()

show_fav = st.checkbox("⭐ 즐겨찾기만 보기")

if show_fav:
    filtered_df = filtered_df[filtered_df.index.isin(st.session_state.fav)]

# -----------------------------
# 6. 연락처 목록 출력 (핵심 수정 부분)
# -----------------------------
st.write(f"총 {len(filtered_df)}명의 연락처")
st.divider()

for i, row in filtered_df.iterrows():
    is_fav = i in st.session_state.fav
    star_icon = "★" if is_fav else "☆"
    
    # [핵심] 별표와 이름을 아주 좁은 간격으로 배치
    c1, c2 = st.columns([0.1, 0.9])
    
    with c1:
        # 버튼 클릭 시 즉시 반영을 위해 rerun 호출
        if st.button(star_icon, key=f"fav_{i}"):
            if is_fav:
                st.session_state.fav.remove(i)
            else:
                st.session_state.fav.add(i)
            st.rerun()

    with c2:
        st.markdown(f'<div class="name-label">{row["이름"]} ({row["직급"]})</div>', unsafe_allow_html=True)
    
    # 상세 정보 출력 (부서/업무/전화번호)
    tel = row['전화']
    mobile = row['휴대폰']
    st.markdown(f"""
    <div class="contact-info-box">
        <div class="meta-text">{row['부서']} | {row['업무']}</div>
        <div style="margin-top: 5px;">
            <a class="phone-link" href="tel:{tel}">📞 {tel}</a> &nbsp;&nbsp; 
            <a class="phone-link" href="tel:{mobile}">📱 {mobile}</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# 7. PDF 생성 기능
# -----------------------------
st.markdown("### 📄 리스트 내보내기")
if st.button("📄 PDF 파일 생성"):
    try:
        pdfmetrics.registerFont(TTFont('KoreanFont', 'NanumGothic.ttf'))
    except:
        st.error("❌ 'NanumGothic.ttf' 폰트 파일이 필요합니다.")
        st.stop()

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(tmp.name, leftMargin=20, rightMargin=20, topMargin=20, bottomMargin=20)
    
    styles = getSampleStyleSheet()
    styles["Normal"].fontName = 'KoreanFont'
    styles["Normal"].fontSize = 9

    frame1 = Frame(doc.leftMargin, doc.bottomMargin, (doc.width/2)-5, doc.height, id='col1')
    frame2 = Frame(doc.leftMargin + (doc.width/2)+5, doc.bottomMargin, (doc.width/2)-5, doc.height, id='col2')
    doc.addPageTemplates([PageTemplate(id='TwoCol', frames=[frame1, frame2])])

    content = [Paragraph("<b>총무팀 비상연락망</b>", styles["Normal"]), Spacer(1, 10)]
    
    for dept, group in filtered_df.groupby("부서"):
        content.append(Paragraph(f"<br/><b>[{dept}]</b>", styles["Normal"]))
        for _, r in group.iterrows():
            txt = f"• {r['이름']} {r['직급']}: {r['전화']} / {r['휴대폰']}"
            content.append(Paragraph(txt, styles["Normal"]))

    doc.build(content)
    with open(tmp.name, "rb") as f:
        st.download_button("📥 PDF 다운로드", f, file_name="contact_list.pdf")

# -----------------------------
# 8. 데이터 새로고침
# -----------------------------
if st.button("🔄 데이터 강제 새로고침"):
    st.cache_data.clear()
    st.rerun()
