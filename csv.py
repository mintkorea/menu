import pandas as pd
import streamlit as st

def get_integrated_data_v4():
    target_files = [
        '성의회관.csv', '의산연01.csv', '대학본관.csv', 
        '병원별관.csv', '서울성모병원.CSV', '옴니버스B.csv', '옴니버스A.csv'
    ]
    
    all_dfs = []
    for file_path in target_files:
        try:
            try:
                df = pd.read_csv(file_path, encoding='utf-8-sig')
            except:
                df = pd.read_csv(file_path, encoding='cp949')

            df = df.loc[:, ~df.columns.duplicated()]
            
            # [핵심 수정] 원본에 건물명 컬럼이 있는지 확인
            # 'building_name' 또는 '건물명' 등의 컬럼이 있다면 이를 보존합니다.
            if 'building_name' not in df.columns:
                if '건물명' in df.columns:
                    df = df.rename(columns={'건물명': 'building_name'})
                else:
                    # 컬럼이 아예 없을 때만 파일명으로 채웁니다.
                    df['building_name'] = file_path.split('.')[0]
            
            # 시설명이 없는 행 제거
            df = df.dropna(subset=['name'])
            all_dfs.append(df)
        except:
            continue
            
    if not all_dfs: return None
        
    combined = pd.concat(all_dfs, ignore_index=True, sort=False)
    
    # 중복 제거 (의산연 본관/별관 구분 포함)
    combined = combined.drop_duplicates(subset=['name', 'building_name', 'floor', 'room'], keep='first')
    
    # 성의회관 대강당 유령 데이터 제거
    combined = combined[~((combined['building_name'] == '성의회관') & (combined['name'] == '대강당'))]
    
    return combined

# --- 실행 및 확인 ---
final_df = get_integrated_data_v4()

if final_df is not None:
    st.title("🏢 가톨릭대학교 성의교정 시설 안내")
    
    # 현재 데이터에 잡힌 실제 건물 목록 추출
    actual_buildings = sorted(final_df['building_name'].unique())
    
    st.success(f"✅ 총 **{len(final_df)}개** 시설 통합 완료")
    st.info(f"📍 인식된 건물: {', '.join(actual_buildings)}")

    # [검색창 로직 생략 - 이전과 동일]
