import pandas as pd

def debug_sungui_hall():
    file_name = '성으회관0.csv'
    print(f"--- [{file_name}] 정제 테스트 시작 ---")
    
    try:
        # 1. 한글 깨짐 방지를 위한 인코딩 설정
        try:
            df = pd.read_csv(file_name, encoding='utf-8-sig')
        except:
            df = pd.read_csv(file_name, encoding='cp949')

        # 2. 중복 컬럼명 제거 (InvalidIndexError 방지)
        df = df.loc[:, ~df.columns.duplicated()]

        # 3. 데이터 중간에 삽입된 'name' 행(중복 제목) 강제 제거
        if 'name' in df.columns:
            # 제목 행이 데이터로 들어가 있는 경우를 모두 제외합니다.
            df = df[df['name'].astype(str).str.lower() != 'name']

        # 4. 층수(Floor) 데이터 규격화 (예: 14F -> 14F 그대로 유지)
        if 'floor' in df.columns:
            df['floor'] = df['floor'].astype(str).str.strip().str.upper()

        # 5. 필수 정보(시설명)가 없는 빈 줄은 과감히 삭제
        df = df.dropna(subset=['name'])
        
        # 6. 인덱스 초기화 (번호를 0번부터 다시 매김)
        df = df.reset_index(drop=True)

        print(f"✅ 성공: 총 {len(df)}건의 데이터를 불러왔습니다.")
        
        # 7. 결과 확인 (상위 10개 행 출력)
        return df

    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        return None

# 실행 및 출력
sungui_df = debug_sungui_hall()
if sungui_df is not None:
    print(sungui_df.head(10))
