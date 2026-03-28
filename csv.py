import pandas as pd
import streamlit as st

def safe_read_and_clean(file_path):
    try:
        # 1. 인코딩 처리 (utf-8-sig 우선, 안되면 cp949)
        try:
            df = pd.read_csv(file_path, encoding='utf-8-sig')
        except:
            df = pd.read_csv(file_path, encoding='cp949')

        # 2. 중복 컬럼 제거 (InvalidIndexError 방지)
        df = df.loc[:, ~df.columns.duplicated()]

        # 3. [에러 수정 핵심] 데이터 중간에 낀 제목행 'name' 제거
        # .strAccessor를 사용하여 숫자/NaN이 섞여도 에러가 나지 않게 처리합니다.
        if 'name' in df.columns:
            # name 컬럼을 문자열로 강제 변환 후 비교
            is_header = df['name'].astype(str).str.strip().str.lower() == 'name'
            df = df[~is_header]

        # 4. 필수 데이터(시설명) 없는 행 삭제 (문자열 'nan'도 포함)
        df = df.dropna(subset=['name'])
        df = df[df['name'].astype(str).str.lower() != 'nan']
        df = df[df['name'].astype(str).str.strip() != '']
        
        # 5. 층수 보정 (-6 -> B6F 등)
        def fix_floor(f):
            f_str = str(f).strip().upper()
            if f_str in ['NAN', 'NONE', '']: return "정보없음"
            if f_str.startswith('-'): return f"B{f_str[1:]}F"
            if f_str.isdigit(): return f_str + "F"
            return f_str
            
        if 'floor' in df.columns:
            df['floor'] = df['floor'].apply(fix_floor)
        
        # 6. 건물명 기록
        df['building_name'] = file_path.split('.')[0]
        
        return df.reset_index(drop=True)

    except Exception as e:
        # 화면에 에러 원인 표시
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
    # 모든 건물 데이터 하나로 합치기
    final_db = pd.concat(all_dfs, ignore_index=True, sort=False)
    
    # 필수 컬럼 정리 및 빈 값 채우기
    cols = ['name', 'building_name', 'floor', 'room', 'category', 'description']
    for col in cols:
        if col not in final_db.columns: final_db[col] = "정보없음"
    
    final_db = final_db[cols]
    
    # 최종 결과 저장
    final_db.to_csv('integrated_campus_db_final.csv', index=False, encoding='utf-8-sig')
    
    st.success(f"🎊 [최종 통합 완료] 총 {len(all_dfs)}개 건물을 합쳤습니다!")
    st.info(f"📊 전체 데이터 개수: {len(final_df)}개")
    st.dataframe(final_db)
    
    # 다운로드 버튼
    csv_data = final_db.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
    st.download_button("📥 통합 DB 다운로드", data=csv_data, file_name='integrated_campus_db_final.csv')
