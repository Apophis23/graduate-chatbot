# graduate-chatbot
이 레포지토리는 인하대학교 컴퓨터공학과 2024-2학기 컴퓨터공학 종합 설계 (CSE4205-002) 10팀 AAAI의 프로젝트 디렉토리입니다.

저희 프로젝트는 복잡한 졸업사정 요건을 학생들 및 교직원이 쉽게 처리할 수 있도록 도울 수 있는 챗봇을 구성하는 것으로 목표로 진행하였습니다.

이 어플리케이션은 RAG와 LLAMA, Chagpt를 활용해서 성적표 pdf 입력시 졸업 가능여부를 알려주고, 학생들에게 부족한 부분을 알려줍니다.

백엔드 및 전체적인 UI 구성은 (https://github.com/ruizguille/tech-trends-chatbot/tree/master) 해당 프로젝트를 참고하였습니다.

## 구조
이 레포지토리는 2가지 메인 디렉토리로 구성되어 있습니다.
- backend/ : FastAPI와 RAG를 활용하여 구성된 백엔드 코드입니다.
- frontend/ : React 프론트엔드 코드입니다. Vite.js를 빌드 도구 및 번들러로 사용합니다.

## 설치
### 파이썬 및 종속성
- Python 3.11 이상.
- Node.js 18 이상.
- Poetry (Python 패키지 관리자).

### 백엔드
1. backend 폴더로 이동해서 가상환경 생성
bash
    cd backend
    python -m venv 가상환경이름
2. 가상환경 활성화
bash
    ./venv/Scripts/activate
3. poetry로 python 종속성 설치
bash
    poetry install

### 프론트엔드
1. frontend 폴더로 이동해서 자바스크립트 종속성 설치
bash
    cd frontend
    npm install

## 어플리케이션 실행
1. 백엔드 폴더에서 가상환경을 활성화 하고 백엔드 서버 시작
bash
    cd backend
    uvicorn app.main:app --reload
2. 다른 터미널을 활용하여 프론트엔드 서버 시작
bash
    cd frontend
    npm run dev
3. 웹 브라우저에서 http://localhost:3000을 열어 애플리케이션에 접속