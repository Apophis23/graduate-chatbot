import asyncio
from fastapi import HTTPException  # 추가
import fitz
import openai
import os
import random
import pdfplumber
from app.prompt import *
from app.course import *
from app.config import Settings
from app.message import *
from app.course import *

def load_pdf_text(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def preprocess_text(text):
    # 정규 표현식 패턴 정의
    pattern = r"[A-Z]{3}\d{4}\s.*?\s\d\.\d\s[A-Z]\d?\s[가-힣]+"
    # 정규식을 사용하여 패턴에 맞는 모든 문자열 추출
    matches = re.findall(pattern, text)
    # 추출된 항목을 줄바꿈으로 이어붙여 반환
    return "\n".join(matches)

def extract_major_info(text):
    major_info = {}
    
    # 전공 추출
    major_match = re.search(r'소 속\s+.*\s+(\S+)\s+컴퓨터공학', text)
    if major_match:
        major_info['주전공'] = major_match.group(1)
    else:
        major_info['주전공'] = '정보 없음'
    
    # 복수전공 추출
    double_major_match = re.search(r'\[복수전공:(.*?),', text)
    if double_major_match:
        major_info['복수전공'] = double_major_match.group(1).strip()
    else:
        major_info['복수전공'] = '없음'
    
    return major_info

def remove_retake_courses(text):
    # 정규식 패턴: '재 '로 시작하고 다음 학수번호가 나타나기 전까지의 내용을 매칭
    pattern = r"재 [A-Z]{3}\d{4,5}.*?(?=[A-Z]{3}\d{4,5}|\Z)"
    # 매칭된 부분을 공백으로 대체
    cleaned_text = re.sub(pattern, "", text, flags=re.DOTALL)
    # 중복 공백 제거
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    return cleaned_text

def extract_course_info(text):
    courses = []
    
    # 과목 정보 패턴 정의
    # 학수번호 과 목 명 학점평점전공 복 연 융 학 부
    pattern = re.compile(
        r'(?P<course_code>[A-Z]{3}\d{4,5})\s+'      # 학수번호
        r'(?P<course_name>.+?(?=\s\d+\.\d))\s'       # 과목명                  
        r'(?P<credit>\d+\.\d)\s+'                    # 학점
        r'(?P<grade>[A-Z]\+?|P|F|-)\s+'              # 평점
        r'(?P<classification>\S+)'                   # 전공 분류
    )
    
    # 모든 과목 정보 찾기
    for match in pattern.finditer(text):
        course = {
            '학수번호': match.group('course_code'),
            '과목명': match.group('course_name').strip(),
            '학점': float(match.group('credit')),
            '평점': match.group('grade'),
            '전공구분': match.group('classification'),
        }
        courses.append(course)
    
    return courses

def calculate_credit_totals(courses):
    total_credits = {}
    
    # 전공 구분별 학점 초기화
    classifications = ['전필', '전선', '교필', '교선', '일선', '기타']
    for cls in classifications:
        total_credits[cls] = 0.0
    
    for course in courses:
        cls = course['전공구분']
        credit = course['학점']
        
        if course['평점'] in '-':
            continue
        if cls in total_credits:
            total_credits[cls] += credit
        else:
            total_credits['기타'] += credit  # 정의되지 않은 전공구분은 '기타'로 처리
    
    return total_credits

def recommend_system(transcript_text, course):
    recommend_number = random.randint(5, 8)
    recommend = [f"{key} : {value}" for key, value in course.items() if key not in transcript_text]
    recommend_list = random.sample(recommend, min(recommend_number, len(recommend)))
    return recommend_list

def make_response(message, file):
    response = ""
    transcript_text = ""
    
    if os.path.exists("./uploads/temp.pdf"):
        transcript_text += load_pdf_text('./uploads/temp.pdf')
    
    if "영어" in message in message:
        text = "인하대학교 소프트웨어 융합대학 영어 졸업 기준을 안내해 드리겠습니다.\n\n2016학년도 이후 신입생 및 2018학년도 이후 3학년 편입생 기준 졸업요건은 아래와 같습니다:\n\n"
        for item in english:
            text += f"• {item}\n\n"
        text+="\n 영어성적을 미취득 하신 경우 대학원 진학 희망자는 TOEIC이나 TEPS, 취업 희망자는 OPIc 취득을 추천합니다.\n"
        response = text
    
    elif "사용법" in message or "가이드" in message:
        response = f"인하대학교 졸업사정 챗봇의 사용법을 알려드리겠습니다.\n\n 1. 인하대학교 포털시스템에서 참고용 성적표를 다운로드 해주세요. \n\n 2. 성적표와 \'졸업가능여부 알려줘\'와 같이 입력하면 졸업 가능 여부 및 부족한 부분을 알려드립니다. \n\n 3. 기타 영어 졸업 요건 및 졸업고사 대체 요건을 확인하고 싶다면 \'영어 졸업 요건 알려줘\', \'졸업 고사 대체 요건 알려줘\'와 같이 입력해 주세요!" 
        
    elif "졸업고사" in message or "졸업 고사" in message or "제출 서류" in message:
        text = "졸업 고사 대체를 위해 필요한 내용을 알려드리겠습니다. \n\n 성적요건을 충족하셨더라도 아래 요건 중 하나를 선택해서 과사무실에 제출 혹은 진행해 주세요.\n\n \n\n 졸업고사를 대체하기 위한 조건은 아래와 같습니다.\n\n"
        for item in submit_list:
            text += f"{item}\n\n"
        text += "\n 상기한 내용 중 하나를 반드시 선택하여 제출하거나 응시하시여 졸업에 차질 없도록 준비해주세요!"
        response = text
    
    elif "전공" in message and "추천" in message:
        recommend_list = recommend_system(transcript_text, CSE_course)
        text = "물론입니다! 현재 성적표상에서 수강하지 않은 전공 과목 중 몇가지를 추천해 드리겠습니다!\n\n"
        for item in recommend_list:
            text += f"• {item}\n\n"
        text+="\n 위와 같은 과목을 수강하는 것을 권장드립니다! \n"
        response = text
        
    elif "핵심" in message and "교양" in message:
        recommend_list = recommend_system(transcript_text, core_general_course)
        text = "물론입니다! 현재 성적표상에서 수강하지 않은 핵심 교양 영역의 과목 중 몇가지를 추천해 드리겠습니다!\n\n"
        for item in recommend_list:
            text += f"• {item}\n\n"
        text+="\n 위와 같은 과목을 수강하는 것을 권장드립니다! \n"
        response = text
    
    elif "일반" in message and "교양" in message:
        recommend_list = recommend_system(transcript_text, general_course)
        text = "물론입니다! 현재 성적표상에서 수강하지 않은 일반 교양 영역의 과목 중 몇가지를 추천해 드리겠습니다!\n\n"
        # Add bullet points
        for item in recommend_list:
            text += f"• {item}\n\n"
        text+="\n 위와 같은 과목을 수강하는 것을 권장드립니다! \n"
        response = text
    
    elif file == None:
        response += "작업을 수행하기 위해서 참고용 성적표가 필요합니다. 참고용 성적표를 입력해 주세요."
    
    else:
        response = graduation_requirements
    return response