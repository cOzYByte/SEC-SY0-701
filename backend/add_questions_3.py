"""
Additional CompTIA Security+ SY0-701 Questions - Batch 3
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import uuid
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

additional_questions_3 = [
    {
        "domain": 1,
        "domain_name": "General Security Concepts",
        "question": "What is the difference between encoding and encryption?",
        "options": [
            {"id": "a", "text": "They are the same thing"},
            {"id": "b", "text": "Encoding transforms data format; encryption protects confidentiality"},
            {"id": "c", "text": "Encoding uses keys; encryption doesn't"},
            {"id": "d", "text": "Encoding is more secure than encryption"}
        ],
        "correct_answer": "b",
        "explanation": "Encoding transforms data into another format for compatibility (like Base64) - it's not for security. Encryption uses keys to protect data confidentiality and is designed for security."
    },
    {
        "domain": 1,
        "domain_name": "General Security Concepts",
        "question": "What is a nonce in cryptography?",
        "options": [
            {"id": "a", "text": "A permanent key"},
            {"id": "b", "text": "A number used only once to prevent replay attacks"},
            {"id": "c", "text": "A type of hash"},
            {"id": "d", "text": "A certificate type"}
        ],
        "correct_answer": "b",
        "explanation": "A nonce (number used once) is a random or pseudo-random number used only once in a cryptographic communication. It prevents replay attacks by ensuring each request is unique."
    },
    {
        "domain": 1,
        "domain_name": "General Security Concepts",
        "question": "What is PKI (Public Key Infrastructure)?",
        "options": [
            {"id": "a", "text": "A type of firewall"},
            {"id": "b", "text": "A framework for managing digital certificates and keys"},
            {"id": "c", "text": "A network protocol"},
            {"id": "d", "text": "A password policy"}
        ],
        "correct_answer": "b",
        "explanation": "PKI is a framework that manages digital certificates and public-private key pairs. It includes Certificate Authorities, Registration Authorities, and certificate management systems."
    },
    {
        "domain": 1,
        "domain_name": "General Security Concepts",
        "question": "What is the purpose of a digital signature?",
        "options": [
            {"id": "a", "text": "To encrypt data"},
            {"id": "b", "text": "To verify authenticity and integrity of data"},
            {"id": "c", "text": "To compress files"},
            {"id": "d", "text": "To delete files securely"}
        ],
        "correct_answer": "b",
        "explanation": "Digital signatures verify the authenticity (who signed it) and integrity (data hasn't changed) of digital messages or documents. They use asymmetric cryptography."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is an insider threat?",
        "options": [
            {"id": "a", "text": "External hackers"},
            {"id": "b", "text": "Threats from people with legitimate access"},
            {"id": "c", "text": "Malware from the internet"},
            {"id": "d", "text": "Physical break-ins"}
        ],
        "correct_answer": "b",
        "explanation": "Insider threats come from people with legitimate access to systems - employees, contractors, or partners. They can be malicious or unintentional (negligent) and are hard to detect."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is tailgating in physical security?",
        "options": [
            {"id": "a", "text": "Following too closely while driving"},
            {"id": "b", "text": "Following someone through a secure door without authorization"},
            {"id": "c", "text": "Tracking someone's location"},
            {"id": "d", "text": "Monitoring network traffic"}
        ],
        "correct_answer": "b",
        "explanation": "Tailgating (or piggybacking) is following an authorized person through a secure entrance without proper authentication. It's a common physical security threat."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is dumpster diving in security?",
        "options": [
            {"id": "a", "text": "A swimming technique"},
            {"id": "b", "text": "Searching through trash for sensitive information"},
            {"id": "c", "text": "A network scanning method"},
            {"id": "d", "text": "Data recovery"}
        ],
        "correct_answer": "b",
        "explanation": "Dumpster diving involves searching through discarded materials for sensitive information like documents, passwords, or hardware. Proper document destruction prevents this."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is pharming?",
        "options": [
            {"id": "a", "text": "Growing crops"},
            {"id": "b", "text": "Redirecting users to fraudulent websites via DNS manipulation"},
            {"id": "c", "text": "A phishing variant using phones"},
            {"id": "d", "text": "Collecting user data"}
        ],
        "correct_answer": "b",
        "explanation": "Pharming redirects users to fraudulent websites by manipulating DNS records or hosts files. Unlike phishing, victims don't need to click a link - they're automatically redirected."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is shoulder surfing?",
        "options": [
            {"id": "a", "text": "A water sport"},
            {"id": "b", "text": "Observing someone's screen or keyboard to steal information"},
            {"id": "c", "text": "Network monitoring"},
            {"id": "d", "text": "Carrying equipment"}
        ],
        "correct_answer": "b",
        "explanation": "Shoulder surfing is observing someone's screen, keyboard, or documents to steal sensitive information like passwords or PINs. Privacy screens and awareness help prevent it."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is an on-path attack previously known as?",
        "options": [
            {"id": "a", "text": "Path injection"},
            {"id": "b", "text": "Man-in-the-middle attack"},
            {"id": "c", "text": "Directory traversal"},
            {"id": "d", "text": "Route hijacking"}
        ],
        "correct_answer": "b",
        "explanation": "On-path attack is the modern term for what was previously called man-in-the-middle (MITM) attack. The attacker positions themselves between two communicating parties."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is IPSec primarily used for?",
        "options": [
            {"id": "a", "text": "Email encryption"},
            {"id": "b", "text": "Securing IP communications at the network layer"},
            {"id": "c", "text": "Web browsing"},
            {"id": "d", "text": "File sharing"}
        ],
        "correct_answer": "b",
        "explanation": "IPSec (Internet Protocol Security) secures IP communications by authenticating and encrypting network packets. It operates at the network layer and is commonly used in VPNs."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is the purpose of an SSL/TLS certificate?",
        "options": [
            {"id": "a", "text": "To speed up websites"},
            {"id": "b", "text": "To verify website identity and enable encrypted connections"},
            {"id": "c", "text": "To block malware"},
            {"id": "d", "text": "To store passwords"}
        ],
        "correct_answer": "b",
        "explanation": "SSL/TLS certificates verify website identity to browsers and enable encrypted HTTPS connections. They're issued by trusted Certificate Authorities."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is a screened subnet?",
        "options": [
            {"id": "a", "text": "A hidden network"},
            {"id": "b", "text": "A network segment protected by firewalls on both sides"},
            {"id": "c", "text": "A wireless network"},
            {"id": "d", "text": "A backup network"}
        ],
        "correct_answer": "b",
        "explanation": "A screened subnet (formerly DMZ) is a network segment protected by firewalls on both the internet and internal network sides. It hosts public-facing services."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is SNMPv3's main improvement over earlier versions?",
        "options": [
            {"id": "a", "text": "Faster performance"},
            {"id": "b", "text": "Authentication and encryption support"},
            {"id": "c", "text": "More device support"},
            {"id": "d", "text": "Better compatibility"}
        ],
        "correct_answer": "b",
        "explanation": "SNMPv3 adds authentication and encryption capabilities that were missing from SNMPv1 and SNMPv2. Earlier versions transmitted community strings in plaintext."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is SSH used for?",
        "options": [
            {"id": "a", "text": "Web browsing"},
            {"id": "b", "text": "Secure remote access and file transfer"},
            {"id": "c", "text": "Email encryption"},
            {"id": "d", "text": "Video conferencing"}
        ],
        "correct_answer": "b",
        "explanation": "SSH (Secure Shell) provides encrypted remote access to systems, secure file transfer (SFTP/SCP), and tunneling capabilities. It replaced insecure protocols like Telnet and FTP."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is S/MIME used for?",
        "options": [
            {"id": "a", "text": "Instant messaging"},
            {"id": "b", "text": "Secure email encryption and signing"},
            {"id": "c", "text": "Web security"},
            {"id": "d", "text": "File compression"}
        ],
        "correct_answer": "b",
        "explanation": "S/MIME (Secure/Multipurpose Internet Mail Extensions) provides email encryption and digital signing. It uses certificates to secure email content and verify sender identity."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is a COOP (Continuity of Operations Plan)?",
        "options": [
            {"id": "a", "text": "A cooperative agreement"},
            {"id": "b", "text": "A plan to maintain essential functions during disruptions"},
            {"id": "c", "text": "A chicken coop design"},
            {"id": "d", "text": "A communication plan"}
        ],
        "correct_answer": "b",
        "explanation": "A COOP ensures essential government functions continue during emergencies. It includes alternate facilities, essential functions identification, and succession planning."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is the purpose of degaussing?",
        "options": [
            {"id": "a", "text": "Measuring magnetism"},
            {"id": "b", "text": "Destroying data on magnetic media"},
            {"id": "c", "text": "Calibrating monitors"},
            {"id": "d", "text": "Testing hard drives"}
        ],
        "correct_answer": "b",
        "explanation": "Degaussing uses a powerful magnetic field to erase data from magnetic media like hard drives and tapes. It's a data sanitization method that renders media unusable."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is a legal hold?",
        "options": [
            {"id": "a", "text": "A type of lawsuit"},
            {"id": "b", "text": "Requirement to preserve data for potential litigation"},
            {"id": "c", "text": "A security lock"},
            {"id": "d", "text": "A legal agreement"}
        ],
        "correct_answer": "b",
        "explanation": "A legal hold requires preservation of relevant data and documents when litigation is anticipated. Normal retention policies are suspended for potentially relevant data."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is RPO (Recovery Point Objective)?",
        "options": [
            {"id": "a", "text": "Recovery speed"},
            {"id": "b", "text": "Maximum acceptable amount of data loss"},
            {"id": "c", "text": "Recovery process outline"},
            {"id": "d", "text": "Restoration priority order"}
        ],
        "correct_answer": "b",
        "explanation": "RPO defines the maximum acceptable amount of data loss measured in time. A 4-hour RPO means you can afford to lose up to 4 hours of data, requiring backups at least every 4 hours."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is the purpose of an after-action report?",
        "options": [
            {"id": "a", "text": "Employee evaluation"},
            {"id": "b", "text": "Documenting incident response for future improvement"},
            {"id": "c", "text": "Financial reporting"},
            {"id": "d", "text": "Legal documentation"}
        ],
        "correct_answer": "b",
        "explanation": "An after-action report documents what happened during an incident, what worked, what didn't, and recommendations for improvement. It's part of the lessons learned phase."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is a disaster recovery plan (DRP)?",
        "options": [
            {"id": "a", "text": "Insurance policy"},
            {"id": "b", "text": "Procedures to restore IT systems after a disaster"},
            {"id": "c", "text": "Emergency evacuation plan"},
            {"id": "d", "text": "Data backup schedule"}
        ],
        "correct_answer": "b",
        "explanation": "A DRP documents procedures to restore IT systems and operations after a disaster. It includes recovery priorities, procedures, and responsible parties."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is asset management in security?",
        "options": [
            {"id": "a", "text": "Financial investments"},
            {"id": "b", "text": "Tracking and managing organizational IT assets"},
            {"id": "c", "text": "Real estate management"},
            {"id": "d", "text": "Employee management"}
        ],
        "correct_answer": "b",
        "explanation": "Asset management tracks organizational IT assets including hardware, software, and data. You can't protect what you don't know you have - it's fundamental to security."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is a BPA (Business Partners Agreement)?",
        "options": [
            {"id": "a", "text": "A merger agreement"},
            {"id": "b", "text": "Agreement defining how business partners interact"},
            {"id": "c", "text": "A sales contract"},
            {"id": "d", "text": "An employment contract"}
        ],
        "correct_answer": "b",
        "explanation": "A BPA defines the relationship, responsibilities, and expectations between business partners, including data sharing, security requirements, and liability provisions."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is qualitative risk analysis?",
        "options": [
            {"id": "a", "text": "Using exact dollar amounts"},
            {"id": "b", "text": "Using subjective ratings like high, medium, low"},
            {"id": "c", "text": "Automated risk scanning"},
            {"id": "d", "text": "Statistical analysis"}
        ],
        "correct_answer": "b",
        "explanation": "Qualitative risk analysis uses subjective ratings (high/medium/low) rather than specific monetary values. It's faster but less precise than quantitative analysis."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is the purpose of security governance?",
        "options": [
            {"id": "a", "text": "Government regulations"},
            {"id": "b", "text": "Framework for security decision-making and accountability"},
            {"id": "c", "text": "Security software management"},
            {"id": "d", "text": "Network governance"}
        ],
        "correct_answer": "b",
        "explanation": "Security governance provides the framework for security decision-making, defines roles and responsibilities, and ensures alignment with business objectives and compliance requirements."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is a statement of work (SOW)?",
        "options": [
            {"id": "a", "text": "Employee job description"},
            {"id": "b", "text": "Document defining project deliverables and requirements"},
            {"id": "c", "text": "Financial statement"},
            {"id": "d", "text": "Security policy"}
        ],
        "correct_answer": "b",
        "explanation": "A SOW defines project scope, deliverables, timelines, and requirements for work to be performed. It's part of contracts and ensures clear expectations between parties."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What does CISO stand for?",
        "options": [
            {"id": "a", "text": "Chief Information Systems Operator"},
            {"id": "b", "text": "Chief Information Security Officer"},
            {"id": "c", "text": "Central Information Security Operations"},
            {"id": "d", "text": "Corporate Information Systems Office"}
        ],
        "correct_answer": "b",
        "explanation": "The CISO (Chief Information Security Officer) is the senior executive responsible for an organization's information security strategy, policies, and implementation."
    },
    {
        "domain": 1,
        "domain_name": "General Security Concepts",
        "question": "What is the purpose of key stretching?",
        "options": [
            {"id": "a", "text": "Making keys longer physically"},
            {"id": "b", "text": "Increasing the computational effort to crack passwords"},
            {"id": "c", "text": "Extending key validity periods"},
            {"id": "d", "text": "Distributing keys across systems"}
        ],
        "correct_answer": "b",
        "explanation": "Key stretching uses algorithms like PBKDF2, bcrypt, or scrypt to increase the computational effort needed to crack passwords, making brute-force attacks much slower."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is a botnet?",
        "options": [
            {"id": "a", "text": "A network of robots"},
            {"id": "b", "text": "A network of compromised computers controlled by an attacker"},
            {"id": "c", "text": "An automated help system"},
            {"id": "d", "text": "A chatbot network"}
        ],
        "correct_answer": "b",
        "explanation": "A botnet is a network of compromised computers (bots/zombies) controlled by an attacker (botmaster). Botnets are used for DDoS attacks, spam, and other malicious activities."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is a content delivery network (CDN) security benefit?",
        "options": [
            {"id": "a", "text": "Faster content delivery only"},
            {"id": "b", "text": "DDoS protection and traffic distribution"},
            {"id": "c", "text": "Data encryption only"},
            {"id": "d", "text": "User authentication"}
        ],
        "correct_answer": "b",
        "explanation": "CDNs distribute content across multiple servers, providing DDoS protection by absorbing attack traffic, reducing load on origin servers, and often including WAF capabilities."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is mean time to detect (MTTD)?",
        "options": [
            {"id": "a", "text": "Average time to fix issues"},
            {"id": "b", "text": "Average time to discover a security incident"},
            {"id": "c", "text": "Time between failures"},
            {"id": "d", "text": "Detection tool response time"}
        ],
        "correct_answer": "b",
        "explanation": "MTTD measures the average time between when a security incident occurs and when it's detected. Lower MTTD means faster detection and potentially reduced impact."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is a risk appetite?",
        "options": [
            {"id": "a", "text": "Desire for risky investments"},
            {"id": "b", "text": "Amount of risk an organization is willing to accept"},
            {"id": "c", "text": "Risk assessment methodology"},
            {"id": "d", "text": "Risk mitigation budget"}
        ],
        "correct_answer": "b",
        "explanation": "Risk appetite is the amount and type of risk an organization is willing to accept in pursuit of its objectives. It guides risk management decisions and resource allocation."
    },
    {
        "domain": 1,
        "domain_name": "General Security Concepts",
        "question": "What is the difference between authorization and authentication?",
        "options": [
            {"id": "a", "text": "They are the same thing"},
            {"id": "b", "text": "Authentication verifies identity; authorization determines access rights"},
            {"id": "c", "text": "Authorization comes before authentication"},
            {"id": "d", "text": "Authentication is more important"}
        ],
        "correct_answer": "b",
        "explanation": "Authentication verifies who you are (identity). Authorization determines what you're allowed to do (permissions). Authentication must occur before authorization."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is a watering hole attack target?",
        "options": [
            {"id": "a", "text": "Water treatment facilities"},
            {"id": "b", "text": "Websites frequently visited by target group"},
            {"id": "c", "text": "Drinking water"},
            {"id": "d", "text": "Swimming pools"}
        ],
        "correct_answer": "b",
        "explanation": "Watering hole attacks compromise websites frequently visited by the target group (like industry forums). When targets visit these sites, malware is delivered to their systems."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is tokenization?",
        "options": [
            {"id": "a", "text": "Creating digital tokens"},
            {"id": "b", "text": "Replacing sensitive data with non-sensitive placeholders"},
            {"id": "c", "text": "Network segmentation"},
            {"id": "d", "text": "User authentication"}
        ],
        "correct_answer": "b",
        "explanation": "Tokenization replaces sensitive data (like credit card numbers) with non-sensitive tokens. The original data is stored securely elsewhere and can only be retrieved with proper authorization."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is threat modeling?",
        "options": [
            {"id": "a", "text": "Creating 3D threat models"},
            {"id": "b", "text": "Systematic identification and prioritization of threats"},
            {"id": "c", "text": "Training threat actors"},
            {"id": "d", "text": "Designing security products"}
        ],
        "correct_answer": "b",
        "explanation": "Threat modeling systematically identifies potential threats, vulnerabilities, and attack vectors to prioritize security efforts. Common frameworks include STRIDE and PASTA."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is inherent risk?",
        "options": [
            {"id": "a", "text": "Risk after controls are applied"},
            {"id": "b", "text": "Risk before any controls are implemented"},
            {"id": "c", "text": "Inherited risk from parent company"},
            {"id": "d", "text": "Internal risk only"}
        ],
        "correct_answer": "b",
        "explanation": "Inherent risk is the level of risk before any controls are implemented. Residual risk is what remains after controls are applied. The goal is to reduce inherent risk to acceptable residual risk."
    },
    {
        "domain": 1,
        "domain_name": "General Security Concepts",
        "question": "What is federation in identity management?",
        "options": [
            {"id": "a", "text": "A government structure"},
            {"id": "b", "text": "Linking identity systems across organizations"},
            {"id": "c", "text": "Combining databases"},
            {"id": "d", "text": "Network federation"}
        ],
        "correct_answer": "b",
        "explanation": "Federation links identity systems across organizational boundaries, allowing users to use one set of credentials across multiple organizations or services (like SAML or OAuth)."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is a RAT (Remote Access Trojan)?",
        "options": [
            {"id": "a", "text": "A rodent-themed virus"},
            {"id": "b", "text": "Malware providing unauthorized remote control"},
            {"id": "c", "text": "A remote support tool"},
            {"id": "d", "text": "A network monitoring tool"}
        ],
        "correct_answer": "b",
        "explanation": "A RAT is malware that provides attackers with unauthorized remote control over infected systems. It can capture keystrokes, screenshots, and enable surveillance."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is data masking?",
        "options": [
            {"id": "a", "text": "Hiding data files"},
            {"id": "b", "text": "Obscuring sensitive data with fictional but realistic data"},
            {"id": "c", "text": "Encrypting data"},
            {"id": "d", "text": "Deleting data"}
        ],
        "correct_answer": "b",
        "explanation": "Data masking replaces sensitive data with realistic but fictional data. It's used in non-production environments to protect real data while maintaining data format and usability."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is a TTX (Tabletop Exercise)?",
        "options": [
            {"id": "a", "text": "Physical security test"},
            {"id": "b", "text": "Discussion-based exercise walking through scenarios"},
            {"id": "c", "text": "Network penetration test"},
            {"id": "d", "text": "Software testing"}
        ],
        "correct_answer": "b",
        "explanation": "A tabletop exercise is a discussion-based session where team members walk through scenarios to test plans and identify gaps without actually performing technical actions."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is a control framework?",
        "options": [
            {"id": "a", "text": "Remote control system"},
            {"id": "b", "text": "Organized set of security controls and guidelines"},
            {"id": "c", "text": "Quality control process"},
            {"id": "d", "text": "Project management framework"}
        ],
        "correct_answer": "b",
        "explanation": "A control framework is an organized set of security controls and guidelines (like NIST, ISO 27001, CIS Controls) that organizations use to implement and assess their security programs."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is the purpose of HSM in cloud environments?",
        "options": [
            {"id": "a", "text": "High-speed networking"},
            {"id": "b", "text": "Secure key management in multi-tenant environments"},
            {"id": "c", "text": "Storage management"},
            {"id": "d", "text": "Host monitoring"}
        ],
        "correct_answer": "b",
        "explanation": "Cloud HSMs provide secure key management in multi-tenant cloud environments, ensuring cryptographic keys are protected with dedicated hardware even in shared infrastructure."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is continuous monitoring?",
        "options": [
            {"id": "a", "text": "24/7 video surveillance"},
            {"id": "b", "text": "Ongoing assessment of security controls and threats"},
            {"id": "c", "text": "Employee monitoring"},
            {"id": "d", "text": "Network speed monitoring"}
        ],
        "correct_answer": "b",
        "explanation": "Continuous monitoring provides ongoing assessment of security controls, vulnerabilities, and threats. It enables real-time risk awareness and faster response to security issues."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is the shared responsibility model in cloud security?",
        "options": [
            {"id": "a", "text": "Everyone is equally responsible"},
            {"id": "b", "text": "Division of security duties between cloud provider and customer"},
            {"id": "c", "text": "Sharing passwords"},
            {"id": "d", "text": "Team collaboration"}
        ],
        "correct_answer": "b",
        "explanation": "The shared responsibility model divides security duties between cloud provider (security OF the cloud - infrastructure) and customer (security IN the cloud - data, applications, access)."
    }
]

async def add_questions():
    for q in additional_questions_3:
        q["id"] = str(uuid.uuid4())
    
    result = await db.questions.insert_many(additional_questions_3)
    print(f"Added {len(result.inserted_ids)} new questions")
    
    total = await db.questions.count_documents({})
    print(f"Total questions in database: {total}")

if __name__ == "__main__":
    asyncio.run(add_questions())
