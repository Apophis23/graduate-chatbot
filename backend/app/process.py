import asyncio

english = ["TOEIC : 700점",
           "TOEIC Speaking : 130점",
           "TOEFL(PBT) : 540점",
           "TOEFL(CBT) : 207점", 
           "TOEFL(IBT) : 76점", 
           "NEW TEPS : 327점",
           "OPIc : IM1", 
           "IELTS : 6.0"]

def make_response(message, file):
    response = ""
    if "영어" in message or "졸업" in message or "기준" in message:
        text = "인하대학교 소프트웨어 융합대학 영어 졸업 기준을 안내해 드리겠습니다.\n\n2016학년도 이후 신입생 및 2018학년도 이후 3학년 편입생 기준 졸업요건은 아래와 같습니다:\n\n"
        # Add bullet points
        for item in english:
            text += f"• {item}\n\n"
        
        text+="\n 영어성적을 미취득 하신 경우 대학원 진학 희망자는 TOEIC이나 TEPS, 취업 희망자는 OPIc 취득을 추천합니다.\n"
        response = text
    return response
