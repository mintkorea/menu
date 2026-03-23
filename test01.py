import streamlit as st
import pandas as pd

# 1. 구글 시트 URL 설정
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSGYiqRoXeOInxtwCEa_HXEEM3YVEtOWITy5jf83wkIg2CBHF6ttUKWpS2PtlPx4EOjjxsNJ2idTPzn/pub?gid=954211169&single=true&output=csv"

# 페이지 설정 (모바일 최적화)
st.set_page_config(page_title="성의교정 안내", page_icon="🏥", layout="centered")

@st.cache_data(ttl=300)
def load_data(url):
    try:
        df = pd.read_csv(url)
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        return df
    except Exception as e:
        return pd.DataFrame()

# 데이터 로드
df = load_data(SHEET_CSV_URL)

# 상단 헤더
st.title("🏥 성의교정 안내")

if not df.empty:
    # 전처리
    df['건물'] = df['건물'].fillna('미분류').astype(str)
    building_list = sorted(df['건물'].unique().tolist())

    # --- 검색 및 필터 (모바일 전용 레이아웃) ---
    search_query = st.text_input("🔍 검색어 (부서, 교수명, 호수)", placeholder="예: 서태석, 1416")
    
    selected_building = st.selectbox("🏢 건물 선택", ["전체 건물"] + building_list)

    # 필터링 로직
    filtered_df = df.copy()
    if selected_building != "전체 건물":
        filtered_df = filtered_df[filtered_df['건물'] == selected_building]
    
    if search_query:
        mask = filtered_df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
        filtered_df = filtered_df[mask]

    st.divider()

    # --- 결과 출력 (카드 형태) ---
    if not filtered_df.empty:
        st.caption(f"검색 결과: {len(filtered_df)}건")
        
        for _, row in filtered_df.iterrows():
            # 모바일에서 보기 편한 카드 스타일 구성
            with st.container():
                st.markdown(f"""
                <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #004a99;">
                    <p style="margin: 0; font-size: 0.8rem; color: #555;">{row['건물']} | {row['층']}</p>
                    <h4 style="margin: 5px 0; color: #111;">{row['명칭']}</h4>
                    <p style="margin: 0; font-size: 0.9rem;"><b>위치:</b> {row['호수'] if pd.notna(row['호수']) else '-'}</p>
                    <p style="margin: 5px 0 0 0; font-size: 0.85rem; color: #444;">{row['비고'] if pd.notna(row['비고']) else ''}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("일치하는 정보가 없습니다.")
else:
    st.error("데이터를 불러올 수 없습니다.")

# 하단 고정 안내
st.caption("데이터 수정: 관리용 구글 시트에서 수행")
