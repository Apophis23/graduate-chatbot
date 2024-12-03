import asyncio
from fastapi import HTTPException  # 추가
import fitz
import openai

english = ["TOEIC : 700점",
           "TOEIC Speaking : 130점",
           "TOEFL(PBT) : 540점",
           "TOEFL(CBT) : 207점", 
           "TOEFL(IBT) : 76점", 
           "NEW TEPS : 327점",
           "OPIc : IM1", 
           "IELTS : 6.0"]

def extract_images_from_pdf(file):
    try:
        images = []
        # Reset file pointer to the beginning
        file.file.seek(0)
        doc = fitz.open(stream=file.file.read(), filetype='pdf')
        for page_index in range(len(doc)):
            for img_index, img in enumerate(doc.get_page_images(page_index)):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                images.append((image_bytes, image_ext))
        return images
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"PDF image extraction error: {e}")

def make_response(message, file):
    response = ""
    if "영어" in message in message:
        text = "인하대학교 소프트웨어 융합대학 영어 졸업 기준을 안내해 드리겠습니다.\n\n2016학년도 이후 신입생 및 2018학년도 이후 3학년 편입생 기준 졸업요건은 아래와 같습니다:\n\n"
        # Add bullet points
        for item in english:
            text += f"• {item}\n\n"
        text+="\n 영어성적을 미취득 하신 경우 대학원 진학 희망자는 TOEIC이나 TEPS, 취업 희망자는 OPIc 취득을 추천합니다.\n"
        response = text
    elif file == None:
        response += "졸업 가능 여부를 계산하기 위해서 성적표가 필요합니다. 성적표를 입력해 주세요."
    elif "사용법" in message or "가이드" in message:
        text = "인하대학교 졸업사정 챗봇의 사용법을 알려드리겠습니다.\n\n 1. 인하대학교 포털시스템에서 참고용 성적표를 다운로드 해주세요. \n\n 2. 성적표와 \'졸업가능여부 알려줘\'와 같이 입력하면 졸업 가능 여부 및 부족한 부분을 알려드립니다."
    else:
        try:
            messages = [{"role": "system", "content": "당신은 졸업 요건에 대한 정보를 제공하는 도움이 되는 어시스턴트입니다."},{"role": "user", "content": [{"type": "text", "text": f"사용자의 질문:\n{message}"}]}]
            
            if file:
                images = extract_images_from_pdf("./인하대학교_전현태_성적표.pdf")
            
            print("file : ", images)
            
            for image_bytes, image_ext in images:
                base64_image = base64.b64encode(image_bytes).decode('utf-8')
                image_message = {"type": "image_url", "image_url": {
                    "url": f"data:image/{image_ext};base64,{base64_image}"}
                }
                messages[1]["content"].append(image_message)
                
            # gpt 50 token
            gpt4_response = openai.chat.completions.create(model="gpt-4o", messages=messages,
            max_tokens=1024,
            )
                   
            response = gpt4_response.choices[0].message.content

            # 최종 응답 반환
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    return response
