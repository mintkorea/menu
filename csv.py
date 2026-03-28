import pandas as pd
import streamlit as st

def safe_clean_file(file_path):
    try:
        # 1. 인코딩 처리 (한글 깨짐 방지)
        try:
            df = pd.read_csv(file_path, encoding='utf-8-sig')
        except:
            df = pd.read_csv(file_path, encoding='cp949')

        # 2. 중복 컬럼 제거 (InvalidIndexError 방지)
        df = df.loc[:, ~df.columns.duplicated()]

        # 3. 데이터 중간에 낀 'name' 행 제거
        if 'name' in df.columns:
            df = df[df['name'].astype(str).str.lower() != 'name']

        # 4. 필수 데이터(시설명) 없는 행 삭제
        df = df.dropna(subset=['name'])
        
        # 5. 층수 보정 로직 (지하층 -6 -> B6F, 숫자만 있으면 F 추가)
        def fix_floor(f):
            f = str(f).strip().upper()
            if f in ['NAN', 'NONE', '']: return ""
            if f.startswith('-'): return f"B{f[1:]}F"
            if f.isdigit(): return f + "F"
            if not f.endswith('F'): return f + "F"
            return f
            
        if 'floor' in df.columns:
            df['floor'] = df['floor'].apply(fix_floor)
        
        # 6. 건물명 기록 (파일명에서 확장자 제외)
        df['building_name'] = file_path.split('.')[0]
        
        return df.reset_index(drop=True)
    except Exception as e:
        st.error(f"⚠️ {file_path} 처리 중 오류: {e}")
        return None

# --- 전체 통합 실행 ---
target_files = [
    '성의회관.csv', '의산연01.csv', '대학본관.csv', 
    '병원별관.csv', '서울성모병원.CSV', '옴니버스B.csv'
]

df_list = []
for f in target_files:
    temp_df = safe_clean_file(f)
    if temp_df is not None:
        df_list.append(temp_df)

if df_list:
    # 모든 파일 하나로 합치기
    final_db = pd.concat(df_list, ignore_index=True, sort=False)
    
    # 7. 필수 컬럼 순서 고정 및 빈 값 채우기
    cols = ['name', 'building_name', 'floor', 'room', 'category', 'description']
    for col in cols:
        if col not in final_db.columns: final_db[col] = ""
    
    final_db = final_db[cols]
    
    # 8. 최종 결과 저장 (Excel에서도 잘 열리게 utf-8-sig)
    final_db.to_csv('integrated_campus_db.csv', index=False, encoding='utf-8-sig')
    
    st.success(f"🎊 대성공! 총 {len(target_files)}개 건물, 전체 {len(final_db)}개 데이터가 통합되었습니다.")
    st.write("### 🏢 가톨릭대학교 성의교정 통합 시설 데이터베이스")
    st.dataframe(final_db)
    
    # 다운로드 버튼 생성
    csv = final_db.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
    st.download_button("📥 통합 DB 파일 다운로드", data=csv, file_name='integrated_campus_db.csv', mime='text/csv')
