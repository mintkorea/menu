import pandas as pd

def debug_seoul_hospital():
    file_name = '서울성모병원.CSV'
    try:
        # 1. 인코딩 해결
        try:
            df = pd.read_csv(file_name, encoding='utf-8-sig')
        except:
            df = pd.read_csv(file_name, encoding='cp949')

        # 2. 중복 컬럼명 제거 (InvalidIndexError 방지)
        df = df.loc[:, ~df.columns.duplicated()]

        # 3. 데이터 중간에 삽입된 'name' 행들 제거 (백지의 주범)
        if 'name' in df.columns:
            df = df[df['name'].astype(str).str.lower() != 'name']

        # 4. 층수 변환 (-6 -> B6F)
        def convert_floor(f):
            f = str(f).strip().upper()
            if f.startswith('-'): return f"B{f[1:]}F"
            if f.isdigit(): return f + "F"
            return f
        
        if 'floor' in df.columns:
            df['floor'] = df['floor'].apply(convert_floor)

        # 5. 필요한 컬럼만 추출
        # 성모병원은 'room' 컬럼이 있으므로 이를 살립니다.
        df = df[['name', 'building', 'floor', 'room', 'category']].dropna(subset=['name'])
        
        print(f"✅ {file_name} 읽기 성공! 데이터 {len(df)}건을 찾았습니다.")
        print(df.head(10)) # 상위 10개 출력해서 확인
        return df

    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        return None

# 실행
test_df = debug_seoul_hospital()
