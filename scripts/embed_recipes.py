from sentence_transformers import SentenceTransformer
from supabase import create_client
from app.config import settings

supabase = create_client(settings.supabase_url, settings.supabase_key)

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def process_row(row):
    cleaned_ingredients = row['Cleaned_Ingredients']
    embedding = model.encode(cleaned_ingredients)
    return embedding

def fetch_batch_from_supabase(last_processed_id, batch_size):
    response = supabase.table('recipe_data').select('id, Cleaned_Ingredients').is_('Embedding', None).gt('id', last_processed_id).order('id').limit(batch_size).execute()
    rows = response.data
    return rows

def proces_database(batch_size=500):
    last_processed_id = 0
    while True:
        rows = fetch_batch_from_supabase(last_processed_id, batch_size)
        if not rows:
            print('All rows from database are processed')
            break
        for row in rows:
            embedding = process_row(row)
            embedding = embedding.tolist()
            supabase.table('recipe_data').update({"Embedding": embedding}).eq("id", row['id']).execute()
            last_processed_id = row['id']
        print(f"Processed up to row ID {last_processed_id}")

proces_database()