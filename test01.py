import streamlit as st
import pandas as pd

# 1. 구글 시트 URL 설정
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSGYiqRoXeOInxtwCEa_HXEEM3YVEtOWITy5jf83wkIg2CBHF6ttUKWpS2PtlPx4EOjjxsNJ2idTPzn/pub?gid=954211169&single=true&output=csv"

# 페이지 설정 (중앙 정렬)
st.set_page_config(page_title="성의교정 안내", page_icon="🏥", layout="centered")

# --- CSS: 상단 여백 제거 및 타이틀 폰트 조절 ---
st.markdown("""
    <style>
    /* 상단 기본 여백 제거 */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }
    /* 타이틀 스타일 */
    .mobile-title {
        font-size: 24px !important;
        font-weight: 700;
        margin-bottom: 5px;
        color: #111;
    }
    /* 검색 버튼 스타일 커스텀 */
    div.stButton > button {
        width: 100%;
        background-color: #004a99;
        color: white;
        height: 3em;
        border-radius: 5px;
    }
    </style>
    <h3 class="mobile-title">🏥 성의교정 & 성모병원 안내</h3>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)
def load_data(url):
    try:
        df = pd.read_csv(url)
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        return df
    except Exception:
        return pd.DataFrame()

df = load_data(SHEET_CSV_URL)

if not df.empty:
    # 전처리
    df['건물'] = df['건물'].fillna('미분류').astype(str)
    building_list = sorted(df['건물'].unique().tolist())

    # --- 검색 영역 ---
    # 검색어 입력과 검색 버튼을 한 줄에 배치하거나 수직으로 배치
    search_query = st.text_input("🔍 검색어", placeholder="부서, 교수명, 호수 입력", label_visibility="collapsed")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_building = st.selectbox("건물 선택", ["전체 건물"] + building_list, label_visibility="collapsed")
    with col2:
        # 버튼을 눌러야만 검색되게 하려면 state를 쓸 수 있지만, 
        # 사용성상 버튼은 '확인'용으로 두고 즉시 검색되게 유지하는 것이 모바일에서 더 편합니다.
        search_btn = st.button("검색")

    # 필터링 로직
    filtered_df = df.copy()
    if selected_building != "전체 건물":
        filtered_df = filtered_df[filtered_df['건물'] == selected_building]
    
    if search_query:
        mask = filtered_df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
        filtered_df = filtered_df[mask]

    st.markdown(f"<p style='font-size: 0.8rem; color: gray; margin-top: -10px;'>결과: {len(filtered_df)}건</p>", unsafe_allow_html=True)
    st.divider()

    # --- 결과 카드 출력 ---
    if not filtered_df.empty:
        for _, row in filtered_df.iterrows():
            st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 12px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #004a99; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                <p style="margin: 0; font-size: 0.75rem; color: #666;">{row['건물']} | {row['층']}</p>
                <h5 style="margin: 3px 0; color: #111; font-size: 1rem;">{row['명칭']}</h5>
                <p style="margin: 0; font-size: 0.85rem;"><b>위치:</b> {row['호수'] if pd.notna(row['호수']) else '-'}</p>
                <p style="margin: 3px 0 0 0; font-size: 0.8rem; color: #444;">{row['비고'] if pd.notna(row['비고']) else ''}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("일치하는 정보가 없습니다.")
else:
    st.error("데이터를 불러올 수 없습니다.")
