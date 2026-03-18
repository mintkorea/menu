import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# 파일 저장 경로 설정 (데이터 유실 방지)
LEAVE_FILE = 'leaves.csv'

def load_data():
    if os.path.exists(LEAVE_FILE):
        return pd.read_csv(LEAVE_FILE)
    return pd.DataFrame(columns=['날짜', '성명', '대근자'])

st.set_page_config(page_title="C조 근무 편성표", layout="wide")
st.write("###### 🗓️ C조 근무편성 (3일 주기 / 초소형 모드)")

# 데이터 로드
leaves_df = load_data()
c_names = ["김태언", "이정석", "이태원"]
res = []

# 3일 주기 근무 로직 적용 (3월 18일 근무 포함)
for day in range(1, 32):
    target = datetime(2026, 3, day)
    t_str = target.strftime('%Y-%m-%d')
    
    if day % 3 == 0:
        cycle_idx = (day // 3) - 1
        idx = (cycle_idx // 2) % 3
        a, b, c = c_names[idx], c_names[(idx+1)%3], c_names[(idx+2)%3]
        if cycle_idx % 2 == 1: b, c = c, b
        
        # 연차 데이터 대조
        l_name, s_name = "", ""
        current_leave = leaves_df[leaves_df['날짜'] == t_str]
        if not current_leave.empty:
            l_name = current_leave.iloc[0]['성명']
            s_name = current_leave.iloc[0]['대근자']
            if l_name in [a, b, c]: a = l_name
            
        res.append({
            "일자": f"{target.month}/{target.day:02d}",
            "조장": "황재업", "A(회관)": a, "B(산연)": b, "C(산연)": c, 
            "연차": l_name, "맞대근": s_name
        })

# 스타일 설정: 폰트 8px로 극단적 축소
def style_ultra_mini(val):
    color = ''
    if val == "황재업": color = 'background-color: #D9EAD3'
    elif val == "김태언": color = 'background-color: #FFF2CC'
    elif val == "이정석": color = 'background-color: #D0E0E3'
    elif val == "이태원": color = 'background-color: #F4CCCC'
    return f'{color}; font-size: 8px; padding: 0px; text-align: center;'

if res:
    st.dataframe(
        pd.DataFrame(res).style.applymap(style_ultra_mini),
        use_container_width=True,
        hide_index=True,
        height=600
    )
