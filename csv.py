import pandas as pd
import numpy as np

def final_app_data_standardization(file_list):
    standard_columns = ['facility_name', 'building', 'floor', 'room_no', 'category', 'description', 'map_image']
    integrated_list = []

    for file in file_list:
        try:
            # 1. 인코딩 및 읽기
            try:
                df = pd.read_csv(file, encoding='utf-8-sig')
            except:
                df = pd.read_csv(file, encoding='cp949')

            # 2. 컬럼명 매핑
            df.rename(columns={'name': 'facility_name', 'room': 'room_no', 'zone': 'description'}, inplace=True)

            # 3. 층수(Floor) 표준화 (B1, 1F, 2F... 형식으로 통일)
            def clean_floor(f):
                f = str(f).strip().upper()
                if f == 'NAN' or not f: return ""
                if f.startswith('-'): return f"B{f[1:]}F" # -6 -> B6F
                if f.isdigit(): return f + "F"
                if not f.endswith('F'): return f + "F"
                return f
            
            df['floor'] = df['floor'].apply(clean_floor)

            # 4. 건물명(Building) 표준화
            # 파일명이나 데이터 내 건물명을 앱에서 사용할 공식 명칭으로 변환
            building_map = {
                '대학본관': '대학본관',
                '병원별관': '병원별관',
                '서울성모병원': '서울성모병원',
                '성으회관0': '성의회관',
                '옴니버스B': '옴니버스파크B',
                '의산연01': '의과학연구원'
            }
            # 파일 이름(확장자 제외)을 기준으로 건물명 보정
            current_b_name = file.split('.')[0]
            df['building'] = building_map.get(current_b_name, df['building'].iloc[0] if 'building' in df.columns else current_b_name)

            # 5. 앱용 도면 이미지 경로 생성 (예: 대학본관_4F.png)
            df['map_image'] = df['building'] + "_" + df['floor'] + ".png"

            # 6. 필수 컬럼 확보 및 데이터 정리
            for col in standard_columns:
                if col not in df.columns: df[col] = ""
            
            # 헤더 중복 제거 및 공백 행 제거
            df = df[df['facility_name'] != 'name']
            df.dropna(subset=['facility_name'], inplace=True)
            
            integrated_list.append(df[standard_columns])

        except Exception as e:
            print(f"파일 처리 중 오류: {file} -> {e}")

    # 최종 병합
    final_df = pd.concat(integrated_list, ignore_index=True)
    
    # 7. 검색 최적화: 검색어 컬럼 추가 (시설명 + 호실번호 + 설명 합치기)
    final_df['search_tag'] = (final_df['facility_name'] + " " + 
                             final_df['room_no'].astype(str) + " " + 
                             final_df['description'].astype(str)).str.strip()

    final_df.to_csv('campus_app_master_db.csv', index=False, encoding='utf-8-sig')
    print("✨ 앱 마스터 DB 생성 완료 (campus_app_master_db.csv)")
    return final_df

# 실행
files = ['대학본관.csv', '병원별관.csv', '서울성모병원.CSV', '성으회관0.csv', '옴니버스B.csv', '의산연01.csv']
master_db = final_app_data_standardization(files)
