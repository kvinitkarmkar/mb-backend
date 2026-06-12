from fastapi import APIRouter, HTTPException
from app.db.supabase import get_supabase

router = APIRouter()


@router.get("/")
async def get_courses():
    """Saare courses"""
    supabase = get_supabase()
    result = supabase.table("courses").select("*").execute()
    return {"data": result.data}


@router.get("/{course_id}/subjects")
async def get_subjects(course_id: str):
    """Course ke subjects"""
    supabase = get_supabase()
    result = supabase.table("subjects").select("*").eq(
        "course_id", course_id
    ).order("order_index").execute()
    return {"data": result.data}


@router.get("/subjects/{subject_id}/chapters")
async def get_chapters(subject_id: str):
    """Subject ke chapters"""
    supabase = get_supabase()
    result = supabase.table("chapters").select("*").eq(
        "subject_id", subject_id
    ).order("order_index").execute()
    return {"data": result.data}
