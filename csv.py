import pandas as pd
import os

def generate_app_master_db(file_list):
    # 1. 앱에서 사용할 표준 컬럼 구조
    std_cols = ['facility_name', 'building', 'floor', 'room_no', 'category', 'description', 'map_id']
    integrated_data = []

    # 건물명 매핑 (파일명 기준 통일)
    building_names = {
        '대학본관': '대학본관',
        '병원별관': '병원별관',
        '서울성모병원': '서울성모병원',
        '성으회관0': '성의회관',
        '옴니버스B': '옴니버스파크B',
        '의산연01': '의과학연구원'
    }

    for file in file_list:
        try:
            # 인코딩 대응 (UTF-8-SIG 또는 CP949)
            try:
                df = pd.read_csv(file, encoding='utf-8-sig')
            except:
                df = pd.read_csv(file, encoding='cp949')

            # 2. 컬럼명 표준화
            mapping = {'name': 'facility_name', 'room': 'room_no', 'zone': 'description'}
            df.rename(columns=mapping, inplace=True)

            # 3. 층수(Floor) 형식 통일 (예: -6 -> B6F, 4 -> 4F)
            def normalize_floor(f):
                f = str(f).strip().upper()
                if f == 'NAN' or not f: return ""
                if f.startswith('-'): return f"B{f[1:]}F"
                if f.isdigit(): return f + "F"
                if not f.endswith('F'): return f + "F"
                return f
            
            df['floor'] = df['floor'].apply(normalize_floor)

            # 4. 건물명 보정 및 이미지 매핑 키 생성
            b_key = file.split('.')[0]
            df['building'] = building_names.get(b_key, b_key)
            
            # 앱에서 이미지를 불러올 때 쓸 ID (예: 옴니버스파크B_4F)
            df['map_id'] = df['building'] + "_" + df['floor']

            # 5. 필수 컬럼 확보 및 불필요한 행 제거
            for col in std_cols:
                if col not in df.columns: df[col] = ""
            
            df = df[df['facility_name'] != 'name'] # 헤더 중복 제거
            df = df.dropna(subset=['facility_name']) # 빈 행 제거

            integrated_data.append(df[std_cols])
            print(f"✅ {file} 통합 완료")

        except Exception as e:
            print(f"❌ {file} 처리 중 오류: {e}")

    # 데이터 합치기
    if integrated_data:
        final_df = pd.concat(integrated_data, ignore_index=True)
        final_df.drop_duplicates(inplace=True)
        
        # 저장
        final_df.to_csv('campus_master_db.csv', index=False, encoding='utf-8-sig')
        print("\n🚀 모든 데이터가 'campus_master_db.csv'로 통합되었습니다.")
        return final_df
    return None

# 실행
files = ['대학본관.csv', '병원별관.csv', '서울성모병원.CSV', '성으회관0.csv', '옴니버스B.csv', '의산연01.csv']
master_db = generate_app_master_db(files)
