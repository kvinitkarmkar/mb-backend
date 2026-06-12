from fastapi import APIRouter
from typing import Optional
from app.db.supabase import get_supabase

router = APIRouter()


@router.get("/")
async def get_announcements(course: Optional[str] = None):
    """Active announcements"""
    supabase = get_supabase()
    query = supabase.table("announcements").select("*").eq("is_active", True)

    if course:
        query = query.eq("course", course)

    result = query.order("created_at", desc=True).execute()
    return {"data": result.data}
