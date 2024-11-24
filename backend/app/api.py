from uuid import uuid4
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
import asyncio

router = APIRouter()

# 메모리 기반 데이터 저장소 (임시)
chats = {}

# Pydantic 모델 정의
class ChatMessage(BaseModel):
    message: str

async def sse_stream(chat_id: str, message: str):
    """
    SSE 스트림을 생성하는 비동기 제너레이터
    """
    yield f"{message}\n"
    await asyncio.sleep(1)  # 비동기 처리 시뮬레이션 (필요에 따라 제거)

@router.post('/chats')
async def create_new_chat():
    chat_id = str(uuid4())[:8]
    chats[chat_id] = []  # 채팅 기록 초기화
    print(f"New chat created: {chat_id}")  # 생성된 채팅 ID를 콘솔에 출력
    return {"id": chat_id}

@router.post('/chats/{chat_id}')
async def chat(chat_id: str, chat_message: ChatMessage):
    if chat_id not in chats:
        raise HTTPException(status_code=404, detail=f"Chat {chat_id} does not exist")

    chats[chat_id].append(chat_message.message)

    print(f"Chat ID: {chat_id}, Received Message: {chat_message.message}")

    return EventSourceResponse(sse_stream(chat_id, chat_message.message))
