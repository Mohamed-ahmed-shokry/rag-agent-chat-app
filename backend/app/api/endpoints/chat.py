# chat endpoint to handle chat requests and responses

from fastapi import APIRouter, HTTPException
from app.api.models import ChatRequest, ChatResponse
from app.services import chat_service
import asyncio 

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    if not request.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    try:
        # Assuming get_chat_response is async
        answer = await chat_service.get_chat_response(request.query)
        # If sync: answer = chat_service.get_chat_response(request.query)
        return ChatResponse(answer=answer)
    except Exception as e:
        # Log the exception e
        print(f"Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")



