import pandas as pd
import os

# 1. 파일 리스트 (경로 확인 필수)
# 스트림릿 클라우드라면 파일들이 py 파일과 같은 위치에 있는지 확인하세요.
file_names = [
    '대학본관.csv', '병원별관.csv', '서울성모병원.CSV', 
    '성으회관0.csv', '옴니버스B.csv', '의산연01.csv'
]

standard_columns = ['name', 'campus', 'building', 'floor', 'room', 'category', 'description', 'hours']
combined_data = []

for file in file_names:
    # 파일 존재 여부 확인
    if not os.path.exists(file):
        print(f"⚠️ 파일을 찾을 수 없음 (건너뜀): {file}")
        continue
        
    try:
        # 데이터 읽기 (한글 깨짐 방지를 위해 cp949 또는 utf-8-sig 시도)
        try:
            df = pd.read_csv(file, skip_blank_lines=True, encoding='utf-8-sig')
        except:
            df = pd.read_csv(file, skip_blank_lines=True, encoding='cp949')
        
        # 중간 헤더 제거 및 빈 줄 제거
        df = df.dropna(subset=['name']) # 이름이 없는 행 제거
        df = df[df['name'] != 'name']   # 중복 헤더 제거
        
        # 표준 컬럼 맞추기
        for col in standard_columns:
            if col not in df.columns:
                df[col] = ""
        
        df = df[standard_columns]
        combined_data.append(df)
        print(f"✅ {file} 읽기 성공 ({len(df)}개 행)")
        
    except Exception as e:
        print(f"❌ {file} 처리 중 에러: {e}")

# 2. 통합 대상이 있는지 확인 (에러 방지 핵심)
if combined_data:
    final_df = pd.concat(combined_data, ignore_index=True)
    final_df.drop_duplicates(inplace=True)
    
    # 결과 저장
    final_df.to_csv('integrated_building_data.csv', index=False, encoding='utf-8-sig')
    print(f"\n🎉 총 {len(final_df)}개의 데이터를 통합하여 저장했습니다.")
else:
    print("\n❌ 통합할 데이터가 없습니다. 파일 파일명과 경로를 다시 확인해주세요.")
