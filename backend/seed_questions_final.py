import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

final_questions = [
    # Final additions Domain 1: General Security Concepts (10+)
    {"domain": "General Security Concepts", "question": "What is control testing?", "options": ["Verify control effectiveness", "No testing", "Skip testing", "Assumed working"], "correct_answer": "Verify control effectiveness"},
    {"domain": "General Security Concepts", "question": "What is continuous monitoring?", "options": ["Real-time system observation", "Periodic checks", "No monitoring", "Manual monitoring"], "correct_answer": "Real-time system observation"},
    {"domain": "General Security Concepts", "question": "What is data exfiltration?", "options": ["Unauthorized data removal", "Authorized export", "Data transfer", "Data sync"], "correct_answer": "Unauthorized data removal"},
    {"domain": "General Security Concepts", "question": "What is APT?", "options": ["Advanced Persistent Threat", "Automated Penetration Test", "Access Point Tool", "Application Protocol"], "correct_answer": "Advanced Persistent Threat"},
    {"domain": "General Security Concepts", "question": "What is zero-day exploit?", "options": ["Attack before patch available", "Known vulnerability", "Patched vulnerability", "Old vulnerability"], "correct_answer": "Attack before patch available"},
    {"domain": "General Security Concepts", "question": "What is vulnerability window?", "options": ["Time before patch", "Time to patch", "Update period", "Maintenance window"], "correct_answer": "Time before patch"},
    {"domain": "General Security Concepts", "question": "What is attestation statement?", "options": ["Formal compliance declaration", "Agreement", "Contract", "Policy"], "correct_answer": "Formal compliance declaration"},
    {"domain": "General Security Concepts", "question": "What is control validation?", "options": ["Confirm control works", "Test control", "Approve control", "Monitor control"], "correct_answer": "Confirm control works"},
    {"domain": "General Security Concepts", "question": "What is control effectiveness?", "options": ["Measure control success", "Control exists", "Control implemented", "Control planned"], "correct_answer": "Measure control success"},
    {"domain": "General Security Concepts", "question": "What is shadow IT?", "options": ["Unauthorized systems/software", "Approved systems", "Licensed software", "Documented systems"], "correct_answer": "Unauthorized systems/software"},
    
    # Final additions Domain 2: Threats, Vulnerabilities & Mitigations (20+)
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is DLL injection?", "options": ["Load malicious DLL", "Normal DLL loading", "Library compilation", "File creation"], "correct_answer": "Load malicious DLL"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is code injection?", "options": ["Insert malicious code", "Write code", "Compile code", "Run code"], "correct_answer": "Insert malicious code"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is command injection?", "options": ["Execute system commands", "User commands", "Script commands", "API commands"], "correct_answer": "Execute system commands"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is path traversal?", "options": ["Access files outside directory", "Navigate folders", "Access allowed files", "Folder navigation"], "correct_answer": "Access files outside directory"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is arbitrary file upload?", "options": ["Upload any file type", "Allowed uploads", "Checked uploads", "Validated uploads"], "correct_answer": "Upload any file type"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is insecure direct object reference?", "options": ["Access unauthorized objects", "Authorized access", "Direct access", "Checked access"], "correct_answer": "Access unauthorized objects"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is broken authentication?", "options": ["Weak password implementation", "Strong auth", "Multi-factor", "Secure authentication"], "correct_answer": "Weak password implementation"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is sensitive data exposure?", "options": ["Unprotected sensitive data", "Protected data", "Encrypted data", "Secure data"], "correct_answer": "Unprotected sensitive data"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is XML external entity?", "options": ["XXE attack", "XML processing", "File parsing", "Data handling"], "correct_answer": "XXE attack"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is insecure configuration?", "options": ["Default settings left", "Hardened settings", "Secure configuration", "Best practices"], "correct_answer": "Default settings left"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is using components with known vulnerabilities?", "options": ["Outdated libraries", "Updated libraries", "Patched libraries", "Secure libraries"], "correct_answer": "Outdated libraries"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is insufficient logging?", "options": ["Inadequate event recording", "Complete logging", "Detailed logs", "Audit logs"], "correct_answer": "Inadequate event recording"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is broken access control?", "options": ["Insufficient permission enforcement", "Strong access control", "Proper authorization", "Role-based access"], "correct_answer": "Insufficient permission enforcement"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is OWASP?", "options": ["Open Web Application Security Project", "Web Security Standard", "Application Security", "Web Safety"], "correct_answer": "Open Web Application Security Project"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is OWASP Top 10?", "options": ["Most critical web vulnerabilities", "Best practices", "Security controls", "Testing methods"], "correct_answer": "Most critical web vulnerabilities"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is CWE?", "options": ["Common Weakness Enumeration", "Computer Weakness", "Critical Weakness", "Code Weakness"], "correct_answer": "Common Weakness Enumeration"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is bug bounty?", "options": ["Pay for vulnerability disclosure", "Bug reporting", "Security testing", "Vulnerability scanning"], "correct_answer": "Pay for vulnerability disclosure"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is responsible disclosure?", "options": ["Report vulnerability privately first", "Public disclosure", "No disclosure", "Immediate public"], "correct_answer": "Report vulnerability privately first"},
    
    # Final additions Domain 3: Security Architecture (20+)
    {"domain": "Security Architecture", "question": "What is data classification policy?", "options": ["Rules for data sensitivity levels", "Data backup", "Data storage", "Data retention"], "correct_answer": "Rules for data sensitivity levels"},
    {"domain": "Security Architecture", "question": "What is data retention policy?", "options": ["How long to keep data", "Data backup", "Data deletion", "Data archiving"], "correct_answer": "How long to keep data"},
    {"domain": "Security Architecture", "question": "What is data destruction?", "options": ["Secure data erasure", "Data deletion", "File removal", "Format disk"], "correct_answer": "Secure data erasure"},
    {"domain": "Security Architecture", "question": "What is certificate management?", "options": ["Manage digital certificates", "Create certificates", "Revoke certificates", "Store certificates"], "correct_answer": "Manage digital certificates"},
    {"domain": "Security Architecture", "question": "What is key escrow?", "options": ["Third party holds backup keys", "First party storage", "Secure storage", "Encrypted storage"], "correct_answer": "Third party holds backup keys"},
    {"domain": "Security Architecture", "question": "What is key recovery?", "options": ["Retrieve lost keys", "Backup keys", "Store keys", "Delete keys"], "correct_answer": "Retrieve lost keys"},
    {"domain": "Security Architecture", "question": "What is certificate pinning?", "options": ["Lock app to specific cert", "Pin certificate", "Store certificate", "Verify certificate"], "correct_answer": "Lock app to specific cert"},
    {"domain": "Security Architecture", "question": "What is certificate chaining?", "options": ["Linked trust hierarchy", "Certificate binding", "Certificate linking", "Single certificate"], "correct_answer": "Linked trust hierarchy"},
    {"domain": "Security Architecture", "question": "What is certificate revocation?", "options": ["Invalidate certificate", "Renew certificate", "Extend certificate", "Recreate certificate"], "correct_answer": "Invalidate certificate"},
    {"domain": "Security Architecture", "question": "What is CRL?", "options": ["Certificate Revocation List", "Certificate Record List", "Crypto Revocation List", "Control Revocation List"], "correct_answer": "Certificate Revocation List"},
    {"domain": "Security Architecture", "question": "What is OCSP?", "options": ["Online Certificate Status Protocol", "Operational Certificate Status", "Official Certificate Service", "Online Certificate Service"], "correct_answer": "Online Certificate Status Protocol"},
    {"domain": "Security Architecture", "question": "What is trust model?", "options": ["How trust is established", "Trust chain", "Trust level", "Trust evaluation"], "correct_answer": "How trust is established"},
    {"domain": "Security Architecture", "question": "What is public key infrastructure?", "options": ["PKI system for certificates", "Public key system", "Encryption system", "Cryptographic system"], "correct_answer": "PKI system for certificates"},
    {"domain": "Security Architecture", "question": "What is certificate authority?", "options": ["Issues and signs certificates", "Stores certificates", "Distributes certificates", "Revokes certificates"], "correct_answer": "Issues and signs certificates"},
    {"domain": "Security Architecture", "question": "What is registration authority?", "options": ["Verifies certificate requests", "Issues certificates", "Revokes certificates", "Stores certificates"], "correct_answer": "Verifies certificate requests"},
    {"domain": "Security Architecture", "question": "What is validation authority?", "options": ["Confirms certificate status", "Issues certificates", "Stores certificates", "Revokes certificates"], "correct_answer": "Confirms certificate status"},
    {"domain": "Security Architecture", "question": "What is repository?", "options": ["Certificate storage location", "Code storage", "Data storage", "File storage"], "correct_answer": "Certificate storage location"},
    {"domain": "Security Architecture", "question": "What is DNSSEC?", "options": ["DNS Security Extensions", "Domain Name Security", "DNS Encryption", "Domain Security"], "correct_answer": "DNS Security Extensions"},
    {"domain": "Security Architecture", "question": "What is DANE?", "options": ["DNS-based Authentication of Named Entities", "Domain Name Extension", "DNS Authentication", "Domain Authentication"], "correct_answer": "DNS-based Authentication of Named Entities"},
    {"domain": "Security Architecture", "question": "What is CAA record?", "options": ["Certificate Authority Authorization", "Certificate Approval Authority", "Certificate Auditing Authority", "Certificate Administration Authority"], "correct_answer": "Certificate Authority Authorization"},
    
    # Final additions Domain 4: Security Operations (20+)
    {"domain": "Security Operations", "question": "What is false negative?", "options": ["Miss actual attack", "Detect attack", "Alert on threat", "Correct detection"], "correct_answer": "Miss actual attack"},
    {"domain": "Security Operations", "question": "What is true positive?", "options": ["Correctly detect threat", "Wrong detection", "No detection", "Incorrect alert"], "correct_answer": "Correctly detect threat"},
    {"domain": "Security Operations", "question": "What is true negative?", "options": ["Correctly identify no threat", "Detect threat", "Miss threat", "Wrong detection"], "correct_answer": "Correctly identify no threat"},
    {"domain": "Security Operations", "question": "What is containment strategy?", "options": ["Limit damage spread", "Prevent incident", "Respond to incident", "Recover from incident"], "correct_answer": "Limit damage spread"},
    {"domain": "Security Operations", "question": "What is short-term containment?", "options": ["Immediate temporary fix", "Long-term fix", "Permanent fix", "Partial fix"], "correct_answer": "Immediate temporary fix"},
    {"domain": "Security Operations", "question": "What is long-term containment?", "options": ["Permanent fix", "Temporary fix", "Immediate fix", "Partial fix"], "correct_answer": "Permanent fix"},
    {"domain": "Security Operations", "question": "What is evidence handling?", "options": ["Preserve incident evidence", "Delete evidence", "Ignore evidence", "Share evidence"], "correct_answer": "Preserve incident evidence"},
    {"domain": "Security Operations", "question": "What is chain of evidence?", "options": ["Track evidence custody", "Store evidence", "Collect evidence", "Analyze evidence"], "correct_answer": "Track evidence custody"},
    {"domain": "Security Operations", "question": "What is file integrity monitoring?", "options": ["Track file changes", "Create files", "Delete files", "Backup files"], "correct_answer": "Track file changes"},
    {"domain": "Security Operations", "question": "What is host-based intrusion detection?", "options": ["Monitor individual systems", "Monitor network", "Monitor users", "Monitor all"], "correct_answer": "Monitor individual systems"},
    {"domain": "Security Operations", "question": "What is network-based intrusion detection?", "options": ["Monitor network traffic", "Monitor systems", "Monitor users", "Monitor access"], "correct_answer": "Monitor network traffic"},
    {"domain": "Security Operations", "question": "What is behavior-based detection?", "options": ["Monitor for abnormal activity", "Signature detection", "Rule-based detection", "Policy detection"], "correct_answer": "Monitor for abnormal activity"},
    {"domain": "Security Operations", "question": "What is signature-based detection?", "options": ["Match known patterns", "Monitor behavior", "Track changes", "Watch anomalies"], "correct_answer": "Match known patterns"},
    {"domain": "Security Operations", "question": "What is anomaly detection?", "options": ["Identify unusual behavior", "Normal activity", "Expected activity", "Baseline activity"], "correct_answer": "Identify unusual behavior"},
    {"domain": "Security Operations", "question": "What is machine learning in security?", "options": ["AI for threat detection", "Manual detection", "Rule-based detection", "Signature detection"], "correct_answer": "AI for threat detection"},
    {"domain": "Security Operations", "question": "What is deception technology?", "options": ["Honeypots and decoys", "Detection systems", "Firewalls", "Access control"], "correct_answer": "Honeypots and decoys"},
    {"domain": "Security Operations", "question": "What is honeyfile?", "options": ["Fake sensitive file", "Real file", "Backup file", "System file"], "correct_answer": "Fake sensitive file"},
    {"domain": "Security Operations", "question": "What is honeytoken?", "options": ["Fake credential", "Real credential", "Service token", "Access token"], "correct_answer": "Fake credential"},
    {"domain": "Security Operations", "question": "What is honeyclient?", "options": ["Fake client system", "Real client", "Web client", "Network client"], "correct_answer": "Fake client system"},
    {"domain": "Security Operations", "question": "What is canary deployment?", "options": ["Test on small subset", "Deploy to all", "Deploy to group", "Deploy slowly"], "correct_answer": "Test on small subset"},
    
    # Final additions Domain 5: Security Program Management (20+)
    {"domain": "Security Program Management", "question": "What is information classification?", "options": ["Categorize data by sensitivity", "Data collection", "Data storage", "Data protection"], "correct_answer": "Categorize data by sensitivity"},
    {"domain": "Security Program Management", "question": "What is data steward?", "options": ["Responsible for data", "Collects data", "Stores data", "Deletes data"], "correct_answer": "Responsible for data"},
    {"domain": "Security Program Management", "question": "What is privacy impact assessment?", "options": ["Evaluate privacy risks", "Privacy compliance", "Privacy policies", "Privacy training"], "correct_answer": "Evaluate privacy risks"},
    {"domain": "Security Program Management", "question": "What is data inventory?", "options": ["Catalog of data assets", "Data location", "Data type", "Data value"], "correct_answer": "Catalog of data assets"},
    {"domain": "Security Program Management", "question": "What is data flow mapping?", "options": ["Track data movement", "Store data", "Protect data", "Access data"], "correct_answer": "Track data movement"},
    {"domain": "Security Program Management", "question": "What is data owner?", "options": ["Executive responsible for data", "Data user", "Data collector", "Data analyst"], "correct_answer": "Executive responsible for data"},
    {"domain": "Security Program Management", "question": "What is information owner?", "options": ["Business owner of info", "Technical owner", "Data owner", "System owner"], "correct_answer": "Business owner of info"},
    {"domain": "Security Program Management", "question": "What is custodian?", "options": ["Implements data protection", "Owns data", "Uses data", "Accesses data"], "correct_answer": "Implements data protection"},
    {"domain": "Security Program Management", "question": "What is processor?", "options": ["Processes data on behalf", "Owns data", "Stores data", "Accesses data"], "correct_answer": "Processes data on behalf"},
    {"domain": "Security Program Management", "question": "What is security controls testing?", "options": ["Verify controls work", "Implement controls", "Monitor controls", "Document controls"], "correct_answer": "Verify controls work"},
    {"domain": "Security Program Management", "question": "What is control environment?", "options": ["Culture supporting controls", "Physical environment", "Network environment", "System environment"], "correct_answer": "Culture supporting controls"},
    {"domain": "Security Program Management", "question": "What is risk appetite?", "options": ["Acceptable risk level", "Maximum risk", "No risk", "Unknown risk"], "correct_answer": "Acceptable risk level"},
    {"domain": "Security Program Management", "question": "What is risk tolerance?", "options": ["Acceptable variation in risk", "No variation", "No tolerance", "Full tolerance"], "correct_answer": "Acceptable variation in risk"},
    {"domain": "Security Program Management", "question": "What is residual risk?", "options": ["Risk after mitigations", "Original risk", "Total risk", "Final risk"], "correct_answer": "Risk after mitigations"},
    {"domain": "Security Program Management", "question": "What is inherent risk?", "options": ["Risk before controls", "Risk after controls", "Total risk", "Final risk"], "correct_answer": "Risk before controls"},
    {"domain": "Security Program Management", "question": "What is risk register?", "options": ["Document of identified risks", "Risk mitigation", "Risk acceptance", "Risk analysis"], "correct_answer": "Document of identified risks"},
    {"domain": "Security Program Management", "question": "What is risk matrix?", "options": ["Probability vs impact grid", "Risk list", "Risk analysis", "Risk measurement"], "correct_answer": "Probability vs impact grid"},
    {"domain": "Security Program Management", "question": "What is heat map?", "options": ["Visual risk distribution", "Temperature chart", "Risk graph", "Risk diagram"], "correct_answer": "Visual risk distribution"},
    {"domain": "Security Program Management", "question": "What is risk dashboard?", "options": ["Real-time risk view", "Risk report", "Risk analysis", "Risk listing"], "correct_answer": "Real-time risk view"},
    {"domain": "Security Program Management", "question": "What is risk communication?", "options": ["Share risk information", "Risk analysis", "Risk management", "Risk acceptance"], "correct_answer": "Share risk information"},
]

async def seed_questions():
    inserted_count = 0
    for q in final_questions:
        # Check if question already exists (case-insensitive)
        existing = await db.questions.find_one({"question": {"$regex": f"^{q['question']}$", "$options": "i"}})
        if not existing:
            await db.questions.insert_one(q)
            inserted_count += 1
        else:
            print(f"Skipped duplicate: {q['question']}")
    
    print(f"Inserted {inserted_count} new questions. Skipped {len(final_questions) - inserted_count} duplicates.")

if __name__ == "__main__":
    asyncio.run(seed_questions())
