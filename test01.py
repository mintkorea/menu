import streamlit as st
import pandas as pd
import os

# 페이지 설정
st.set_page_config(page_title="가톨릭대 성의교정 통합 안내", layout="wide")

@st.cache_data
def load_all_data():
    # 불러올 파일 목록
    files = {
        "대학본관": "대학본관.csv",
        "병원별관": "병원별관 입주현황.CSV",
        "성모병원": "성모병원 입주현황.CSV",
        "성의회관": "성의회관 입주현황.CSV",
        "옴니버스": "옴니버스 입주현황.csv",
        "의산연": "의산연 입주현황.csv"
    }
    
    combined_df = pd.DataFrame()
    
    for bname, fname in files.items():
        if os.path.exists(fname):
            # CSV 읽기 (인코딩 에러 방지를 위해 cp949 사용)
            df = pd.read_csv(fname, encoding='cp949')
            # 건물명 컬럼이 없는 경우 추가
            if '건물' not in df.columns:
                df['건물'] = bname
            combined_df = pd.concat([combined_df, df], ignore_index=True)
            
    return combined_df

# 데이터 로드
try:
    master_df = load_all_data()
except Exception as e:
    st.error(f"파일을 읽는 중 오류가 발생했습니다. 파일명과 인코딩을 확인해주세요: {e}")
    st.stop()

# UI 구성
st.title("🏢 성의교정 & 성모병원 통합 검색 시스템")
st.info("원본 CSV 데이터를 기반으로 실시간 안내를 제공합니다.")

# 검색창
search_query = st.text_input("🔍 검색어 입력 (부서명, 교수명, 시설명, 호수 등)", placeholder="예: '서태석', '산부인과', '1416'")

# 필터 및 결과 출력
if search_query:
    # 전체 컬럼에서 검색어가 포함된 행 찾기
    mask = master_df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
    results = master_df[mask]
    
    if not results.empty:
        st.success(f"'{search_query}' 검색 결과 {len(results)}건")
        # 검색된 결과 테이블로 표시
        st.dataframe(results, use_container_width=True, hide_index=True)
    else:
        st.warning("검색 결과가 없습니다.")
else:
    # 검색어가 없을 때 기본 화면 (건물별 통계 등)
    st.write("왼쪽 사이드바에서 건물을 선택하거나 검색어를 입력하세요.")
    st.sidebar.header("건물별 현황")
    st.sidebar.write(master_df['건물'].value_counts())
