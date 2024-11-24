from uuid import uuid4
from fastapi import APIRouter, HTTPException, UploadFile, Form
from sse_starlette.sse import EventSourceResponse
import asyncio

router = APIRouter()

# 메모리 기반 데이터 저장소 (임시)
chats = {}

async def sse_stream(chat_id: str, message: str, file_name: str):
    yield f"Message: {message}\n\n"
    if file_name != "No file uploaded":
        yield f"File Name: {file_name}\n\n"
    await asyncio.sleep(1)

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
    print(f"Chat ID: {chat_id}, Received Message: {message}, File Name: {file_name}")

    # SSE 스트림에 파일명 추가
    return EventSourceResponse(sse_stream(chat_id, message, file_name))
