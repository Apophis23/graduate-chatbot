from uuid import uuid4
from fastapi import APIRouter, HTTPException, UploadFile, Form
from sse_starlette.sse import EventSourceResponse
from process import *
import asyncio

router = APIRouter()

# 메모리 기반 데이터 저장소 (임시)
chats = {}

async def sse_stream(chat_id: str, message: str, file_name: str):
    # 한 글자씩 스트림
    for char in message:
        yield f"{char}"
        await asyncio.sleep(0.001)  # 약간의 딜레이로 생성 느낌 구현
    print("\n")
    '''
    # 파일명이 있는 경우
    if file_name != "No file uploaded":
        yield f"data: File Name: {file_name}\n\n"
    '''
    
@router.post('/chats')
async def create_new_chat():
    chat_id = str(uuid4())[:8]
    chats[chat_id] = []  # 채팅 기록 초기화
    print(f"New chat created: {chat_id}")  # 생성된 채팅 ID를 콘솔에 출력
    return {"id": chat_id}

@router.post('/chats/{chat_id}')
async def chat(chat_id: str, message: str = Form(...), file: UploadFile = None):
    if chat_id not in chats:
        raise HTTPException(status_code=404, detail=f"Chat {chat_id} does not exist")

    # 메시지 추가
    chats[chat_id].append(message)

    # 파일명 출력 (파일이 있을 경우)
    file_name = file.filename if file else None
    response = make_response(message, file)
    print(response)

    print(f"Chat ID: {chat_id}, Received Message: {message}, File Name: {file_name}")

    # SSE 스트림에 파일명 추가
    return EventSourceResponse(sse_stream(chat_id, response, file_name))
