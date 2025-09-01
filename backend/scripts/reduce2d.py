import numpy as np
import pickle
from sklearn.decomposition import PCA
from app.db.connection import get_connection
import ast
import os
PCA_DIM = 2
MODEL_PATH = "scripts/pca_model.pkl"

def fetch_embeddings():
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("SELECT id, embedding FROM recipes_master WHERE embedding IS NOT NULL;")
        rows = cur.fetchall()
        ids = []
        vectors = []
        for row in rows:
            ids.append(row[0])
           
            if isinstance(row[1], str):
                vector = ast.literal_eval(row[1])
            else:
                vector = row[1]
            vectors.append(vector)
        return ids, np.array(vectors)

def save_pca_model(pca: PCA):
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(pca, f)

def update_xy_coords(ids, coords):
    with get_connection() as conn, conn.cursor() as cur:
        for i, (x, y) in zip(ids, coords):
            cur.execute(
                "UPDATE recipes_master SET x = %s, y = %s WHERE id = %s;",
                (float(x), float(y), i)
            )
        conn.commit()

def run():
    ids, vectors = fetch_embeddings()
    print(f"Fetched {len(vectors)} embeddings")

    pca = PCA(n_components=PCA_DIM)
    coords = pca.fit_transform(vectors)

    save_pca_model(pca)
    update_xy_coords(ids, coords)
    print("2D coordinates stored in DB and PCA model saved.")

if __name__ == "__main__":
    run()
