from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from bson import ObjectId

from app.db.mongodb import get_db

router = APIRouter()


def serialize_doc(doc):
    """MongoDB document ko JSON serializable banao"""
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc


@router.get("/")
async def get_questions(
    course: Optional[str] = None,
    subject_id: Optional[str] = None,
    chapter_id: Optional[str] = None,
    topic_id: Optional[str] = None,
    question_type: Optional[str] = None,
    difficulty: Optional[str] = None,
    medium: Optional[str] = "english",
    source_type: Optional[str] = None,
    year: Optional[str] = None,
    limit: int = Query(default=20, le=100),
    skip: int = 0,
):
    """
    Questions fetch karo â€” filters ke saath
    """
    db = get_db()
    query = {}

    if course:
        query["course"] = course
    if subject_id:
        query["subject_id"] = subject_id
    if chapter_id:
        query["chapter_id"] = chapter_id
    if topic_id:
        query["topic_id"] = topic_id
    if question_type:
        query["question_type"] = question_type
    if difficulty:
        query["difficulty"] = difficulty
    if medium:
        query["medium"] = medium
    if source_type:
        query["source.type"] = source_type
    if year:
        query["source.year"] = year

    cursor = db.questions.find(query).skip(skip).limit(limit)
    questions = []
    async for doc in cursor:
        questions.append(serialize_doc(doc))

    total = await db.questions.count_documents(query)

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": questions
    }


@router.get("/pyq")
async def get_pyq_questions(
    course: Optional[str] = None,
    chapter_id: Optional[str] = None,
    year: Optional[str] = None,
    medium: str = "english",
    limit: int = 20,
):
    """Sirf PYQ questions"""
    db = get_db()
    query = {"source.type": "pyq", "medium": medium}

    if course:
        query["course"] = course
    if chapter_id:
        query["chapter_id"] = chapter_id
    if year:
        query["source.year"] = year

    cursor = db.questions.find(query).limit(limit)
    questions = []
    async for doc in cursor:
        questions.append(serialize_doc(doc))

    return {"total": len(questions), "data": questions}


@router.get("/random")
async def get_random_questions(
    course: str,
    chapter_id: Optional[str] = None,
    topic_id: Optional[str] = None,
    difficulty: Optional[str] = None,
    medium: str = "english",
    count: int = Query(default=10, le=50),
):
    """Random questions â€” quiz ke liye"""
    db = get_db()
    query = {"course": course, "medium": medium}

    if chapter_id:
        query["chapter_id"] = chapter_id
    if topic_id:
        query["topic_id"] = topic_id
    if difficulty:
        query["difficulty"] = difficulty

    pipeline = [
        {"$match": query},
        {"$sample": {"size": count}}
    ]

    questions = []
    async for doc in db.questions.aggregate(pipeline):
        questions.append(serialize_doc(doc))

    return {"total": len(questions), "data": questions}


@router.get("/by-topic/{topic_id}")
async def get_questions_by_topic(
    topic_id: str,
    medium: str = "english",
    limit: int = 20,
):
    """Topic ke saare questions â€” weakness analysis ke liye"""
    db = get_db()
    cursor = db.questions.find({
        "topic_id": topic_id,
        "medium": medium
    }).limit(limit)

    questions = []
    async for doc in cursor:
        questions.append(serialize_doc(doc))

    return {"topic_id": topic_id, "total": len(questions), "data": questions}


@router.get("/{question_id}")
async def get_question(question_id: str):
    """Single question by ID"""
    db = get_db()
    try:
        doc = await db.questions.find_one({"_id": ObjectId(question_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid question ID")

    if not doc:
        raise HTTPException(status_code=404, detail="Question not found")

    return serialize_doc(doc)


@router.post("/")
async def create_question(question: dict):
    """New question add karo"""
    db = get_db()
    result = await db.questions.insert_one(question)
    return {"id": str(result.inserted_id), "message": "Question created"}


@router.post("/bulk")
async def bulk_create_questions(questions: List[dict]):
    """Multiple questions ek saath add karo"""
    db = get_db()
    result = await db.questions.insert_many(questions)
    return {
        "inserted": len(result.inserted_ids),
        "ids": [str(id) for id in result.inserted_ids]
    }
