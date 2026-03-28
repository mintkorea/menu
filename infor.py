import pandas as pd
import streamlit as st
import io
import zipfile

# --- 1. 파일 정보 설정 ---
def get_file_info():
    return {
        '의산연본관.csv': '🔬 의산연 본관',
        '대학본관.csv': '🏢 대학 본관',
        '의산연별관.csv': '🧪 의산연 별관',
        '성의회관.csv': '⛪ 성의회관',
        '병원별관.csv': '🏥 병원 별관',
        '옴니버스A.csv': '🍏 옴니버스파크(A)',
        '옴니버스B.csv': '🍎 옴니버스파크(B)',
        '서울성모병원.CSV': '🚑 서울성모병원'
    }

# --- 2. 메인 UI ---
def main():
    st.set_page_config(page_title="데이터 장바구니", layout="centered")
    
    st.markdown("""
        <style>
        .m-title { font-size: 1.2rem; font-weight: bold; color: #1E3A8A; margin-bottom: 20px; }
        .cart-box { 
            background-color: #f8f9fa; padding: 15px; border-radius: 12px; 
            border: 2px dashed #007bff; margin-bottom: 25px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='m-title'>🛒 성의교정 데이터 수정 장바구니</div>", unsafe_allow_html=True)

    file_map = get_file_info()
    files = list(file_map.keys())

    # --- [Step 1] 파일 선택 (멀티 셀렉트 / 장바구니) ---
    st.subheader("1. 수정할 파일들을 선택하세요 (중복 선택 가능)")
    selected_files = st.multiselect(
        "파일 목록",
        options=files,
        format_func=lambda x: file_map[x],
        default=None,
        label_visibility="collapsed"
    )

    # --- [Step 2] 장바구니 및 일괄 다운로드 ---
    if selected_files:
        st.markdown(f"### 2. 선택된 파일: {len(selected_files)}개")
        
        # 압축 파일을 담을 버퍼 메모리 생성
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for file_name in selected_files:
                try:
                    # 파일 읽기 (인코딩 대응)
                    try: df = pd.read_csv(file_name, encoding='utf-8-sig')
                    except: df = pd.read_csv(file_name, encoding='cp949')
                    
                    # CSV 데이터를 메모리에 저장
                    csv_data = df.to_csv(index=False, encoding='utf-8-sig')
                    zip_file.writestr(file_name, csv_data)
                except:
                    st.warning(f"⚠️ {file_name} 파일을 서버에서 찾을 수 없어 제외되었습니다.")

        # 압축 파일 다운로드 버튼
        st.markdown("<div class='cart-box'>", unsafe_allow_html=True)
        st.download_button(
            label="📦 선택한 파일들을 하나의 압축파일(.zip)로 받기",
            data=zip_buffer.getvalue(),
            file_name="성의교정_수정용_데이터.zip",
            mime="application/zip",
            type="primary",
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # 선택된 파일 목록 미리보기
        with st.expander("📋 선택된 파일 리스트 확인"):
            for f in selected_files:
                st.write(f"- {file_map[f]} ({f})")

    else:
        st.info("💡 위 목록에서 수정하고 싶은 파일들을 클릭하여 장바구니에 담아주세요.")

    st.markdown("---")
    st.caption("주의: 다운로드한 .zip 파일의 압축을 풀면 개별 CSV 파일들이 나옵니다. 수정 후 동일한 이름으로 서버에 올려주세요.")

if __name__ == "__main__":
    main()
