from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.services import vector_store
import os
import tempfile

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

def process_file(file_path: str, filename: str):
    """Loads, chunks, and stores a single file."""
    _, ext = os.path.splitext(filename)
    ext = ext.lower()

    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext == ".txt":
        loader = TextLoader(file_path, encoding='utf-8')
    else:
        print(f"Unsupported file type: {ext}")
        return 0

    documents = loader.load()
    if not documents:
        print("Could not load any documents from the file.")
        return 0

    # Add source metadata
    for doc in documents:
        doc.metadata["source"] = filename
        # PyPDFLoader adds 'page', TextLoader might not, handle appropriately

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = text_splitter.split_documents(documents)

    if chunks:
        vector_store.add_documents(chunks)
        return len(chunks)
    else:
        print("No chunks were created from the document.")
        return 0

def process_uploaded_file(file):
    """Handles uploaded file, saves temporarily, processes, then deletes."""
    try:
        # Create a temporary file to store the upload
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
            tmp.write(file.file.read())
            tmp_path = tmp.name

        # Process the temporary file
        num_chunks = process_file(tmp_path, file.filename)

    except Exception as e:
        print(f"Error processing file {file.filename}: {e}")
        num_chunks = 0 # Ensure cleanup happens
    finally:
        # Clean up the temporary file
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.remove(tmp_path)

    return num_chunks