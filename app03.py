import streamlit as st
import pandas as pd
import tempfile

# PDF 관련 라이브러리
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame, PageTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# -----------------------------
# 1. 기본 설정
# -----------------------------
st.set_page_config(page_title="비상연락망", layout="wide")

# -----------------------------
# 2. 커스텀 스타일 (모바일 최적화 및 별표 디자인)
# -----------------------------
st.markdown("""
<style>
    /* 전체 타이틀 스타일 */
    .main-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
    }

    /* 연락처 카드 컨테이너 */
    .contact-card {
        border-bottom: 1px solid #eee;
        padding: 10px 0;
        margin-bottom: 5px;
    }

    /* 별표와 이름을 한 줄로 배치하는 flex 박스 */
    .name-row {
        display: flex;
        align-items: center;
        gap: 5px; /* 별표와 이름 사이 간격 */
    }

    .name-text {
        font-weight: bold;
        font-size: 16px;
        color: #333;
    }

    .dept-info {
        color: #666;
        font-size: 13px;
        margin-top: 2px;
    }

    .phone-links {
        margin-top: 5px;
        font-size: 14px;
    }

    .phone-links a {
        text-decoration: none;
        color: #007bff;
    }

    /* 스트림릿 버튼을 투명한 별표 아이콘으로 변신 */
    div[data-testid="stButton"] > button {
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
        line-height: 1 !important;
        width: auto !important;
        height: auto !important;
        color: #ffc107 !important; /* 즐겨찾기 별 색상 */
        font-size: 18px !important;
    }
    
    div[data-testid="stButton"] > button:hover {
        color: #ff9800 !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📞 총무팀 비상연락망</div>', unsafe_allow_html=True)

# -----------------------------
# 3. 구글시트 데이터 로드
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
# 4. 전화번호 포맷 변환
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
# 5. 검색 및 필터 UI
# -----------------------------
col1, col2 = st.columns([2, 1])

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

filtered_df = filtered_df.sort_values(by=["부서", "이름"])

# -----------------------------
# 6. 즐겨찾기 로직
# -----------------------------
if "fav" not in st.session_state:
    st.session_state.fav = set()

show_fav = st.checkbox("⭐ 즐겨찾기만 보기")

if show_fav:
    filtered_df = filtered_df[filtered_df.index.isin(st.session_state.fav)]

# -----------------------------
# 7. 연락처 리스트 출력
# -----------------------------
st.markdown("### 📋 연락처 목록")

for i, row in filtered_df.iterrows():
    is_fav = i in st.session_state.fav
    star_icon = "★" if is_fav else "☆"
    
    # 카드 레이아웃 시작
    with st.container():
        # 별표 버튼과 이름을 가로로 배치하기 위해 아주 작은 컬럼 사용
        c_star, c_name = st.columns([0.08, 0.92])
        
        with c_star:
            if st.button(star_icon, key=f"fav_{i}"):
                if is_fav:
                    st.session_state.fav.remove(i)
                else:
                    st.session_state.fav.add(i)
                st.rerun()
        
        with c_name:
            st.markdown(f'<div class="name-text">{row["이름"]} ({row["직급"]})</div>', unsafe_allow_html=True)
            
        # 하단 정보
        tel = row['전화']
        mobile = row['휴대폰']
        st.markdown(f"""
        <div class="contact-card">
            <div class="dept-info">{row['부서']} | {row['업무']}</div>
            <div class="phone-links">
                📞 <a href="tel:{tel}">{tel}</a> &nbsp;&nbsp; 
                📱 <a href="tel:{mobile}">{mobile}</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------
# 8. PDF 생성 섹션
# -----------------------------
st.divider()
st.markdown("### 📄 PDF 다운로드")

if st.button("📄 PDF 생성"):
    try:
        pdfmetrics.registerFont(TTFont('KoreanFont', 'NanumGothic.ttf'))
    except:
        st.error("❌ 서버에 NanumGothic.ttf 폰트 파일이 필요합니다.")
        st.stop()

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(tmp.name, leftMargin=20, rightMargin=20, topMargin=20, bottomMargin=20)
    
    styles = getSampleStyleSheet()
    styles["Normal"].fontName = 'KoreanFont'
    styles["Normal"].fontSize = 9
    styles["Normal"].leading = 12

    # 2단 레이아웃 설정
    frame1 = Frame(doc.leftMargin, doc.bottomMargin, (doc.width/2)-5, doc.height, id='col1')
    frame2 = Frame(doc.leftMargin + (doc.width/2)+5, doc.bottomMargin, (doc.width/2)-5, doc.height, id='col2')
    doc.addPageTemplates([PageTemplate(id='TwoCol', frames=[frame1, frame2])])

    content = []
    content.append(Paragraph("<b>총무팀 비상연락망</b>", styles["Normal"]))
    content.append(Spacer(1, 10))

    groups = filtered_df.groupby("부서")
    for dept, group in groups:
        content.append(Paragraph(f"<br/><b>[ {dept} ]</b>", styles["Normal"]))
        for _, row in group.iterrows():
            text = f"• <b>{row['이름']} {row['직급']}</b>: {row['전화']} / {row['휴대폰']} ({row['업무']})"
            content.append(Paragraph(text, styles["Normal"]))

    doc.build(content)

    with open(tmp.name, "rb") as f:
        st.download_button("📥 PDF 다운로드", f, file_name="emergency_contacts.pdf")

# -----------------------------
# 9. 새로고침
# -----------------------------
st.divider()
if st.button("🔄 데이터 새로고침"):
    st.cache_data.clear()
    st.rerun()
