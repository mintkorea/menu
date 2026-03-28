import pandas as pd

def final_perfect_merge():
    # 파일 리스트
    files = ['대학본관.csv', '병원별관.csv', '서울성모병원.CSV', '성으회관0.csv', '옴니버스B.csv', '의산연01.csv']
    all_data = []

    for file in files:
        try:
            # 1. 인코딩 처리
            try:
                df = pd.read_csv(file, encoding='utf-8-sig')
            except:
                df = pd.read_csv(file, encoding='cp949')

            # 2. [에러 해결 핵심] 중복된 컬럼명 제거
            # 이름이 같은 컬럼이 여러 개 있다면 첫 번째만 남기고 삭제합니다.
            df = df.loc[:, ~df.columns.duplicated()]

            # 3. 데이터 중간에 삽입된 불필요한 제목 행 제거
            if 'name' in df.columns:
                # name 컬럼의 값이 'name'인 행(제목줄 반복)을 제외합니다.
                df = df[df['name'].astype(str).str.lower() != 'name']
            
            # 4. 컬럼명 표준화
            mapping = {
                'name': 'facility_name', 
                'room': 'room_no', 
                'zone': 'description'
            }
            df.rename(columns=mapping, inplace=True)

            # 5. 층수(Floor) 데이터 규격화
            def normalize_floor(f):
                f = str(f).strip().upper()
                if f in ['NAN', 'NONE', '']: return ""
                if f.startswith('-'): return f"B{f[1:]}F" # -6 -> B6F
                if f.isdigit(): return f + "F"           # 4 -> 4F
                if not f.endswith('F'): return f + "F"   # B1 -> B1F
                return f
            
            if 'floor' in df.columns:
                df['floor'] = df['floor'].apply(normalize_floor)

            # 6. 유효한 데이터만 남기기 (시설명이 없는 빈 줄 제거)
            df = df.dropna(subset=['facility_name'])
            
            # 7. 건물명 추가 (파일명 기준)
            df['building_name'] = file.split('.')[0]
            
            all_data.append(df)
            print(f"✅ {file} 정제 완료")

        except Exception as e:
            print(f"❌ {file} 처리 중 오류 발생: {e}")

    # 8. 최종 합치기
    if all_data:
        # ignore_index=True를 사용하여 인덱스 충돌을 원천 차단합니다.
        final_df = pd.concat(all_data, ignore_index=True, sort=False)
        
        # 필수 컬럼 순서 고정 및 누락 컬럼 생성
        cols = ['facility_name', 'building_name', 'floor', 'room_no', 'category', 'description']
        for col in cols:
            if col not in final_df.columns:
                final_df[col] = ""
        
        final_df = final_df[cols]
        
        # 최종 결과 저장
        final_df.to_csv('integrated_campus_db.csv', index=False, encoding='utf-8-sig')
        print("\n🚀 통합 성공! 'integrated_campus_db.csv' 파일이 생성되었습니다.")
        return final_df

# 실행
master_db = final_perfect_merge()
