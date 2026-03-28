import pandas as pd

def final_perfect_merge():
    # 1. 대상 파일 리스트
    files = ['대학본관.csv', '병원별관.csv', '서울성모병원.CSV', '성으회관0.csv', '옴니버스B.csv', '의산연01.csv']
    all_data = []

    for file in files:
        try:
            # 2. 인코딩 에러 방지 (utf-8-sig는 엑셀 특유의 깨짐을 잡음)
            try:
                df = pd.read_csv(file, encoding='utf-8-sig')
            except:
                df = pd.read_csv(file, encoding='cp949')

            # 3. [핵심] 데이터 중간에 섞인 '제목 행' 강제 제거
            # 컬럼 이름이 데이터 값으로 들어가 있는 경우(중복 헤더)를 모두 삭제
            if 'name' in df.columns:
                df = df[df['name'].astype(str).str.lower() != 'name']
            
            # 4. 컬럼명 표준화 (어떤 형식이든 하나로 통합)
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
                if f.startswith('-'): return f"B{f[1:]}F" # 음수 층 처리
                if f.isdigit(): return f + "F"           # 숫자만 있는 경우
                if not f.endswith('F'): return f + "F"   # 그 외
                return f
            
            if 'floor' in df.columns:
                df['floor'] = df['floor'].apply(normalize_floor)

            # 6. 시설명(facility_name)이 비어있는 무의미한 행 제거
            df = df.dropna(subset=['facility_name'])
            
            # 7. 건물명 자동 부여 (파일명 기준)
            df['building_name'] = file.split('.')[0]
            
            all_data.append(df)
            print(f"✅ {file} 정제 완료")

        except Exception as e:
            print(f"❌ {file} 처리 중 오류 발생: {e}")

    # 8. 최종 합치기 및 저장
    if all_data:
        # 모든 파일의 컬럼을 맞추기 위해 빈 컬럼 생성
        final_df = pd.concat(all_data, ignore_index=True, sort=False)
        
        # 필수 컬럼 순서 고정
        cols = ['facility_name', 'building_name', 'floor', 'room_no', 'category', 'description']
        for col in cols:
            if col not in final_df.columns: final_df[col] = ""
            
        final_df = final_df[cols]
        
        # 결과 저장 (한글 깨짐 방지 utf-8-sig)
        final_df.to_csv('integrated_campus_db.csv', index=False, encoding='utf-8-sig')
        print("\n🚀 통합 성공! 'integrated_campus_db.csv' 파일이 생성되었습니다.")
        return final_df

# 실행
master_db = final_perfect_merge()
