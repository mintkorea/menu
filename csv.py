import pandas as pd

def test_single_file(file_name):
    print(f"--- [{file_name}] 분석 시작 ---")
    try:
        # 1. 인코딩 해결 (엑셀 호환 모드)
        try:
            df = pd.read_csv(file_name, encoding='utf-8-sig')
        except:
            df = pd.read_csv(file_name, encoding='cp949')

        # 2. 중복 컬럼명 즉시 제거 (InvalidIndexError 방지)
        df = df.loc[:, ~df.columns.duplicated()]

        # 3. 데이터 중간에 낀 제목행(name, campus...) 제거
        if 'name' in df.columns:
            df = df[df['name'].astype(str).str.lower() != 'name']

        # 4. 컬럼명 표준화 (앱에서 쓸 이름으로 통일)
        mapping = {'name': 'facility_name', 'room': 'room_no', 'zone': 'description'}
        df.rename(columns=mapping, inplace=True)

        # 5. 층수(Floor) 데이터 정규화 (-6 -> B6F, 4 -> 4F)
        def fix_floor(f):
            f = str(f).strip().upper()
            if f in ['NAN', 'NONE', '']: return ""
            if f.startswith('-'): return f"B{f[1:]}F"
            if f.isdigit(): return f + "F"
            if not f.endswith('F'): return f + "F"
            return f
        
        if 'floor' in df.columns:
            df['floor'] = df['floor'].apply(fix_floor)

        # 6. 시설명 없는 빈 행 삭제 및 건물명 추가
        df = df.dropna(subset=['facility_name'])
        df['building_name'] = file_name.split('.')[0]
        
        # 7. 인덱스 초기화 (번호 꼬임 방지)
        df = df.reset_index(drop=True)
        
        print(f"✅ 결과: {len(df)}개의 유효한 데이터 발견")
        return df

    except Exception as e:
        print(f"❌ 실패 이유: {e}")
        return None
