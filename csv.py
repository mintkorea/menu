import pandas as pd
import os
import glob

# 1. 현재 폴더에 있는 모든 CSV 파일 목록을 자동으로 가져옵니다.
# (파일명 오타나 대소문자 문제를 원천 봉쇄합니다)
extension = 'csv'
all_filenames = [i for i in glob.glob(f'*.{extension}')] + [i for i in glob.glob(f'*.{extension.upper()}')]

# 2. 표준 규격 설정
standard_columns = ['name', 'campus', 'building', 'floor', 'room', 'category', 'description', 'hours']
combined_list = []

print(f"🔎 발견된 CSV 파일: {all_filenames}")

for file in all_filenames:
    try:
        # 인코딩 문제 해결을 위해 여러 방식을 시도합니다.
        for encoding in ['utf-8-sig', 'cp949', 'euc-kr']:
            try:
                df = pd.read_csv(file, skip_blank_lines=True, encoding=encoding)
                break
            except:
                continue
        
        # 데이터가 아예 없는 경우 건너뜁니다.
        if df.empty:
            continue

        # [핵심] 파일 중간에 끼어있는 헤더('name'이 다시 나오는 줄)와 진짜 빈 줄 제거
        df = df.dropna(subset=[df.columns[0]]) # 첫 번째 컬럼이 비어있으면 삭제
        df = df[df.iloc[:, 0] != df.columns[0]] # 데이터 내용이 컬럼명과 같으면 삭제

        # 없는 컬럼은 빈 값으로 생성
        for col in standard_columns:
            if col not in df.columns:
                df[col] = ""
        
        # 표준 컬럼 순서로 정리
        df = df[standard_columns]
        
        # 앞뒤 공백 제거
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        
        combined_list.append(df)
        print(f"✅ 처리 완료: {file} ({len(df)}행)")

    except Exception as e:
        print(f"❌ 오류 발생 ({file}): {e}")

# 3. 최종 통합 및 저장
if combined_list:
    final_df = pd.concat(combined_list, ignore_index=True)
    final_df.drop_duplicates(inplace=True) # 완전 중복 데이터 제거
    
    # 결과 저장
    output_file = 'final_integrated_data.csv'
    final_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print("\n" + "="*30)
    print(f"🎉 통합 성공!")
    print(f"📁 생성된 파일명: {output_file}")
    print(f"📊 총 장소 개수: {len(final_df)}개")
    print("="*30)
else:
    print("\n❌ 실패: 폴더 내에 읽을 수 있는 CSV 파일이 하나도 없습니다.")
    print("현재 실행 경로:", os.getcwd())
