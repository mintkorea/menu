import pandas as pd
import os

def standardize_campus_data(file_list):
    # 최종 앱에서 사용할 표준 컬럼 구조
    std_cols = ['facility_name', 'building', 'floor', 'room_no', 'category', 'description', 'map_key']
    integrated_df = []

    for file in file_list:
        try:
            # 1. 인코딩 대응 (한글 깨짐 방지)
            try:
                df = pd.read_csv(file, encoding='utf-8-sig')
            except:
                df = pd.read_csv(file, encoding='cp949')

            # 2. 컬럼명 표준화 (파일마다 다른 헤더 통합)
            rename_map = {
                'name': 'facility_name',
                'room': 'room_no',
                'zone': 'description' # 구역 정보는 비고란으로 통합
            }
            df.rename(columns=rename_map, inplace=True)

            # 3. 층수(Floor) 데이터 정규화 (예: -6 -> B6F, 4 -> 4F)
            def fix_floor(f):
                f = str(f).strip().upper()
                if f == 'NAN' or not f: return ""
                if f.startswith('-'): return f"B{f[1:]}F"
                if f.isdigit(): return f + "F"
                if not f.endswith('F'): return f + "F"
                return f
            
            df['floor'] = df['floor'].apply(fix_floor)

            # 4. 건물명 표준화 및 이미지 매칭 키(map_key) 생성
            # 앱에서 '건물명_층수.png'로 도면을 불러올 수 있게 설계
            b_name = file.split('.')[0]
            if 'building' not in df.columns:
                df['building'] = b_name
            
            df['map_key'] = df['building'] + "_" + df['floor']

            # 5. 필수 컬럼 확보 및 데이터 정제
            for col in std_cols:
                if col not in df.columns:
                    df[col] = ""
            
            # 중간에 섞인 헤더 행이나 빈 행 제거
            df = df[df['facility_name'] != 'name']
            df = df.dropna(subset=['facility_name'])

            integrated_df.append(df[std_cols])
            print(f"✅ 처리 완료: {file}")

        except Exception as e:
            print(f"❌ 오류 발생 ({file}): {e}")

    # 모든 데이터 결합
    if integrated_df:
        final_db = pd.concat(integrated_df, ignore_index=True)
        # 중복 데이터 제거 및 정리
        final_db.drop_duplicates(inplace=True)
        
        # CSV 저장 (엑셀 호환 UTF-8-SIG)
        final_db.to_csv('integrated_campus_master.csv', index=False, encoding='utf-8-sig')
        return final_db
    return None

# 실행 리스트
csv_files = ['대학본관.csv', '병원별관.csv', '서울성모병원.CSV', '성으회관0.csv', '옴니버스B.csv', '의산연01.csv']
master_data = standardize_campus_data(csv_files)
