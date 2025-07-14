import pandas as pd
import os
from app.db.connection import get_connection
from tqdm import tqdm
from psycopg2.extras import execute_batch
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-small-en-v1.5")


script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.abspath(os.path.join(script_dir, "..", "..", "data", "kaggle-recipes", "ingredients-mapping.csv"))

def load_recipes(path):
    df = pd.read_csv(path)
    df = df.dropna(subset=["Title", "Cleaned_Ingredients"])
    df["Title"] = df["Title"].astype(str).str.strip()
    df["Cleaned_Ingredients"] = df["Cleaned_Ingredients"].astype(str).str.strip()
    df["title_ingredients"] = df["Title"] + ". Ingredients: " + df["Cleaned_Ingredients"]
    return df

def insert_batch(df_batch):
    embeddings = model.encode(df_batch["title_ingredients"].tolist(), normalize_embeddings=True)
    
    rows = [
        (
            row["Title"],
            row["Ingredients"],
            row["Instructions"],
            row["Image_Name"],
            row["Cleaned_Ingredients"],
            row["title_ingredients"],
            embedding.tolist()
        )
        for (_, row), embedding in zip(df_batch.iterrows(), embeddings)
    ]

    with get_connection() as conn, conn.cursor() as cur:
        execute_batch(
            cur,
            """
            INSERT INTO recipes_master (
                title,
                ingredients,
                instructions,
                image_name,
                cleaned_ingredients,
                title_ingredients,
                embedding
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            rows
        )
        conn.commit()

def run_pipeline():
    df = load_recipes(csv_path)
    print(f"Processing {len(df)} recipes...")

    BATCH_SIZE = 300
    
    for i in tqdm(range(0, len(df), BATCH_SIZE)):
        df_batch = df.iloc[i:i + BATCH_SIZE]
        insert_batch(df_batch)

    print("Done inserting all embeddings into recipes_master.")

if __name__ == "__main__":
    run_pipeline()