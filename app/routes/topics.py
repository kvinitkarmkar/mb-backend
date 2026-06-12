from fastapi import APIRouter
from app.db.supabase import get_supabase

router = APIRouter()


@router.get("/{chapter_id}")
async def get_topics(chapter_id: str):
    """Chapter ke topics"""
    supabase = get_supabase()
    result = supabase.table("topics").select("*").eq(
        "chapter_id", chapter_id
    ).order("order_index").execute()
    return {"data": result.data}
