from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.db.supabase import get_supabase

router = APIRouter()


class UserCreate(BaseModel):
    firebase_uid: str
    name: str
    email: str
    gender: Optional[str] = None
    date_of_birth: Optional[str] = None
    course: Optional[str] = None
    authority: Optional[str] = None
    exam_year_target: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    preferred_language: str = "english"


class UserUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    course: Optional[str] = None
    authority: Optional[str] = None
    exam_year_target: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    preferred_language: Optional[str] = None


@router.post("/")
async def create_user(user: UserCreate):
    """Naya user create karo"""
    supabase = get_supabase()

    # Check karo user already exist karta hai
    existing = supabase.table("users").select("*").eq(
        "firebase_uid", user.firebase_uid
    ).execute()

    if existing.data:
        return {"message": "User already exists", "data": existing.data[0]}

    result = supabase.table("users").insert(user.dict()).execute()

    if not result.data:
        raise HTTPException(status_code=400, detail="User creation failed")

    return {"message": "User created", "data": result.data[0]}


@router.get("/{firebase_uid}")
async def get_user(firebase_uid: str):
    """User profile fetch karo"""
    supabase = get_supabase()
    result = supabase.table("users").select("*").eq(
        "firebase_uid", firebase_uid
    ).execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="User not found")

    return {"data": result.data[0]}


@router.patch("/{firebase_uid}")
async def update_user(firebase_uid: str, update: UserUpdate):
    """User profile update karo"""
    supabase = get_supabase()
    update_data = {k: v for k, v in update.dict().items() if v is not None}

    result = supabase.table("users").update(update_data).eq(
        "firebase_uid", firebase_uid
    ).execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User updated", "data": result.data[0]}
