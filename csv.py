import pandas as pd

def process_sungui_hall():
    file_name = '성의회관.csv'
    print(f"--- [{file_name}] 파일 읽기 시작 ---")
    
    try:
        # 1. 인코딩 해결 (한글 깨짐 방지)
        try:
            df = pd.read_csv(file_name, encoding='utf-8-sig')
        except:
            df = pd.read_csv(file_name, encoding='cp949')

        # 2. 컬럼명 출력 (백지 원인 파악용 - 실행 시 터미널 확인)
        print("현재 파일의 컬럼들:", df.columns.tolist())

        # 3. 중복된 컬럼명 제거
        df = df.loc[:, ~df.columns.duplicated()]

        # 4. 데이터 중간에 낀 제목 행('name') 강제 제거
        if 'name' in df.columns:
            df = df[df['name'].astype(str).str.lower() != 'name']

        # 5. 필수 데이터 정제 (공백 제거 및 NaN 처리)
        # 'name' 컬럼이 비어있지 않은 행만 남깁니다.
        df = df.dropna(subset=['name'])
        df = df[df['name'].astype(str).str.strip() != '']

        # 6. 인덱스 초기화 (0번부터 다시 번호 매기기)
        df = df.reset_index(drop=True)

        print(f"✅ 성공: {len(df)}건의 데이터를 찾았습니다.")
        return df

    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        return None

# 실행 및 데이터 출력
sungui_df = process_sungui_hall()
if sungui_df is not None:
    # 7. 데이터가 있다면 상위 20개를 출력합니다.
    import streamlit as st
    st.write("### 성의회관 데이터 프리뷰")
    st.dataframe(sungui_df)
