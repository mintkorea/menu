import pandas as pd
import streamlit as st

def safe_read_and_clean(file_path):
    try:
        try:
            df = pd.read_csv(file_path, encoding='utf-8-sig')
        except:
            df = pd.read_csv(file_path, encoding='cp949')

        df = df.loc[:, ~df.columns.duplicated()]

        if 'name' in df.columns:
            # 숫자나 NaN이 있어도 안전하게 처리
            is_header = df['name'].astype(str).str.strip().str.lower() == 'name'
            df = df[~is_header]

        df = df.dropna(subset=['name'])
        df = df[df['name'].astype(str).str.strip() != '']
        
        # 건물명 기록
        df['building_name'] = file_path.split('.')[0]
        
        return df.reset_index(drop=True)
    except Exception as e:
        st.error(f"⚠️ {file_path} 읽기 실패: {e}")
        return None

# --- 전체 통합 실행 ---
target_files = [
    '성의회관.csv', '의산연01.csv', '대학본관.csv', 
    '병원별관.csv', '서울성모병원.CSV', '옴니버스B.csv', '옴니버스A.csv'
]

all_dfs = []
for f in target_files:
    temp_df = safe_read_and_clean(f)
    if temp_df is not None:
        all_dfs.append(temp_df)

if all_dfs:
    # [변수명 통일: final_df로 고쳤습니다]
    final_df = pd.concat(all_dfs, ignore_index=True, sort=False)
    
    # 필수 컬럼 정리
    cols = ['name', 'building_name', 'floor', 'room', 'category', 'description']
    for col in cols:
        if col not in final_df.columns: final_df[col] = "정보없음"
    
    final_df = final_df[cols]
    
    # 화면 출력 및 저장
    st.success(f"🎊 [최종 통합 완료] 총 {len(all_dfs)}개 건물을 합쳤습니다!")
    # 이제 에러 없이 숫자가 뜰 거예요!
    st.info(f"📊 전체 데이터 개수: {len(final_df)}개")
    st.dataframe(final_df)
    
    # CSV 저장 및 다운로드 버튼
    csv_data = final_df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
    st.download_button("📥 통합 DB 다운로드", data=csv_data, file_name='integrated_campus_db_v3.csv')
