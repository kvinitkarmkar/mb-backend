from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.db.mongodb import connect_mongodb, close_mongodb
from app.db.supabase import init_supabase
from app.routes import questions, users, courses, topics, progress, announcements
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_mongodb()
    init_supabase()
    print("âœ… MongoDB + Supabase connected")
    yield
    # Shutdown
    await close_mongodb()
    print("ðŸ”´ Connections closed")


app = FastAPI(
    title="MinersBuddy API",
    description="Backend API for MinersBuddy Mining Exam Prep App",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production mein specific origin dena
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(questions.router, prefix="/api/v1/questions", tags=["Questions"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(courses.router, prefix="/api/v1/courses", tags=["Courses"])
app.include_router(topics.router, prefix="/api/v1/topics", tags=["Topics"])
app.include_router(progress.router, prefix="/api/v1/progress", tags=["Progress"])
app.include_router(announcements.router, prefix="/api/v1/announcements", tags=["Announcements"])


@app.get("/")
async def root():
    return {"message": "MinersBuddy API is running! â›ï¸", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
