import streamlit as st
import pandas as pd
import re
from collections import Counter

st.set_page_config(page_title="카톡 요약 게시판", layout="wide")

# ---------------------------
# 1. 카톡 TXT 파싱 (안정 버전)
# ---------------------------
def parse_kakao(text):
    lines = text.split("\n")

    data = []
    current = None

    for line in lines:
        # 카톡 기본 패턴 감지 (날짜 + , 포함)
        if "," in line and ":" in line:
            try:
                date_part, rest = line.split(",", 1)
                user, message = rest.split(":", 1)

                current = {
                    "datetime": date_part.strip(),
                    "user": user.strip(),
                    "message": message.strip()
                }
                data.append(current)

            except:
                continue
        else:
            # 줄바꿈 메시지 이어붙이기
            if current:
                current["message"] += " " + line.strip()

    return pd.DataFrame(data)


# ---------------------------
# 2. 요약 + 키워드
# ---------------------------
def summarize(messages):
    text = " ".join(messages)

    words = re.findall(r'\w+', text)
    keywords = Counter(words)

    top_keywords = [k for k, v in keywords.most_common(5)]

    summary = " / ".join(top_keywords) if top_keywords else "요약 없음"

    return summary, top_keywords


# ---------------------------
# 3. 토픽 분류
# ---------------------------
def classify(msg):
    if "회의" in msg:
        return "회의"
    elif "공지" in msg:
        return "공지"
    elif "자료" in msg or "파일" in msg:
        return "업무"
    elif "일정" in msg:
        return "일정"
    else:
        return "일반"


# ---------------------------
# UI
# ---------------------------
st.title("📊 카카오톡 요약 게시판")

uploaded = st.file_uploader("📂 카톡 TXT 파일 업로드", type="txt")

if uploaded:
    text = uploaded.read().decode("utf-8")

    df = parse_kakao(text)

    # ✅ 방어 코드 (핵심)
    if df.empty or "message" not in df.columns:
        st.error("❌ 카톡 TXT 형식을 인식하지 못했습니다.\n\n👉 대화 내보내기 파일인지 확인해주세요.")
        st.stop()

    # 토픽 분류
    df["topic"] = df["message"].apply(classify)

    # 날짜 추출
    df["date"] = df["datetime"].apply(lambda x: x.split(",")[0] if "," in x else x)

    # ---------------------------
    # 사이드바 필터
    # ---------------------------
    st.sidebar.title("🔍 필터")

    topics = df["topic"].unique().tolist()
    selected_topics = st.sidebar.multiselect("토픽 선택", topics, default=topics)

    df = df[df["topic"].isin(selected_topics)]

    # ---------------------------
    # 게시판 출력
    # ---------------------------
    grouped = df.groupby("date")

    for date, group in grouped:
        st.markdown(f"## 📅 {date}")

        # 요약
        summary, keywords = summarize(group["message"].tolist())

        st.markdown("### 🧠 요약")
        st.info(summary)

        # 키워드
        st.markdown("### 🏷 키워드")
        if keywords:
            st.write(", ".join(keywords))
        else:
            st.write("없음")

        # 토픽 표시
        st.markdown("### 📁 포함 토픽")
        st.write(", ".join(group["topic"].unique()))

        # 원본보기
        with st.expander("📄 원본보기"):
            for _, row in group.iterrows():
                st.write(f"**[{row['topic']}] {row['user']}**: {row['message']}")

        st.divider()
