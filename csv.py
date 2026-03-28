import pandas as pd
import numpy as np
import os

def standardize_campus_data(file_list):
    integrated_data = []
    
    # 표준 컬럼 정의
    target_columns = ['facility_name', 'campus', 'building', 'floor', 'room_no', 'category', 'description']

    for file in file_list:
        try:
            # CSV 읽기 (UTF-8 또는 CP949 대응)
            try:
                df = pd.read_csv(file, encoding='utf-8')
            except:
                df = pd.read_csv(file, encoding='cp949')

            # 1. 컬럼명 매핑 (파일마다 다른 헤더를 표준명으로 통일)
            column_mapping = {
                'name': 'facility_name',
                'room': 'room_no',
                'zone': 'description' # zone 정보는 비고란으로 통합
            }
            df.rename(columns=column_mapping, inplace=True)

            # 2. 필수 컬럼 유무 확인 및 생성
            for col in target_columns:
                if col not in df.columns:
                    df[col] = ""

            # 3. 데이터 정제: 층수(floor) 포맷 통일 (예: 4F, 04, 4 -> 4F로 통일)
            def clean_floor(x):
                x = str(x).strip().upper()
                if x == 'NAN' or x == "": return ""
                # 숫자만 있는 경우 'F' 붙이기 (지하는 B 유지)
                if x.isdigit(): return f"{int(x)}F"
                if not x.endswith('F') and not x.startswith('B'): return f"{x}F"
                return x

            df['floor'] = df['floor'].apply(clean_floor)

            # 4. 데이터 정제: 시설명(facility_name) 공백 제거 및 결측치 처리
            df = df[df['facility_name'].notna()]
            df['facility_name'] = df['facility_name'].str.strip()

            # 5. 필요한 컬럼만 추출하여 리스트에 추가
            df_standard = df[target_columns]
            integrated_data.append(df_standard)
            print(f"성공: {file} ({len(df)}건)")

        except Exception as e:
            print(f"오류 발생: {file} -> {e}")

    # 모든 데이터 합치기
    if integrated_data:
        final_df = pd.concat(integrated_data, ignore_index=True)
        # 중복 데이터 제거
        final_df.drop_duplicates(inplace=True)
        return final_df
    else:
        return None

# 실행 부분
files = ['대학본관.csv', '병원별관.csv', '서울성모병원.CSV', '성으회관0.csv', '옴니버스B.csv', '의산연01.csv']
final_result = standardize_campus_data(files)

if final_result is not None:
    final_result.to_csv('integrated_campus_map.csv', index=False, encoding='utf-8-sig')
    print("\n--- 통합 완료: integrated_campus_map.csv 저장됨 ---")
    print(final_result.head())
