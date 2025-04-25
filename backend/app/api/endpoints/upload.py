#  upload endpoint to handle file uploads and process them
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services import document_processor
from app.api.models import UploadResponse
import asyncio

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    if not file.filename:
         raise HTTPException(status_code=400, detail="No filename provided.")

    allowed_extensions = {".txt", ".pdf"}
    ext = "." + file.filename.split(".")[-1].lower()
    if ext not in allowed_extensions:
         raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}. Allowed: {allowed_extensions}")

    try:
        num_chunks = await asyncio.get_event_loop().run_in_executor(
            None, document_processor.process_uploaded_file, file
        )
        # num_chunks = document_processor.process_uploaded_file(file) # If sync processing is acceptable

        if num_chunks > 0:
             return UploadResponse(
                 message="File processed successfully.",
                 filename=file.filename,
                 chunks_added=num_chunks
             )
        else:
             # Handle cases where processing failed or yielded no chunks
             raise HTTPException(status_code=500, detail=f"Failed to process or extract content from {file.filename}.")

    except Exception as e:
         # Log the exception e
         print(f"Upload error: {e}")
         raise HTTPException(status_code=500, detail=f"An error occurred processing the file: {str(e)}")

