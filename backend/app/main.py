from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from sentence_transformers import SentenceTransformer
from .db.connection import get_connection
from .embedder import embed_text
from .db.queries import get_top_50_recipes
import pickle
import numpy as np

try:
    with open("pca_model.pkl", "rb") as f:
        pca_model = pickle.load(f)
except FileNotFoundError:
    print("WARNING! No pca model found.")
    pca_model = None
        
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

    query_coords = None

    query_vector = embed_text(query)

    results = get_top_50_recipes(query_vector)

    if pca_model:
        query_vector_np = np.array(query_vector).reshape(1, -1)
        coordinates = pca_model.transform(query_vector_np)
        query_coords = {"x": coordinates[0, 0], "y": coordinates[0, 1]}

    formatted_results = [
        {"title": r[0], "image": r[1], "x": r[3], "y": r[4]}
        for r in results if r[3] is not None and r[4] is not None
    ]

    return {
        "results": formatted_results,
        "queryCoords": query_coords
    }