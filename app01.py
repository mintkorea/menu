import google.generativeai as genai
import PIL.Image

# 1. API 키 설정
genai.configure(api_key="AIzaSyCXNQ3b9qcaJjQAGua3-vcgRZ2j0wASaXM")

# 2. 모델 설정 (1.5 Flash가 이미지 처리에 효율적입니다)
model = genai.GenerativeModel('gemini-1.5-flash')

def convert_table_image_to_text(image_path):
    try:
        # 3. 이미지 로드
        img = PIL.Image.open(image_path)
        
        # 4. 프롬프트 작성 (표 형식 지정)
        prompt = """
        이 이미지에 있는 표를 읽어서 Markdown 형식으로 변환해줘. 
        텍스트가 누락되지 않도록 주의하고, 표의 구조를 그대로 유지해줘.
        """
        
        # 5. API 호출
        response = model.generate_content([prompt, img])
        
        print("변환 결과:")
        print(response.text)
        
    except Exception as e:
        print(f"에러 발생: {e}")

# 실행
convert_table_image_to_text('table_image.png')
