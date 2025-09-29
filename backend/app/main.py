from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from botocore.exceptions import ClientError
from typing import List
from sentence_transformers import SentenceTransformer
from .db.connection import get_connection
from .embedder import embed_text
from .db.queries import get_top_50_recipes
import pickle
import numpy as np
from .aws_client import s3
import os
from dotenv import load_dotenv

load_dotenv()

bucket_name = os.getenv("S3_BUCKET_NAME")

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

@app.get("/api/image-url/{image_name}")
def get_image_url(image_name: str):

    if not bucket_name:
        raise HTTPException(status_code=500, detail="S3 bucket name unknown")
    
    object_key = f"food-images/{image_name}.jpg"

    try:
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_key},
            ExpiresIn=900
        )
        return {"url": url}

    except ClientError as e:
        print(f"Error generating presinged URL: {e}")
        raise HTTPException(status_code=404, detail="Image not found")