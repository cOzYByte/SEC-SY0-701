import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

questions = [
    # Domain 1: General Security Concepts (~120 questions total)
    {
        "domain": "General Security Concepts",
        "question": "What is the primary goal of confidentiality in information security?",
        "options": ["Prevent unauthorized access to data", "Ensure data availability", "Verify data integrity", "Track data changes"],
        "correct_answer": "Prevent unauthorized access to data"
    },
    {
        "domain": "General Security Concepts",
        "question": "Which principle ensures that data has not been altered?",
        "options": ["Confidentiality", "Integrity", "Availability", "Non-repudiation"],
        "correct_answer": "Integrity"
    },
    # Add ~118 more for this domain...

    # Domain 2: Threats, Vulnerabilities & Mitigations (~120 questions total)
    {
        "domain": "Threats, Vulnerabilities & Mitigations",
        "question": "What is a common mitigation for SQL injection attacks?",
        "options": ["Input validation", "Firewall rules", "Encryption", "Multi-factor authentication"],
        "correct_answer": "Input validation"
    },
    {
        "domain": "Threats, Vulnerabilities & Mitigations",
        "question": "Which type of attack involves tricking users into revealing sensitive information?",
        "options": ["Phishing", "DDoS", "Man-in-the-middle", "Buffer overflow"],
        "correct_answer": "Phishing"
    },
    # Add ~118 more for this domain...

    # Domain 3: Security Architecture (~120 questions total)
    {
        "domain": "Security Architecture",
        "question": "What does the CIA triad stand for?",
        "options": ["Confidentiality, Integrity, Availability", "Control, Identification, Authentication", "Cryptography, Integrity, Access", "Compliance, Integrity, Assurance"],
        "correct_answer": "Confidentiality, Integrity, Availability"
    },
    {
        "domain": "Security Architecture",
        "question": "Which model enforces mandatory access controls?",
        "options": ["Bell-LaPadula", "Biba", "Clark-Wilson", "Role-Based Access Control"],
        "correct_answer": "Bell-LaPadula"
    },
    # Add ~118 more for this domain...

    # Domain 4: Security Operations (~120 questions total)
    {
        "domain": "Security Operations",
        "question": "What is the purpose of a Security Information and Event Management (SIEM) system?",
        "options": ["Monitor and analyze security events", "Encrypt data at rest", "Manage user identities", "Perform vulnerability scans"],
        "correct_answer": "Monitor and analyze security events"
    },
    {
        "domain": "Security Operations",
        "question": "Which tool is used for log analysis in security operations?",
        "options": ["Wireshark", "Splunk", "Nmap", "Metasploit"],
        "correct_answer": "Splunk"
    },
    # Add ~118 more for this domain...

    # Domain 5: Security Program Management (~120 questions total)
    {
        "domain": "Security Program Management",
        "question": "What is the first step in risk management?",
        "options": ["Risk assessment", "Risk mitigation", "Risk monitoring", "Risk acceptance"],
        "correct_answer": "Risk assessment"
    },
    {
        "domain": "Security Program Management",
        "question": "Which framework provides guidelines for information security management?",
        "options": ["ISO 27001", "NIST SP 800-53", "COBIT", "All of the above"],
        "correct_answer": "All of the above"
    },
    # Add ~118 more for this domain...
]

async def seed_questions():
    inserted_count = 0
    for q in questions:
        # Check if question already exists (case-insensitive)
        existing = await db.questions.find_one({"question": {"$regex": f"^{q['question']}$", "$options": "i"}})
        if not existing:
            await db.questions.insert_one(q)
            inserted_count += 1
        else:
            print(f"Skipped duplicate: {q['question']}")
    
    print(f"Inserted {inserted_count} new questions. Skipped {len(questions) - inserted_count} duplicates.")

if __name__ == "__main__":
    asyncio.run(seed_questions())