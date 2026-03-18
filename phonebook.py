import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# --- 1. 설정 및 데이터 로드 함수 ---
st.set_page_config(page_title="보안 통합 관리 시스템", layout="wide")

# 연차 데이터 저장 파일 경로
LEAVE_FILE = 'leave_data.csv'

def load_leaves():
    if os.path.exists(LEAVE_FILE):
        return pd.read_csv(LEAVE_FILE)
    return pd.DataFrame(columns=['날짜', '성명', '대근자'])

def save_leaves(df):
    df.to_csv(LEAVE_FILE, index=False, encoding='utf-8-sig')

# 28명 전체 명단 (이미지 기반)
CONTACT_DATA = [
    {"조": "공통", "직위": "소장", "성명": "이규용", "연락처": "010-8883-6580"},
    {"조": "공통", "직위": "부소장", "성명": "박상현", "연락처": "010-3193-4603"},
    {"조": "공통", "직위": "반장", "성명": "유정수", "연락처": "010-5316-8065"},
    {"조": "공통", "직위": "반장", "성명": "오제준", "연락처": "010-3352-8933"},
    {"조": "공통", "직위": "반장", "성명": "이강택", "연락처": "010-9048-6708"},
    {"조": "A조", "직위": "조장", "성명": "배준용", "연락처": "010-4717-7065"},
    {"조": "A조", "직위": "조원", "성명": "이명구", "연락처": "010-8638-5819"},
    {"조": "A조", "직위": "조원", "성명": "김영중", "연락처": "010-7726-5963"},
    {"조": "A조", "직위": "조원", "성명": "김삼동", "연락처": "010-2345-8081"},
    {"조": "B조", "직위": "조장", "성명": "심규천", "연락처": "010-8287-9895"},
    {"조": "B조", "직위": "조원", "성명": "임종현", "연락처": "010-7741-6732"},
    {"조": "B조", "직위": "조원", "성명": "권영국", "연락처": "010-4085-9982"},
    {"조": "B조", "직위": "조원", "성명": "전준수", "연락처": "010-5687-7107"},
    {"조": "C조", "직위": "조장", "성명": "황재업", "연락처": "010-9278-6622"},
    {"조": "C조", "직위": "조원", "성명": "이태원", "연락처": "010-9265-7881"},
    {"조": "C조", "직위": "조원", "성명": "김태언", "연락처": "010-5386-5386"},
    {"조": "C조", "직위": "조원", "성명": "이정석", "연락처": "010-2417-1173"},
    {"조": "A조", "직위": "조장", "성명": "손병휘", "연락처": "010-9966-2090"},
    {"조": "A조", "직위": "조원", "성명": "권순호", "연락처": "010-2539-1799"},
    {"조": "A조", "직위": "조원", "성명": "김진식", "연락처": "010-3277-0808"},
    {"조": "B조", "직위": "조장", "성명": "황일범", "연락처": "010-8929-4294"},
    {"조": "B조", "직위": "조원", "성명": "이상길", "연락처": "010-9904-0247"},
    {"조": "B조", "직위": "조원", "성명": "허용", "연락처": "010-8845-0163"},
    {"조": "C조", "직위": "조장", "성명": "피재영", "연락처": "010-9359-2569"},
    {"조": "C조", "직위": "조원", "성명": "남형민", "연락처": "010-8767-7073"},
    {"조": "C조", "직위": "조원", "성명": "강경훈", "연락처": "010-3436-6107"},
    {"조": "기숙사", "직위": "조원", "성명": "유시균", "연락처": "010-8737-5770"},
    {"조": "기숙사", "직위": "조원", "성명": "이상헌", "연락처": "010-4285-4231"}
]

# --- 2. 메뉴 선택 (사이드바) ---
menu = st.sidebar.selectbox("메뉴 선택", ["📱 비상연락망", "📝 연차 관리", "🗓️ C조 근무표"])

# --- [메뉴 1: 비상연락망] ---
if menu == "📱 비상연락망":
    st.subheader("📱 비상연락망 (클릭 시 전화연결)")
    df = pd.DataFrame(CONTACT_DATA)
    sel_group = st.selectbox("조 필터", ["전체", "A조", "B조", "C조", "공통", "기숙사"])
    disp_df = df if sel_group == "전체" else df[df['조'] == sel_group]
    
    cards_html = ""
    for _, r in disp_df.iterrows():
        tel = r['연락처'].replace('-', '')
        cards_html += f'''
        <div class="card" onclick="window.location.href='tel:{tel}'">
            <div class="name">{r['성명']}</div>
            <div class="rank">{r['직위']}</div>
            <div class="phone">{r['연락처'][-4:]}</div>
        </div>
        '''
    st.components.v1.html(f"""
    <style>
        .container {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 4px; font-family: sans-serif; }}
        .card {{ background: #fff; border: 1px solid #ddd; border-radius: 4px; padding: 5px 2px; text-align: center; cursor: pointer; }}
        .name {{ font-weight: bold; font-size: 11px; }}
        .rank {{ font-size: 8px; color: #666; }}
        .phone {{ font-size: 8px; color: #2e7d32; font-weight: bold; }}
    </style>
    <div class="container">{cards_html}</div>
    """, height=600, scrolling=True)

# --- [메뉴 2: 연차 관리] ---
elif menu == "📝 연차 관리":
    st.subheader("📝 연차 신청 및 현황")
    leaves_df = load_leaves()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("##### [신청]")
        with st.form("leave_form", clear_on_submit=True):
            name = st.selectbox("성명", sorted([p['성명'] for p in CONTACT_DATA]))
            date = st.date_input("날짜", datetime.now())
            sub = st.text_input("맞대근자")
            if st.form_submit_button("등록"):
                new_data = pd.DataFrame([[str(date), name, sub]], columns=['날짜', '성명', '대근자'])
                leaves_df = pd.concat([leaves_df, new_data]).drop_duplicates()
                save_leaves(leaves_df)
                st.success("저장되었습니다.")
                st.rerun()

    with col2:
        st.write("##### [현황 리스트]")
        if not leaves_df.empty:
            st.dataframe(leaves_df, use_container_width=True, hide_index=True)
            if st.button("전체 삭제 (주의)"):
                save_leaves(pd.DataFrame(columns=['날짜', '성명', '대근자']))
                st.rerun()
        else:
            st.info("등록된 연차가 없습니다.")

# --- [메뉴 3: C조 근무표] ---
elif menu == "🗓️ C조 근무표":
    st.subheader("🗓️ C조 근무표 (3일 주기)")
    leaves_df = load_leaves()
    c_names = ["김태언", "이정석", "이태원"]
    res = []
    
    # 요일 설정
    weekday_kr = ["월", "화", "수", "목", "금", "토", "일"]
    
    for day in range(1, 32):
        target = datetime(2026, 3, day)
        if day % 3 == 0:
            cycle_idx = (day // 3) - 1
            idx = (cycle_idx // 2) % 3
            a, b, c = c_names[idx], c_names[(idx+1)%3], c_names[(idx+2)%3]
            if cycle_idx % 2 == 1: b, c = c, b
            
            t_str = target.strftime('%Y-%m-%d')
            w_kr = weekday_kr[target.weekday()]
            
            # 연차 확인
            l_name, s_name = "", ""
            match = leaves_df[leaves_df['날짜'] == t_str]
            if not match.empty:
                l_name = match.iloc[0]['성명']
                s_name = match.iloc[0]['대근자']
                if l_name in [a, b, c]: a = l_name
            
            res.append({
                "일자": f"{target.month}/{target.day:02d}({w_kr})",
                "조장": "황재업", "A(회관)": a, "B(산연)": b, "C(산연)": c, "연차": l_name
            })
            
    df_res = pd.DataFrame(res)
    
    def style_ultra(val):
        color = ''
        if val == "황재업": color = 'background-color: #D9EAD3'
        elif val == "김태언": color = 'background-color: #FFF2CC'
        elif val == "이정석": color = 'background-color: #D0E0E3'
        elif val == "이태원": color = 'background-color: #F4CCCC'
        return f'{color}; font-size: 8px; text-align: center; padding: 0px;'

    st.dataframe(
        df_res.style.applymap(style_ultra),
        use_container_width=True, hide_index=True, height=600
    )
