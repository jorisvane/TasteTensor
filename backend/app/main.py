from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List

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
    all_items = ["apple", "banana", "grape"]
    results = [item for item in all_items if query.lower() in item.lower()]
    return {"results": results}