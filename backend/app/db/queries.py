from .connection import get_connection

def get_top_50_recipes(query_vector: list[float]):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT title, image_name, instructions, x, y 
            FROM recipes_master
            ORDER BY embedding <#> %s::vector
            LIMIT 50;
        """, (query_vector,))
        return cur.fetchall()
