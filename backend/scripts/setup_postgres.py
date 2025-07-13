from app.connection import get_connection

def create_table():
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS recipes_master (
                id SERIAL PRIMARY KEY,
                title TEXT,
                ingredients TEXT,
                instructions TEXT,
                image_name TEXT,
                cleaned_ingredients TEXT,
                title_ingredients TEXT,
                embedding vector(384)
            );
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_recipes_embedding
            ON recipes_master
            USING hnsw (embedding vector_cosine_ops)
            WITH (m = 16, ef_construction = 64);
        """)
        conn.commit()

create_table()