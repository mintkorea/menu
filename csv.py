import pandas as pd

def clean_file(file_name):
    print(f"--- {file_name} 처리 시작 ---")
    try:
        # 1. 인코딩 해결 (utf-8-sig 또는 cp949)
        try:
            df = pd.read_csv(file_name, encoding='utf-8-sig')
        except:
            df = pd.read_csv(file_name, encoding='cp949')

        # 2. [중요] 중복 컬럼명 제거 (InvalidIndexError 방지)
        df = df.loc[:, ~df.columns.duplicated()]

        # 3. 데이터 중간에 낀 제목행(name, campus...) 제거
        if 'name' in df.columns:
            df = df[df['name'].astype(str).str.lower() != 'name']

        # 4. 컬럼명 표준화
        mapping = {'name': 'facility_name', 'room': 'room_no', 'zone': 'description'}
        df.rename(columns=mapping, inplace=True)

        # 5. 층수(Floor) 데이터 통일 (-6 -> B6F, 4 -> 4F)
        def fix_floor(f):
            f = str(f).strip().upper()
            if f in ['NAN', 'NONE', '']: return ""
            if f.startswith('-'): return f"B{f[1:]}F"
            if f.isdigit(): return f + "F"
            if not f.endswith('F'): return f + "F"
            return f
        
        if 'floor' in df.columns:
            df['floor'] = df['floor'].apply(fix_floor)

        # 6. 시설명 없는 빈 행 삭제 및 건물명 기록
        df = df.dropna(subset=['facility_name'])
        df['building_name'] = file_name.split('.')[0]
        
        # 7. 인덱스 초기화 (번호 꼬임 방지)
        df = df.reset_index(drop=True)
        
        print(f"✅ {file_name} 완료: {len(df)}개 행 추출")
        return df

    except Exception as e:
        print(f"❌ {file_name} 실패: {e}")
        return None
