import json
from sentence_transformers import SentenceTransformer

from supabase import create_client
from app.config import settings

supabase = create_client(settings.supabase_url, settings.supabase_key)

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
# embeddings = model.encode(sentences)

data = supabase.table('recipe_data').select('id, Cleaned_ingredients').execute()