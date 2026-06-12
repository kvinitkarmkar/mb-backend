# MinersBuddy Backend API â›ï¸

FastAPI backend for MinersBuddy Mining Exam Prep App.

## Tech Stack
- **FastAPI** â€” Python web framework
- **MongoDB Atlas** â€” MCQ Questions storage
- **Supabase** â€” Users, Courses, Progress storage
- **Railway** â€” Deployment

## Project Structure
```
app/
â”œâ”€â”€ main.py              # FastAPI app entry point
â”œâ”€â”€ core/
â”‚   â””â”€â”€ config.py        # Environment settings
â”œâ”€â”€ db/
â”‚   â”œâ”€â”€ mongodb.py       # MongoDB connection
â”‚   â””â”€â”€ supabase.py      # Supabase connection
â””â”€â”€ routes/
    â”œâ”€â”€ questions.py     # MCQ Questions (MongoDB)
    â”œâ”€â”€ users.py         # User profiles (Supabase)
    â”œâ”€â”€ courses.py       # Courses/Subjects/Chapters
    â”œâ”€â”€ topics.py        # Topics
    â”œâ”€â”€ progress.py      # Quiz results + Weakness tracking
    â””â”€â”€ announcements.py # Announcements
```

## API Endpoints

### Questions (MongoDB)
```
GET  /api/v1/questions/              # All questions with filters
GET  /api/v1/questions/pyq           # PYQ questions only
GET  /api/v1/questions/random        # Random questions for quiz
GET  /api/v1/questions/by-topic/{id} # Topic questions
GET  /api/v1/questions/{id}          # Single question
POST /api/v1/questions/              # Add question
POST /api/v1/questions/bulk          # Bulk add questions
```

### Users (Supabase)
```
POST  /api/v1/users/              # Create user
GET   /api/v1/users/{firebase_uid} # Get user
PATCH /api/v1/users/{firebase_uid} # Update user
```

### Progress & Weakness (Supabase)
```
POST /api/v1/progress/quiz-result        # Save quiz result
POST /api/v1/progress/topic-attempt      # Single topic attempt
POST /api/v1/progress/bulk-topic-attempt # Bulk topic attempts
GET  /api/v1/progress/weakness/{user_id} # Weakness analysis
GET  /api/v1/progress/chapter/{user_id}  # Chapter progress
```

### Courses (Supabase)
```
GET /api/v1/courses/                          # All courses
GET /api/v1/courses/{id}/subjects             # Course subjects
GET /api/v1/courses/subjects/{id}/chapters    # Subject chapters
```

## Local Setup

```bash
# 1. Clone karo
git clone <repo>
cd minersbuddy-backend

# 2. Virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Dependencies install
pip install -r requirements.txt

# 4. Environment variables
cp .env.example .env
# .env mein apni values daalo

# 5. Run karo
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs

## Railway Deployment

1. GitHub pe push karo
2. railway.app pe New Project
3. GitHub repo connect karo
4. Environment variables add karo:
   - MONGODB_URI
   - MONGODB_DB_NAME
   - SUPABASE_URL
   - SUPABASE_KEY
5. Deploy! ðŸš€

## Weakness Score Logic

```
weakness_score = 1 - (correct / total)

0.0 - 0.3 = Strong  ðŸ’š
0.3 - 0.6 = Average ðŸŸ¡
0.6 - 1.0 = Weak    ðŸ”´
```
