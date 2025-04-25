# pydantic models for request and response validation 
from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str

class UploadResponse(BaseModel):
    message: str
    filename: str
    chunks_added: int
