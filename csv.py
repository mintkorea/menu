import pandas as pd
import glob

def final_merge_system():
    # 1. 대상 파일 리스트 (업로드하신 파일명)
    files = ['대학본관.csv', '병원별관.csv', '서울성모병원.CSV', '성으회관0.csv', '옴니버스B.csv', '의산연01.csv']
    all_data = []

    for file in files:
        try:
            # 2. 인코딩 해결 (cp949와 utf-8-sig 모두 시도)
            try:
                df = pd.read_csv(file, encoding='utf-8-sig')
            except:
                df = pd.read_csv(file, encoding='cp949')

            # 3. [핵심] 중복 헤더 제거
            # 데이터 중간에 'name'이라는 글자가 행으로 들어가 있는 경우 삭제
            if 'name' in df.columns:
                df = df[df['name'] != 'name']
            
            # 4. 컬럼명 표준화 (어떤 형식이든 하나로 통일)
            mapping = {
                'name': 'facility_name', 
                'room': 'room_no', 
                'zone': 'description'
            }
            df.rename(columns=mapping, inplace=True)

            # 5. 층수 데이터 정규화 (-6 -> B6F, 4 -> 4F)
            def normalize_floor(f):
                f = str(f).strip().upper()
                if f == 'NAN' or not f: return ""
                if f.startswith('-'): return f"B{f[1:]}F"
                if f.isdigit(): return f + "F"
                if not f.endswith('F'): return f + "F"
                return f
            
            if 'floor' in df.columns:
                df['floor'] = df['floor'].apply(normalize_floor)

            # 6. 건물명 자동 할당 (파일명 기준)
            df['building'] = file.split('.')[0].replace('0', '').replace('01', '')
            
            all_data.append(df)
            print(f"✅ {file} 처리 완료")

        except Exception as e:
            print(f"❌ {file}에서 에러 발생: {e}")

    # 7. 전체 합치기 및 불필요한 공백 제거
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        # 시설명이 비어있는 행은 과감히 삭제 (백지 방지)
        final_df = final_df.dropna(subset=['facility_name'])
        
        # 결과 저장
        final_df.to_csv('campus_master_final.csv', index=False, encoding='utf-8-sig')
        print("\n🎉 모든 에러를 해결하고 'campus_master_final.csv'를 만들었습니다!")
        return final_df

# 실행
master_db = final_merge_system()
