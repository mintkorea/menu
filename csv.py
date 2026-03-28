import pandas as pd

def safe_load_and_standardize(file_path):
    # 1. 인코딩 에러 방지
    try:
        df = pd.read_csv(file_path, encoding='utf-8-sig')
    except:
        df = pd.read_csv(file_path, encoding='cp949')

    # 2. 데이터 중간에 삽입된 잘못된 헤더 행 제거
    # (컬럼명이 데이터 값으로 들어가 있는 경우 제거)
    if 'name' in df.columns:
        df = df[df['name'] != 'name']
    
    # 3. 컬럼명 강제 통일
    mapping = {'name': 'facility_name', 'room': 'room_no', 'zone': 'description'}
    df.rename(columns=mapping, inplace=True)

    # 4. 층수 데이터 강제 문자열화 및 규격화
    def normalize_floor(x):
        val = str(x).strip().upper()
        if val == 'NAN' or not val: return ""
        if val.startswith('-'): return "B" + val[1:] + "F" # -6 -> B6F
        if val.isdigit(): return val + "F" # 4 -> 4F
        return val

    if 'floor' in df.columns:
        df['floor'] = df['floor'].apply(normalize_floor)
    
    return df

# 사용 예시
# final_df = safe_load_and_standardize('서울성모병원.CSV')
