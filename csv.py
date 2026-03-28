import pandas as pd

def clean_and_merge(file_list):
    all_dfs = []
    
    for file in file_list:
        try:
            # 1. 인코딩 에러 방지 (utf-8-sig는 엑셀 한글 깨짐을 방지함)
            try:
                df = pd.read_csv(file, encoding='utf-8-sig')
            except:
                df = pd.read_csv(file, encoding='cp949')

            # 2. 데이터 중간에 낀 중복 헤더 행 제거 (중요!)
            # 'name' 컬럼에 'name'이라는 글자가 있는 행을 모두 삭제
            if 'name' in df.columns:
                df = df[df['name'] != 'name']

            # 3. 컬럼명 표준화
            mapping = {'name': 'facility_name', 'room': 'room_no', 'zone': 'description'}
            df.rename(columns=mapping, inplace=True)

            # 4. 층수(floor) 데이터 강제 통일 (-6 -> B6F, 4 -> 4F)
            def fix_floor(x):
                val = str(x).strip().upper()
                if val == 'NAN' or not val: return ""
                if val.startswith('-'): return f"B{val[1:]}F" # 음수 층 처리
                if val.isdigit(): return f"{val}F" # 숫자만 있는 경우
                if not val.endswith('F'): return f"{val}F"
                return val

            if 'floor' in df.columns:
                df['floor'] = df['floor'].apply(fix_floor)

            # 5. 빈 행 제거
            df = df.dropna(subset=['facility_name'])
            
            all_dfs.append(df)
            print(f"✅ {file} 읽기 성공")

        except Exception as e:
            print(f"❌ {file} 처리 중 에러: {e}")

    # 최종 합치기
    if all_dfs:
        final_df = pd.concat(all_dfs, ignore_index=True)
        # 필요한 컬럼만 정리 (순서 고정)
        cols = ['facility_name', 'building', 'floor', 'room_no', 'category', 'description']
        for col in cols:
            if col not in final_df.columns: final_df[col] = ""
            
        final_df = final_df[cols]
        final_df.to_csv('integrated_campus_db.csv', index=False, encoding='utf-8-sig')
        print("\n🚀 통합 완료! 'integrated_campus_db.csv' 파일을 확인하세요.")
        return final_df

# 실행
files = ['대학본관.csv', '병원별관.csv', '서울성모병원.CSV', '성으회관0.csv', '옴니버스B.csv', '의산연01.csv']
unified_data = clean_and_merge(files)
