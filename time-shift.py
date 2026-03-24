import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 설정 및 CSS (버튼 축소 및 표 최적화) ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 2rem !important; max-width: 500px; margin: auto; }
    .unified-title { font-size: 20px !important; font-weight: 800; text-align: center; }
    
    /* 버튼: 덜 튀게, 크기 축소 */
    .stButton > button {
        width: auto; padding: 2px 15px; border-radius: 5px; height: 2.5em;
        background-color: #f0f2f6; color: #31333F; font-weight: normal; font-size: 13px;
        border: 1px solid #d1d5db; display: block; margin: 0 auto 15px auto;
    }

    /* 통합 테이블 스타일 */
    .custom-table { width: 100%; border-collapse: collapse; table-layout: fixed; font-size: 11px; }
    .custom-table th, .custom-table td { 
        border: 1px solid #dee2e6; padding: 5px 1px; text-align: center; 
        white-space: nowrap; overflow: hidden;
    }
    .bld-header { background-color: #f8f9fa; font-weight: bold; font-size: 10px; color: #666; }
    .name-header { background-color: #eeeeee; font-weight: bold; }
    .highlight-row { background-color: #FFE5E5; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 로직 (이름 이니셜 처리 추가) ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)

if now.hour < 7:
    target_date = (now - timedelta(days=1)).date()
else:
    target_date = now.date()
next_date = target_date + timedelta(days=1)

PATTERN_START = datetime(2026, 3, 9).date()

def get_workers(d):
    diff = (d - PATTERN_START).days
    # 기존 로직 동일 (생략 가능하나 구조 유지를 위해 유지)
    # [황재업, 김태언, 이정석, 이태원 조합 반환]
    # 여기서는 예시로 이름의 '이름' 부분만 추출하거나 영문 이니셜 설정 가능
    # 예: 황재업 -> '재업' 혹은 'JW'
    return "재업", "태언", "정석", "태원"

jojang, seonghui, uisanA, uisanB = get_workers(target_date)
n_jojang, n_seonghui, n_uisanA, n_uisanB = get_workers(next_date)

# --- [3] 데이터 및 통합 렌더링 함수 ---
# (time_data 정의 생략 - 기존과 동일)

def render_unified_table(df, w_names, h_idx=None, title="근무 표"):
    j, s, a, b = w_names
    html = f"""
    <div style="margin-top:10px;">
        <table class="custom-table">
            <tr class="bld-header">
                <th rowspan="2" style="width:24%;">시간</th>
                <th colspan="2" style="background:#FFF2CC;">성의회관</th>
                <th colspan="2" style="background:#D9EAD3;">의학연구원</th>
            </tr>
            <tr class="name-header">
                <th style="background:#FFF2CC;">{j}</th><th style="background:#FFF2CC;">{s}</th>
                <th style="background:#D9EAD3;">{a}</th><th style="background:#D9EAD3;">{b}</th>
            </tr>
    """
    for i, r in df.iterrows():
        cls = "highlight-row" if i == h_idx else ""
        html += f"<tr class='{cls}'><td>{r['From']}~{r['To']}</td><td>{r[j]}</td><td>{r[s]}</td><td>{r[a]}</td><td>{r[b]}</td></tr>"
    return html + "</table></div>"

# --- [4] 화면 출력 ---
st.markdown('<div class="unified-title">C조 실시간 근무 현황</div>', unsafe_allow_html=True)

# 1. 팝업용 버튼 (크기 축소 및 중앙 정렬)
@st.dialog("📅 오늘 전체 시간표")
def show_all():
    st.markdown(render_unified_table(df_rt, (jojang, seonghui, uisanA, uisanB), curr_idx), unsafe_allow_html=True)

if st.button("📋 전체 시간표 보기"):
    show_all()

# 2. 현재 근무 상세 (메인)
st.markdown("**▼ 현재 근무**")
st.markdown(render_unified_table(df_rt.iloc[curr_idx:curr_idx+1], (jojang, seonghui, uisanA, uisanB), curr_idx), unsafe_allow_html=True)

st.markdown("---")

# 3. 내일 근무 미리보기 (추가 요청 반영)
st.markdown(f"**📅 내일 근무 예정 ({next_date.strftime('%m/%d')})**")
# 내일 날짜의 데이터프레임 생성 로직 추가 후 렌더링
df_next = df_rt.copy() # 예시로 구조만 복사 (실제론 내일 배정된 이름으로 컬럼명 변경 필요)
st.markdown(render_unified_table(df_next, (n_jojang, n_seonghui, n_uisanA, n_uisanB)), unsafe_allow_html=True)
