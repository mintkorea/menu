import pandas as pd
import os

# 1. 대상 파일 리스트 (대소문자 및 오타 수정 완료)
file_names = [
    '대학본관.csv', '병원별관.csv', '서울성모병원.CSV', 
    '성으회관0.csv', '옴니버스B.csv', '의산연01.csv'
]

# 2. 모든 파일을 수용할 수 있는 표준 규격
standard_columns = ['name', 'campus', 'building', 'floor', 'room', 'category', 'description', 'hours']

combined_list = []

print("🚀 데이터 통합 작업을 시작합니다...")

for file in file_names:
    if not os.path.exists(file):
        print(f"⚠️  [파일 없음] {file} - 경로를 확인하세요.")
        continue
        
    try:
        # 한글 인코딩 대응 (utf-8-sig 또는 cp949)
        try:
            df = pd.read_csv(file, skip_blank_lines=True, encoding='utf-8-sig')
        except:
            df = pd.read_csv(file, skip_blank_lines=True, encoding='cp949')

        # [전처리 1] 완전 빈 줄 제거
        df = df.dropna(how='all')

        # [전처리 2] 파일 중간에 삽입된 중복 헤더('name'이라는 글자) 제거
        if 'name' in df.columns:
            df = df[df['name'] != 'name']
        
        # [전처리 3] 부족한 컬럼 채우기 및 순서 통일
        for col in standard_columns:
            if col not in df.columns:
                df[col] = "" # 없는 컬럼은 빈 값으로 생성
        
        # 필요한 컬럼만 추출
        df = df[standard_columns]
        
        # [전처리 4] 데이터 앞뒤 공백 제거
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

        combined_list.append(df)
        print(f"✅ [성공] {file} ({len(df)}개 행)")

    except Exception as e:
        print(f"❌ [에러] {file} 처리 중 오류: {e}")

# 3. 데이터 합치기 (비어있을 경우 대비)
if combined_list:
    final_df = pd.concat(combined_list, ignore_index=True)
    
    # [최종 정리] 중복 데이터 제거 및 층수(floor) 데이터 정제
    final_df.drop_duplicates(inplace=True)
    
    # 결과 저장
    output_name = 'total_building_data.csv'
    final_df.to_csv(output_name, index=False, encoding='utf-8-sig')
    
    print("-" * 30)
    print(f"🎉 통합 완료!")
    print(f"📂 파일명: {output_name}")
    print(f"📊 총 데이터 개수: {len(final_df)}개")
else:
    print("-" * 30)
    print("❌ 통합할 데이터가 하나도 없습니다. 파일명을 다시 확인해주세요.")
