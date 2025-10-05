import os
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import openai
import faiss
import numpy as np
from io import BytesIO
import uvicorn

# Load OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Allow frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store resumes + embeddings
resumes = []
embeddings = []

# Helper: get embedding
def get_embedding(text: str):
    response = openai.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response.data[0].embedding

@app.post("/index_resumes")
async def index_resumes(files: list[UploadFile]):
    results = []
    for f in files:
        try:
            content = await f.read()
            text = ""
            if f.filename.lower().endswith(".pdf"):
                from PyPDF2 import PdfReader
                reader = PdfReader(BytesIO(content))
                for page in reader.pages:
                    text += page.extract_text() or ""
            elif f.filename.lower().endswith(".docx"):
                import docx
                doc = docx.Document(BytesIO(content))
                for para in doc.paragraphs:
                    text += para.text + "\n"
            elif f.filename.lower().endswith(".txt"):
                text = content.decode("utf-8")
            else:
                raise ValueError("Unsupported file type")

            # Get embedding
            emb = get_embedding(text)
            resumes.append({"filename": f.filename, "text": text})
            embeddings.append(np.array(emb).astype("float32"))
            results.append({"filename": f.filename, "status": "success"})
        except Exception as e:
            results.append({"filename": f.filename, "status": "failed", "error": str(e)})
    return {"results": results}

@app.post("/query")
async def query_job(job_description: str = Form(...), top_k: int = Form(3)):
    if not embeddings:
        return {"results": []}
    
    job_emb = np.array(get_embedding(job_description)).astype("float32")
    index = faiss.IndexFlatL2(len(job_emb))
    index.add(np.array(embeddings))
    D, I = index.search(np.array([job_emb]), k=min(top_k, len(resumes)))
    
    results = []
    for j, i in enumerate(I[0]):
        res = resumes[i]
        results.append({
            "filename": res["filename"],
            "score": float(D[0][j]),
            "snippet": res["text"][:500] + ("..." if len(res["text"]) > 500 else "")
        })
    return {"results": results}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)