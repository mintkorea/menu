import streamlit as st
import pandas as pd
import tempfile

# PDF 관련 라이브러리
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame, PageTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# -----------------------------
# 1. 기본 설정 및 모바일 강제 고정 CSS
# -----------------------------
st.set_page_config(page_title="비상연락망", layout="wide")

st.markdown("""
<style>
    /* 1. 모바일에서 컬럼이 상하로 쌓이는 현상 방지 */
    [data-testid="column"] {
        width: fit-content !important;
        flex: unset !important;
        min-width: unset !important;
    }
    
    /* 컬럼 간의 기본 간격 제거 */
    [data-testid="stHorizontalBlock"] {
        gap: 0px !important;
    }

    /* 2. 별표 버튼 스타일 (텍스트처럼 투명하게) */
    div[data-testid="stButton"] > button {
        border: none !important;
        background: transparent !important;
        padding: 0px !important;
        margin: 0px !important;
        line-height: 1 !important;
        color: #ffc107 !important;
        font-size: 22px !important; /* 별 크기 */
        box-shadow: none !important;
    }

    /* 3. 이름 및 직급 스타일 */
    .name-container {
        display: inline-block;
        margin-left: -12px; /* 별표와 이름 사이의 간격을 강제로 좁힘 */
        margin-top: 2px;
    }
    
    .name-text {
        font-weight: bold;
        font-size: 18px;
        color: #333;
        white-space: nowrap;
    }

    /* 4. 카드 하단 정보 (잘림 방지 및 줄바꿈 허용) */
    .info-box {
        border-bottom: 1px solid #f0f0f0;
        padding: 5px 0 15px 28px; /* 별표 위치만큼 왼쪽 여백 확보 */
        margin-bottom: 10px;
    }

    .meta-info {
        color: #666;
        font-size: 14px;
        line-height: 1.5;
        word-break: keep-all; /* 단어 단위 줄바꿈 */
        white-space: normal;
    }

    .phone-link {
        font-size: 14px;
        text-decoration: none;
        color: #007bff;
        font-weight: 500;
        display: inline-block;
        margin-top: 6px;
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
# 4. 필터 UI
# -----------------------------
col_search, col_dept = st.columns([1.5, 1])
with col_search:
    keyword = st.text_input("🔍 검색 (이름/업무)")
with col_dept:
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
# 5. 즐겨찾기 상태 관리
# -----------------------------
if "fav" not in st.session_state:
    st.session_state.fav = set()

show_fav = st.checkbox("⭐ 즐겨찾기만 보기")
if show_fav:
    filtered_df = filtered_df[filtered_df.index.isin(st.session_state.fav)]

# -----------------------------
# 6. 연락처 목록 출력 (최종 최적화)
# -----------------------------
st.write(f"총 {len(filtered_df)}명의 연락처")
st.divider()

for i, row in filtered_df.iterrows():
    is_fav = i in st.session_state.fav
    star_icon = "★" if is_fav else "☆"
    
    # 별표와 이름 한 줄 배치 (컬럼 비율 극단적 조정)
    c1, c2 = st.columns([0.01, 0.99])
    
    with c1:
        if st.button(star_icon, key=f"fav_{i}"):
            if is_fav: st.session_state.fav.remove(i)
            else: st.session_state.fav.add(i)
            st.rerun()

    with c2:
        # 이름을 별표 옆으로 당김
        st.markdown(f'<div class="name-container"><span class="name-text">{row["이름"]} ({row["직급"]})</span></div>', unsafe_allow_html=True)
    
    # 상세 정보 (부서, 업무, 전화번호)
    tel = row['전화']
    mobile = row['휴대폰']
    st.markdown(f"""
    <div class="info-box">
        <div class="meta-info"><b>{row['부서']}</b> | {row['업무']}</div>
        <div>
            <a class="phone-link" href="tel:{tel}">📞 {tel}</a> &nbsp;&nbsp; 
            <a class="phone-link" href="tel:{mobile}">📱 {mobile}</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# 7. PDF 생성 및 기타
# -----------------------------
st.markdown("### 📄 리스트 내보내기")
if st.button("📄 PDF 파일 생성"):
    try:
        pdfmetrics.registerFont(TTFont('KoreanFont', 'NanumGothic.ttf'))
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
            st.download_button("📥 PDF 다운로드", f, file_name="contacts.pdf")
    except:
        st.error("❌ PDF 생성 실패 (서버에 NanumGothic.ttf 필요)")

if st.button("🔄 데이터 강제 새로고침"):
    st.cache_data.clear()
    st.rerun()
