# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import chat, upload
from app.core.config import OPENAI_API_KEY # Ensure key is loaded on startup

app = FastAPI(title="AI Chat App")

# CORS Middleware (adjust origins as needed for development/production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins for development
    # allow_origins=["http://localhost:3000"], # Example for React dev server
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)

app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])

@app.get("/")
def read_root():
    return {"message": "AI Chat App Backend is running"}

# Add uvicorn run command for development 
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)