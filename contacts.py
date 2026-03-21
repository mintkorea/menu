import streamlit as st
import pandas as pd

# 번호 변환 함수
def format_phone(number):
    number = str(number).strip()
    if number.startswith('*1'):
        # *1-5672 형태에서 5672만 추출 후 02-2258 접합
        suffix = number.replace('*1-', '').replace('*1', '')
        return f"02-2258-{suffix}"
    elif len(number) == 4:
        # 4자리 내선번호는 02-3147 접합
        return f"02-3147-{number}"
    return number

# 데이터 구성 (예시)
data = [
    {"명칭": "전기팀", "구내번호": "*1-5672", "분류": "주요연락처"},
    {"명칭": "성의회관", "구내번호": "8300", "분류": "주요연락처"},
    {"명칭": "통합관제", "구내번호": "2258-5555", "분류": "주요연락처"},
]
df = pd.DataFrame(data)

st.title("📱 성의교정 스마트 연락망")

# 검색 및 출력 루프
for _, row in df.iterrows():
    real_phone = format_phone(row['구내번호'])
    
    with st.container():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{row['명칭']}**")
            st.caption(f"내선: {row['구내번호']}")
        with col2:
            # 변환된 real_phone으로 전화걸기 링크 생성
            st.markdown(f"""
                <a href="tel:{real_phone.replace('-', '')}" style="text-decoration:none;">
                    <button style="width:100%; border:none; background-color:#28a745; color:white; padding:8px; border-radius:5px;">📞 연결</button>
                </a>
            """, unsafe_allow_html=True)
        st.divider()

