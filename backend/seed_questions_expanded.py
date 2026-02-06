import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

additional_questions = [
    # Additional Domain 1: General Security Concepts (25+ more)
    {"domain": "General Security Concepts", "question": "What is the AAA model?", "options": ["Authentication, Authorization, Accounting", "Access, Audit, Approval", "Authentication, Allocation, Auditing", "Authorization, Audit, Alerting"], "correct_answer": "Authentication, Authorization, Accounting"},
    {"domain": "General Security Concepts", "question": "Which is a strong password characteristic?", "options": ["At least 12 characters, mixed case, numbers, symbols", "Short password", "Dictionary words", "Personal information"], "correct_answer": "At least 12 characters, mixed case, numbers, symbols"},
    {"domain": "General Security Concepts", "question": "What is session management?", "options": ["Control user sessions", "Create sessions", "Delete sessions", "No management"], "correct_answer": "Control user sessions"},
    {"domain": "General Security Concepts", "question": "What is token-based authentication?", "options": ["Use tokens for access", "Password only", "No authentication", "Physical keys"], "correct_answer": "Use tokens for access"},
    {"domain": "General Security Concepts", "question": "What is SSO?", "options": ["Single Sign-On", "Simple Security Override", "Single Server Operation", "System Security Option"], "correct_answer": "Single Sign-On"},
    {"domain": "General Security Concepts", "question": "What is federated identity?", "options": ["Shared identity across systems", "Local identity only", "No identity sharing", "Isolated identity"], "correct_answer": "Shared identity across systems"},
    {"domain": "General Security Concepts", "question": "What is OAuth?", "options": ["Open authorization protocol", "Old authentication", "Offline authorization", "One basic auth"], "correct_answer": "Open authorization protocol"},
    {"domain": "General Security Concepts", "question": "What is SAML?", "options": ["Security Assertion Markup Language", "Secure Authentication Markup Layer", "System Access Management Language", "Secure Application Markup Language"], "correct_answer": "Security Assertion Markup Language"},
    {"domain": "General Security Concepts", "question": "What is certificate pinning?", "options": ["Lock certificate to app", "Share certificates", "No pinning", "Random pinning"], "correct_answer": "Lock certificate to app"},
    {"domain": "General Security Concepts", "question": "What is blockchain?", "options": ["Distributed ledger technology", "Database system", "Network protocol", "Encryption method"], "correct_answer": "Distributed ledger technology"},
    {"domain": "General Security Concepts", "question": "What is steganography?", "options": ["Hide data in other data", "Encrypt data", "Compress data", "Transfer data"], "correct_answer": "Hide data in other data"},
    {"domain": "General Security Concepts", "question": "What is watermarking?", "options": ["Embed copyright info", "Add water to data", "Delete data", "Copy data"], "correct_answer": "Embed copyright info"},
    {"domain": "General Security Concepts", "question": "What is information lifecycle?", "options": ["Creation, use, retention, disposal", "Creation only", "Storage only", "No lifecycle"], "correct_answer": "Creation, use, retention, disposal"},
    {"domain": "General Security Concepts", "question": "What is PII?", "options": ["Personally Identifiable Information", "Personal Internet Interface", "Public Identity Information", "Potential Impact Index"], "correct_answer": "Personally Identifiable Information"},
    {"domain": "General Security Concepts", "question": "What is PHI?", "options": ["Protected Health Information", "Personal Health Index", "Physical Health Interface", "Privacy Health Initiative"], "correct_answer": "Protected Health Information"},
    {"domain": "General Security Concepts", "question": "What is data minimization?", "options": ["Collect only necessary data", "Collect all data", "No collection", "Random collection"], "correct_answer": "Collect only necessary data"},
    {"domain": "General Security Concepts", "question": "What is privacy by design?", "options": ["Build privacy into systems", "Add privacy later", "No privacy", "Privacy optional"], "correct_answer": "Build privacy into systems"},
    {"domain": "General Security Concepts", "question": "What is accountability?", "options": ["Responsibility for actions", "No responsibility", "Shared blame", "No tracking"], "correct_answer": "Responsibility for actions"},
    {"domain": "General Security Concepts", "question": "What is transparency?", "options": ["Clear disclosure of practices", "Hidden practices", "Secret operations", "No disclosure"], "correct_answer": "Clear disclosure of practices"},
    {"domain": "General Security Concepts", "question": "What is data sovereignty?", "options": ["Data in specific country", "Global data", "No location rules", "Random location"], "correct_answer": "Data in specific country"},
    {"domain": "General Security Concepts", "question": "What is residual risk?", "options": ["Risk remaining after mitigation", "Initial risk", "No risk", "Unknown risk"], "correct_answer": "Risk remaining after mitigation"},
    {"domain": "General Security Concepts", "question": "What is inherent risk?", "options": ["Risk before controls", "Risk after controls", "No risk", "Managed risk"], "correct_answer": "Risk before controls"},
    {"domain": "General Security Concepts", "question": "What is business logic vulnerability?", "options": ["Flaw in program logic", "Database issue", "Network problem", "User error"], "correct_answer": "Flaw in program logic"},
    {"domain": "General Security Concepts", "question": "What is insecure deserialization?", "options": ["Vulnerability in object handling", "Secure conversion", "Data encryption", "Network transport"], "correct_answer": "Vulnerability in object handling"},
    {"domain": "General Security Concepts", "question": "What is type confusion?", "options": ["Exploiting type mishandling", "Correct type use", "Type safety", "Type validation"], "correct_answer": "Exploiting type mishandling"},
    
    # Additional Domain 2: Threats, Vulnerabilities & Mitigations (25+ more)
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is cryptanalysis?", "options": ["Breaking encryption", "Using encryption", "Creating encryption", "No encryption"], "correct_answer": "Breaking encryption"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is a side-channel attack?", "options": ["Exploit physical characteristics", "Direct attack", "Social engineering", "No attack"], "correct_answer": "Exploit physical characteristics"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is timing attack?", "options": ["Use execution time for info", "Direct timing", "No timing", "No information"], "correct_answer": "Use execution time for info"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is power analysis attack?", "options": ["Monitor power consumption", "Power failure", "No power", "Power surge"], "correct_answer": "Monitor power consumption"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is privilege escalation?", "options": ["Gain higher privileges", "Lose privileges", "No privileges", "Shared privileges"], "correct_answer": "Gain higher privileges"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is lateral movement?", "options": ["Move across systems", "Go backwards", "No movement", "Fixed position"], "correct_answer": "Move across systems"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is credential harvesting?", "options": ["Steal credentials", "Create credentials", "No credentials", "Manage credentials"], "correct_answer": "Steal credentials"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is credential stuffing?", "options": ["Try stolen creds elsewhere", "Create credentials", "No stuffing", "Share credentials"], "correct_answer": "Try stolen creds elsewhere"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is pass-the-hash?", "options": ["Use hashes to authenticate", "Create hash", "Delete hash", "Compare hashes"], "correct_answer": "Use hashes to authenticate"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is pass-the-ticket?", "options": ["Reuse Kerberos tickets", "Create tickets", "Delete tickets", "Manage tickets"], "correct_answer": "Reuse Kerberos tickets"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is golden ticket?", "options": ["Forged Kerberos TGT", "Real ticket", "Database ticket", "Network ticket"], "correct_answer": "Forged Kerberos TGT"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is silver ticket?", "options": ["Forged Kerberos service ticket", "Real ticket", "User ticket", "Admin ticket"], "correct_answer": "Forged Kerberos service ticket"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is Kerberos delegation?", "options": ["Improper privilege delegation", "Proper delegation", "No delegation", "Full delegation"], "correct_answer": "Improper privilege delegation"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is mimikatz?", "options": ["Post-exploitation tool", "Antivirus", "Firewall", "Intrusion detection"], "correct_answer": "Post-exploitation tool"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is PTH attack?", "options": ["Pass-the-Hash attack", "Password attack", "Phishing attack", "No attack"], "correct_answer": "Pass-the-Hash attack"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is LSASS?", "options": ["Windows authentication process", "Linux process", "User process", "System service"], "correct_answer": "Windows authentication process"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is dumping LSASS?", "options": ["Extract credentials", "Delete process", "Stop process", "Start process"], "correct_answer": "Extract credentials"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is SAM database?", "options": ["Windows security account manager", "Linux database", "User database", "File database"], "correct_answer": "Windows security account manager"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is registry dumping?", "options": ["Extract Windows registry", "Delete registry", "Update registry", "Back up registry"], "correct_answer": "Extract Windows registry"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is UAC bypass?", "options": ["Bypass User Account Control", "Enable UAC", "Disable UAC", "Check UAC"], "correct_answer": "Bypass User Account Control"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is privilege escalation vulnerability?", "options": ["Flaw allowing higher privileges", "No flaw", "Correct privileges", "Lower privileges"], "correct_answer": "Flaw allowing higher privileges"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is kernel exploit?", "options": ["Attack kernel", "Protect kernel", "Harden kernel", "Monitor kernel"], "correct_answer": "Attack kernel"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is format string attack?", "options": ["Exploit format specifiers", "String formatting", "No format", "Safe format"], "correct_answer": "Exploit format specifiers"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is Use-After-Free?", "options": ["Access freed memory", "Allocate memory", "Free memory", "Safe memory"], "correct_answer": "Access freed memory"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is integer overflow?", "options": ["Number exceeds limit", "Safe number", "Limited number", "No overflow"], "correct_answer": "Number exceeds limit"},
    {"domain": "Threats, Vulnerabilities & Mitigations", "question": "What is double free?", "options": ["Free memory twice", "Free once", "Allocate twice", "No free"], "correct_answer": "Free memory twice"},
    
    # Additional Domain 3: Security Architecture (25+ more)
    {"domain": "Security Architecture", "question": "What is RBAC?", "options": ["Role-Based Access Control", "Random Based", "Rule-Based", "Resource-Based"], "correct_answer": "Role-Based Access Control"},
    {"domain": "Security Architecture", "question": "What is ABAC?", "options": ["Attribute-Based Access Control", "Account-Based", "Activity-Based", "Access-Based"], "correct_answer": "Attribute-Based Access Control"},
    {"domain": "Security Architecture", "question": "What is rule-based access control?", "options": ["Rules determine access", "Role determines", "Attributes determine", "Random rules"], "correct_answer": "Rules determine access"},
    {"domain": "Security Architecture", "question": "What is Biba model?", "options": ["Integrity protection model", "Confidentiality model", "Availability model", "Hybrid model"], "correct_answer": "Integrity protection model"},
    {"domain": "Security Architecture", "question": "What is Clark-Wilson?", "options": ["Commercial integrity model", "Government model", "Public model", "Private model"], "correct_answer": "Commercial integrity model"},
    {"domain": "Security Architecture", "question": "What is Chinese Wall model?", "options": ["Conflict of interest control", "Network wall", "Firewall", "Boundary"], "correct_answer": "Conflict of interest control"},
    {"domain": "Security Architecture", "question": "What is information flow model?", "options": ["Control data movement", "Network flow", "User flow", "Access flow"], "correct_answer": "Control data movement"},
    {"domain": "Security Architecture", "question": "What is take-grant model?", "options": ["Rights transfer model", "Direct rights", "No transfer", "Revoke only"], "correct_answer": "Rights transfer model"},
    {"domain": "Security Architecture", "question": "What is lattice model?", "options": ["Ordered security levels", "Random levels", "No levels", "Single level"], "correct_answer": "Ordered security levels"},
    {"domain": "Security Architecture", "question": "What is privilege creep?", "options": ["Accumulation of unnecessary access", "Loss of access", "No access", "Revoked access"], "correct_answer": "Accumulation of unnecessary access"},
    {"domain": "Security Architecture", "question": "What is privileged access management?", "options": ["Control admin access", "User access", "No control", "Full access"], "correct_answer": "Control admin access"},
    {"domain": "Security Architecture", "question": "What is PAM?", "options": ["Privileged Access Management", "Public Access Module", "Personal Access Manager", "Public Access Manager"], "correct_answer": "Privileged Access Management"},
    {"domain": "Security Architecture", "question": "What is JEA?", "options": ["Just Enough Administration", "Justice and Equity", "Just-In-Time", "Joint Enterprise"], "correct_answer": "Just Enough Administration"},
    {"domain": "Security Architecture", "question": "What is JIT access?", "options": ["Just-In-Time access grant", "Just in time", "Access timing", "No timing"], "correct_answer": "Just-In-Time access grant"},
    {"domain": "Security Architecture", "question": "What is entitlement creep?", "options": ["Excessive permission accumulation", "No accumulation", "Permission removal", "Managed permissions"], "correct_answer": "Excessive permission accumulation"},
    {"domain": "Security Architecture", "question": "What is object reuse?", "options": ["Reusing media with residual data", "Clean reuse", "Formatted reuse", "Secure reuse"], "correct_answer": "Reusing media with residual data"},
    {"domain": "Security Architecture", "question": "What is covert channel?", "options": ["Unauthorized communication path", "Authorized path", "No channel", "Monitored channel"], "correct_answer": "Unauthorized communication path"},
    {"domain": "Security Architecture", "question": "What is timing channel?", "options": ["Covert through timing", "Normal timing", "Fast timing", "Slow timing"], "correct_answer": "Covert through timing"},
    {"domain": "Security Architecture", "question": "What is storage channel?", "options": ["Covert through storage", "Direct storage", "No storage", "Hidden storage"], "correct_answer": "Covert through storage"},
    {"domain": "Security Architecture", "question": "What is TCSEC?", "options": ["Trusted Computer System Evaluation Criteria", "Technical Computer Security", "Trusted Computing Standards", "Technical Certification"], "correct_answer": "Trusted Computer System Evaluation Criteria"},
    {"domain": "Security Architecture", "question": "What is Common Criteria?", "options": ["International security evaluation standard", "Local standard", "National standard", "Company standard"], "correct_answer": "International security evaluation standard"},
    {"domain": "Security Architecture", "question": "What is Orange Book?", "options": ["TCSEC publication", "Red Book", "Blue Book", "White Book"], "correct_answer": "TCSEC publication"},
    {"domain": "Security Architecture", "question": "What is FIPS?", "options": ["Federal Information Processing Standards", "First Implementation Priority", "Federal Information Protocol", "First Information Privacy"], "correct_answer": "Federal Information Processing Standards"},
    {"domain": "Security Architecture", "question": "What is EAL?", "options": ["Evaluation Assurance Level", "Enterprise Access Level", "Essential Assurance Level", "Extended Access Level"], "correct_answer": "Evaluation Assurance Level"},
    {"domain": "Security Architecture", "question": "What is security governance?", "options": ["Oversight of security program", "Technical implementation", "User training", "Incident response"], "correct_answer": "Oversight of security program"},
    
    # Additional Domain 4: Security Operations (35+ more)
    {"domain": "Security Operations", "question": "What is ETL?", "options": ["Extract, Transform, Load", "Electronic Transfer Link", "External Telemetry Link", "Event Tracking Link"], "correct_answer": "Extract, Transform, Load"},
    {"domain": "Security Operations", "question": "What is SOAR?", "options": ["Security Orchestration, Automation, Response", "System Operational And Response", "Security Operations Analysis Report", "System Organization And Response"], "correct_answer": "Security Orchestration, Automation, Response"},
    {"domain": "Security Operations", "question": "What is ticketing system?", "options": ["Track incidents and tasks", "Sell tickets", "Verify tickets", "No tracking"], "correct_answer": "Track incidents and tasks"},
    {"domain": "Security Operations", "question": "What is ITSM?", "options": ["IT Service Management", "Information Technology Standards", "IT Security Monitoring", "IT System Manager"], "correct_answer": "IT Service Management"},
    {"domain": "Security Operations", "question": "What is ITIL?", "options": ["IT Infrastructure Library", "IT Information Library", "IT Integration Library", "IT Integration Lifecycle"], "correct_answer": "IT Infrastructure Library"},
    {"domain": "Security Operations", "question": "What is change advisory board?", "options": ["Approve changes", "Request changes", "Execute changes", "No oversight"], "correct_answer": "Approve changes"},
    {"domain": "Security Operations", "question": "What is change control?", "options": ["Manage system changes", "No control", "User control", "Random changes"], "correct_answer": "Manage system changes"},
    {"domain": "Security Operations", "question": "What is RFC?", "options": ["Request for Change", "Remote File Copy", "Request for Code", "Remote Function Call"], "correct_answer": "Request for Change"},
    {"domain": "Security Operations", "question": "What is emergency change?", "options": ["Urgent required change", "Planned change", "No change", "Optional change"], "correct_answer": "Urgent required change"},
    {"domain": "Security Operations", "question": "What is change window?", "options": ["Scheduled change time", "Random time", "No time", "Anytime"], "correct_answer": "Scheduled change time"},
    {"domain": "Security Operations", "question": "What is backout plan?", "options": ["Revert failed change", "Continue on failure", "Accept failure", "No plan"], "correct_answer": "Revert failed change"},
    {"domain": "Security Operations", "question": "What is vulnerability management?", "options": ["Find and fix vulnerabilities", "Only detect", "No action", "Ignore"], "correct_answer": "Find and fix vulnerabilities"},
    {"domain": "Security Operations", "question": "What is CVSS?", "options": ["Common Vulnerability Scoring System", "Computer Virus Severity", "Critical Vulnerability Scale", "Cyber Vulnerability Score"], "correct_answer": "Common Vulnerability Scoring System"},
    {"domain": "Security Operations", "question": "What is EPSS?", "options": ["Exploit Prediction Scoring System", "Event Processing Security System", "Event Prediction Score", "Exploit Priority System"], "correct_answer": "Exploit Prediction Scoring System"},
    {"domain": "Security Operations", "question": "What is vulnerability dashboard?", "options": ["Visual vulnerability view", "Security view", "Performance view", "User view"], "correct_answer": "Visual vulnerability view"},
    {"domain": "Security Operations", "question": "What is remediation timeline?", "options": ["Deadline for fix", "Random deadline", "No deadline", "Optional deadline"], "correct_answer": "Deadline for fix"},
    {"domain": "Security Operations", "question": "What is SLA?", "options": ["Service Level Agreement", "Security Logging Agreement", "System Level Agreement", "Software License Agreement"], "correct_answer": "Service Level Agreement"},
    {"domain": "Security Operations", "question": "What is MTBF?", "options": ["Mean Time Between Failures", "Mean Time Before Fix", "Minimum Time Before Failure", "Mean Test Before Failure"], "correct_answer": "Mean Time Between Failures"},
    {"domain": "Security Operations", "question": "What is MTTF?", "options": ["Mean Time To Failure", "Mean Time To Fix", "Minimum Time To Failure", "Mean Test To Failure"], "correct_answer": "Mean Time To Failure"},
    {"domain": "Security Operations", "question": "What is incident severity?", "options": ["Impact level", "Time to fix", "Number affected", "Cost"], "correct_answer": "Impact level"},
    {"domain": "Security Operations", "question": "What is priority?", "options": ["Urgency of resolution", "Impact level", "Cost", "User count"], "correct_answer": "Urgency of resolution"},
    {"domain": "Security Operations", "question": "What is playbook?", "options": ["Documented incident procedure", "User manual", "Technical guide", "Policy document"], "correct_answer": "Documented incident procedure"},
    {"domain": "Security Operations", "question": "What is IOC?", "options": ["Indicator of Compromise", "Input/Output Control", "Internet Operating Center", "Integrated Operations Center"], "correct_answer": "Indicator of Compromise"},
    {"domain": "Security Operations", "question": "What is IOA?", "options": ["Indicator of Attack", "Input Output Adapter", "Internet Operating Address", "Integrated Operations Alert"], "correct_answer": "Indicator of Attack"},
    {"domain": "Security Operations", "question": "What is YARA?", "options": ["Malware identification tool", "Programming language", "System tool", "Network tool"], "correct_answer": "Malware identification tool"},
    {"domain": "Security Operations", "question": "What is Sigma?", "options": ["Generic detection rules", "Specific rules", "No rules", "Manual rules"], "correct_answer": "Generic detection rules"},
    {"domain": "Security Operations", "question": "What is threat hunting methodology?", "options": ["Proactive threat searching", "Reactive response", "No methodology", "Random search"], "correct_answer": "Proactive threat searching"},
    {"domain": "Security Operations", "question": "What is OSINT?", "options": ["Open Source Intelligence", "Operational Security Intel", "Operating System Intel", "Online Security Intel"], "correct_answer": "Open Source Intelligence"},
    {"domain": "Security Operations", "question": "What is dark web?", "options": ["Hidden internet part", "Normal web", "Surface web", "Deep web"], "correct_answer": "Hidden internet part"},
    {"domain": "Security Operations", "question": "What is Tor?", "options": ["Anonymous network", "Normal network", "Secure network", "Public network"], "correct_answer": "Anonymous network"},
    {"domain": "Security Operations", "question": "What is privacy-preserving logging?", "options": ["Log without exposing data", "Log all data", "No logging", "Random logging"], "correct_answer": "Log without exposing data"},
    
    # Additional Domain 5: Security Program Management (25+ more)
    {"domain": "Security Program Management", "question": "What is NIST CSF?", "options": ["Cybersecurity Framework", "Computer Security", "Network Security", "National Security"], "correct_answer": "Cybersecurity Framework"},
    {"domain": "Security Program Management", "question": "What is ISO 27001?", "options": ["Information security management", "IT security", "Network security", "Data security"], "correct_answer": "Information security management"},
    {"domain": "Security Program Management", "question": "What is COBIT?", "options": ["Control Objectives for IT", "Computer Objectives", "Control Organization", "Corporate Objectives"], "correct_answer": "Control Objectives for IT"},
    {"domain": "Security Program Management", "question": "What is COSO?", "options": ["Committee of Sponsoring Organizations", "Computer Security Organization", "Corporate Security", "Compliance Organization"], "correct_answer": "Committee of Sponsoring Organizations"},
    {"domain": "Security Program Management", "question": "What is ITIL?", "options": ["IT Infrastructure Library", "IT Information Library", "IT Infrastructure Lifecycle", "IT Integration Library"], "correct_answer": "IT Infrastructure Library"},
    {"domain": "Security Program Management", "question": "What is TOGAF?", "options": ["The Open Group Architecture Framework", "Technical Operations", "Technology Overview", "Technical Organization"], "correct_answer": "The Open Group Architecture Framework"},
    {"domain": "Security Program Management", "question": "What is FAIR model?", "options": ["Factor Analysis of Information Risk", "Framework for Assessment", "Financial Analysis", "Financial Assessment"], "correct_answer": "Factor Analysis of Information Risk"},
    {"domain": "Security Program Management", "question": "What is threat modeling?", "options": ["Identify system threats", "Prevent threats", "Monitor threats", "No threats"], "correct_answer": "Identify system threats"},
    {"domain": "Security Program Management", "question": "What is STRIDE?", "options": ["Spoofing, Tampering, Repudiation, Information Disclosure, DoS, EoP", "Security Threat", "System Testing", "Security Training"], "correct_answer": "Spoofing, Tampering, Repudiation, Information Disclosure, DoS, EoP"},
    {"domain": "Security Program Management", "question": "What is PASTA?", "options": ["Process for Attack Simulation Threat Analysis", "Process Analysis", "Practical Analysis", "Procedural Analysis"], "correct_answer": "Process for Attack Simulation Threat Analysis"},
    {"domain": "Security Program Management", "question": "What is OCTAVE?", "options": ["Operationally Critical Threat Assessment", "Operational Capability", "Organizational Assessment", "Operational Assessment"], "correct_answer": "Operationally Critical Threat Assessment"},
    {"domain": "Security Program Management", "question": "What is trike?", "options": ["Open source risk management", "Risk tracking", "Risk management tool", "Risk assessment"], "correct_answer": "Open source risk management"},
    {"domain": "Security Program Management", "question": "What is GDPR?", "options": ["General Data Protection Regulation", "Government Data Protection", "General Data Processing", "Government Database"], "correct_answer": "General Data Protection Regulation"},
    {"domain": "Security Program Management", "question": "What is CCPA?", "options": ["California Consumer Privacy Act", "Corporate Consumer Protection", "California Compliance", "Corporate Privacy Act"], "correct_answer": "California Consumer Privacy Act"},
    {"domain": "Security Program Management", "question": "What is HIPAA?", "options": ["Health Insurance Portability and Accountability Act", "Health Information", "Healthcare Insurance", "Hospital Privacy"], "correct_answer": "Health Insurance Portability and Accountability Act"},
    {"domain": "Security Program Management", "question": "What is PCI DSS?", "options": ["Payment Card Industry Data Security Standard", "Personal Computer", "Public Card Industry", "Payment Card Information"], "correct_answer": "Payment Card Industry Data Security Standard"},
    {"domain": "Security Program Management", "question": "What is SOC 2?", "options": ["Service Organization Control 2", "System Organization Control", "Security Organization", "Software Organization"], "correct_answer": "Service Organization Control 2"},
    {"domain": "Security Program Management", "question": "What is attestation?", "options": ["Verify compliance", "Certify system", "Provide assurance", "All of the above"], "correct_answer": "All of the above"},
    {"domain": "Security Program Management", "question": "What is internal audit?", "options": ["In-house compliance review", "External review", "No audit", "Partial audit"], "correct_answer": "In-house compliance review"},
    {"domain": "Security Program Management", "question": "What is external audit?", "options": ["Independent compliance review", "Internal review", "No audit", "Self audit"], "correct_answer": "Independent compliance review"},
    {"domain": "Security Program Management", "question": "What is security scorecard?", "options": ["Vendor security rating", "Performance score", "User score", "System score"], "correct_answer": "Vendor security rating"},
    {"domain": "Security Program Management", "question": "What is maturity assessment?", "options": ["Evaluate program level", "No evaluation", "Random assessment", "No maturity"], "correct_answer": "Evaluate program level"},
    {"domain": "Security Program Management", "question": "What is capability maturity model?", "options": ["Framework for process improvement", "Process level", "Capability level", "Maturity level"], "correct_answer": "Framework for process improvement"},
    {"domain": "Security Program Management", "question": "What is security metrics?", "options": ["Measure security effectiveness", "Count issues", "List vulnerabilities", "Monitor systems"], "correct_answer": "Measure security effectiveness"},
    {"domain": "Security Program Management", "question": "What is KRI?", "options": ["Key Risk Indicator", "Key Response Index", "Key Reporting Index", "Key Result Indicator"], "correct_answer": "Key Risk Indicator"},
]

async def seed_questions():
    inserted_count = 0
    for q in additional_questions:
        # Check if question already exists (case-insensitive)
        existing = await db.questions.find_one({"question": {"$regex": f"^{q['question']}$", "$options": "i"}})
        if not existing:
            await db.questions.insert_one(q)
            inserted_count += 1
        else:
            print(f"Skipped duplicate: {q['question']}")
    
    print(f"Inserted {inserted_count} new questions. Skipped {len(additional_questions) - inserted_count} duplicates.")

if __name__ == "__main__":
    asyncio.run(seed_questions())
