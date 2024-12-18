from fastapi import APIRouter
from backend.app.database import supabase

router = APIRouter()

@router.get("/first-row")
async def get_first_row():
    data = supabase.table("recipe_data").select("*").limit(1).execute()
    return data.data[0]['Title'] if data.data else {"message": "No data found"}
