import pandas as pd

def final_perfect_merge():
    files = ['대학본관.csv', '병원별관.csv', '서울성모병원.CSV', '성으회관0.csv', '옴니버스B.csv', '의산연01.csv']
    all_data = []

    for file in files:
        try:
            try:
                df = pd.read_csv(file, encoding='utf-8-sig')
            except:
                df = pd.read_csv(file, encoding='cp949')

            # --- [에러 해결 핵심: 중복 컬럼 제거] ---
            # 동일한 이름의 컬럼이 여러 개 있을 경우 첫 번째만 남기고 삭제
            df = df.loc[:, ~df.columns.duplicated()]

            # 데이터 중간에 낀 제목 행 제거
            if 'name' in df.columns:
                df = df[df['name'].astype(str).str.lower() != 'name']
            
            # 컬럼명 표준화
            mapping = {'name': 'facility_name', 'room': 'room_no', 'zone': 'description'}
            df.rename(columns=mapping, inplace=True)

            # 층수 데이터 규격화
            def normalize_floor(f):
                f = str(f).strip().upper()
                if f in ['NAN', 'NONE', '']: return ""
                if f.startswith('-'): return f"B{f[1:]}F"
                if f.isdigit(): return f + "F"
                if not f.endswith('F'): return f + "F"
                return f
            
            if 'floor' in df.columns:
                df['floor'] = df['floor'].apply(normalize_floor)

            # 데이터가 있는 행만 남기기
            df = df.dropna(subset=['facility_name'])
            df['building_name'] = file.split('.')[0]
            
            all_data.append(df)
            print(f"✅ {file} 정제 완료")

        except Exception as e:
            print(f"❌ {file} 처리 중 오류: {e}")

    if all_data:
        # ignore_index=True를 통해 인덱스 충돌 방지
        final_df = pd.concat(all_data, ignore_index=True, sort=False)
        
        # 출력할 컬럼 고정
        cols = ['facility_name', 'building_name', 'floor', 'room_no', 'category', 'description']
        for col in cols:
            if col not in final_df.columns:
                final_df[col] = ""
        
        final_df = final_df[cols]
        final_df.to_csv('integrated_campus_db.csv', index=False, encoding='utf-8-sig')
        return final_df

master_db = final_perfect_merge()
