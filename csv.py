import pandas as pd
import streamlit as st

def get_verified_data():
    # 1. 대상 파일 리스트 (의산연별관 포함)
    target_files = [
        '성의회관.csv', '의산연01.csv', '의산연별관.csv', '대학본관.csv', 
        '병원별관.csv', '서울성모병원.CSV', '옴니버스B.csv', '옴니버스A.csv'
    ]
    
    all_dfs = []
    for file_path in target_files:
        try:
            # 파일 읽기 (인코딩 대응)
            try:
                df = pd.read_csv(file_path, encoding='utf-8-sig')
            except:
                df = pd.read_csv(file_path, encoding='cp949')

            # 건물명 강제 지정 (의산연01 -> 의산연본관)
            if '의산연01' in file_path:
                df['building'] = '의산연본관'
            elif '의산연별관' in file_path:
                df['building'] = '의산연별관'
            elif 'building' not in df.columns:
                df['building'] = file_path.split('.')[0]

            # 컬럼명 표준화
            df = df.rename(columns={'building_name': 'building', '시설명': 'name'})
            
            # 시설 이름이 있는 행만 유지
            df = df.dropna(subset=['name'])
            all_dfs.append(df)
        except:
            continue
            
    if not all_dfs: return None
        
    combined = pd.concat(all_dfs, ignore_index=True, sort=False)
    
    # 중복 제거 (이름, 건물, 층, 호실이 모두 같을 때만)
    combined = combined.drop_duplicates(subset=['name', 'building', 'floor', 'room'], keep='first')
    
    # 성의회관 대강당 등 유령 데이터 필터링
    combined = combined[~((combined['building'] == '성의회관') & (combined['name'] == '대강당'))]
    
    return combined

# --- 실행부 ---
st.title("📊 성의교정 시설 데이터 정밀 검증")

final_df = get_verified_data()

if final_df is not None:
    st.success(f"🎊 총 **{len(final_df)}개**의 데이터가 로드되었습니다.")
    
    # 2. [핵심] 건물별 데이터 분포 확인
    st.subheader("🏢 건물별 추출 현황 (1,147개의 정체)")
    
    # 건물별 개수 집계
    stats = final_df['building'].value_counts().reset_index()
    stats.columns = ['건물명', '시설 수']
    
    # 화면에 표로 출력
    st.table(stats)
    
    # 3. 데이터 누락 여부 판단 가이드
    st.info("""
    **💡 1,147개로 줄어든 이유 체크포인트:**
    1. **의산연본관 vs 별관**: 두 건물의 숫자가 각각 정상적으로 잡혔나요?
    2. **중복 제거**: 혹시 같은 호실에 이름만 다른 데이터가 중복으로 처리되어 삭제되었을 수 있습니다.
    3. **성의회관**: 아까 115개였던 숫자가 '대강당' 삭제 후 몇 개가 되었는지 확인해 보세요.
    """)
    
    # 전체 데이터 미리보기
    with st.expander("🔍 전체 데이터 리스트 (확인용)"):
        st.dataframe(final_df)
else:
    st.error("파일을 읽어오지 못했습니다. CSV 파일들이 서버에 있는지 확인해 주세요.")
