import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import calendar

# 1. 28명 전체 명단 (오류 수정 완료)
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

st.set_page_config(page_title="보안 통합 관리", layout="wide")

if 'leaves' not in st.session_state:
    st.session_state.leaves = pd.DataFrame(columns=['날짜', '성명', '대근자'])

tab1, tab2, tab3, tab4 = st.tabs(["📱 연락망", "📝 연차신청", "📅 현황판", "🗓️ C조 근무표"])

# --- TAB 1: 연락망 (4열 배치) ---
with tab1:
    df = pd.DataFrame(CONTACT_DATA)
    sel_group = st.selectbox("조 필터", ["전체"] + sorted(list(df['조'].unique())))
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
        .rank {{ font-size: 8px; color: #666; margin: 1px 0; }}
        .phone {{ font-size: 8px; color: #2e7d32; }}
    </style>
    <div class="container">{cards_html}</div>
    """, height=650, scrolling=True)

# --- TAB 4: C조 근무표 (한글 요일, 9px 폰트) ---
with tab4:
    weekday_kr = ["월", "화", "수", "목", "금", "토", "일"]
    c_names = ["김태언", "이정석", "이태원"]
    start_d = datetime(2026, 3, 1) #
    
    res = []
    for i in range(31):
        target = start_d + timedelta(days=i)
        t_str = target.strftime('%Y-%m-%d')
        w_kr = weekday_kr[target.weekday()]
        
        # ABC 2회 연속 근무 루틴
        idx = (i // 2) % 3
        a, b, c = c_names[idx], c_names[(idx+1)%3], c_names[(idx+2)%3]
        if i % 2 == 1: b, c = c, b # B/C 교대
        
        # 연차 반영 (연차자는 A 배치)
        l_name = ""
        lp = st.session_state.leaves[st.session_state.leaves['날짜'] == t_str]
        if not lp.empty:
            l_name = lp.iloc[0]['성명']
            if l_name in [a, b, c]: a = l_name
            
        res.append({
            "일자": f"{target.month}/{target.day}({w_kr})",
            "조장": "황재업", "A(회관)": a, "B(산연)": b, "C(산연)": c, "연차": l_name
        })

    def style_mini(val):
        color = ''
        if val == "황재업": color = 'background-color: #D9EAD3' #
        elif val == "김태언": color = 'background-color: #FFF2CC' #
        elif val == "이정석": color = 'background-color: #D0E0E3' #
        elif val == "이태원": color = 'background-color: #F4CCCC' #
        return f'{color}; font-size: 9px; padding: 1px; text-align: center;'

    st.dataframe(pd.DataFrame(res).style.applymap(style_mini), use_container_width=True, height=600)
