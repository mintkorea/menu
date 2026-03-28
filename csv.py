import pandas as pd
import streamlit as st

def get_final_complete_data():
    # 대상 파일 리스트 (의산연별관 추가)
    target_files = [
        '성의회관.csv', '의산연01.csv', '의산연별관.csv', '대학본관.csv', 
        '병원별관.csv', '서울성모병원.CSV', '옴니버스B.csv', '옴니버스A.csv'
    ]
    
    all_dfs = []
    for file_path in target_files:
        try:
            # 1. 파일 읽기
            try:
                df = pd.read_csv(file_path, encoding='utf-8-sig')
            except:
                df = pd.read_csv(file_path, encoding='cp949')

            # 2. 건물명 처리 로직
            # 파일명이 '의산연01'이면 '의산연본관'으로, 그 외엔 데이터 내 building 컬럼 유지
            if file_path == '의산연01.csv':
                df['building'] = '의산연본관'
            elif 'building' not in df.columns:
                df['building'] = file_path.split('.')[0]

            # 3. 필수 컬럼 표준화
            cols_map = {'building_name': 'building', '시설명': 'name'}
            df = df.rename(columns=cols_map)
            
            standard_cols = ['name', 'campus', 'building', 'floor', 'room', 'category', 'description']
            for c in standard_cols:
                if c not in df.columns:
                    df[c] = "성의교정" if c == 'campus' else ""

            # 4. 유효 행 추출
            df = df.dropna(subset=['name'])
            all_dfs.append(df[standard_cols])
        except Exception as e:
            # 파일이 실제로 없는 경우(예: 별관 파일명 오타) 건너뜀
            continue
            
    if not all_dfs: return None
        
    combined = pd.concat(all_dfs, ignore_index=True)
    
    # [최종 정제] 중복 제거 및 성의회관 대강당 필터링
    combined = combined.drop_duplicates(subset=['name', 'building', 'floor', 'room'], keep='first')
    combined = combined[~((combined['building'] == '성의회관') & (combined['name'] == '대강당'))]
    
    return combined

# --- 메인 실행 ---
final_df = get_final_complete_data()

if final_df is not None:
    st.title("🏥 성의교정 시설 통합 가이드 (본관/별관 분리 완료)")
    
    # 건물 목록 확인용
    b_list = sorted(final_df['building'].unique())
    st.success(f"✅ 총 **{len(final_df)}개** 시설 통합 완료! (인식된 건물: {', '.join(b_list)})")

    # 이후 검색 및 조회 로직은 동일...
