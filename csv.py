import pandas as pd
import os

# 1. 통합할 파일 리스트
file_names = [
    '대학본관.csv', '병원별관.csv', '서울성모병원.CSV', 
    '성으회관0.csv', '옴니버스B.csv', '의산연01.csv'
]

# 2. 표준 컬럼 설정 (모든 파일이 이 형식을 따르도록 통합)
standard_columns = ['name', 'campus', 'building', 'floor', 'room', 'category', 'description', 'hours']

combined_data = []

for file in file_names:
    try:
        # 파일 읽기 (빈 줄 무시)
        df = pd.read_csv(file, skip_blank_lines=True)
        
        # 파일 중간에 header가 다시 등장하는 경우 제거 (name 컬럼 값이 'name'인 행 삭제)
        df = df[df['name'] != 'name']
        
        # 없는 컬럼은 빈 값으로 생성, 있는 컬럼만 유지
        for col in standard_columns:
            if col not in df.columns:
                df[col] = ""
        
        # 표준 컬럼 순서대로 재배치
        df = df[standard_columns]
        
        # 데이터 앞뒤 공백 제거 (Trim)
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        
        combined_data.append(df)
        print(f"✅ {file} 처리 완료")
        
    except Exception as e:
        print(f"❌ {file} 처리 중 오류 발생: {e}")

# 3. 모든 데이터 하나로 합치기
final_df = pd.concat(combined_data, ignore_index=True)

# 4. 전체 빈 행 한 번 더 제거 및 중복 제거
final_df.dropna(how='all', inplace=True)
final_df.drop_duplicates(inplace=True)

# 5. 결과 저장
final_df.to_csv('integrated_building_data.csv', index=False, encoding='utf-8-sig')
print("\n🎉 모든 파일이 'integrated_building_data.csv'로 통합되었습니다!")
