from fastapi import FastAPI, Form
import uvicorn
from backend.app.routes import router
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer

app = FastAPI()

app.include_router(router)

# what is this
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# what is post and Form
@app.post("/search")
async def search(query: str = Form(...)):
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    embedding = model.encode(query)
    print(f"User searched for: {query}, and this is the embedding : {embedding}")
    return {"message": f"You searched for '{query}' and the embedding is \n {embedding}"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)