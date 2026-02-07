from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

app = FastAPI()

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/questions")
async def get_questions():
    questions = await db.questions.find().to_list(1000)
    # Convert ObjectId to string for JSON serialization
    for q in questions:
        q["_id"] = str(q["_id"])
    return questions

# Add this to your main.py

@app.get("/questions/count_by_domain")
async def count_by_domain():
    pipeline = [
        {"$group": {"_id": "$domain", "count": {"$sum": 1}}},
        {"$project": {"domain": "$_id", "count": 1, "_id": 0}}
    ]
    results = await db.questions.aggregate(pipeline).to_list(length=None)
    return results