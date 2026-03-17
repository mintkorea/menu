import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import calendar

# 1. 명단 데이터 (코드에 직접 내장)
CONTACT_DATA = [
    {"조": "공통", "직위": "보안소장", "성명": "이규용", "연락처": "010-8883-6580"},
    {"조": "공통", "직위": "보안부소장", "성명": "박상현", "연락처": "010-3193-4603"},
    {"조": "공통", "직위": "보안반장", "성명": "유정수", "연락처": "010-5316-8065"},
    {"조": "공통", "직위": "보안반장", "성명": "오제준", "연락처": "010-3352-8933"},
    {"조": "공통", "직위": "보안반장", "성명": "이강택", "연락처": "010-9048-6708"},
    {"조": "A조", "직위": "보안조장", "성명": "배준용", "연락처": "010-4717-7065"},
    {"조": "A조", "직위": "보안조원", "성명": "이명구", "연락처": "010-8638-5819"},
    {"조": "A조", "직위": "보안조원", "성명": "김영중", "연락처": "010-7726-5963"},
    {"조": "A조", "직위": "보안조원", "성명": "김삼동", "연락처": "010-2345-8081"},
    {"조": "B조", "직위": "보안조장", "성명": "심규천", "연락처": "010-8287-9895"},
    {"조": "B조", "직위": "보안조원", "성명": "임종현", "연락처": "010-7741-6732"},
    {"조": "B조", "직위": "보안조원", "성명": "권영국", "연락처": "010-4085-9982"},
    {"조": "B조", "직위": "보안조원", "성명": "전준수", "연락처": "010-5687-7107"},
    {"조": "C조", "직위": "보안조장", "성명": "황재업", "연락처": "010-9278-6622"},
    {"조": "C조", "직위": "보안조원", "성명": "이태원", "연락처": "010-9265-7881"},
    {"조": "C조", "직위": "보안조원", "성명": "김태언", "연락처": "010-5386-5386"},
    {"조": "C조", "직위": "보안조원", "성명": "이정석", "연락처": "010-2417-1173"},
    {"조": "A조", "직위": "보안조장", "성명": "손병휘", "연락처": "010-9966-2090"},
    {"조": "B조", "직위": "보안조장", "성명": "황일범", "연락처": "010-8929-4294"},
    {"조": "C조", "직위": "보안조장", "성명": "피재영", "연락처": "010-9359-2569"},
    {"조": "기숙사", "직위": "보안조원", "성명": "유시균", "연락처": "010-8737-5770"},
    {"조": "기숙사", "직위": "보안조원", "성명": "이상헌", "연락처": "010-4285-4231"}
]

st.set_page_config(page_title="보안 통합 관리", layout="wide")

# 세션 상태 (연차 데이터 저장용)
if 'leaves' not in st.session_state:
    st.session_state.leaves = pd.DataFrame(columns=['날짜', '성명', '대근자'])

# --- 디자인 수정 (코드 노출 방지 핵심) ---
st.markdown("""
<style>
    .grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
        gap: 10px;
    }
    .card {
        background: #ffffff; border: 1px solid #ddd; border-radius: 12px;
        padding: 15px; text-align: center; transition: 0.3s; height: 110px;
        display: flex; flex-direction: column; justify-content: center;
    }
    .card:hover { background: #1b5e20; color: white !important; }
    .card:hover div { color: white !important; }
    .card .phone { display: none; font-weight: bold; font-size: 0.9em; }
    .card:hover .name-tag { display: none; }
    .card:hover .phone { display: block; }
    .call-link {
        color: #ffeb3b !important; text-decoration: none; border: 1px solid #ffeb3b;
        padding: 2px 8px; border-radius: 6px; margin-top: 8px; display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# 메인 메뉴 탭
tab_call, tab_apply, tab_calendar, tab_work = st.tabs(["📱 연락망", "📝 연차신청", "📅 현황판", "🗓️ C조 근무표"])

# --- TAB 1: 연락망 ---
with tab_call:
    df = pd.DataFrame(CONTACT_DATA)
    sel_group = st.selectbox("조 필터", ["전체"] + sorted(list(df['조'].unique())))
    disp_df = df if sel_group == "전체" else df[df['조'] == sel_group]
    
    html = '<div class="grid-container">'
    for _, r in disp_df.iterrows():
        tel = r['연락처'].replace('-', '')
        html += f'''
        <div class="card">
            <div class="name-tag">
                <div style="font-weight:bold; font-size:1.1em;">{r['성명']}</div>
                <div style="font-size:0.8em; color:gray;">{r['직위']}</div>
            </div>
            <div class="phone">
                {r['연락처']}<br>
                <a href="tel:{tel}" class="call-link">📞 통화</a>
            </div>
        </div>
        '''
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

# --- TAB 2: 연차신청 ---
with tab_apply:
    st.subheader("신규 연차 등록")
    with st.form("leave_form"):
        name = st.selectbox("성명", sorted([p['성명'] for p in CONTACT_DATA]))
        date = st.date_input("날짜", datetime.now())
        sub = st.text_input("맞대근자")
        if st.form_submit_button("신청 완료"):
            new_row = pd.DataFrame([[str(date), name, sub]], columns=['날짜', '성명', '대근자'])
            st.session_state.leaves = pd.concat([st.session_state.leaves, new_row]).drop_duplicates()
            st.success(f"{name}님 등록되었습니다.")

# --- TAB 3: 현황판 ---
with tab_calendar:
    m = st.selectbox("월 선택", range(1, 13), index=datetime.now().month-1)
    last_day = calendar.monthrange(2026, m)[1]
    cols = [f"{m}/{d:02d}" for d in range(1, last_day+1)]
    names = sorted(list(set([p['성명'] for p in CONTACT_DATA])))
    
    matrix = pd.DataFrame("", index=names, columns=cols)
    for _, r in st.session_state.leaves.iterrows():
        dt = datetime.strptime(r['날짜'], '%Y-%m-%d')
        if dt.month == m:
            matrix.at[r['성명'], f"{m}/{dt.day:02d}"] = "연차"
    
    st.dataframe(matrix.style.applymap(lambda x: 'background-color: #ffcdd2' if x == "연차" else ''))

# --- TAB 4: C조 근무표 ---
with tab_work:
    st.subheader("🗓️ C조 ABC 순환 편성")
    c_list = ["김태언", "이정석", "이태원"]
    start_d = datetime(2026, 3, 1)
    
    results = []
    for i in range(31):
        target_d = start_d + timedelta(days=i)
        t_str = target_d.strftime('%Y-%m-%d')
        
        # 기본 루틴 (2일씩 순환)
        idx = (i // 2) % 3
        a, b, c = c_list[idx], c_list[(idx+1)%3], c_list[(idx+2)%3]
        if i % 2 == 1: b, c = c, b # B,C 교대
        
        # 연차 체크
        leave_p = st.session_state.leaves[st.session_state.leaves['날짜'] == t_str]
        l_name, s_name = "", ""
        if not leave_p.empty:
            l_name = leave_p.iloc[0]['성명']
            s_name = leave_p.iloc[0]['대근자']
            # 규칙: 연차자는 무조건 A자리 배치
            if l_name in [a, b, c]: a = l_name
            
        results.append([target_d.strftime('%m/%d(%a)'), "황재업", a, b, c, l_name, s_name])
    
    st.table(pd.DataFrame(results, columns=["일자", "조장", "A(회관)", "B(의산연)", "C(의산연)", "연차", "맞대근"]))
