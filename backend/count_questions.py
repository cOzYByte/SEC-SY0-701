import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

async def count_questions():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    total = await db.questions.count_documents({})
    
    # Count by domain
    domains = [
        "General Security Concepts",
        "Threats, Vulnerabilities & Mitigations",
        "Security Architecture",
        "Security Operations",
        "Security Program Management"
    ]
    
    for domain in domains:
        count = await db.questions.count_documents({"domain": domain})
        print(f"{domain}: {count}")
    
    print(f"\nTotal questions in database: {total}")
    client.close()

asyncio.run(count_questions())
