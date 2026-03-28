import pandas as pd

def debug_single_file(file_name):
    print(f"--- [{file_name}] 파일 읽기 시도 ---")
    try:
        # 1. 인코딩 에러 방지 (한글 깨짐 차단)
        try:
            df = pd.read_csv(file_name, encoding='utf-8-sig')
        except:
            df = pd.read_csv(file_name, encoding='cp949')

        # 2. [백지 해결 핵심] 데이터 중간에 낀 제목줄(name, campus...) 강제 제거
        # 'name' 컬럼에 'name'이라는 글자가 들어있는 행을 모두 지웁니다.
        if 'name' in df.columns:
            df = df[df['name'].astype(str).str.lower() != 'name']

        # 3. 층수 데이터 변환 (-6 -> B6F)
        def convert_floor(f):
            f = str(f).strip().upper()
            if f.startswith('-'): return f"B{f[1:]}F"
            if f.isdigit(): return f + "F"
            return f
        
        if 'floor' in df.columns:
            df['floor'] = df['floor'].apply(convert_floor)

        # 4. 필수 데이터가 없는 행(빈 줄) 삭제
        df = df.dropna(subset=['name'])
        
        print(f"✅ 성공: {len(df)}개의 데이터를 읽어왔습니다.")
        print(df.head(10)) # 상위 10개 데이터 출력
        return df

    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        return None

# 실행
hospital_df = debug_single_file('서울성모병원.CSV')
