from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from sentence_transformers import SentenceTransformer
from .db.connection import get_connection
from .embedder import embed_text
from .db.queries import get_top_50_recipes

conn = get_connection()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/ping")
def ping():
    return {"message": "Hallo dit is Joris"}

@app.get("/api/search")
def search(query: str) -> dict:

    query_vector = embed_text(query)

    results = get_top_50_recipes(query_vector)

    return {"results": [
        {"title": r[0], "image": r[1]} for r in results
    ]}