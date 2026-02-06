import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

milestone_questions = [
    {"domain": "General Security Concepts", "question": "What is security architecture?", "options": ["Blueprint for security implementation", "Security tools", "Security policies", "Security team"], "correct_answer": "Blueprint for security implementation"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is defense evasion?", "options": ["Bypassing security controls", "Implementing controls", "Monitoring controls", "Maintaining controls"], "correct_answer": "Bypassing security controls"},
    {"domain": "Security Architecture", "question": "What is security principle?", "options": ["Fundamental security rule", "Security policy", "Security control", "Security practice"], "correct_answer": "Fundamental security rule"},
    {"domain": "Security Operations", "question": "What is security operation center?", "options": ["24/7 monitoring center", "Office space", "Server room", "Network center"], "correct_answer": "24/7 monitoring center"},
    {"domain": "Security Program Management", "question": "What is security vision?", "options": ["Long-term security goal", "Current state", "Short-term plan", "Annual objective"], "correct_answer": "Long-term security goal"},
]

async def seed_questions():
    inserted_count = 0
    for q in milestone_questions:
        # Check if question already exists (case-insensitive)
        existing = await db.questions.find_one({"question": {"$regex": f"^{q['question']}$", "$options": "i"}})
        if not existing:
            await db.questions.insert_one(q)
            inserted_count += 1
        else:
            print(f"Skipped duplicate: {q['question']}")
    
    print(f"Inserted {inserted_count} new questions. Skipped {len(milestone_questions) - inserted_count} duplicates.")

if __name__ == "__main__":
    asyncio.run(seed_questions())
