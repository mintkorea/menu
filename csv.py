import pandas as pd

def clean_single_file(file_path):
    print(f"--- [{file_path}] 정제 시작 ---")
    try:
        # 1. 인코딩 확인하며 읽기
        try:
            df = pd.read_csv(file_path, encoding='utf-8-sig')
        except:
            df = pd.read_csv(file_path, encoding='cp949')

        # 2. 중복된 컬럼명 제거 (InvalidIndexError의 주범)
        # 똑같은 이름의 컬럼이 있으면 첫 번째 것만 남깁니다.
        df = df.loc[:, ~df.columns.duplicated()]

        # 3. 데이터 중간에 낀 제목행(name, campus...) 제거
        if 'name' in df.columns:
            df = df[df['name'].astype(str).str.lower() != 'name']

        # 4. 컬럼명 표준화
        mapping = {'name': 'facility_name', 'room': 'room_no', 'zone': 'description'}
        df.rename(columns=mapping, inplace=True)

        # 5. 층수(Floor) 데이터 통일 (-6 -> B6F, 4 -> 4F)
        def normalize_floor(f):
            f = str(f).strip().upper()
            if f in ['NAN', 'NONE', '']: return ""
            if f.startswith('-'): return f"B{f[1:]}F"
            if f.isdigit(): return f + "F"
            if not f.endswith('F'): return f + "F"
            return f
        
        if 'floor' in df.columns:
            df['floor'] = df['floor'].apply(normalize_floor)

        # 6. 시설명 없는 빈 행 삭제 및 건물명 기록
        df = df.dropna(subset=['facility_name'])
        df['building_name'] = file_path.split('.')[0]
        
        # 7. 인덱스 초기화 (번호를 0부터 다시 매김)
        df = df.reset_index(drop=True)
        
        print(f"✅ {file_path} 정제 성공: {len(df)}건")
        return df

    except Exception as e:
        print(f"❌ {file_path} 실패: {e}")
        return None
