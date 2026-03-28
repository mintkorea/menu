import pandas as pd
import streamlit as st

# --- 1. [함수 정의] 반드시 실행부보다 위에 있어야 합니다 ---
def get_verified_data():
    target_files = [
        '성의회관.csv', '의산연01.csv', '의산연별관.csv', '대학본관.csv', 
        '병원별관.csv', '서울성모병원.CSV', '옴니버스B.csv', '옴니버스A.csv'
    ]
    
    all_dfs = []
    for file_path in target_files:
        try:
            # 파일 읽기
            try:
                df = pd.read_csv(file_path, encoding='utf-8-sig')
            except:
                df = pd.read_csv(file_path, encoding='cp949')

            # [컬럼명 표준화]
            df = df.rename(columns={'building_name': 'building', '시설명': 'name'})
            
            # [오류 교정] building 컬럼이 '1'이거나 숫자인 경우 파일명으로 덮어쓰기
            # 특히 의산연별관에서 발생한 '1' 현상을 방지합니다.
            if 'building' in df.columns:
                # 숫자로 변환 가능한 값(1 등)이 들어있으면 파일명에서 추출한 이름으로 교체
                is_numeric_building = pd.to_numeric(df['building'], errors='coerce').notnull()
                if is_numeric_building.any():
                    if '의산연01' in file_path: df['building'] = '의산연본관'
                    elif '의산연별관' in file_path: df['building'] = '의산연별관'
                    else: df['building'] = file_path.split('.')[0]
            else:
                # 컬럼 자체가 없으면 파일명으로 생성
                if '의산연01' in file_path: df['building'] = '의산연본관'
                elif '의산연별관' in file_path: df['building'] = '의산연별관'
                else: df['building'] = file_path.split('.')[0]

            # 시설 이름이 있는 행만 유지
            df = df.dropna(subset=['name'])
            all_dfs.append(df)
        except:
            continue
            
    if not all_dfs: return None
        
    combined = pd.concat(all_dfs, ignore_index=True, sort=False)
    
    # 중복 제거 (이름, 건물, 층, 호실 기준)
    combined = combined.drop_duplicates(subset=['name', 'building', 'floor', 'room'], keep='first')
    
    # 성의회관 유령 데이터 제거
    combined = combined[~((combined['building'] == '성의회관') & (combined['name'] == '대강당'))]
    
    return combined

# --- 2. [실행부] 함수 정의가 끝난 후 호출합니다 ---
st.title("📊 성의교정 시설 데이터 정밀 검증")

# 여기서 함수를 호출하므로 NameError가 발생하지 않습니다.
final_df = get_verified_data()

if final_df is not None:
    st.success(f"🎊 총 **{len(final_df)}개**의 데이터가 통합되었습니다.")
    
    # 건물별 분포 확인
    st.subheader("🏢 건물별 최종 추출 현황")
    stats = final_df['building'].value_counts().reset_index()
    stats.columns = ['건물명', '시설 수']
    st.table(stats)
    
    # '1'이라고 나왔던 데이터들이 제대로 '의산연별관' 등으로 들어갔는지 확인
    with st.expander("🔍 전체 데이터 상세보기"):
        st.dataframe(final_df)
else:
    st.error("데이터를 불러오지 못했습니다. CSV 파일 위치를 확인해 주세요.")
