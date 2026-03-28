import pandas as pd

def final_perfect_merge():
    # 처리할 파일 리스트
    files = ['대학본관.csv', '병원별관.csv', '서울성모병원.CSV', '성으회관0.csv', '옴니버스B.csv', '의산연01.csv']
    all_data = []

    for file in files:
        try:
            # 1. 인코딩 대응 (Excel 한글 깨짐 방지용 utf-8-sig 우선)
            try:
                df = pd.read_csv(file, encoding='utf-8-sig')
            except:
                df = pd.read_csv(file, encoding='cp949')

            # 2. [에러 해결 핵심 1] 중복된 컬럼명 강제 제거
            # 컬럼 이름이 같은 게 여러 개 있다면 첫 번째만 남기고 삭제합니다.
            df = df.loc[:, ~df.columns.duplicated()]

            # 3. [에러 해결 핵심 2] 데이터 중간에 삽입된 '중복 제목 행' 제거
            # name 컬럼 값이 'name'인 행을 필터링하여 유효한 데이터만 남깁니다.
            if 'name' in df.columns:
                df = df[df['name'].astype(str).str.lower() != 'name']
            
            # 4. 컬럼명 표준화
            mapping = {
                'name': 'facility_name', 
                'room': 'room_no', 
                'zone': 'description'
            }
            df.rename(columns=mapping, inplace=True)

            # 5. 층수(Floor) 데이터 규격화 (-6 -> B6F, 4 -> 4F)
            def normalize_floor(f):
                f = str(f).strip().upper()
                if f in ['NAN', 'NONE', '']: return ""
                if f.startswith('-'): return f"B{f[1:]}F"
                if f.isdigit(): return f + "F"
                if not f.endswith('F'): return f + "F"
                return f
            
            if 'floor' in df.columns:
                df['floor'] = df['floor'].apply(normalize_floor)

            # 6. 시설명이 비어있는 행 제거 및 건물명 추가
            df = df.dropna(subset=['facility_name'])
            df['building_name'] = file.split('.')[0]
            
            # 7. 개별 파일의 인덱스를 초기화하여 합칠 때 충돌 방지
            df = df.reset_index(drop=True)
            
            all_data.append(df)
            print(f"✅ {file} 정제 완료")

        except Exception as e:
            print(f"❌ {file} 처리 중 오류 발생: {e}")

    # 8. 최종 데이터 통합
    if all_data:
        # ignore_index=True를 사용하여 인덱스 번호를 0부터 새로 부여
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
