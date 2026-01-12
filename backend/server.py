from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime, timezone, timedelta
import bcrypt
import jwt

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# JWT Configuration
JWT_SECRET = os.environ.get('JWT_SECRET', 'secplus-study-app-secret-key-2024')
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

app = FastAPI()
api_router = APIRouter(prefix="/api")
security = HTTPBearer()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ============ MODELS ============

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    created_at: str

class TokenResponse(BaseModel):
    token: str
    user: UserResponse

class QuestionOption(BaseModel):
    id: str
    text: str

class Question(BaseModel):
    id: str
    domain: int
    domain_name: str
    question: str
    options: List[QuestionOption]
    correct_answer: str
    explanation: str

class AnswerSubmit(BaseModel):
    question_id: str
    selected_answer: str
    time_taken: int = 0

class ExamSubmit(BaseModel):
    answers: List[AnswerSubmit]
    mode: str
    total_time: int = 0

class ProgressResponse(BaseModel):
    total_questions_answered: int
    correct_answers: int
    accuracy: float
    domain_stats: dict
    current_streak: int
    longest_streak: int
    last_study_date: Optional[str]

# Spaced Repetition Models (SM-2 Algorithm)
class SpacedRepetitionCard(BaseModel):
    question_id: str
    ease_factor: float = 2.5  # Starting ease factor
    interval: int = 0  # Days until next review
    repetitions: int = 0  # Number of successful reviews
    next_review: str  # ISO date string
    last_review: Optional[str] = None

class ReviewSubmit(BaseModel):
    question_id: str
    quality: int  # 0-5 rating (0-2 = fail, 3-5 = pass)

class SpacedRepetitionStats(BaseModel):
    total_cards: int
    due_today: int
    mastered: int  # Cards with interval > 21 days
    learning: int  # Cards with interval <= 21 days
    new_cards: int  # Cards never reviewed

# ============ AUTH HELPERS ============

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_token(user_id: str) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRATION_HOURS),
        "iat": datetime.now(timezone.utc)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = await db.users.find_one({"id": user_id}, {"_id": 0})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ============ AUTH ROUTES ============

@api_router.post("/auth/register", response_model=TokenResponse)
async def register(user_data: UserCreate):
    existing = await db.users.find_one({"email": user_data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_id = str(uuid.uuid4())
    user = {
        "id": user_id,
        "email": user_data.email,
        "name": user_data.name,
        "password_hash": hash_password(user_data.password),
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.users.insert_one(user)
    
    # Initialize progress
    await db.progress.insert_one({
        "user_id": user_id,
        "total_questions_answered": 0,
        "correct_answers": 0,
        "domain_stats": {str(i): {"answered": 0, "correct": 0} for i in range(1, 6)},
        "current_streak": 0,
        "longest_streak": 0,
        "last_study_date": None,
        "history": []
    })
    
    token = create_token(user_id)
    return TokenResponse(
        token=token,
        user=UserResponse(id=user_id, email=user_data.email, name=user_data.name, created_at=user["created_at"])
    )

@api_router.post("/auth/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    user = await db.users.find_one({"email": credentials.email}, {"_id": 0})
    if not user or not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_token(user["id"])
    return TokenResponse(
        token=token,
        user=UserResponse(id=user["id"], email=user["email"], name=user["name"], created_at=user["created_at"])
    )

@api_router.get("/auth/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    return UserResponse(
        id=current_user["id"],
        email=current_user["email"],
        name=current_user["name"],
        created_at=current_user["created_at"]
    )

# ============ QUESTIONS ROUTES ============

@api_router.get("/questions", response_model=List[Question])
async def get_questions(domain: Optional[int] = None, limit: int = 50, current_user: dict = Depends(get_current_user)):
    query = {}
    if domain:
        query["domain"] = domain
    questions = await db.questions.find(query, {"_id": 0}).limit(limit).to_list(limit)
    return questions

@api_router.get("/questions/practice", response_model=List[Question])
async def get_practice_questions(domain: Optional[int] = None, count: int = 10, current_user: dict = Depends(get_current_user)):
    pipeline = []
    if domain:
        pipeline.append({"$match": {"domain": domain}})
    pipeline.append({"$sample": {"size": count}})
    pipeline.append({"$project": {"_id": 0}})
    questions = await db.questions.aggregate(pipeline).to_list(count)
    return questions

@api_router.get("/questions/exam", response_model=List[Question])
async def get_exam_questions(current_user: dict = Depends(get_current_user)):
    # SY0-701 has ~90 questions, weighted by domain
    domain_weights = {1: 11, 2: 20, 3: 16, 4: 25, 5: 18}
    all_questions = []
    
    for domain, count in domain_weights.items():
        pipeline = [
            {"$match": {"domain": domain}},
            {"$sample": {"size": count}},
            {"$project": {"_id": 0}}
        ]
        questions = await db.questions.aggregate(pipeline).to_list(count)
        all_questions.extend(questions)
    
    import random
    random.shuffle(all_questions)
    return all_questions

@api_router.get("/questions/flashcards", response_model=List[Question])
async def get_flashcards(domain: Optional[int] = None, count: int = 20, current_user: dict = Depends(get_current_user)):
    pipeline = []
    if domain:
        pipeline.append({"$match": {"domain": domain}})
    pipeline.append({"$sample": {"size": count}})
    pipeline.append({"$project": {"_id": 0}})
    questions = await db.questions.aggregate(pipeline).to_list(count)
    return questions

# ============ PROGRESS ROUTES ============

@api_router.get("/progress", response_model=ProgressResponse)
async def get_progress(current_user: dict = Depends(get_current_user)):
    progress = await db.progress.find_one({"user_id": current_user["id"]}, {"_id": 0})
    if not progress:
        return ProgressResponse(
            total_questions_answered=0,
            correct_answers=0,
            accuracy=0.0,
            domain_stats={},
            current_streak=0,
            longest_streak=0,
            last_study_date=None
        )
    
    accuracy = 0.0
    if progress["total_questions_answered"] > 0:
        accuracy = (progress["correct_answers"] / progress["total_questions_answered"]) * 100
    
    return ProgressResponse(
        total_questions_answered=progress["total_questions_answered"],
        correct_answers=progress["correct_answers"],
        accuracy=round(accuracy, 1),
        domain_stats=progress["domain_stats"],
        current_streak=progress["current_streak"],
        longest_streak=progress["longest_streak"],
        last_study_date=progress.get("last_study_date")
    )

@api_router.post("/progress/submit")
async def submit_answers(submission: ExamSubmit, current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    progress = await db.progress.find_one({"user_id": user_id})
    
    if not progress:
        progress = {
            "user_id": user_id,
            "total_questions_answered": 0,
            "correct_answers": 0,
            "domain_stats": {str(i): {"answered": 0, "correct": 0} for i in range(1, 6)},
            "current_streak": 0,
            "longest_streak": 0,
            "last_study_date": None,
            "history": []
        }
    
    results = []
    correct_count = 0
    
    for answer in submission.answers:
        question = await db.questions.find_one({"id": answer.question_id}, {"_id": 0})
        if question:
            is_correct = answer.selected_answer == question["correct_answer"]
            if is_correct:
                correct_count += 1
            
            domain_key = str(question["domain"])
            if domain_key not in progress["domain_stats"]:
                progress["domain_stats"][domain_key] = {"answered": 0, "correct": 0}
            
            progress["domain_stats"][domain_key]["answered"] += 1
            if is_correct:
                progress["domain_stats"][domain_key]["correct"] += 1
            
            results.append({
                "question_id": answer.question_id,
                "selected_answer": answer.selected_answer,
                "correct_answer": question["correct_answer"],
                "is_correct": is_correct,
                "explanation": question["explanation"],
                "question": question["question"],
                "options": question["options"],
                "domain": question["domain"],
                "domain_name": question["domain_name"]
            })
    
    progress["total_questions_answered"] += len(submission.answers)
    progress["correct_answers"] += correct_count
    
    # Update streak
    today = datetime.now(timezone.utc).date().isoformat()
    last_date = progress.get("last_study_date")
    
    if last_date:
        last_date_obj = datetime.fromisoformat(last_date).date() if isinstance(last_date, str) else last_date
        today_obj = datetime.fromisoformat(today)
        diff = (today_obj - datetime.fromisoformat(str(last_date_obj))).days
        
        if diff == 1:
            progress["current_streak"] += 1
        elif diff > 1:
            progress["current_streak"] = 1
    else:
        progress["current_streak"] = 1
    
    progress["longest_streak"] = max(progress["longest_streak"], progress["current_streak"])
    progress["last_study_date"] = today
    
    # Save session history
    session = {
        "id": str(uuid.uuid4()),
        "mode": submission.mode,
        "date": datetime.now(timezone.utc).isoformat(),
        "total_questions": len(submission.answers),
        "correct_answers": correct_count,
        "total_time": submission.total_time
    }
    
    if "history" not in progress:
        progress["history"] = []
    progress["history"].append(session)
    
    await db.progress.update_one(
        {"user_id": user_id},
        {"$set": progress},
        upsert=True
    )
    
    accuracy = (correct_count / len(submission.answers) * 100) if submission.answers else 0
    
    return {
        "results": results,
        "summary": {
            "total": len(submission.answers),
            "correct": correct_count,
            "incorrect": len(submission.answers) - correct_count,
            "accuracy": round(accuracy, 1)
        }
    }

@api_router.get("/progress/history")
async def get_history(limit: int = 10, current_user: dict = Depends(get_current_user)):
    progress = await db.progress.find_one({"user_id": current_user["id"]}, {"_id": 0})
    if not progress or "history" not in progress:
        return []
    return progress["history"][-limit:][::-1]

@api_router.get("/progress/weak-areas")
async def get_weak_areas(current_user: dict = Depends(get_current_user)):
    progress = await db.progress.find_one({"user_id": current_user["id"]}, {"_id": 0})
    if not progress:
        return []
    
    domain_names = {
        "1": "General Security Concepts",
        "2": "Threats, Vulnerabilities & Mitigations",
        "3": "Security Architecture",
        "4": "Security Operations",
        "5": "Security Program Management"
    }
    
    weak_areas = []
    for domain, stats in progress.get("domain_stats", {}).items():
        if stats["answered"] > 0:
            accuracy = (stats["correct"] / stats["answered"]) * 100
            weak_areas.append({
                "domain": int(domain),
                "domain_name": domain_names.get(domain, f"Domain {domain}"),
                "answered": stats["answered"],
                "correct": stats["correct"],
                "accuracy": round(accuracy, 1)
            })
    
    weak_areas.sort(key=lambda x: x["accuracy"])
    return weak_areas

# ============ SPACED REPETITION ROUTES ============

def calculate_sm2(quality: int, repetitions: int, ease_factor: float, interval: int):
    """
    SM-2 Algorithm for spaced repetition
    quality: 0-5 (0-2 = fail, 3-5 = pass)
    Returns: (new_repetitions, new_ease_factor, new_interval)
    """
    if quality < 3:
        # Failed - reset
        return 0, max(1.3, ease_factor - 0.2), 1
    
    # Passed
    if repetitions == 0:
        new_interval = 1
    elif repetitions == 1:
        new_interval = 3
    else:
        new_interval = round(interval * ease_factor)
    
    new_ease_factor = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    new_ease_factor = max(1.3, new_ease_factor)
    
    return repetitions + 1, new_ease_factor, new_interval

@api_router.get("/spaced-repetition/stats", response_model=SpacedRepetitionStats)
async def get_sr_stats(current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    today = datetime.now(timezone.utc).date().isoformat()
    
    # Get all questions count
    total_questions = await db.questions.count_documents({})
    
    # Get user's SR cards
    cards = await db.spaced_repetition.find({"user_id": user_id}, {"_id": 0}).to_list(1000)
    
    reviewed_ids = {c["question_id"] for c in cards}
    new_cards = total_questions - len(reviewed_ids)
    
    due_today = 0
    mastered = 0
    learning = 0
    
    for card in cards:
        if card["next_review"] <= today:
            due_today += 1
        if card["interval"] > 21:
            mastered += 1
        else:
            learning += 1
    
    # Include new cards in due count (limit to 10 new per day)
    due_today += min(10, new_cards)
    
    return SpacedRepetitionStats(
        total_cards=total_questions,
        due_today=due_today,
        mastered=mastered,
        learning=learning,
        new_cards=new_cards
    )

@api_router.get("/spaced-repetition/due")
async def get_due_cards(limit: int = 20, current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    today = datetime.now(timezone.utc).date().isoformat()
    
    # Get cards due for review
    due_cards = await db.spaced_repetition.find(
        {"user_id": user_id, "next_review": {"$lte": today}},
        {"_id": 0}
    ).sort("next_review", 1).limit(limit).to_list(limit)
    
    due_question_ids = [c["question_id"] for c in due_cards]
    
    # Get new questions (never reviewed)
    reviewed_ids = [c["question_id"] async for c in db.spaced_repetition.find({"user_id": user_id}, {"question_id": 1})]
    
    new_needed = max(0, limit - len(due_cards))
    if new_needed > 0:
        new_questions = await db.questions.find(
            {"id": {"$nin": reviewed_ids}},
            {"_id": 0}
        ).limit(min(10, new_needed)).to_list(min(10, new_needed))
    else:
        new_questions = []
    
    # Get full question data for due cards
    due_questions = []
    if due_question_ids:
        due_questions = await db.questions.find(
            {"id": {"$in": due_question_ids}},
            {"_id": 0}
        ).to_list(len(due_question_ids))
    
    # Combine and add SR metadata
    result = []
    
    for q in due_questions:
        card = next((c for c in due_cards if c["question_id"] == q["id"]), None)
        result.append({
            **q,
            "sr_data": {
                "ease_factor": card["ease_factor"] if card else 2.5,
                "interval": card["interval"] if card else 0,
                "repetitions": card["repetitions"] if card else 0,
                "is_new": False
            }
        })
    
    for q in new_questions:
        result.append({
            **q,
            "sr_data": {
                "ease_factor": 2.5,
                "interval": 0,
                "repetitions": 0,
                "is_new": True
            }
        })
    
    return result

@api_router.post("/spaced-repetition/review")
async def submit_review(review: ReviewSubmit, current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    today = datetime.now(timezone.utc)
    
    # Validate quality rating
    if review.quality < 0 or review.quality > 5:
        raise HTTPException(status_code=400, detail="Quality must be between 0 and 5")
    
    # Get existing card or create new
    existing = await db.spaced_repetition.find_one(
        {"user_id": user_id, "question_id": review.question_id},
        {"_id": 0}
    )
    
    if existing:
        repetitions = existing["repetitions"]
        ease_factor = existing["ease_factor"]
        interval = existing["interval"]
    else:
        repetitions = 0
        ease_factor = 2.5
        interval = 0
    
    # Calculate new values using SM-2
    new_reps, new_ef, new_interval = calculate_sm2(review.quality, repetitions, ease_factor, interval)
    
    # Calculate next review date
    next_review = (today + timedelta(days=new_interval)).date().isoformat()
    
    card_data = {
        "user_id": user_id,
        "question_id": review.question_id,
        "ease_factor": new_ef,
        "interval": new_interval,
        "repetitions": new_reps,
        "next_review": next_review,
        "last_review": today.isoformat()
    }
    
    await db.spaced_repetition.update_one(
        {"user_id": user_id, "question_id": review.question_id},
        {"$set": card_data},
        upsert=True
    )
    
    return {
        "success": True,
        "next_review": next_review,
        "interval": new_interval,
        "ease_factor": round(new_ef, 2),
        "repetitions": new_reps
    }

# ============ SEED DATA ============

@api_router.post("/seed-questions")
async def seed_questions():
    # Check if questions already exist
    count = await db.questions.count_documents({})
    if count > 0:
        return {"message": f"Questions already seeded ({count} questions)"}
    
    questions = get_seed_questions()
    await db.questions.insert_many(questions)
    return {"message": f"Seeded {len(questions)} questions"}

def get_seed_questions():
    """CompTIA Security+ SY0-701 Practice Questions"""
    questions = [
        # Domain 1: General Security Concepts (12%)
        {
            "id": str(uuid.uuid4()),
            "domain": 1,
            "domain_name": "General Security Concepts",
            "question": "Which security principle ensures that users have only the minimum access necessary to perform their job functions?",
            "options": [
                {"id": "a", "text": "Separation of duties"},
                {"id": "b", "text": "Least privilege"},
                {"id": "c", "text": "Defense in depth"},
                {"id": "d", "text": "Need to know"}
            ],
            "correct_answer": "b",
            "explanation": "The principle of least privilege ensures users are given only the minimum levels of access needed to perform their job functions. This limits potential damage from accidents or malicious actions."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 1,
            "domain_name": "General Security Concepts",
            "question": "What type of control is a security awareness training program?",
            "options": [
                {"id": "a", "text": "Technical control"},
                {"id": "b", "text": "Physical control"},
                {"id": "c", "text": "Administrative control"},
                {"id": "d", "text": "Compensating control"}
            ],
            "correct_answer": "c",
            "explanation": "Security awareness training is an administrative (managerial) control. Administrative controls include policies, procedures, and training programs that govern how people should act."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 1,
            "domain_name": "General Security Concepts",
            "question": "The CIA triad consists of which three components?",
            "options": [
                {"id": "a", "text": "Confidentiality, Integrity, Authentication"},
                {"id": "b", "text": "Confidentiality, Integrity, Availability"},
                {"id": "c", "text": "Control, Integrity, Availability"},
                {"id": "d", "text": "Confidentiality, Identity, Availability"}
            ],
            "correct_answer": "b",
            "explanation": "The CIA triad consists of Confidentiality (keeping data secret), Integrity (ensuring data hasn't been altered), and Availability (ensuring data is accessible when needed)."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 1,
            "domain_name": "General Security Concepts",
            "question": "Which concept requires multiple people to complete a sensitive task?",
            "options": [
                {"id": "a", "text": "Least privilege"},
                {"id": "b", "text": "Job rotation"},
                {"id": "c", "text": "Separation of duties"},
                {"id": "d", "text": "Mandatory vacations"}
            ],
            "correct_answer": "c",
            "explanation": "Separation of duties divides critical functions among different people, requiring multiple individuals to complete a sensitive task. This prevents fraud and errors."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 1,
            "domain_name": "General Security Concepts",
            "question": "What is the primary purpose of non-repudiation?",
            "options": [
                {"id": "a", "text": "Prevent unauthorized access"},
                {"id": "b", "text": "Ensure data integrity"},
                {"id": "c", "text": "Prove the origin of data or actions"},
                {"id": "d", "text": "Encrypt sensitive data"}
            ],
            "correct_answer": "c",
            "explanation": "Non-repudiation ensures that a party cannot deny the authenticity of their signature on a document or the sending of a message. It provides proof of origin and integrity."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 1,
            "domain_name": "General Security Concepts",
            "question": "Which authentication factor is 'something you are'?",
            "options": [
                {"id": "a", "text": "Password"},
                {"id": "b", "text": "Smart card"},
                {"id": "c", "text": "Fingerprint"},
                {"id": "d", "text": "Security token"}
            ],
            "correct_answer": "c",
            "explanation": "Biometrics like fingerprints represent 'something you are'. Other factors include: something you know (password), something you have (smart card/token), somewhere you are (location)."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 1,
            "domain_name": "General Security Concepts",
            "question": "What is defense in depth?",
            "options": [
                {"id": "a", "text": "Using the strongest single security control"},
                {"id": "b", "text": "Multiple layers of security controls"},
                {"id": "c", "text": "Deep packet inspection"},
                {"id": "d", "text": "Penetration testing methodology"}
            ],
            "correct_answer": "b",
            "explanation": "Defense in depth is a security strategy using multiple layers of controls. If one layer fails, others continue to provide protection. It's like having multiple locks on a door."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 1,
            "domain_name": "General Security Concepts",
            "question": "Which term describes the process of verifying that a user is who they claim to be?",
            "options": [
                {"id": "a", "text": "Authorization"},
                {"id": "b", "text": "Accounting"},
                {"id": "c", "text": "Authentication"},
                {"id": "d", "text": "Auditing"}
            ],
            "correct_answer": "c",
            "explanation": "Authentication verifies identity (who you are). Authorization determines what you can access (permissions). Accounting/Auditing tracks what you did."
        },
        # Domain 2: Threats, Vulnerabilities, and Mitigations (22%)
        {
            "id": str(uuid.uuid4()),
            "domain": 2,
            "domain_name": "Threats, Vulnerabilities & Mitigations",
            "question": "What type of malware encrypts files and demands payment for decryption?",
            "options": [
                {"id": "a", "text": "Spyware"},
                {"id": "b", "text": "Trojan"},
                {"id": "c", "text": "Ransomware"},
                {"id": "d", "text": "Rootkit"}
            ],
            "correct_answer": "c",
            "explanation": "Ransomware encrypts victim's files and demands ransom payment for the decryption key. Examples include WannaCry, Petya, and Ryuk."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 2,
            "domain_name": "Threats, Vulnerabilities & Mitigations",
            "question": "A user receives an email appearing to be from their bank asking them to verify account details. What type of attack is this?",
            "options": [
                {"id": "a", "text": "Vishing"},
                {"id": "b", "text": "Smishing"},
                {"id": "c", "text": "Phishing"},
                {"id": "d", "text": "Whaling"}
            ],
            "correct_answer": "c",
            "explanation": "Phishing uses fraudulent emails to trick users into revealing sensitive information. Vishing uses voice calls, smishing uses SMS, and whaling targets high-profile executives."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 2,
            "domain_name": "Threats, Vulnerabilities & Mitigations",
            "question": "Which attack exploits a vulnerability before a patch is available?",
            "options": [
                {"id": "a", "text": "Brute force attack"},
                {"id": "b", "text": "Zero-day attack"},
                {"id": "c", "text": "Dictionary attack"},
                {"id": "d", "text": "Rainbow table attack"}
            ],
            "correct_answer": "b",
            "explanation": "A zero-day attack exploits a previously unknown vulnerability before the vendor has released a patch. These are particularly dangerous because there's no fix available."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 2,
            "domain_name": "Threats, Vulnerabilities & Mitigations",
            "question": "What type of attack floods a server with traffic to make it unavailable?",
            "options": [
                {"id": "a", "text": "Man-in-the-middle"},
                {"id": "b", "text": "SQL injection"},
                {"id": "c", "text": "DDoS"},
                {"id": "d", "text": "Cross-site scripting"}
            ],
            "correct_answer": "c",
            "explanation": "A Distributed Denial of Service (DDoS) attack floods a target with traffic from multiple sources, overwhelming its resources and making it unavailable to legitimate users."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 2,
            "domain_name": "Threats, Vulnerabilities & Mitigations",
            "question": "An attacker inserts malicious SQL code into a web form. What type of attack is this?",
            "options": [
                {"id": "a", "text": "Cross-site scripting (XSS)"},
                {"id": "b", "text": "SQL injection"},
                {"id": "c", "text": "Buffer overflow"},
                {"id": "d", "text": "LDAP injection"}
            ],
            "correct_answer": "b",
            "explanation": "SQL injection attacks insert malicious SQL statements into application queries through user input fields, potentially allowing unauthorized database access or manipulation."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 2,
            "domain_name": "Threats, Vulnerabilities & Mitigations",
            "question": "What is social engineering?",
            "options": [
                {"id": "a", "text": "Hacking social media accounts"},
                {"id": "b", "text": "Manipulating people to reveal information"},
                {"id": "c", "text": "Creating fake social networks"},
                {"id": "d", "text": "Engineering secure social systems"}
            ],
            "correct_answer": "b",
            "explanation": "Social engineering manipulates people into breaking security procedures or revealing confidential information. It exploits human psychology rather than technical vulnerabilities."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 2,
            "domain_name": "Threats, Vulnerabilities & Mitigations",
            "question": "Which type of malware disguises itself as legitimate software?",
            "options": [
                {"id": "a", "text": "Virus"},
                {"id": "b", "text": "Worm"},
                {"id": "c", "text": "Trojan"},
                {"id": "d", "text": "Adware"}
            ],
            "correct_answer": "c",
            "explanation": "A Trojan (Trojan horse) disguises itself as legitimate software to trick users into installing it. Unlike viruses and worms, Trojans don't replicate themselves."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 2,
            "domain_name": "Threats, Vulnerabilities & Mitigations",
            "question": "What is the purpose of a rootkit?",
            "options": [
                {"id": "a", "text": "To encrypt files"},
                {"id": "b", "text": "To hide malicious activity"},
                {"id": "c", "text": "To spread via email"},
                {"id": "d", "text": "To display advertisements"}
            ],
            "correct_answer": "b",
            "explanation": "A rootkit hides malicious activity and provides continued privileged access to a system. It modifies the OS to conceal the presence of malware and attacker activities."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 2,
            "domain_name": "Threats, Vulnerabilities & Mitigations",
            "question": "An attacker positions themselves between two communicating parties. What attack is this?",
            "options": [
                {"id": "a", "text": "Replay attack"},
                {"id": "b", "text": "On-path attack (MITM)"},
                {"id": "c", "text": "Session hijacking"},
                {"id": "d", "text": "Pass-the-hash"}
            ],
            "correct_answer": "b",
            "explanation": "An on-path attack (formerly man-in-the-middle/MITM) intercepts communication between two parties, potentially altering or eavesdropping on the data exchange."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 2,
            "domain_name": "Threats, Vulnerabilities & Mitigations",
            "question": "Which threat actor typically has the most resources and sophistication?",
            "options": [
                {"id": "a", "text": "Script kiddies"},
                {"id": "b", "text": "Hacktivists"},
                {"id": "c", "text": "Nation-state actors"},
                {"id": "d", "text": "Insider threats"}
            ],
            "correct_answer": "c",
            "explanation": "Nation-state actors are government-sponsored groups with significant resources, advanced capabilities, and sophisticated attack methods. They often target critical infrastructure."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 2,
            "domain_name": "Threats, Vulnerabilities & Mitigations",
            "question": "What is privilege escalation?",
            "options": [
                {"id": "a", "text": "Granting admin rights to users"},
                {"id": "b", "text": "An attacker gaining higher access levels"},
                {"id": "c", "text": "Increasing password complexity"},
                {"id": "d", "text": "Adding more security controls"}
            ],
            "correct_answer": "b",
            "explanation": "Privilege escalation occurs when an attacker gains elevated access rights beyond what was initially authorized, often moving from regular user to administrator privileges."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 2,
            "domain_name": "Threats, Vulnerabilities & Mitigations",
            "question": "What vulnerability allows an attacker to execute scripts in a victim's browser?",
            "options": [
                {"id": "a", "text": "SQL injection"},
                {"id": "b", "text": "Cross-site scripting (XSS)"},
                {"id": "c", "text": "Buffer overflow"},
                {"id": "d", "text": "Directory traversal"}
            ],
            "correct_answer": "b",
            "explanation": "Cross-site scripting (XSS) injects malicious scripts into trusted websites. When victims visit the site, the script executes in their browser, potentially stealing data."
        },
        # Domain 3: Security Architecture (18%)
        {
            "id": str(uuid.uuid4()),
            "domain": 3,
            "domain_name": "Security Architecture",
            "question": "Which network device filters traffic based on predetermined security rules?",
            "options": [
                {"id": "a", "text": "Switch"},
                {"id": "b", "text": "Router"},
                {"id": "c", "text": "Firewall"},
                {"id": "d", "text": "Hub"}
            ],
            "correct_answer": "c",
            "explanation": "A firewall monitors and filters incoming and outgoing network traffic based on predetermined security rules, acting as a barrier between trusted and untrusted networks."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 3,
            "domain_name": "Security Architecture",
            "question": "What is a DMZ in network security?",
            "options": [
                {"id": "a", "text": "A type of firewall"},
                {"id": "b", "text": "A network segment between internal and external networks"},
                {"id": "c", "text": "A VPN configuration"},
                {"id": "d", "text": "A wireless security protocol"}
            ],
            "correct_answer": "b",
            "explanation": "A DMZ (Demilitarized Zone) is a network segment that sits between an internal network and the internet, hosting public-facing services while protecting internal resources."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 3,
            "domain_name": "Security Architecture",
            "question": "Which protocol provides secure remote access over an encrypted tunnel?",
            "options": [
                {"id": "a", "text": "Telnet"},
                {"id": "b", "text": "FTP"},
                {"id": "c", "text": "VPN"},
                {"id": "d", "text": "HTTP"}
            ],
            "correct_answer": "c",
            "explanation": "A VPN (Virtual Private Network) creates an encrypted tunnel over a public network, allowing secure remote access to resources as if directly connected to the private network."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 3,
            "domain_name": "Security Architecture",
            "question": "What does NAC stand for in network security?",
            "options": [
                {"id": "a", "text": "Network Access Control"},
                {"id": "b", "text": "Network Automated Configuration"},
                {"id": "c", "text": "New Authentication Certificate"},
                {"id": "d", "text": "Network Analysis Center"}
            ],
            "correct_answer": "a",
            "explanation": "Network Access Control (NAC) restricts unauthorized users and devices from accessing a network. It enforces security policies before granting network access."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 3,
            "domain_name": "Security Architecture",
            "question": "Which encryption standard is considered most secure for wireless networks?",
            "options": [
                {"id": "a", "text": "WEP"},
                {"id": "b", "text": "WPA"},
                {"id": "c", "text": "WPA2"},
                {"id": "d", "text": "WPA3"}
            ],
            "correct_answer": "d",
            "explanation": "WPA3 is the newest and most secure wireless encryption standard. It provides stronger encryption, protection against offline dictionary attacks, and improved security for open networks."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 3,
            "domain_name": "Security Architecture",
            "question": "What is the purpose of network segmentation?",
            "options": [
                {"id": "a", "text": "To increase network speed"},
                {"id": "b", "text": "To isolate and protect network sections"},
                {"id": "c", "text": "To reduce hardware costs"},
                {"id": "d", "text": "To simplify network management"}
            ],
            "correct_answer": "b",
            "explanation": "Network segmentation divides a network into smaller segments, limiting the spread of breaches and allowing different security controls for different data sensitivity levels."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 3,
            "domain_name": "Security Architecture",
            "question": "What is Zero Trust Architecture?",
            "options": [
                {"id": "a", "text": "Never trusting any user or device"},
                {"id": "b", "text": "Zero security controls"},
                {"id": "c", "text": "Trusting only internal users"},
                {"id": "d", "text": "A backup security model"}
            ],
            "correct_answer": "a",
            "explanation": "Zero Trust Architecture operates on 'never trust, always verify' - no user or device is trusted by default regardless of location. Every access request must be authenticated and authorized."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 3,
            "domain_name": "Security Architecture",
            "question": "Which cloud service model provides the most control to the customer?",
            "options": [
                {"id": "a", "text": "SaaS"},
                {"id": "b", "text": "PaaS"},
                {"id": "c", "text": "IaaS"},
                {"id": "d", "text": "FaaS"}
            ],
            "correct_answer": "c",
            "explanation": "IaaS (Infrastructure as a Service) provides the most customer control, including OS, applications, and data. PaaS manages the platform, and SaaS manages everything except user data."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 3,
            "domain_name": "Security Architecture",
            "question": "What is the primary function of an IDS?",
            "options": [
                {"id": "a", "text": "Block malicious traffic"},
                {"id": "b", "text": "Detect and alert on suspicious activity"},
                {"id": "c", "text": "Encrypt network traffic"},
                {"id": "d", "text": "Authenticate users"}
            ],
            "correct_answer": "b",
            "explanation": "An Intrusion Detection System (IDS) monitors network traffic for suspicious activity and alerts administrators. Unlike an IPS, it doesn't actively block threats."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 3,
            "domain_name": "Security Architecture",
            "question": "What is the difference between IDS and IPS?",
            "options": [
                {"id": "a", "text": "IDS blocks, IPS monitors"},
                {"id": "b", "text": "IDS monitors, IPS blocks"},
                {"id": "c", "text": "They are the same"},
                {"id": "d", "text": "IDS is hardware, IPS is software"}
            ],
            "correct_answer": "b",
            "explanation": "IDS (Intrusion Detection System) monitors and alerts on threats. IPS (Intrusion Prevention System) actively blocks detected threats in addition to alerting."
        },
        # Domain 4: Security Operations (28%)
        {
            "id": str(uuid.uuid4()),
            "domain": 4,
            "domain_name": "Security Operations",
            "question": "What is the first step in incident response?",
            "options": [
                {"id": "a", "text": "Eradication"},
                {"id": "b", "text": "Containment"},
                {"id": "c", "text": "Preparation"},
                {"id": "d", "text": "Recovery"}
            ],
            "correct_answer": "c",
            "explanation": "The incident response phases are: Preparation, Identification, Containment, Eradication, Recovery, and Lessons Learned. Preparation comes first, including planning and training."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 4,
            "domain_name": "Security Operations",
            "question": "What does SIEM stand for?",
            "options": [
                {"id": "a", "text": "Security Information and Event Management"},
                {"id": "b", "text": "System Integration and Event Monitoring"},
                {"id": "c", "text": "Security Intelligence and Enterprise Management"},
                {"id": "d", "text": "Secure Information Exchange Method"}
            ],
            "correct_answer": "a",
            "explanation": "SIEM (Security Information and Event Management) collects and analyzes log data from multiple sources, providing real-time monitoring, threat detection, and incident response capabilities."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 4,
            "domain_name": "Security Operations",
            "question": "What is the purpose of a vulnerability scan?",
            "options": [
                {"id": "a", "text": "To exploit vulnerabilities"},
                {"id": "b", "text": "To identify security weaknesses"},
                {"id": "c", "text": "To remove malware"},
                {"id": "d", "text": "To encrypt data"}
            ],
            "correct_answer": "b",
            "explanation": "Vulnerability scanning identifies security weaknesses in systems, applications, and networks. Unlike penetration testing, it doesn't attempt to exploit the vulnerabilities found."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 4,
            "domain_name": "Security Operations",
            "question": "What is the chain of custody in digital forensics?",
            "options": [
                {"id": "a", "text": "A backup procedure"},
                {"id": "b", "text": "Documentation of evidence handling"},
                {"id": "c", "text": "A type of encryption"},
                {"id": "d", "text": "A network protocol"}
            ],
            "correct_answer": "b",
            "explanation": "Chain of custody documents who handled evidence, when, and what was done. It ensures evidence integrity and admissibility in legal proceedings."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 4,
            "domain_name": "Security Operations",
            "question": "What backup type copies only data that changed since the last full backup?",
            "options": [
                {"id": "a", "text": "Full backup"},
                {"id": "b", "text": "Incremental backup"},
                {"id": "c", "text": "Differential backup"},
                {"id": "d", "text": "Mirror backup"}
            ],
            "correct_answer": "c",
            "explanation": "Differential backup copies all data changed since the last full backup. Incremental backup copies only data changed since the last backup of any type."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 4,
            "domain_name": "Security Operations",
            "question": "What is the primary purpose of penetration testing?",
            "options": [
                {"id": "a", "text": "To fix vulnerabilities"},
                {"id": "b", "text": "To simulate real-world attacks"},
                {"id": "c", "text": "To install security software"},
                {"id": "d", "text": "To train security staff"}
            ],
            "correct_answer": "b",
            "explanation": "Penetration testing simulates real-world attacks to identify exploitable vulnerabilities before malicious actors do. It goes beyond scanning by actively attempting exploitation."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 4,
            "domain_name": "Security Operations",
            "question": "What metric measures how long a system can be unavailable?",
            "options": [
                {"id": "a", "text": "RPO"},
                {"id": "b", "text": "RTO"},
                {"id": "c", "text": "MTTR"},
                {"id": "d", "text": "MTBF"}
            ],
            "correct_answer": "b",
            "explanation": "RTO (Recovery Time Objective) is the maximum acceptable time a system can be down. RPO (Recovery Point Objective) defines acceptable data loss measured in time."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 4,
            "domain_name": "Security Operations",
            "question": "What is the purpose of log aggregation?",
            "options": [
                {"id": "a", "text": "To delete old logs"},
                {"id": "b", "text": "To centralize logs from multiple sources"},
                {"id": "c", "text": "To encrypt log files"},
                {"id": "d", "text": "To compress log storage"}
            ],
            "correct_answer": "b",
            "explanation": "Log aggregation centralizes logs from multiple sources into a single location, making it easier to analyze, correlate events, and detect security incidents."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 4,
            "domain_name": "Security Operations",
            "question": "What does EDR stand for?",
            "options": [
                {"id": "a", "text": "Enterprise Data Recovery"},
                {"id": "b", "text": "Endpoint Detection and Response"},
                {"id": "c", "text": "External Defense Router"},
                {"id": "d", "text": "Encrypted Data Repository"}
            ],
            "correct_answer": "b",
            "explanation": "EDR (Endpoint Detection and Response) monitors endpoints for suspicious activity, provides threat intelligence, and enables rapid response to detected threats."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 4,
            "domain_name": "Security Operations",
            "question": "What is a honeypot?",
            "options": [
                {"id": "a", "text": "A secure password storage"},
                {"id": "b", "text": "A decoy system to attract attackers"},
                {"id": "c", "text": "A type of firewall"},
                {"id": "d", "text": "An encryption algorithm"}
            ],
            "correct_answer": "b",
            "explanation": "A honeypot is a decoy system designed to attract attackers. It helps security teams study attack methods and detect intrusion attempts without risking production systems."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 4,
            "domain_name": "Security Operations",
            "question": "What is the purpose of change management?",
            "options": [
                {"id": "a", "text": "To prevent all system changes"},
                {"id": "b", "text": "To control and document system modifications"},
                {"id": "c", "text": "To speed up deployments"},
                {"id": "d", "text": "To reduce IT costs"}
            ],
            "correct_answer": "b",
            "explanation": "Change management ensures system modifications are properly planned, tested, documented, and approved before implementation, reducing risks of unintended consequences."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 4,
            "domain_name": "Security Operations",
            "question": "What is SOAR in security operations?",
            "options": [
                {"id": "a", "text": "Security Operations and Risk"},
                {"id": "b", "text": "Security Orchestration, Automation, and Response"},
                {"id": "c", "text": "System Operations and Recovery"},
                {"id": "d", "text": "Secure Online Access Rights"}
            ],
            "correct_answer": "b",
            "explanation": "SOAR (Security Orchestration, Automation, and Response) integrates security tools and automates incident response workflows, improving efficiency and consistency."
        },
        # Domain 5: Security Program Management and Oversight (20%)
        {
            "id": str(uuid.uuid4()),
            "domain": 5,
            "domain_name": "Security Program Management",
            "question": "What is the primary purpose of a risk assessment?",
            "options": [
                {"id": "a", "text": "To eliminate all risks"},
                {"id": "b", "text": "To identify and evaluate potential threats"},
                {"id": "c", "text": "To purchase insurance"},
                {"id": "d", "text": "To train employees"}
            ],
            "correct_answer": "b",
            "explanation": "Risk assessment identifies, evaluates, and prioritizes potential threats and vulnerabilities. It helps organizations make informed decisions about security controls and resource allocation."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 5,
            "domain_name": "Security Program Management",
            "question": "Which compliance framework focuses on credit card data security?",
            "options": [
                {"id": "a", "text": "HIPAA"},
                {"id": "b", "text": "SOX"},
                {"id": "c", "text": "PCI DSS"},
                {"id": "d", "text": "GDPR"}
            ],
            "correct_answer": "c",
            "explanation": "PCI DSS (Payment Card Industry Data Security Standard) provides security requirements for organizations handling credit card information to protect cardholder data."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 5,
            "domain_name": "Security Program Management",
            "question": "What does GDPR regulate?",
            "options": [
                {"id": "a", "text": "Healthcare data in the US"},
                {"id": "b", "text": "Personal data protection in the EU"},
                {"id": "c", "text": "Financial reporting"},
                {"id": "d", "text": "Government security"}
            ],
            "correct_answer": "b",
            "explanation": "GDPR (General Data Protection Regulation) is an EU regulation governing personal data collection, processing, and storage, giving individuals control over their data."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 5,
            "domain_name": "Security Program Management",
            "question": "What is the purpose of a security policy?",
            "options": [
                {"id": "a", "text": "To define acceptable security behaviors and requirements"},
                {"id": "b", "text": "To install security software"},
                {"id": "c", "text": "To replace technical controls"},
                {"id": "d", "text": "To punish employees"}
            ],
            "correct_answer": "a",
            "explanation": "Security policies define the organization's security requirements, acceptable use, and expected behaviors. They provide the foundation for the security program."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 5,
            "domain_name": "Security Program Management",
            "question": "What risk response involves purchasing insurance?",
            "options": [
                {"id": "a", "text": "Risk acceptance"},
                {"id": "b", "text": "Risk avoidance"},
                {"id": "c", "text": "Risk transference"},
                {"id": "d", "text": "Risk mitigation"}
            ],
            "correct_answer": "c",
            "explanation": "Risk transference shifts risk to a third party, typically through insurance or outsourcing. The organization pays someone else to accept the financial impact of the risk."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 5,
            "domain_name": "Security Program Management",
            "question": "What is the purpose of a Business Impact Analysis (BIA)?",
            "options": [
                {"id": "a", "text": "To analyze competitor businesses"},
                {"id": "b", "text": "To identify critical business functions and impacts"},
                {"id": "c", "text": "To calculate profit margins"},
                {"id": "d", "text": "To review employee performance"}
            ],
            "correct_answer": "b",
            "explanation": "BIA identifies critical business functions and determines the impact of their disruption. It helps prioritize recovery efforts and establish RTOs and RPOs."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 5,
            "domain_name": "Security Program Management",
            "question": "What is third-party risk management?",
            "options": [
                {"id": "a", "text": "Managing internal employees"},
                {"id": "b", "text": "Assessing risks from vendors and partners"},
                {"id": "c", "text": "Installing third-party software"},
                {"id": "d", "text": "Hiring external auditors"}
            ],
            "correct_answer": "b",
            "explanation": "Third-party risk management evaluates and monitors security risks introduced by vendors, suppliers, and partners who have access to organizational data or systems."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 5,
            "domain_name": "Security Program Management",
            "question": "What is the purpose of security awareness training?",
            "options": [
                {"id": "a", "text": "To train IT staff on hacking"},
                {"id": "b", "text": "To educate employees about security threats and practices"},
                {"id": "c", "text": "To replace technical controls"},
                {"id": "d", "text": "To satisfy management requirements only"}
            ],
            "correct_answer": "b",
            "explanation": "Security awareness training educates employees about security threats, policies, and best practices. It reduces human error, which is a leading cause of security incidents."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 5,
            "domain_name": "Security Program Management",
            "question": "What does AUP stand for?",
            "options": [
                {"id": "a", "text": "Advanced User Protection"},
                {"id": "b", "text": "Acceptable Use Policy"},
                {"id": "c", "text": "Automated Update Process"},
                {"id": "d", "text": "Authentication User Protocol"}
            ],
            "correct_answer": "b",
            "explanation": "AUP (Acceptable Use Policy) defines how employees can use organizational IT resources. It covers permitted activities, prohibited behaviors, and consequences of violations."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 5,
            "domain_name": "Security Program Management",
            "question": "What is quantitative risk analysis?",
            "options": [
                {"id": "a", "text": "Using subjective judgments"},
                {"id": "b", "text": "Assigning monetary values to risks"},
                {"id": "c", "text": "Counting security incidents"},
                {"id": "d", "text": "Measuring network traffic"}
            ],
            "correct_answer": "b",
            "explanation": "Quantitative risk analysis assigns monetary values to assets, threats, and impacts. It uses formulas like ALE (Annual Loss Expectancy) to calculate potential losses."
        },
        # Additional questions for better coverage
        {
            "id": str(uuid.uuid4()),
            "domain": 1,
            "domain_name": "General Security Concepts",
            "question": "What is MFA (Multi-Factor Authentication)?",
            "options": [
                {"id": "a", "text": "Using multiple passwords"},
                {"id": "b", "text": "Authentication using two or more different factors"},
                {"id": "c", "text": "Authentication on multiple devices"},
                {"id": "d", "text": "Multiple failed authentication attempts"}
            ],
            "correct_answer": "b",
            "explanation": "MFA requires two or more authentication factors from different categories: something you know, something you have, something you are, or somewhere you are."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 2,
            "domain_name": "Threats, Vulnerabilities & Mitigations",
            "question": "What is a watering hole attack?",
            "options": [
                {"id": "a", "text": "Flooding a server with requests"},
                {"id": "b", "text": "Compromising websites frequented by targets"},
                {"id": "c", "text": "Poisoning water supply systems"},
                {"id": "d", "text": "Redirecting DNS queries"}
            ],
            "correct_answer": "b",
            "explanation": "A watering hole attack compromises websites frequently visited by the target group. When victims visit these sites, malware is delivered to their systems."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 3,
            "domain_name": "Security Architecture",
            "question": "What is microsegmentation?",
            "options": [
                {"id": "a", "text": "Dividing storage into small segments"},
                {"id": "b", "text": "Fine-grained network security controls"},
                {"id": "c", "text": "Breaking down large files"},
                {"id": "d", "text": "Microprocessor security"}
            ],
            "correct_answer": "b",
            "explanation": "Microsegmentation creates fine-grained security zones in data centers and cloud environments, allowing precise control over traffic between workloads."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 4,
            "domain_name": "Security Operations",
            "question": "What is threat hunting?",
            "options": [
                {"id": "a", "text": "Waiting for alerts"},
                {"id": "b", "text": "Proactively searching for hidden threats"},
                {"id": "c", "text": "Hunting for threat actors physically"},
                {"id": "d", "text": "Deleting threat signatures"}
            ],
            "correct_answer": "b",
            "explanation": "Threat hunting proactively searches for hidden threats that may have evaded existing security controls, using techniques like hypothesis-driven investigation and anomaly detection."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 5,
            "domain_name": "Security Program Management",
            "question": "What is data sovereignty?",
            "options": [
                {"id": "a", "text": "Data ownership by users"},
                {"id": "b", "text": "Data subject to laws of the country where it resides"},
                {"id": "c", "text": "Encrypted data storage"},
                {"id": "d", "text": "Government data only"}
            ],
            "correct_answer": "b",
            "explanation": "Data sovereignty means data is subject to the laws and governance of the country where it's stored. This affects where organizations can store and process data."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 2,
            "domain_name": "Threats, Vulnerabilities & Mitigations",
            "question": "What is credential stuffing?",
            "options": [
                {"id": "a", "text": "Creating fake credentials"},
                {"id": "b", "text": "Using stolen credentials across multiple sites"},
                {"id": "c", "text": "Encrypting credentials"},
                {"id": "d", "text": "Storing credentials securely"}
            ],
            "correct_answer": "b",
            "explanation": "Credential stuffing uses stolen username/password pairs from one breach to attempt access on other sites, exploiting password reuse across services."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 3,
            "domain_name": "Security Architecture",
            "question": "What is CASB?",
            "options": [
                {"id": "a", "text": "Computer Automated Security Backup"},
                {"id": "b", "text": "Cloud Access Security Broker"},
                {"id": "c", "text": "Central Authentication Security Bridge"},
                {"id": "d", "text": "Cybersecurity Awareness Security Board"}
            ],
            "correct_answer": "b",
            "explanation": "CASB (Cloud Access Security Broker) sits between users and cloud services, enforcing security policies, providing visibility, and protecting data in cloud applications."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 4,
            "domain_name": "Security Operations",
            "question": "What is the purpose of a tabletop exercise?",
            "options": [
                {"id": "a", "text": "Physical security testing"},
                {"id": "b", "text": "Discussion-based incident response practice"},
                {"id": "c", "text": "Network penetration testing"},
                {"id": "d", "text": "Employee physical fitness"}
            ],
            "correct_answer": "b",
            "explanation": "Tabletop exercises are discussion-based sessions where team members walk through incident scenarios, testing plans and identifying gaps without technical testing."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 1,
            "domain_name": "General Security Concepts",
            "question": "What is the purpose of hashing?",
            "options": [
                {"id": "a", "text": "To encrypt data for transmission"},
                {"id": "b", "text": "To create a fixed-size fingerprint of data"},
                {"id": "c", "text": "To compress files"},
                {"id": "d", "text": "To speed up network traffic"}
            ],
            "correct_answer": "b",
            "explanation": "Hashing creates a fixed-size output (hash/digest) from any input. It's used for integrity verification and password storage. Hashing is one-way and cannot be reversed."
        },
        {
            "id": str(uuid.uuid4()),
            "domain": 3,
            "domain_name": "Security Architecture",
            "question": "What is a proxy server?",
            "options": [
                {"id": "a", "text": "A backup server"},
                {"id": "b", "text": "An intermediary between clients and servers"},
                {"id": "c", "text": "A type of firewall"},
                {"id": "d", "text": "A DNS server"}
            ],
            "correct_answer": "b",
            "explanation": "A proxy server acts as an intermediary between clients and destination servers, providing security, caching, content filtering, and anonymity benefits."
        }
    ]
    return questions

# ============ ROOT ROUTES ============

@api_router.get("/")
async def root():
    return {"message": "SecPlus Study API", "version": "1.0.0"}

@api_router.get("/domains")
async def get_domains():
    return [
        {"id": 1, "name": "General Security Concepts", "weight": 12},
        {"id": 2, "name": "Threats, Vulnerabilities & Mitigations", "weight": 22},
        {"id": 3, "name": "Security Architecture", "weight": 18},
        {"id": 4, "name": "Security Operations", "weight": 28},
        {"id": 5, "name": "Security Program Management", "weight": 20}
    ]

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
