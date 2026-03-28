import pandas as pd
import os

def generate_unified_campus_db(file_list):
    # 1. 앱 표준 컬럼 정의
    std_cols = ['facility_name', 'building', 'floor', 'room_no', 'category', 'description', 'map_id']
    integrated_data = []

    # 건물명 정규화 맵
    building_map = {
        '대학본관': '대학본관', '병원별관': '병원별관', '서울성모병원': '서울성모병원',
        '성으회관0': '성의회관', '옴니버스B': '옴니버스파크B', '의산연01': '의과학연구원'
    }

    for file in file_list:
        try:
            # 인코딩 처리
            try:
                df = pd.read_csv(file, encoding='utf-8-sig')
            except:
                df = pd.read_csv(file, encoding='cp949')

            # 2. 헤더(컬럼명) 표준화
            mapping = {'name': 'facility_name', 'room': 'room_no', 'zone': 'description'}
            df.rename(columns=mapping, inplace=True)

            # 3. 층수(Floor) 형식 통일 로직
            def normalize_floor(f):
                f = str(f).strip().upper()
                if f in ['NAN', '']: return ""
                if f.startswith('-'): return f"B{f[1:]}F" # -6 -> B6F
                if f.isdigit(): return f + "F"           # 4 -> 4F
                if not f.endswith('F'): return f + "F"   # B1 -> B1F
                return f
            
            df['floor'] = df['floor'].apply(normalize_floor)

            # 4. 건물명 보정 및 이미지 연결 ID 생성
            file_key = file.split('.')[0]
            current_b = building_map.get(file_key, file_key)
            df['building'] = current_b
            
            # 앱에서 이미지를 호출할 키 (예: 옴니버스파크B_4F)
            df['map_id'] = df['building'] + "_" + df['floor']

            # 5. 데이터 정제 (불필요한 행 제거 및 누락 컬럼 생성)
            for col in std_cols:
                if col not in df.columns: df[col] = ""
            
            # 헤더가 중복 포함된 경우와 시설명이 비어있는 경우 제외
            df = df[df['facility_name'] != 'name']
            df = df.dropna(subset=['facility_name'])

            integrated_data.append(df[std_cols])
            print(f"✅ 통합 완료: {file} ({current_b})")

        except Exception as e:
            print(f"❌ 오류 발생 ({file}): {e}")

    # 최종 병합 및 저장
    if integrated_data:
        master_df = pd.concat(integrated_data, ignore_index=True)
        master_df.drop_duplicates(inplace=True)
        
        # 엑셀/앱 호환용 UTF-8-SIG 저장
        master_df.to_csv('campus_master_db.csv', index=False, encoding='utf-8-sig')
        print("\n🚀 'campus_master_db.csv' 생성이 완료되었습니다.")
        return master_df
    return None

# 파일 리스트
target_files = ['대학본관.csv', '병원별관.csv', '서울성모병원.CSV', '성으회관0.csv', '옴니버스B.csv', '의산연01.csv']
final_db = generate_unified_campus_db(target_files)
