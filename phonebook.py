
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# --- 1. 설정 및 데이터 관리 ---
st.set_page_config(page_title="보안 통합 관리 시스템", layout="wide")
LEAVE_FILE = 'leave_data.csv'

def load_leaves():
    if os.path.exists(LEAVE_FILE):
        return pd.read_csv(LEAVE_FILE)
    return pd.DataFrame(columns=['날짜', '성명', '대근자'])

def save_leaves(df):
    df.to_csv(LEAVE_FILE, index=False, encoding='utf-8-sig')

# 28명 전체 명단
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

# --- 2. 사이드바 메뉴 ---
menu = st.sidebar.selectbox("메뉴 선택", ["📱 비상연락망", "📝 연차 관리", "🗓️ C조 근무표"])

if menu == "📱 비상연락망":
    st.subheader("📱 비상연락망 (4열 배치)")
    df = pd.DataFrame(CONTACT_DATA)
    sel_group = st.selectbox("조 필터", ["전체", "A조", "B조", "C조", "공통", "기숙사"])
    disp_df = df if sel_group == "전체" else df[df['조'] == sel_group]
    
    cards_html = "".join([f'''
        <div class="card" onclick="window.location.href='tel:{r['연락처'].replace('-', '')}'">
            <div class="name">{r['성명']}</div>
            <div class="rank">{r['직위']}</div>
            <div class="phone">{r['연락처'][-4:]}</div>
        </div>
    ''' for _, r in disp_df.iterrows()])
    
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

elif menu == "📝 연차 관리":
    st.subheader("📝 연차 신청 및 저장")
    leaves_df = load_leaves()
    c_members = sorted([p['성명'] for p in CONTACT_DATA if p['조'] == "C조"])
    
    with st.form("leave_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        name = col1.selectbox("성명", c_members)
        date = col2.date_input("날짜", datetime.now())
        sub = col3.text_input("맞대근자")
        if st.form_submit_button("등록"):
            new_data = pd.DataFrame([[str(date), name, sub]], columns=['날짜', '성명', '대근자'])
            leaves_df = pd.concat([leaves_df, new_data]).drop_duplicates()
            save_leaves(leaves_df)
            st.success("데이터가 안전하게 저장되었습니다.")
            st.rerun()

    st.write("---")
    st.dataframe(leaves_df.sort_values(by='날짜'), use_container_width=True, hide_index=True)
    if st.button("전체 데이터 삭제"):
        save_leaves(pd.DataFrame(columns=['날짜', '성명', '대근자']))
        st.rerun()

elif menu == "🗓️ C조 근무표":
    st.subheader("🗓️ C조 근무표 (9일 김태언 시작 기준)")
    leaves_df = load_leaves()
    
    # 설정값: 입사순위(김태언 > 이태원 > 이정석) 및 회관순번
    staff_rank = {"김태언": 1, "이태원": 2, "이정석": 3}
    a_rotation = ["김태언", "이정석", "이태원"]
    weekday_kr = ["월", "화", "수", "목", "금", "토", "일"]
    
    res = []
    # 3월 3일(화)부터 3월 31일(화)까지 3일 주기 근무
    for day in range(3, 32, 3):
        target = datetime(2026, 3, day)
        t_str = target.strftime('%Y-%m-%d')
        
        # 3월 9일이 로직의 '3회차' 근무임 (3, 6, 9...)
        # 회차 인덱스 (0부터 시작)
        count_idx = (day // 3) - 1
        
        # 1. 회관(A) 근무자 결정: 2회씩 연속 근무
        a_idx = (count_idx // 2) % 3
        a_worker = a_rotation[a_idx]
        
        # 2. 의산연(B, C) 근무자 결정: 나머지 2명 중 선임이 B
        others = [name for name in staff_rank.keys() if name != a_worker]
        # 선임 순으로 정렬
        others_sorted = sorted(others, key=lambda x: staff_rank[x])
        b_worker, c_worker = others_sorted[0], others_sorted[1]
        
        # 3. 교대 규칙: 동일 A 근무자의 2번째 날에는 B/C 교대
        if count_idx % 2 == 1:
            b_worker, c_worker = c_worker, b_worker
            
        # 4. 연차 반영
        l_name = ""
        match = leaves_df[leaves_df['날짜'] == t_str]
        if not match.empty:
            l_name = match.iloc[0]['성명']
            if l_name == a_worker: pass # 이미 A면 유지
            elif l_name in [b_worker, c_worker]: a_worker = l_name # 연차자가 A로 이동
            
        res.append({
            "일자": f"{target.month}/{target.day:02d}({weekday_kr[target.weekday()]})",
            "조장": "황재업", "A(회관)": a_worker, "B(산연)": b_worker, "C(산연)": c_worker, "연차": l_name
        })

    def style_final(val):
        colors = {"황재업": "#D9EAD3", "김태언": "#FFF2CC", "이정석": "#D0E0E3", "이태원": "#F4CCCC"}
        bg = colors.get(val, "")
        return f'background-color: {bg}; font-size: 8px; text-align: center; padding: 0px;'

    st.dataframe(pd.DataFrame(res).style.applymap(style_final), use_container_width=True, hide_index=True, height=600)
