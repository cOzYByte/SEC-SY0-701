"""
Additional CompTIA Security+ SY0-701 Questions - Batch 2
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

additional_questions_2 = [
    # More Domain 1 Questions
    {
        "domain": 1,
        "domain_name": "General Security Concepts",
        "question": "What is the purpose of a hardware security module (HSM)?",
        "options": [
            {"id": "a", "text": "To increase processing speed"},
            {"id": "b", "text": "To securely manage and store cryptographic keys"},
            {"id": "c", "text": "To connect hardware devices"},
            {"id": "d", "text": "To monitor hardware health"}
        ],
        "correct_answer": "b",
        "explanation": "An HSM is a dedicated hardware device designed to securely generate, store, and manage cryptographic keys. It provides tamper-resistant protection for sensitive cryptographic operations."
    },
    {
        "domain": 1,
        "domain_name": "General Security Concepts",
        "question": "What is OCSP (Online Certificate Status Protocol)?",
        "options": [
            {"id": "a", "text": "A method to encrypt certificates"},
            {"id": "b", "text": "A protocol to check certificate revocation status in real-time"},
            {"id": "c", "text": "A certificate backup system"},
            {"id": "d", "text": "A certificate creation protocol"}
        ],
        "correct_answer": "b",
        "explanation": "OCSP allows real-time checking of a certificate's revocation status. It's more efficient than downloading entire CRLs and provides immediate validation."
    },
    {
        "domain": 1,
        "domain_name": "General Security Concepts",
        "question": "What is key escrow?",
        "options": [
            {"id": "a", "text": "Destroying encryption keys"},
            {"id": "b", "text": "Storing copies of encryption keys with a trusted third party"},
            {"id": "c", "text": "Creating backup keys"},
            {"id": "d", "text": "Rotating encryption keys"}
        ],
        "correct_answer": "b",
        "explanation": "Key escrow stores copies of encryption keys with a trusted third party. This enables key recovery if the original is lost, but raises privacy concerns as others can access the keys."
    },
    {
        "domain": 1,
        "domain_name": "General Security Concepts",
        "question": "What is the purpose of steganography?",
        "options": [
            {"id": "a", "text": "To compress data"},
            {"id": "b", "text": "To hide data within other data"},
            {"id": "c", "text": "To encrypt data"},
            {"id": "d", "text": "To delete data securely"}
        ],
        "correct_answer": "b",
        "explanation": "Steganography hides secret data within ordinary-looking files like images, audio, or video. Unlike encryption which makes data unreadable, steganography hides the existence of the data."
    },
    {
        "domain": 1,
        "domain_name": "General Security Concepts",
        "question": "What is attribute-based access control (ABAC)?",
        "options": [
            {"id": "a", "text": "Access control based on user roles"},
            {"id": "b", "text": "Access control based on attributes of users, resources, and environment"},
            {"id": "c", "text": "Access control based on passwords"},
            {"id": "d", "text": "Access control based on time"}
        ],
        "correct_answer": "b",
        "explanation": "ABAC makes access decisions based on attributes such as user characteristics, resource properties, and environmental conditions, providing fine-grained, dynamic access control."
    },
    {
        "domain": 1,
        "domain_name": "General Security Concepts",
        "question": "What is ephemeral key exchange?",
        "options": [
            {"id": "a", "text": "Using permanent keys for exchange"},
            {"id": "b", "text": "Using temporary keys that are discarded after each session"},
            {"id": "c", "text": "Exchanging keys via email"},
            {"id": "d", "text": "Using shared passwords"}
        ],
        "correct_answer": "b",
        "explanation": "Ephemeral key exchange uses temporary keys generated for each session and discarded afterward. This provides Perfect Forward Secrecy - past communications can't be decrypted if keys are later compromised."
    },
    # More Domain 2 Questions
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is a keylogger?",
        "options": [
            {"id": "a", "text": "A tool to manage SSH keys"},
            {"id": "b", "text": "Malware that records keystrokes"},
            {"id": "c", "text": "A keyboard driver"},
            {"id": "d", "text": "A password manager"}
        ],
        "correct_answer": "b",
        "explanation": "A keylogger is malware that records keystrokes to capture sensitive information like passwords, credit card numbers, and messages. They can be software or hardware-based."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is an evil twin attack?",
        "options": [
            {"id": "a", "text": "Creating a duplicate server"},
            {"id": "b", "text": "Setting up a rogue wireless access point mimicking a legitimate one"},
            {"id": "c", "text": "Cloning a hard drive"},
            {"id": "d", "text": "Creating a fake user account"}
        ],
        "correct_answer": "b",
        "explanation": "An evil twin attack creates a rogue Wi-Fi access point with the same name as a legitimate one. Victims connect to it, allowing attackers to intercept traffic or launch other attacks."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is a replay attack?",
        "options": [
            {"id": "a", "text": "Playing back video recordings"},
            {"id": "b", "text": "Capturing and retransmitting valid data to gain unauthorized access"},
            {"id": "c", "text": "Replaying audio messages"},
            {"id": "d", "text": "A type of DDoS attack"}
        ],
        "correct_answer": "b",
        "explanation": "A replay attack captures valid authentication or transaction data and retransmits it to gain unauthorized access. Timestamps, nonces, and session tokens help prevent replay attacks."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is Bluetooth bluesnarfing?",
        "options": [
            {"id": "a", "text": "Sending unsolicited messages via Bluetooth"},
            {"id": "b", "text": "Unauthorized access to information via Bluetooth"},
            {"id": "c", "text": "Jamming Bluetooth signals"},
            {"id": "d", "text": "Pairing devices via Bluetooth"}
        ],
        "correct_answer": "b",
        "explanation": "Bluesnarfing is unauthorized access to information on a Bluetooth-enabled device, such as contacts, emails, and text messages. It exploits vulnerabilities in Bluetooth implementations."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is a CSRF (Cross-Site Request Forgery) attack?",
        "options": [
            {"id": "a", "text": "Stealing cookies from websites"},
            {"id": "b", "text": "Tricking users into performing actions they didn't intend"},
            {"id": "c", "text": "Injecting scripts into web pages"},
            {"id": "d", "text": "Bypassing authentication"}
        ],
        "correct_answer": "b",
        "explanation": "CSRF tricks authenticated users into performing unintended actions on a website. The attacker creates requests that execute actions using the victim's authenticated session."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is shimming in the context of attacks?",
        "options": [
            {"id": "a", "text": "A card skimming technique for chip cards"},
            {"id": "b", "text": "A network attack"},
            {"id": "c", "text": "A type of encryption"},
            {"id": "d", "text": "A software patching method"}
        ],
        "correct_answer": "a",
        "explanation": "Shimming is a technique to capture data from chip-based payment cards. A thin device (shim) is inserted into the card reader to intercept data between the chip and terminal."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is cryptojacking?",
        "options": [
            {"id": "a", "text": "Stealing cryptocurrency wallets"},
            {"id": "b", "text": "Using someone's computer to mine cryptocurrency without consent"},
            {"id": "c", "text": "Encrypting ransomware"},
            {"id": "d", "text": "Breaking encryption"}
        ],
        "correct_answer": "b",
        "explanation": "Cryptojacking secretly uses victim's computing resources to mine cryptocurrency. It can occur through malware or malicious scripts on websites, causing performance degradation."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is a downgrade attack?",
        "options": [
            {"id": "a", "text": "Forcing a system to use older, weaker security protocols"},
            {"id": "b", "text": "Downgrading software versions"},
            {"id": "c", "text": "Reducing network speed"},
            {"id": "d", "text": "Demoting user privileges"}
        ],
        "correct_answer": "a",
        "explanation": "A downgrade attack forces systems to use older, weaker security protocols or cipher suites that have known vulnerabilities, making the connection easier to compromise."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is living off the land (LOTL)?",
        "options": [
            {"id": "a", "text": "Using renewable resources"},
            {"id": "b", "text": "Using legitimate system tools for malicious purposes"},
            {"id": "c", "text": "Off-grid computing"},
            {"id": "d", "text": "A farming technique"}
        ],
        "correct_answer": "b",
        "explanation": "Living off the land uses legitimate, pre-installed system tools (PowerShell, WMI, etc.) for malicious activities. This helps attackers evade detection by not introducing new malware."
    },
    # More Domain 3 Questions
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is a UTM (Unified Threat Management) device?",
        "options": [
            {"id": "a", "text": "A monitoring tool"},
            {"id": "b", "text": "A device combining multiple security functions"},
            {"id": "c", "text": "A type of router"},
            {"id": "d", "text": "A backup server"}
        ],
        "correct_answer": "b",
        "explanation": "A UTM device combines multiple security functions (firewall, IDS/IPS, antivirus, content filtering, VPN) in a single appliance, simplifying security management for smaller organizations."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is the purpose of DNSSEC?",
        "options": [
            {"id": "a", "text": "To speed up DNS queries"},
            {"id": "b", "text": "To authenticate DNS responses and prevent spoofing"},
            {"id": "c", "text": "To encrypt DNS queries"},
            {"id": "d", "text": "To cache DNS records"}
        ],
        "correct_answer": "b",
        "explanation": "DNSSEC adds digital signatures to DNS records, allowing resolvers to verify that responses are authentic and haven't been tampered with. It prevents DNS spoofing attacks."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is SD-WAN?",
        "options": [
            {"id": "a", "text": "Standard network configuration"},
            {"id": "b", "text": "Software-defined approach to managing wide area networks"},
            {"id": "c", "text": "A type of firewall"},
            {"id": "d", "text": "A wireless standard"}
        ],
        "correct_answer": "b",
        "explanation": "SD-WAN uses software to manage WAN connections, providing centralized control, dynamic path selection, and improved performance. It often replaces traditional MPLS connections."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is FIM (File Integrity Monitoring)?",
        "options": [
            {"id": "a", "text": "A file management system"},
            {"id": "b", "text": "Monitoring files for unauthorized changes"},
            {"id": "c", "text": "A file encryption tool"},
            {"id": "d", "text": "A backup solution"}
        ],
        "correct_answer": "b",
        "explanation": "FIM monitors critical system files for unauthorized changes by comparing current file hashes to known-good baselines. It helps detect malware and unauthorized modifications."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is port security on a network switch?",
        "options": [
            {"id": "a", "text": "Physical protection of network ports"},
            {"id": "b", "text": "Limiting which MAC addresses can connect to a port"},
            {"id": "c", "text": "Encrypting port traffic"},
            {"id": "d", "text": "Monitoring port speed"}
        ],
        "correct_answer": "b",
        "explanation": "Port security limits which MAC addresses can connect to a switch port, preventing unauthorized devices from accessing the network and mitigating MAC flooding attacks."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is ZTNA (Zero Trust Network Access)?",
        "options": [
            {"id": "a", "text": "A type of VPN"},
            {"id": "b", "text": "Access control based on identity verification regardless of network location"},
            {"id": "c", "text": "A firewall type"},
            {"id": "d", "text": "A network protocol"}
        ],
        "correct_answer": "b",
        "explanation": "ZTNA provides secure access to applications based on user identity and device posture, regardless of network location. It's a key component of Zero Trust architecture."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is a secure web gateway (SWG)?",
        "options": [
            {"id": "a", "text": "A web server"},
            {"id": "b", "text": "A security solution filtering web traffic for threats"},
            {"id": "c", "text": "A web development tool"},
            {"id": "d", "text": "A content delivery network"}
        ],
        "correct_answer": "b",
        "explanation": "A SWG filters web traffic to protect users from web-based threats, enforcing policies for URL filtering, malware detection, and data loss prevention."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is TLS (Transport Layer Security)?",
        "options": [
            {"id": "a", "text": "A network layer protocol"},
            {"id": "b", "text": "A protocol providing encrypted communications over networks"},
            {"id": "c", "text": "A type of firewall"},
            {"id": "d", "text": "A routing protocol"}
        ],
        "correct_answer": "b",
        "explanation": "TLS provides encrypted communications between clients and servers. It's the successor to SSL and is used in HTTPS, secure email, and other applications requiring secure transport."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is network segmentation?",
        "options": [
            {"id": "a", "text": "Dividing a network into smaller, isolated segments"},
            {"id": "b", "text": "Combining multiple networks"},
            {"id": "c", "text": "Measuring network performance"},
            {"id": "d", "text": "A backup strategy"}
        ],
        "correct_answer": "a",
        "explanation": "Network segmentation divides a network into smaller segments with separate security controls. This limits lateral movement by attackers and contains breaches to specific segments."
    },
    # More Domain 4 Questions
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is the purpose of a forensic image?",
        "options": [
            {"id": "a", "text": "A photograph of evidence"},
            {"id": "b", "text": "A bit-by-bit copy of storage media for analysis"},
            {"id": "c", "text": "A compressed backup"},
            {"id": "d", "text": "A screenshot of an error"}
        ],
        "correct_answer": "b",
        "explanation": "A forensic image is an exact bit-by-bit copy of storage media, including unallocated space and deleted files. It preserves evidence integrity for analysis while protecting the original."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is a false negative in security detection?",
        "options": [
            {"id": "a", "text": "A benign event flagged as malicious"},
            {"id": "b", "text": "A real threat that was not detected"},
            {"id": "c", "text": "A correctly identified threat"},
            {"id": "d", "text": "A system error"}
        ],
        "correct_answer": "b",
        "explanation": "A false negative occurs when a security system fails to detect an actual threat. This is dangerous as it allows attacks to proceed undetected."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is a warm site?",
        "options": [
            {"id": "a", "text": "A site with good heating"},
            {"id": "b", "text": "A partially equipped disaster recovery site"},
            {"id": "c", "text": "A primary data center"},
            {"id": "d", "text": "A testing environment"}
        ],
        "correct_answer": "b",
        "explanation": "A warm site has infrastructure and some pre-installed equipment but requires additional setup before operations can resume. It balances cost and recovery time between hot and cold sites."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What does MTBF stand for?",
        "options": [
            {"id": "a", "text": "Maximum Time Before Failure"},
            {"id": "b", "text": "Mean Time Between Failures"},
            {"id": "c", "text": "Minimum Technical Backup Facility"},
            {"id": "d", "text": "Managed Technical Business Function"}
        ],
        "correct_answer": "b",
        "explanation": "MTBF (Mean Time Between Failures) measures the average time a system operates before failing. It's used to assess system reliability and plan maintenance schedules."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is the purpose of a DMZ in network architecture?",
        "options": [
            {"id": "a", "text": "To store sensitive data"},
            {"id": "b", "text": "To host public-facing services while protecting internal networks"},
            {"id": "c", "text": "To backup data"},
            {"id": "d", "text": "To route traffic faster"}
        ],
        "correct_answer": "b",
        "explanation": "A DMZ (Demilitarized Zone) is a network segment that hosts public-facing services while providing a buffer between the internet and internal networks."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is the kill chain in cybersecurity?",
        "options": [
            {"id": "a", "text": "A malware removal process"},
            {"id": "b", "text": "A model describing the stages of a cyberattack"},
            {"id": "c", "text": "A network termination process"},
            {"id": "d", "text": "A type of firewall rule"}
        ],
        "correct_answer": "b",
        "explanation": "The kill chain (Cyber Kill Chain) describes attack stages: Reconnaissance, Weaponization, Delivery, Exploitation, Installation, Command & Control, and Actions on Objectives."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is XDR (Extended Detection and Response)?",
        "options": [
            {"id": "a", "text": "A type of backup"},
            {"id": "b", "text": "Unified security detection across multiple security layers"},
            {"id": "c", "text": "A firewall type"},
            {"id": "d", "text": "A network protocol"}
        ],
        "correct_answer": "b",
        "explanation": "XDR unifies detection and response across multiple security layers (endpoints, networks, cloud) providing comprehensive visibility and automated response capabilities."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is the purpose of a network tap?",
        "options": [
            {"id": "a", "text": "To increase network speed"},
            {"id": "b", "text": "To passively monitor network traffic"},
            {"id": "c", "text": "To connect wireless devices"},
            {"id": "d", "text": "To block malicious traffic"}
        ],
        "correct_answer": "b",
        "explanation": "A network tap is a hardware device that passively copies network traffic for monitoring without affecting the original traffic flow. It's used for security monitoring and forensics."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is a security baseline?",
        "options": [
            {"id": "a", "text": "The lowest security level"},
            {"id": "b", "text": "A documented set of minimum security configurations"},
            {"id": "c", "text": "A network diagram"},
            {"id": "d", "text": "A type of firewall"}
        ],
        "correct_answer": "b",
        "explanation": "A security baseline is a documented set of minimum security configurations for systems. It provides a consistent security standard and helps identify deviations."
    },
    # More Domain 5 Questions
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is Single Loss Expectancy (SLE)?",
        "options": [
            {"id": "a", "text": "The annual cost of security"},
            {"id": "b", "text": "The expected monetary loss from a single incident"},
            {"id": "c", "text": "The cost of security software"},
            {"id": "d", "text": "The budget for security training"}
        ],
        "correct_answer": "b",
        "explanation": "SLE is the expected monetary loss from a single security incident. It's calculated as Asset Value × Exposure Factor (percentage of asset lost)."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is the purpose of ISO 27001?",
        "options": [
            {"id": "a", "text": "Network standards"},
            {"id": "b", "text": "Information security management system requirements"},
            {"id": "c", "text": "Physical security standards"},
            {"id": "d", "text": "Software development standards"}
        ],
        "correct_answer": "b",
        "explanation": "ISO 27001 is an international standard specifying requirements for establishing, implementing, maintaining, and continually improving an information security management system (ISMS)."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is a data processor under GDPR?",
        "options": [
            {"id": "a", "text": "The person whose data is being processed"},
            {"id": "b", "text": "An entity that processes data on behalf of a controller"},
            {"id": "c", "text": "The regulatory authority"},
            {"id": "d", "text": "A computer system"}
        ],
        "correct_answer": "b",
        "explanation": "Under GDPR, a data processor processes personal data on behalf of a data controller. Processors must follow controller instructions and implement appropriate security measures."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is the purpose of separation of duties?",
        "options": [
            {"id": "a", "text": "To reduce workload"},
            {"id": "b", "text": "To prevent fraud by requiring multiple people for sensitive tasks"},
            {"id": "c", "text": "To improve efficiency"},
            {"id": "d", "text": "To assign job titles"}
        ],
        "correct_answer": "b",
        "explanation": "Separation of duties divides critical tasks among multiple people so no single person can complete a sensitive process alone. This prevents fraud and errors."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is a right-to-audit clause?",
        "options": [
            {"id": "a", "text": "The right to perform financial audits"},
            {"id": "b", "text": "Contractual right to audit vendor security practices"},
            {"id": "c", "text": "Annual reporting requirements"},
            {"id": "d", "text": "Government audit requirements"}
        ],
        "correct_answer": "b",
        "explanation": "A right-to-audit clause gives organizations the contractual right to audit their vendors' security practices. It's important for third-party risk management."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is the purpose of a security assessment?",
        "options": [
            {"id": "a", "text": "To install security software"},
            {"id": "b", "text": "To evaluate the effectiveness of security controls"},
            {"id": "c", "text": "To hire security staff"},
            {"id": "d", "text": "To purchase security equipment"}
        ],
        "correct_answer": "b",
        "explanation": "A security assessment evaluates the effectiveness of security controls, identifies vulnerabilities, and provides recommendations for improvement."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is a gap analysis in security?",
        "options": [
            {"id": "a", "text": "Finding physical gaps in security"},
            {"id": "b", "text": "Comparing current security state to desired state"},
            {"id": "c", "text": "Analyzing network gaps"},
            {"id": "d", "text": "Time between security updates"}
        ],
        "correct_answer": "b",
        "explanation": "A gap analysis compares the current security posture to a desired state (framework, compliance requirement, or best practice) to identify areas needing improvement."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is a risk register?",
        "options": [
            {"id": "a", "text": "A list of risky employees"},
            {"id": "b", "text": "A document tracking identified risks and their treatment"},
            {"id": "c", "text": "A financial ledger"},
            {"id": "d", "text": "An insurance policy"}
        ],
        "correct_answer": "b",
        "explanation": "A risk register documents identified risks, their likelihood, impact, risk level, treatment decisions, and status. It's a key tool for ongoing risk management."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is the purpose of a lessons learned review?",
        "options": [
            {"id": "a", "text": "Employee training evaluation"},
            {"id": "b", "text": "Post-incident analysis to improve future response"},
            {"id": "c", "text": "Testing backup systems"},
            {"id": "d", "text": "Compliance reporting"}
        ],
        "correct_answer": "b",
        "explanation": "A lessons learned review analyzes what went well and what could be improved after an incident or exercise. It helps improve processes and prevent similar incidents."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is SOX compliance primarily focused on?",
        "options": [
            {"id": "a", "text": "Healthcare data"},
            {"id": "b", "text": "Financial reporting and corporate governance"},
            {"id": "c", "text": "Credit card security"},
            {"id": "d", "text": "Government classified information"}
        ],
        "correct_answer": "b",
        "explanation": "SOX (Sarbanes-Oxley Act) focuses on financial reporting accuracy and corporate governance for publicly traded companies. It includes IT controls that affect financial reporting."
    },
    # Additional mixed domain questions
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is spear phishing?",
        "options": [
            {"id": "a", "text": "Phishing attacks targeting everyone"},
            {"id": "b", "text": "Highly targeted phishing attacks on specific individuals"},
            {"id": "c", "text": "Fishing with a spear"},
            {"id": "d", "text": "Phone-based phishing"}
        ],
        "correct_answer": "b",
        "explanation": "Spear phishing targets specific individuals or organizations with personalized messages. Unlike generic phishing, attackers research victims to make messages more convincing."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is the purpose of geofencing?",
        "options": [
            {"id": "a", "text": "Building physical fences"},
            {"id": "b", "text": "Creating virtual boundaries for location-based actions"},
            {"id": "c", "text": "Geographic data analysis"},
            {"id": "d", "text": "Mapping networks"}
        ],
        "correct_answer": "b",
        "explanation": "Geofencing creates virtual geographic boundaries. When devices enter or leave these areas, it can trigger actions like alerts, access restrictions, or policy changes."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is the difference between vulnerability scanning and penetration testing?",
        "options": [
            {"id": "a", "text": "They are the same thing"},
            {"id": "b", "text": "Scanning identifies vulnerabilities; pen testing exploits them"},
            {"id": "c", "text": "Pen testing is automated; scanning is manual"},
            {"id": "d", "text": "Scanning is more thorough than pen testing"}
        ],
        "correct_answer": "b",
        "explanation": "Vulnerability scanning automatically identifies potential vulnerabilities. Penetration testing goes further by actively attempting to exploit vulnerabilities to determine real-world impact."
    },
    {
        "domain": 1,
        "domain_name": "General Security Concepts",
        "question": "What is blockchain primarily known for providing?",
        "options": [
            {"id": "a", "text": "Encryption"},
            {"id": "b", "text": "Immutable, distributed record-keeping"},
            {"id": "c", "text": "Network speed"},
            {"id": "d", "text": "User authentication"}
        ],
        "correct_answer": "b",
        "explanation": "Blockchain provides immutable, distributed record-keeping through cryptographically linked blocks. Once data is recorded, it's extremely difficult to alter without detection."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is a race condition vulnerability?",
        "options": [
            {"id": "a", "text": "A competition between hackers"},
            {"id": "b", "text": "A flaw where timing affects system behavior unexpectedly"},
            {"id": "c", "text": "A network speed issue"},
            {"id": "d", "text": "A type of DDoS attack"}
        ],
        "correct_answer": "b",
        "explanation": "A race condition occurs when the timing of events affects system behavior in unexpected ways. Attackers can exploit these to bypass security checks or gain elevated privileges."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is east-west traffic in a data center?",
        "options": [
            {"id": "a", "text": "Traffic to/from the internet"},
            {"id": "b", "text": "Traffic between servers within the data center"},
            {"id": "c", "text": "Geographic data routing"},
            {"id": "d", "text": "Backup traffic"}
        ],
        "correct_answer": "b",
        "explanation": "East-west traffic flows between servers within a data center or cloud environment. North-south traffic flows between the data center and external networks. Microsegmentation helps secure east-west traffic."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is IOC (Indicator of Compromise)?",
        "options": [
            {"id": "a", "text": "A security certification"},
            {"id": "b", "text": "Evidence that a security incident may have occurred"},
            {"id": "c", "text": "A type of malware"},
            {"id": "d", "text": "An incident report"}
        ],
        "correct_answer": "b",
        "explanation": "IOCs are artifacts or evidence suggesting a security incident may have occurred. Examples include unusual file hashes, suspicious IP addresses, or abnormal network traffic patterns."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is the principle of data minimization?",
        "options": [
            {"id": "a", "text": "Compressing data"},
            {"id": "b", "text": "Collecting only necessary data for specific purposes"},
            {"id": "c", "text": "Deleting all old data"},
            {"id": "d", "text": "Encrypting data"}
        ],
        "correct_answer": "b",
        "explanation": "Data minimization means collecting and retaining only the personal data necessary for specific, stated purposes. It's a key principle in GDPR and other privacy regulations."
    }
]

async def add_questions():
    for q in additional_questions_2:
        q["id"] = str(uuid.uuid4())
    
    result = await db.questions.insert_many(additional_questions_2)
    print(f"Added {len(result.inserted_ids)} new questions")
    
    total = await db.questions.count_documents({})
    print(f"Total questions in database: {total}")

if __name__ == "__main__":
    asyncio.run(add_questions())
