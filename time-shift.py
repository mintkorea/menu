import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta

# --- 1. 데이터 및 로직 설정 ---
START_DATE = datetime(2026, 3, 24).date()
RANK = ["김태언", "이태원", "이정석"]  # 선임 순서
HALL_ROTATION = ["김태언", "이정석", "이태원"] # 회관 순번
WORKER_COLORS = {"황재업": "#E1F5FE", "이태원": "#F3E5F5", "이정석": "#FFFDE7", "김태언": "#E8F5E9"}

def get_daily_layout(target_date):
    diff = (target_date - START_DATE).days
    if diff % 3 != 0: return None
    seq = (diff // 3) + 5 
    hall_worker = HALL_ROTATION[(seq // 2) % 3]
    others = [p for p in RANK if p != hall_worker]
    if seq % 2 == 0: return hall_worker, others[0], others[1]
    else: return hall_worker, others[1], others[0]

# --- 2. UI 레이아웃 ---
st.set_page_config(page_title="성의교정 C조", layout="centered")

with st.sidebar:
    st.header("👤 개인 설정")
    selected_user = st.selectbox("강조할 이름 선택", ["안 함", "황재업"] + RANK)
    st.info("이름을 선택하면 해당 줄이 강조됩니다.")

st.markdown("<h2 style='text-align:center;'>📅 성의교정 C조 근무 시스템</h2>", unsafe_allow_html=True)

# --- 3. HTML 생성 함수 (완전 격리 방식) ---
def generate_html(data_list, highlight_name):
    rows_html = ""
    for row in data_list:
        # 강조 색상 설정
        is_highlight = highlight_name in row.values()
        bg_color = WORKER_COLORS.get(highlight_name, "#ffffff") if is_highlight else "#ffffff"
        
        # 요일 색상 설정
        day_style = ""
        if "토" in row["날짜"]: day_style = "color: blue; font-weight: bold;"
        elif "일" in row["날짜"]: day_style = "color: red; font-weight: bold;"
        
        rows_html += f"""
        <tr style="background-color: {bg_color}; font-weight: {'bold' if is_highlight else 'normal'};">
            <td style="{day_style}">{row['날짜']}</td>
            <td>{row['조장']}</td>
            <td>{row['회관']}</td>
            <td>{row['의산A']}</td>
            <td>{row['의산B']}</td>
        </tr>
        """

    return f"""
    <div style="display: flex; justify-content: center;">
        <table style="width: 100%; border-collapse: collapse; font-family: sans-serif; text-align: center;">
            <thead>
                <tr style="background-color: #f2f2f2;">
                    <th style="border: 1px solid #ddd; padding: 12px;">날짜</th>
                    <th style="border: 1px solid #ddd; padding: 12px;">조장</th>
                    <th style="border: 1px solid #ddd; padding: 12px;">회관</th>
                    <th style="border: 1px solid #ddd; padding: 12px;">의산A</th>
                    <th style="border: 1px solid #ddd; padding: 12px;">의산B</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>
    """

# --- 4. 데이터 생성 및 출력 ---
display_data = []
for i in range(45):
    d = START_DATE + timedelta(days=i)
    res = get_daily_layout(d)
    if res:
        h, a, b = res
        display_data.append({
            "날짜": f"{d.strftime('%m/%d')}({['월','화','수','목','금','토','일'][d.weekday()]})",
            "조장": "황재업", "회관": h, "의산A": a, "의산B": b
        })

# [중요] components.html을 사용하여 HTML을 안전하게 렌더링
full_html = generate_html(display_data, selected_user)
components.html(full_html, height=1000, scrolling=True)
