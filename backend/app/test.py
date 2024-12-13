import fitz
from fastapi import HTTPException
import pdfplumber
import re
# from app.config import *
from app.course import *
import random

def recommend_system(message):
    recommend = [f"{key} : {value}" for key, value in CSE_course.items() if key not in message]
    recommend_list = random.sample(recommend, min(5, len(recommend)))
    return recommend_list

def load_pdf_text(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def preprocess_text(text):
    pattern = r"[A-Z]{3}\d{4}\s.*?\s\d\.\d\s[A-Z]\d?\s[가-힣]+"
    matches = re.findall(pattern, text)
    return "\n".join(matches)

def extract_major_info(text):
    major_info = {}
    major_match = re.search(r'소 속\s+.*\s+(\S+)\s+컴퓨터공학', text)
    if major_match:
        major_info['주전공'] = major_match.group(1)
    else:
        major_info['주전공'] = '정보 없음'
    
    double_major_match = re.search(r'\[복수전공:(.*?),', text)
    if double_major_match:
        major_info['복수전공'] = double_major_match.group(1).strip()
    else:
        major_info['복수전공'] = '없음'
    
    return major_info

def remove_retake_courses(text):
    pattern = r"재 [A-Z]{3}\d{4,5}.*?(?=[A-Z]{3}\d{4,5}|\Z)"
    cleaned_text = re.sub(pattern, "", text, flags=re.DOTALL)
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

transcript_text = load_pdf_text('./인하대학교_전현태_성적표.pdf')
major_info = extract_major_info(transcript_text)
remove_retake = remove_retake_courses(transcript_text)
preprocess = preprocess_text(remove_retake)
course_info = extract_course_info(transcript_text)
credit_totals = calculate_credit_totals(course_info)


#print(transcript_text)
#print(course_info)

#print(major_info)
# print(course_info)
# print(len(course_info))
# print(credit_totals)
# print(preprocess)
# print(remove)

#print(remove_retake)
print(transcript_text)
