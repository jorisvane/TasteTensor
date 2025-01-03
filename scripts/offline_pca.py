from supabase import create_client
from backend.app.config import settings
from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
import ast
import joblib

supabase = create_client(settings.supabase_url, settings.supabase_key)

data = pd.read_csv("embeddings.csv")

data["Embedding"] = data["Embedding"].apply(ast.literal_eval).apply(np.array)

embeddings = np.vstack(data["Embedding"].values)

try:
    pca = joblib.load("backend/app/pca_model.pkl")
except FileNotFoundError:
    pca = PCA(n_components=2)
    pca.fit(embeddings)
    joblib.dump(pca, "backend/app/pca_model.pkl")

pca_embeddings = pca.fit_transform(embeddings)

data["Embedding_2D"] = list(pca_embeddings)

# Upload data in batches
last_processed_id = 9999
batch_size = 500

while last_processed_id < data["id"].max():
    # Select the batch to process
    batch = data[data["id"] > last_processed_id].head(batch_size)

    for _, row in batch.iterrows():
        # Update the corresponding row in Supabase
        supabase.table("recipe_data").update({
            "Embedding_2D": row["Embedding_2D"].tolist()
        }).eq("id", row["id"]).execute()
        last_processed_id = row["id"]

    print(f"Processed up to row ID {last_processed_id}")

print("All rows have been updated.")