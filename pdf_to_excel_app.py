import streamlit as st
import pdfplumber
import pandas as pd
import re
from io import BytesIO

st.set_page_config(page_title="연락망 자동 변환", layout="wide")

st.title("📄 PDF → 연락망 엑셀 변환기")

uploaded_file = st.file_uploader("PDF 업로드", type="pdf")

def extract_data(pdf_file):
    data = []

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            if not text:
                continue

            lines = text.split("\n")

            dept = ""

            for line in lines:
                line = line.strip()

                # 부서 인식 (숫자 시작)
                if re.match(r"^\d+\.", line):
                    dept = line.split(".")[1].strip()
                    continue

                # 이름 + 전화 패턴
                name_phone = re.search(r"([가-힣]{2,4})\s+(010-\d{4}-\d{4})", line)

                if name_phone:
                    name = name_phone.group(1)
                    mobile = name_phone.group(2)

                    # 내선 찾기
                    ext_match = re.search(r"(02-\d{4}-\d{4}|\*1-\d{4}|\d{4})", line)

                    ext = ""
                    if ext_match:
                        ext = ext_match.group(1)
                        ext = ext.replace("02-3147-", "").replace("02-2258-", "")

                    # 직급 추정
                    rank_match = re.search(r"(팀장|차장|과장|대리|사원|책임|부장|UM)", line)
                    rank = rank_match.group(1) if rank_match else ""

                    # 업무 (대충 나머지)
                    job = line
                    job = re.sub(name, "", job)
                    job = re.sub(mobile, "", job)
                    job = re.sub(rank, "", job)
                    job = re.sub(r"(02-\d{4}-\d{4}|\*1-\d{4}|\d{4})", "", job)
                    job = job.strip()

                    data.append([dept, name, rank, job, mobile, ext])

    df = pd.DataFrame(data, columns=["부서","이름","직급","업무","휴대폰","내선"])
    return df

if uploaded_file:
    df = extract_data(uploaded_file)

    st.success(f"{len(df)}건 추출 완료")

    st.dataframe(df)

    # 다운로드
    output = BytesIO()
    df.to_excel(output, index=False)

    st.download_button(
        label="📥 엑셀 다운로드",
        data=output.getvalue(),
        file_name="contacts.xlsx"
    )