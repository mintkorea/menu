import pandas as pd
import os

def build_unified_campus_db(file_list):
    # 1. 최종 통합본에 들어갈 표준 컬럼 정의
    standard_columns = ['facility_name', 'campus', 'building', 'floor', 'room_no', 'category', 'description']
    all_data = []

    for file in file_list:
        if not os.path.exists(file):
            print(f"파일 없음: {file}")
            continue
            
        # 2. 인코딩 대응 (UTF-8-SIG는 한글 깨짐 방지에 좋습니다)
        try:
            df = pd.read_csv(file, encoding='utf-8-sig')
        except:
            df = pd.read_csv(file, encoding='cp949')

        # 3. 개별 파일별 컬럼명 매핑 (동적으로 감지)
        mapping = {
            'name': 'facility_name',
            'room': 'room_no',
            'zone': 'description'  # zone이 있는 경우 비고란으로 통합
        }
        df.rename(columns=mapping, inplace=True)

        # 4. 층수(Floor) 데이터 정규화 (예: 4 -> 4F, B1 -> B1F 등)
        def normalize_floor(f):
            f = str(f).strip().upper()
            if f == 'NAN' or not f: return ""
            if f.isdigit(): return f + "F"
            if f.startswith('-'): return "B" + f[1:] + "F" # -6 -> B6F
            if not f.endswith('F'): return f + "F"
            return f

        if 'floor' in df.columns:
            df['floor'] = df['floor'].apply(normalize_floor)

        # 5. 부족한 컬럼 채우기 및 순서 고정
        for col in standard_columns:
            if col not in df.columns:
                df[col] = ""
        
        # 파일 내부에서 헤더가 반복되는 경우(CSV 병합 시 발생) 제거
        df = df[df['facility_name'] != 'name']
        
        all_data.append(df[standard_columns])
        print(f"처리 완료: {file} ({len(df)}개 항목)")

    # 6. 전체 데이터 병합 및 저장
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        # 빈 줄 및 중복 제거
        final_df.dropna(subset=['facility_name'], inplace=True)
        final_df.drop_duplicates(inplace=True)
        
        output_name = 'standardized_campus_data.csv'
        final_df.to_csv(output_name, index=False, encoding='utf-8-sig')
        print(f"\n✅ 통합 성공! 저장된 파일명: {output_name}")
        return final_df
    return None

# 파일 리스트 (업로드하신 파일명 기준)
target_files = [
    '대학본관.csv', '병원별관.csv', '서울성모병원.CSV', 
    '성으회관0.csv', '옴니버스B.csv', '의산연01.csv'
]

# 실행
unified_df = build_unified_campus_db(target_files)
