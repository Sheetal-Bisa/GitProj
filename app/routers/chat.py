from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Literal

from app.services.openai_client import get_client

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
    last_message = req.messages[-1].content
    # Obtain client lazily at request time. This prevents import-time
    # failures when OPENAI_API_KEY is not set. The app's startup handler
    # already calls get_client() to initialize the client early.
    client = get_client()
    reply = client.generate_response(last_message)
    return ChatResponse(reply=reply)
