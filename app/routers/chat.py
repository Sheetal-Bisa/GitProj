from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Literal

from app.services.gemini import GeminiClient

router = APIRouter()


class ChatMessage(BaseModel):
	role: Literal["user", "assistant", "system"]
	content: str


class ChatRequest(BaseModel):
	messages: List[ChatMessage]


class ChatResponse(BaseModel):
	reply: str


@router.post("/", response_model=ChatResponse)
async def chat(req: ChatRequest):
	from app.services.gemini import get_client
	client = get_client()
	reply = await client.chat([m.model_dump() for m in req.messages])
	return ChatResponse(reply=reply)




