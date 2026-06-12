from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.db.supabase import get_supabase

router = APIRouter()


class QuizResult(BaseModel):
    user_id: str
    chapter_id: str
    score: int
    total_questions: int


class TopicAttempt(BaseModel):
    user_id: str
    topic_id: str
    is_correct: bool


class BulkTopicAttempt(BaseModel):
    user_id: str
    attempts: List[dict]  # [{topic_id, is_correct}]


@router.post("/quiz-result")
async def save_quiz_result(result: QuizResult):
    """Quiz result save karo"""
    supabase = get_supabase()

    data = {
        "user_id": result.user_id,
        "chapter_id": result.chapter_id,
        "score": result.score,
        "total_questions": result.total_questions,
    }

    res = supabase.table("user_progress").upsert(
        data,
        on_conflict="user_id,chapter_id"
    ).execute()

    return {"message": "Progress saved", "data": res.data}


@router.post("/topic-attempt")
async def update_topic_weakness(attempt: TopicAttempt):
    """Topic attempt update karo â€” weakness tracking"""
    supabase = get_supabase()

    # Existing record check karo
    existing = supabase.table("user_topic_weakness").select("*").eq(
        "user_id", attempt.user_id
    ).eq("topic_id", attempt.topic_id).execute()

    if existing.data:
        record = existing.data[0]
        total = record["total_attempts"] + 1
        correct = record["correct_attempts"] + (1 if attempt.is_correct else 0)
        weakness_score = round(1 - (correct / total), 2)

        res = supabase.table("user_topic_weakness").update({
            "total_attempts": total,
            "correct_attempts": correct,
            "weakness_score": weakness_score,
        }).eq("user_id", attempt.user_id).eq("topic_id", attempt.topic_id).execute()
    else:
        weakness_score = 0.0 if attempt.is_correct else 1.0
        res = supabase.table("user_topic_weakness").insert({
            "user_id": attempt.user_id,
            "topic_id": attempt.topic_id,
            "total_attempts": 1,
            "correct_attempts": 1 if attempt.is_correct else 0,
            "weakness_score": weakness_score,
        }).execute()

    return {"message": "Topic weakness updated"}


@router.post("/bulk-topic-attempt")
async def bulk_update_topic_weakness(data: BulkTopicAttempt):
    """Quiz ke baad saare topics ek saath update karo"""
    supabase = get_supabase()

    for attempt in data.attempts:
        topic_id = attempt["topic_id"]
        is_correct = attempt["is_correct"]

        existing = supabase.table("user_topic_weakness").select("*").eq(
            "user_id", data.user_id
        ).eq("topic_id", topic_id).execute()

        if existing.data:
            record = existing.data[0]
            total = record["total_attempts"] + 1
            correct = record["correct_attempts"] + (1 if is_correct else 0)
            weakness_score = round(1 - (correct / total), 2)

            supabase.table("user_topic_weakness").update({
                "total_attempts": total,
                "correct_attempts": correct,
                "weakness_score": weakness_score,
            }).eq("user_id", data.user_id).eq("topic_id", topic_id).execute()
        else:
            supabase.table("user_topic_weakness").insert({
                "user_id": data.user_id,
                "topic_id": topic_id,
                "total_attempts": 1,
                "correct_attempts": 1 if is_correct else 0,
                "weakness_score": 0.0 if is_correct else 1.0,
            }).execute()

    return {"message": f"{len(data.attempts)} topics updated"}


@router.get("/weakness/{user_id}")
async def get_user_weakness(user_id: str, limit: int = 10):
    """
    User ke sabse weak topics â€” Analytics screen ke liye
    weakness_score high = zyada weak
    """
    supabase = get_supabase()

    result = supabase.table("user_topic_weakness").select(
        "*, topics(name)"
    ).eq("user_id", user_id).order(
        "weakness_score", desc=True
    ).limit(limit).execute()

    # Categorize karo
    weak, average, strong = [], [], []
    for item in result.data:
        score = item["weakness_score"]
        if score >= 0.6:
            weak.append(item)
        elif score >= 0.3:
            average.append(item)
        else:
            strong.append(item)

    return {
        "user_id": user_id,
        "summary": {
            "weak": len(weak),
            "average": len(average),
            "strong": len(strong)
        },
        "weak_topics": weak,
        "average_topics": average,
        "strong_topics": strong,
    }


@router.get("/chapter/{user_id}")
async def get_chapter_progress(user_id: str):
    """Chapter wise progress"""
    supabase = get_supabase()

    result = supabase.table("user_progress").select(
        "*, chapters(name)"
    ).eq("user_id", user_id).execute()

    return {"user_id": user_id, "data": result.data}
