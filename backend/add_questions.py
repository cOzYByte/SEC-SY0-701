"""
Additional CompTIA Security+ SY0-701 Questions
Run this script to add more questions to the database
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

additional_questions = [
    # ============ DOMAIN 1: General Security Concepts (More Questions) ============
    {
        "domain": 1,
        "domain_name": "General Security Concepts",
        "question": "Which cryptographic concept ensures that a message has not been altered during transmission?",
        "options": [
            {"id": "a", "text": "Confidentiality"},
            {"id": "b", "text": "Integrity"},
            {"id": "c", "text": "Availability"},
            {"id": "d", "text": "Non-repudiation"}
        ],
        "correct_answer": "b",
        "explanation": "Integrity ensures that data has not been modified or tampered with during transmission or storage. Hash functions and digital signatures are commonly used to verify integrity."
    },
    {
        "domain": 1,
        "domain_name": "General Security Concepts",
        "question": "What is the purpose of salting a password before hashing?",
        "options": [
            {"id": "a", "text": "To encrypt the password"},
            {"id": "b", "text": "To prevent rainbow table attacks"},
            {"id": "c", "text": "To make the password longer"},
            {"id": "d", "text": "To compress the password"}
        ],
        "correct_answer": "b",
        "explanation": "Salting adds random data to a password before hashing, making each hash unique even for identical passwords. This defeats rainbow table attacks and makes password cracking more difficult."
    },
    {
        "domain": 1,
        "domain_name": "General Security Concepts",
        "question": "Which type of access control uses labels like 'Top Secret' and 'Confidential'?",
        "options": [
            {"id": "a", "text": "Discretionary Access Control (DAC)"},
            {"id": "b", "text": "Mandatory Access Control (MAC)"},
            {"id": "c", "text": "Role-Based Access Control (RBAC)"},
            {"id": "d", "text": "Attribute-Based Access Control (ABAC)"}
        ],
        "correct_answer": "b",
        "explanation": "Mandatory Access Control (MAC) uses security labels assigned by administrators. Users cannot change these labels. It's commonly used in military and government environments."
    },
    {
        "domain": 1,
        "domain_name": "General Security Concepts",
        "question": "What does AAA stand for in security?",
        "options": [
            {"id": "a", "text": "Access, Audit, Authorize"},
            {"id": "b", "text": "Authentication, Authorization, Accounting"},
            {"id": "c", "text": "Authenticate, Access, Analyze"},
            {"id": "d", "text": "Authorize, Audit, Access"}
        ],
        "correct_answer": "b",
        "explanation": "AAA stands for Authentication (verifying identity), Authorization (determining access rights), and Accounting (tracking user actions). It's a framework for controlling access to resources."
    },
    {
        "domain": 1,
        "domain_name": "General Security Concepts",
        "question": "Which symmetric encryption algorithm is considered the current standard?",
        "options": [
            {"id": "a", "text": "DES"},
            {"id": "b", "text": "3DES"},
            {"id": "c", "text": "AES"},
            {"id": "d", "text": "RC4"}
        ],
        "correct_answer": "c",
        "explanation": "AES (Advanced Encryption Standard) is the current symmetric encryption standard, supporting key sizes of 128, 192, and 256 bits. DES and 3DES are considered legacy algorithms."
    },
    {
        "domain": 1,
        "domain_name": "General Security Concepts",
        "question": "What is the primary difference between symmetric and asymmetric encryption?",
        "options": [
            {"id": "a", "text": "Symmetric is faster but uses the same key for encryption and decryption"},
            {"id": "b", "text": "Asymmetric uses the same key for both operations"},
            {"id": "c", "text": "Symmetric encryption cannot be used for large files"},
            {"id": "d", "text": "Asymmetric encryption is always faster"}
        ],
        "correct_answer": "a",
        "explanation": "Symmetric encryption uses a single shared key for both encryption and decryption, making it faster. Asymmetric uses a key pair (public/private) and is slower but solves the key distribution problem."
    },
    {
        "domain": 1,
        "domain_name": "General Security Concepts",
        "question": "Which protocol is used to securely exchange keys over an insecure channel?",
        "options": [
            {"id": "a", "text": "RSA"},
            {"id": "b", "text": "Diffie-Hellman"},
            {"id": "c", "text": "AES"},
            {"id": "d", "text": "SHA-256"}
        ],
        "correct_answer": "b",
        "explanation": "Diffie-Hellman is a key exchange protocol that allows two parties to establish a shared secret over an insecure channel. It's widely used in TLS/SSL and VPN connections."
    },
    {
        "domain": 1,
        "domain_name": "General Security Concepts",
        "question": "What is a digital certificate primarily used for?",
        "options": [
            {"id": "a", "text": "Encrypting data at rest"},
            {"id": "b", "text": "Binding a public key to an identity"},
            {"id": "c", "text": "Storing passwords securely"},
            {"id": "d", "text": "Compressing network traffic"}
        ],
        "correct_answer": "b",
        "explanation": "A digital certificate binds a public key to an identity (person, organization, or device). It's issued by a Certificate Authority (CA) and enables secure communications and authentication."
    },
    {
        "domain": 1,
        "domain_name": "General Security Concepts",
        "question": "What is the purpose of a Certificate Revocation List (CRL)?",
        "options": [
            {"id": "a", "text": "To list all valid certificates"},
            {"id": "b", "text": "To list certificates that are no longer trusted"},
            {"id": "c", "text": "To encrypt certificate data"},
            {"id": "d", "text": "To renew expired certificates"}
        ],
        "correct_answer": "b",
        "explanation": "A CRL contains a list of certificates that have been revoked before their expiration date. Systems check the CRL to ensure a certificate hasn't been compromised or invalidated."
    },
    {
        "domain": 1,
        "domain_name": "General Security Concepts",
        "question": "Which hashing algorithm is recommended for new implementations?",
        "options": [
            {"id": "a", "text": "MD5"},
            {"id": "b", "text": "SHA-1"},
            {"id": "c", "text": "SHA-256"},
            {"id": "d", "text": "NTLM"}
        ],
        "correct_answer": "c",
        "explanation": "SHA-256 (part of SHA-2 family) is recommended for new implementations. MD5 and SHA-1 are considered cryptographically broken and should not be used for security purposes."
    },
    {
        "domain": 1,
        "domain_name": "General Security Concepts",
        "question": "What is Perfect Forward Secrecy (PFS)?",
        "options": [
            {"id": "a", "text": "Encryption that never expires"},
            {"id": "b", "text": "Session keys that can't decrypt past sessions if compromised"},
            {"id": "c", "text": "A firewall configuration"},
            {"id": "d", "text": "A type of antivirus software"}
        ],
        "correct_answer": "b",
        "explanation": "Perfect Forward Secrecy ensures that session keys cannot be compromised even if the server's private key is compromised later. Each session uses unique keys that are discarded after use."
    },
    {
        "domain": 1,
        "domain_name": "General Security Concepts",
        "question": "What type of authentication uses something you have, know, and are?",
        "options": [
            {"id": "a", "text": "Single-factor authentication"},
            {"id": "b", "text": "Two-factor authentication"},
            {"id": "c", "text": "Multi-factor authentication"},
            {"id": "d", "text": "Passwordless authentication"}
        ],
        "correct_answer": "c",
        "explanation": "Multi-factor authentication (MFA) uses two or more different authentication factors: something you know (password), something you have (token), and something you are (biometric)."
    },
    # ============ DOMAIN 2: Threats, Vulnerabilities, and Mitigations (More Questions) ============
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What type of attack involves sending specially crafted input to overflow a program's memory buffer?",
        "options": [
            {"id": "a", "text": "SQL injection"},
            {"id": "b", "text": "Buffer overflow"},
            {"id": "c", "text": "Cross-site scripting"},
            {"id": "d", "text": "Directory traversal"}
        ],
        "correct_answer": "b",
        "explanation": "Buffer overflow attacks send more data than a buffer can hold, potentially overwriting adjacent memory and allowing arbitrary code execution. Input validation and safe programming practices prevent this."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is a logic bomb?",
        "options": [
            {"id": "a", "text": "A type of firewall"},
            {"id": "b", "text": "Malicious code that triggers on a specific condition"},
            {"id": "c", "text": "A network scanning tool"},
            {"id": "d", "text": "An encryption algorithm"}
        ],
        "correct_answer": "b",
        "explanation": "A logic bomb is malicious code that remains dormant until triggered by a specific condition, such as a date, time, or user action. It's often planted by insiders."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "Which attack technique captures network traffic to steal credentials?",
        "options": [
            {"id": "a", "text": "Phishing"},
            {"id": "b", "text": "Packet sniffing"},
            {"id": "c", "text": "Brute force"},
            {"id": "d", "text": "Social engineering"}
        ],
        "correct_answer": "b",
        "explanation": "Packet sniffing captures network traffic using tools like Wireshark. Unencrypted credentials can be stolen this way. Using encrypted protocols (HTTPS, SSH) mitigates this risk."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is a supply chain attack?",
        "options": [
            {"id": "a", "text": "Attacking shipping companies"},
            {"id": "b", "text": "Compromising software or hardware before delivery to target"},
            {"id": "c", "text": "Stealing inventory data"},
            {"id": "d", "text": "Disrupting logistics networks"}
        ],
        "correct_answer": "b",
        "explanation": "Supply chain attacks compromise software, hardware, or services before they reach the target organization. The SolarWinds attack is a notable example where malicious code was inserted into software updates."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is typosquatting?",
        "options": [
            {"id": "a", "text": "A typing speed test"},
            {"id": "b", "text": "Registering misspelled domain names to capture traffic"},
            {"id": "c", "text": "A keyboard logging technique"},
            {"id": "d", "text": "A password cracking method"}
        ],
        "correct_answer": "b",
        "explanation": "Typosquatting registers domain names similar to legitimate ones (e.g., goggle.com instead of google.com) to capture users who mistype URLs, often for phishing or malware distribution."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What distinguishes a worm from a virus?",
        "options": [
            {"id": "a", "text": "Worms require user interaction to spread"},
            {"id": "b", "text": "Worms can self-replicate without host files"},
            {"id": "c", "text": "Viruses spread faster than worms"},
            {"id": "d", "text": "Worms only affect mobile devices"}
        ],
        "correct_answer": "b",
        "explanation": "Worms are self-replicating malware that spread across networks without requiring a host file or user interaction. Viruses attach to files and require user action to spread."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is a fileless malware attack?",
        "options": [
            {"id": "a", "text": "Malware that deletes all files"},
            {"id": "b", "text": "Malware that operates entirely in memory"},
            {"id": "c", "text": "Malware that compresses files"},
            {"id": "d", "text": "Malware spread through file sharing"}
        ],
        "correct_answer": "b",
        "explanation": "Fileless malware operates in memory without writing to disk, making it harder to detect with traditional antivirus. It often uses legitimate system tools like PowerShell."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is an Advanced Persistent Threat (APT)?",
        "options": [
            {"id": "a", "text": "A one-time attack"},
            {"id": "b", "text": "A prolonged, targeted attack by sophisticated threat actors"},
            {"id": "c", "text": "A type of antivirus software"},
            {"id": "d", "text": "A network protocol"}
        ],
        "correct_answer": "b",
        "explanation": "APTs are prolonged, targeted attacks typically conducted by nation-states or organized groups. They use multiple attack vectors and maintain persistence in the target network over extended periods."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is DNS poisoning?",
        "options": [
            {"id": "a", "text": "Overloading DNS servers"},
            {"id": "b", "text": "Corrupting DNS cache to redirect users to malicious sites"},
            {"id": "c", "text": "Encrypting DNS queries"},
            {"id": "d", "text": "Blocking DNS traffic"}
        ],
        "correct_answer": "b",
        "explanation": "DNS poisoning (cache poisoning) corrupts DNS resolver caches to redirect users to malicious websites. DNSSEC helps prevent this by digitally signing DNS records."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is ARP spoofing used for?",
        "options": [
            {"id": "a", "text": "Encrypting network traffic"},
            {"id": "b", "text": "Intercepting traffic by associating attacker's MAC with victim's IP"},
            {"id": "c", "text": "Speeding up network connections"},
            {"id": "d", "text": "Blocking malware"}
        ],
        "correct_answer": "b",
        "explanation": "ARP spoofing sends fake ARP messages to link the attacker's MAC address with a legitimate IP, allowing interception of traffic (man-in-the-middle). Dynamic ARP inspection prevents this."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is a drive-by download?",
        "options": [
            {"id": "a", "text": "Downloading while driving"},
            {"id": "b", "text": "Malware downloaded without user consent when visiting a website"},
            {"id": "c", "text": "A fast download method"},
            {"id": "d", "text": "Downloading from removable drives"}
        ],
        "correct_answer": "b",
        "explanation": "Drive-by downloads install malware automatically when users visit compromised websites, exploiting browser or plugin vulnerabilities without requiring user clicks or consent."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is credential harvesting?",
        "options": [
            {"id": "a", "text": "Collecting login credentials through deceptive means"},
            {"id": "b", "text": "Creating strong passwords"},
            {"id": "c", "text": "Resetting forgotten passwords"},
            {"id": "d", "text": "Encrypting credentials"}
        ],
        "correct_answer": "a",
        "explanation": "Credential harvesting collects usernames and passwords through phishing sites, keyloggers, or social engineering. These credentials are often sold or used for account takeover."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is a birthday attack?",
        "options": [
            {"id": "a", "text": "Attacking on someone's birthday"},
            {"id": "b", "text": "Exploiting hash collision probability"},
            {"id": "c", "text": "Guessing passwords based on birthdates"},
            {"id": "d", "text": "A type of DDoS attack"}
        ],
        "correct_answer": "b",
        "explanation": "A birthday attack exploits the mathematics of the birthday problem to find hash collisions faster than brute force. It's used against weak hash functions to forge digital signatures."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is pretexting in social engineering?",
        "options": [
            {"id": "a", "text": "Sending text messages"},
            {"id": "b", "text": "Creating a fabricated scenario to extract information"},
            {"id": "c", "text": "Writing pre-formatted texts"},
            {"id": "d", "text": "Testing security controls"}
        ],
        "correct_answer": "b",
        "explanation": "Pretexting creates a fabricated scenario or false identity to manipulate victims into providing information. For example, pretending to be IT support to obtain passwords."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is a pass-the-hash attack?",
        "options": [
            {"id": "a", "text": "Sharing passwords via hash tags"},
            {"id": "b", "text": "Using captured password hashes to authenticate without cracking"},
            {"id": "c", "text": "Hashing passwords for storage"},
            {"id": "d", "text": "A type of encryption"}
        ],
        "correct_answer": "b",
        "explanation": "Pass-the-hash uses captured NTLM or other password hashes to authenticate to systems without needing to crack the actual password. It exploits authentication protocols."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is an injection attack?",
        "options": [
            {"id": "a", "text": "Physically injecting hardware"},
            {"id": "b", "text": "Inserting malicious code through user input fields"},
            {"id": "c", "text": "Injecting network packets"},
            {"id": "d", "text": "A type of vaccine"}
        ],
        "correct_answer": "b",
        "explanation": "Injection attacks insert malicious code through input fields that are processed by interpreters. SQL injection, command injection, and LDAP injection are common types."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is session hijacking?",
        "options": [
            {"id": "a", "text": "Stealing a valid session token to impersonate a user"},
            {"id": "b", "text": "Ending user sessions"},
            {"id": "c", "text": "Creating new sessions"},
            {"id": "d", "text": "Session timeout configuration"}
        ],
        "correct_answer": "a",
        "explanation": "Session hijacking steals or predicts valid session tokens to take over authenticated user sessions. Using HTTPS, secure cookies, and session regeneration helps prevent this."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is a Denial of Service (DoS) amplification attack?",
        "options": [
            {"id": "a", "text": "Making the attack louder"},
            {"id": "b", "text": "Using third-party servers to multiply attack traffic"},
            {"id": "c", "text": "Amplifying radio signals"},
            {"id": "d", "text": "Increasing bandwidth"}
        ],
        "correct_answer": "b",
        "explanation": "Amplification attacks use third-party servers (like DNS or NTP) to multiply attack traffic. A small request generates a much larger response directed at the victim."
    },
    # ============ DOMAIN 3: Security Architecture (More Questions) ============
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is the purpose of a jump server (bastion host)?",
        "options": [
            {"id": "a", "text": "To increase network speed"},
            {"id": "b", "text": "To provide secure access to internal networks"},
            {"id": "c", "text": "To store backups"},
            {"id": "d", "text": "To host public websites"}
        ],
        "correct_answer": "b",
        "explanation": "A jump server (bastion host) is a hardened system that provides secure access to internal networks. Administrators connect to it first, then to internal systems, creating an audit trail."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is a WAF (Web Application Firewall)?",
        "options": [
            {"id": "a", "text": "A wireless access firewall"},
            {"id": "b", "text": "A firewall that filters HTTP/HTTPS traffic for web attacks"},
            {"id": "c", "text": "A wide area network firewall"},
            {"id": "d", "text": "A Windows application firewall"}
        ],
        "correct_answer": "b",
        "explanation": "A WAF filters HTTP/HTTPS traffic to protect web applications from attacks like SQL injection, XSS, and CSRF. It operates at Layer 7 (application layer) of the OSI model."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is the difference between HIDS and NIDS?",
        "options": [
            {"id": "a", "text": "HIDS monitors host systems; NIDS monitors network traffic"},
            {"id": "b", "text": "HIDS is newer than NIDS"},
            {"id": "c", "text": "NIDS monitors hosts; HIDS monitors networks"},
            {"id": "d", "text": "They are the same thing"}
        ],
        "correct_answer": "a",
        "explanation": "HIDS (Host-based IDS) monitors individual host systems for suspicious activity. NIDS (Network-based IDS) monitors network traffic. Both are important for comprehensive detection."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is SASE (Secure Access Service Edge)?",
        "options": [
            {"id": "a", "text": "A type of VPN"},
            {"id": "b", "text": "Cloud-delivered convergence of network and security services"},
            {"id": "c", "text": "A firewall brand"},
            {"id": "d", "text": "A type of encryption"}
        ],
        "correct_answer": "b",
        "explanation": "SASE combines network services (SD-WAN) with security services (SWG, CASB, ZTNA, FWaaS) delivered from the cloud, providing secure access regardless of user location."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is containerization in security?",
        "options": [
            {"id": "a", "text": "Shipping security equipment"},
            {"id": "b", "text": "Isolating applications in lightweight virtual environments"},
            {"id": "c", "text": "Storing data in containers"},
            {"id": "d", "text": "A type of encryption"}
        ],
        "correct_answer": "b",
        "explanation": "Containerization (like Docker) isolates applications in lightweight environments sharing the host OS kernel. It provides isolation, portability, and efficient resource usage."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is infrastructure as code (IaC)?",
        "options": [
            {"id": "a", "text": "Writing code for buildings"},
            {"id": "b", "text": "Managing infrastructure through machine-readable definition files"},
            {"id": "c", "text": "Physical infrastructure management"},
            {"id": "d", "text": "A programming language"}
        ],
        "correct_answer": "b",
        "explanation": "IaC manages and provisions infrastructure through code/configuration files rather than manual processes. This enables version control, consistency, and automated security compliance."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is the purpose of a reverse proxy?",
        "options": [
            {"id": "a", "text": "To speed up outbound traffic"},
            {"id": "b", "text": "To protect backend servers by handling client requests"},
            {"id": "c", "text": "To reverse network direction"},
            {"id": "d", "text": "To block all traffic"}
        ],
        "correct_answer": "b",
        "explanation": "A reverse proxy sits in front of backend servers, handling client requests, providing load balancing, SSL termination, caching, and hiding internal server details."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is network address translation (NAT)?",
        "options": [
            {"id": "a", "text": "Translating network names"},
            {"id": "b", "text": "Mapping private IP addresses to public IP addresses"},
            {"id": "c", "text": "A type of encryption"},
            {"id": "d", "text": "A routing protocol"}
        ],
        "correct_answer": "b",
        "explanation": "NAT maps private IP addresses to public IP addresses, allowing multiple devices to share a single public IP. It provides some security by hiding internal network structure."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is a stateful firewall?",
        "options": [
            {"id": "a", "text": "A firewall in a specific state"},
            {"id": "b", "text": "A firewall that tracks connection states"},
            {"id": "c", "text": "A firewall for state governments"},
            {"id": "d", "text": "A firewall that only blocks traffic"}
        ],
        "correct_answer": "b",
        "explanation": "A stateful firewall tracks the state of network connections (TCP handshake, etc.) and makes filtering decisions based on connection context, not just individual packets."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is the principle behind a honeypot?",
        "options": [
            {"id": "a", "text": "Attracting bees"},
            {"id": "b", "text": "Attracting attackers to a decoy system for analysis"},
            {"id": "c", "text": "Storing honey data"},
            {"id": "d", "text": "A type of encryption"}
        ],
        "correct_answer": "b",
        "explanation": "A honeypot is a decoy system designed to attract attackers, allowing security teams to study attack techniques and detect intrusions without risking production systems."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is a VPN concentrator?",
        "options": [
            {"id": "a", "text": "A device that manages multiple VPN connections"},
            {"id": "b", "text": "A tool to focus VPN signals"},
            {"id": "c", "text": "A type of router"},
            {"id": "d", "text": "A VPN client"}
        ],
        "correct_answer": "a",
        "explanation": "A VPN concentrator is a network device that manages multiple VPN tunnels, handling encryption/decryption and providing secure remote access for many users simultaneously."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is the purpose of 802.1X?",
        "options": [
            {"id": "a", "text": "Wireless encryption"},
            {"id": "b", "text": "Port-based network access control"},
            {"id": "c", "text": "Network speed specification"},
            {"id": "d", "text": "A routing protocol"}
        ],
        "correct_answer": "b",
        "explanation": "802.1X is an IEEE standard for port-based network access control. It authenticates devices before granting network access, commonly used with RADIUS servers."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is a load balancer?",
        "options": [
            {"id": "a", "text": "A device that distributes traffic across multiple servers"},
            {"id": "b", "text": "A tool to measure weight"},
            {"id": "c", "text": "A type of firewall"},
            {"id": "d", "text": "A backup server"}
        ],
        "correct_answer": "a",
        "explanation": "A load balancer distributes network traffic across multiple servers to ensure reliability, availability, and optimal resource utilization. It can also provide SSL termination."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is software-defined networking (SDN)?",
        "options": [
            {"id": "a", "text": "Networks built with software"},
            {"id": "b", "text": "Separating network control plane from data plane"},
            {"id": "c", "text": "A type of firewall"},
            {"id": "d", "text": "Virtual machines"}
        ],
        "correct_answer": "b",
        "explanation": "SDN separates the network control plane from the data plane, allowing centralized, programmable network management. This enables automation and dynamic security policies."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is air gapping?",
        "options": [
            {"id": "a", "text": "Creating gaps in HVAC systems"},
            {"id": "b", "text": "Physically isolating a network from other networks"},
            {"id": "c", "text": "A wireless protocol"},
            {"id": "d", "text": "A type of encryption"}
        ],
        "correct_answer": "b",
        "explanation": "Air gapping physically isolates a secure network from unsecured networks like the internet. It's used for highly sensitive systems but doesn't protect against all threats (USB drives, etc.)."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is data loss prevention (DLP)?",
        "options": [
            {"id": "a", "text": "Recovering lost data"},
            {"id": "b", "text": "Preventing unauthorized data exfiltration"},
            {"id": "c", "text": "Data backup solution"},
            {"id": "d", "text": "A type of encryption"}
        ],
        "correct_answer": "b",
        "explanation": "DLP solutions detect and prevent unauthorized transmission of sensitive data outside the organization. They can monitor endpoints, networks, and cloud services."
    },
    # ============ DOMAIN 4: Security Operations (More Questions) ============
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is the purpose of a security operations center (SOC)?",
        "options": [
            {"id": "a", "text": "Physical security of buildings"},
            {"id": "b", "text": "Centralized monitoring and response to security events"},
            {"id": "c", "text": "Software development"},
            {"id": "d", "text": "Network installation"}
        ],
        "correct_answer": "b",
        "explanation": "A SOC is a centralized facility where security analysts monitor, detect, analyze, and respond to security incidents using a combination of technology solutions and processes."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is the order of volatility in digital forensics?",
        "options": [
            {"id": "a", "text": "Hard drive, RAM, network connections, CPU cache"},
            {"id": "b", "text": "CPU registers, RAM, swap space, hard drive"},
            {"id": "c", "text": "Hard drive, RAM, CPU registers, network"},
            {"id": "d", "text": "Network, hard drive, RAM, CPU"}
        ],
        "correct_answer": "b",
        "explanation": "Order of volatility (most to least volatile): CPU registers/cache, RAM, swap space, hard drive, remote logs, physical media. Collect most volatile evidence first."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is a write blocker used for?",
        "options": [
            {"id": "a", "text": "Preventing writing to storage during forensic acquisition"},
            {"id": "b", "text": "Blocking malicious writes"},
            {"id": "c", "text": "Encrypting data"},
            {"id": "d", "text": "Speeding up writes"}
        ],
        "correct_answer": "a",
        "explanation": "A write blocker prevents any modification to storage media during forensic acquisition, ensuring evidence integrity. It's essential for maintaining chain of custody."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What does MTTR stand for?",
        "options": [
            {"id": "a", "text": "Maximum Time To Respond"},
            {"id": "b", "text": "Mean Time To Repair/Recover"},
            {"id": "c", "text": "Minimum Technical Training Required"},
            {"id": "d", "text": "Managed Threat Testing Report"}
        ],
        "correct_answer": "b",
        "explanation": "MTTR (Mean Time To Repair/Recover) measures the average time to restore a system after a failure. It's a key metric for measuring incident response effectiveness."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is the purpose of network flow analysis?",
        "options": [
            {"id": "a", "text": "Measuring water flow"},
            {"id": "b", "text": "Analyzing metadata about network traffic patterns"},
            {"id": "c", "text": "Blocking network traffic"},
            {"id": "d", "text": "Encrypting network data"}
        ],
        "correct_answer": "b",
        "explanation": "Network flow analysis examines metadata about network connections (source, destination, ports, duration, volume) to detect anomalies and security threats without inspecting packet contents."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is the difference between a hot site and a cold site?",
        "options": [
            {"id": "a", "text": "Temperature differences"},
            {"id": "b", "text": "Hot site has systems ready; cold site has only infrastructure"},
            {"id": "c", "text": "Hot site is outdoors; cold site is indoors"},
            {"id": "d", "text": "They are the same"}
        ],
        "correct_answer": "b",
        "explanation": "A hot site has fully operational duplicate systems ready for immediate failover. A cold site has basic infrastructure (power, cooling) but requires equipment installation before use."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is a runbook?",
        "options": [
            {"id": "a", "text": "A book for runners"},
            {"id": "b", "text": "Documented procedures for routine operations"},
            {"id": "c", "text": "A type of malware"},
            {"id": "d", "text": "A network protocol"}
        ],
        "correct_answer": "b",
        "explanation": "A runbook contains documented procedures for routine operations and incident response. It ensures consistent, repeatable processes and enables automation of common tasks."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is the purpose of a CSIRT?",
        "options": [
            {"id": "a", "text": "Customer service improvement"},
            {"id": "b", "text": "Computer Security Incident Response Team"},
            {"id": "c", "text": "Cloud storage integration"},
            {"id": "d", "text": "Certificate signing requests"}
        ],
        "correct_answer": "b",
        "explanation": "A CSIRT (Computer Security Incident Response Team) is a group responsible for receiving, reviewing, and responding to computer security incidents. They coordinate incident response activities."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is threat intelligence?",
        "options": [
            {"id": "a", "text": "Intelligence about physical threats"},
            {"id": "b", "text": "Evidence-based knowledge about cyber threats"},
            {"id": "c", "text": "IQ testing for threats"},
            {"id": "d", "text": "A type of firewall"}
        ],
        "correct_answer": "b",
        "explanation": "Threat intelligence is evidence-based knowledge about existing or emerging threats, including indicators of compromise (IoCs), attacker tactics, techniques, and procedures (TTPs)."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is a playbook in incident response?",
        "options": [
            {"id": "a", "text": "A book of games"},
            {"id": "b", "text": "Predefined steps for handling specific incident types"},
            {"id": "c", "text": "A training manual"},
            {"id": "d", "text": "A network diagram"}
        ],
        "correct_answer": "b",
        "explanation": "An incident response playbook contains predefined steps for handling specific types of security incidents. It ensures consistent, efficient response and can be automated through SOAR platforms."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is the purpose of patch management?",
        "options": [
            {"id": "a", "text": "Managing fabric patches"},
            {"id": "b", "text": "Systematically applying software updates to fix vulnerabilities"},
            {"id": "c", "text": "Network cable management"},
            {"id": "d", "text": "Database management"}
        ],
        "correct_answer": "b",
        "explanation": "Patch management is the process of identifying, acquiring, testing, and installing software updates to fix security vulnerabilities and bugs in a systematic manner."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is data carving in forensics?",
        "options": [
            {"id": "a", "text": "Physical data destruction"},
            {"id": "b", "text": "Recovering files from raw data without file system metadata"},
            {"id": "c", "text": "Encrypting data"},
            {"id": "d", "text": "Data compression"}
        ],
        "correct_answer": "b",
        "explanation": "Data carving recovers files from raw data (unallocated space) without relying on file system metadata. It's used to recover deleted files based on file signatures and headers."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is the purpose of retention policies?",
        "options": [
            {"id": "a", "text": "Retaining employees"},
            {"id": "b", "text": "Defining how long data should be kept before deletion"},
            {"id": "c", "text": "Memory management"},
            {"id": "d", "text": "Network bandwidth allocation"}
        ],
        "correct_answer": "b",
        "explanation": "Retention policies define how long different types of data should be kept before secure disposal. They balance legal/compliance requirements with storage costs and privacy concerns."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is a sandbox in security?",
        "options": [
            {"id": "a", "text": "A children's play area"},
            {"id": "b", "text": "An isolated environment for safely executing untrusted code"},
            {"id": "c", "text": "A type of firewall"},
            {"id": "d", "text": "A backup solution"}
        ],
        "correct_answer": "b",
        "explanation": "A sandbox is an isolated environment where untrusted or suspicious code can be executed safely without affecting the host system. It's used for malware analysis and application testing."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is configuration management?",
        "options": [
            {"id": "a", "text": "Managing office configurations"},
            {"id": "b", "text": "Tracking and controlling changes to system configurations"},
            {"id": "c", "text": "Network speed configuration"},
            {"id": "d", "text": "Email configuration"}
        ],
        "correct_answer": "b",
        "explanation": "Configuration management tracks and controls changes to system configurations, ensuring systems are configured securely and consistently, and changes are documented."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is the MITRE ATT&CK framework?",
        "options": [
            {"id": "a", "text": "A type of attack"},
            {"id": "b", "text": "A knowledge base of adversary tactics and techniques"},
            {"id": "c", "text": "A firewall product"},
            {"id": "d", "text": "An encryption standard"}
        ],
        "correct_answer": "b",
        "explanation": "MITRE ATT&CK is a knowledge base of adversary tactics, techniques, and procedures (TTPs) based on real-world observations. It helps organizations understand and defend against threats."
    },
    # ============ DOMAIN 5: Security Program Management and Oversight (More Questions) ============
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is the purpose of a security framework?",
        "options": [
            {"id": "a", "text": "A physical frame for security cameras"},
            {"id": "b", "text": "A structured approach to implementing security controls"},
            {"id": "c", "text": "A type of firewall"},
            {"id": "d", "text": "A programming language"}
        ],
        "correct_answer": "b",
        "explanation": "A security framework provides a structured approach to implementing and managing security controls. Examples include NIST CSF, ISO 27001, and CIS Controls."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is HIPAA primarily concerned with?",
        "options": [
            {"id": "a", "text": "Financial data protection"},
            {"id": "b", "text": "Protected health information (PHI)"},
            {"id": "c", "text": "Credit card security"},
            {"id": "d", "text": "Government classified information"}
        ],
        "correct_answer": "b",
        "explanation": "HIPAA (Health Insurance Portability and Accountability Act) protects the privacy and security of Protected Health Information (PHI) in the healthcare industry."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is the formula for calculating Annual Loss Expectancy (ALE)?",
        "options": [
            {"id": "a", "text": "ALE = Asset Value × Risk Factor"},
            {"id": "b", "text": "ALE = Single Loss Expectancy × Annual Rate of Occurrence"},
            {"id": "c", "text": "ALE = Threat × Vulnerability"},
            {"id": "d", "text": "ALE = Impact / Probability"}
        ],
        "correct_answer": "b",
        "explanation": "ALE = SLE × ARO. Single Loss Expectancy (SLE) is the expected monetary loss from a single incident. Annual Rate of Occurrence (ARO) is how often the incident is expected to occur per year."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is the purpose of a penetration test report?",
        "options": [
            {"id": "a", "text": "To describe network architecture"},
            {"id": "b", "text": "To document vulnerabilities found and remediation recommendations"},
            {"id": "c", "text": "To list employee names"},
            {"id": "d", "text": "To track inventory"}
        ],
        "correct_answer": "b",
        "explanation": "A penetration test report documents vulnerabilities discovered, exploitation methods used, potential impact, and remediation recommendations to help organizations improve security."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is risk acceptance?",
        "options": [
            {"id": "a", "text": "Ignoring all risks"},
            {"id": "b", "text": "Acknowledging a risk and deciding not to take action"},
            {"id": "c", "text": "Accepting a job offer"},
            {"id": "d", "text": "A type of insurance"}
        ],
        "correct_answer": "b",
        "explanation": "Risk acceptance means acknowledging a risk exists but deciding the cost of mitigation outweighs the potential impact. The decision should be documented and approved by management."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is due diligence in security?",
        "options": [
            {"id": "a", "text": "Paying bills on time"},
            {"id": "b", "text": "Researching and understanding risks before making decisions"},
            {"id": "c", "text": "A legal requirement"},
            {"id": "d", "text": "Employee training"}
        ],
        "correct_answer": "b",
        "explanation": "Due diligence is the process of researching and understanding risks before making decisions or entering agreements. Due care is taking reasonable steps to protect against known risks."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is a Service Level Agreement (SLA)?",
        "options": [
            {"id": "a", "text": "A sales agreement"},
            {"id": "b", "text": "A contract defining expected service levels"},
            {"id": "c", "text": "A security policy"},
            {"id": "d", "text": "A type of encryption"}
        ],
        "correct_answer": "b",
        "explanation": "An SLA is a contract between a service provider and customer that defines expected service levels, performance metrics, responsibilities, and penalties for non-compliance."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is the purpose of a privacy impact assessment (PIA)?",
        "options": [
            {"id": "a", "text": "To assess network performance"},
            {"id": "b", "text": "To identify and mitigate privacy risks"},
            {"id": "c", "text": "To test passwords"},
            {"id": "d", "text": "To evaluate physical security"}
        ],
        "correct_answer": "b",
        "explanation": "A PIA identifies and evaluates privacy risks associated with collecting, using, and sharing personal information, and recommends measures to mitigate those risks."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is SOC 2 certification?",
        "options": [
            {"id": "a", "text": "Security Operations Center Level 2"},
            {"id": "b", "text": "An audit report on security controls for service organizations"},
            {"id": "c", "text": "A type of firewall"},
            {"id": "d", "text": "A network protocol"}
        ],
        "correct_answer": "b",
        "explanation": "SOC 2 is an audit report that evaluates a service organization's controls related to security, availability, processing integrity, confidentiality, and privacy (Trust Service Criteria)."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is the purpose of a master service agreement (MSA)?",
        "options": [
            {"id": "a", "text": "To define terms for ongoing business relationships"},
            {"id": "b", "text": "To master security skills"},
            {"id": "c", "text": "A type of encryption"},
            {"id": "d", "text": "A backup agreement"}
        ],
        "correct_answer": "a",
        "explanation": "An MSA establishes terms and conditions for an ongoing business relationship, covering intellectual property, liability, confidentiality, and security requirements."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is data classification?",
        "options": [
            {"id": "a", "text": "Sorting data alphabetically"},
            {"id": "b", "text": "Categorizing data based on sensitivity and protection requirements"},
            {"id": "c", "text": "Deleting unnecessary data"},
            {"id": "d", "text": "Encrypting all data"}
        ],
        "correct_answer": "b",
        "explanation": "Data classification categorizes data based on its sensitivity level (public, internal, confidential, restricted) to determine appropriate protection measures and handling procedures."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is a memorandum of understanding (MOU)?",
        "options": [
            {"id": "a", "text": "A legally binding contract"},
            {"id": "b", "text": "A document expressing mutual intent between parties"},
            {"id": "c", "text": "A type of encryption"},
            {"id": "d", "text": "A security policy"}
        ],
        "correct_answer": "b",
        "explanation": "An MOU expresses mutual intent and understanding between parties. It's typically not legally binding like a contract but documents agreed-upon terms and expectations."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is the purpose of security metrics?",
        "options": [
            {"id": "a", "text": "To measure physical distances"},
            {"id": "b", "text": "To quantify security effectiveness and track progress"},
            {"id": "c", "text": "To encrypt data"},
            {"id": "d", "text": "To create passwords"}
        ],
        "correct_answer": "b",
        "explanation": "Security metrics quantify the effectiveness of security controls and programs, track progress toward goals, and help communicate security status to stakeholders."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is vendor risk management?",
        "options": [
            {"id": "a", "text": "Selling to vendors"},
            {"id": "b", "text": "Assessing and managing risks from third-party vendors"},
            {"id": "c", "text": "Vendor pricing"},
            {"id": "d", "text": "A type of insurance"}
        ],
        "correct_answer": "b",
        "explanation": "Vendor risk management assesses and manages security risks introduced by third-party vendors, including evaluating their security practices and monitoring their compliance."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is the NIST Cybersecurity Framework?",
        "options": [
            {"id": "a", "text": "A type of firewall"},
            {"id": "b", "text": "A voluntary framework for managing cybersecurity risk"},
            {"id": "c", "text": "A government agency"},
            {"id": "d", "text": "An encryption standard"}
        ],
        "correct_answer": "b",
        "explanation": "The NIST CSF is a voluntary framework with five functions (Identify, Protect, Detect, Respond, Recover) to help organizations manage and reduce cybersecurity risk."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is change control?",
        "options": [
            {"id": "a", "text": "Controlling currency exchange"},
            {"id": "b", "text": "A formal process for managing changes to systems"},
            {"id": "c", "text": "Changing passwords"},
            {"id": "d", "text": "A type of encryption"}
        ],
        "correct_answer": "b",
        "explanation": "Change control is a formal process for proposing, reviewing, approving, and implementing changes to systems. It minimizes risk and ensures changes are documented and tested."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is the purpose of an interconnection security agreement (ISA)?",
        "options": [
            {"id": "a", "text": "Internet service agreement"},
            {"id": "b", "text": "Documenting security requirements for connecting networks"},
            {"id": "c", "text": "A type of VPN"},
            {"id": "d", "text": "An encryption standard"}
        ],
        "correct_answer": "b",
        "explanation": "An ISA documents security requirements, responsibilities, and technical details for connecting two organizations' networks, ensuring both parties maintain adequate security."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is a business continuity plan (BCP)?",
        "options": [
            {"id": "a", "text": "A marketing plan"},
            {"id": "b", "text": "A plan to maintain operations during and after a disaster"},
            {"id": "c", "text": "A financial plan"},
            {"id": "d", "text": "An employee handbook"}
        ],
        "correct_answer": "b",
        "explanation": "A BCP outlines procedures to maintain critical business operations during and after a disaster. It includes disaster recovery, emergency response, and crisis communication plans."
    },
    # Additional questions for comprehensive coverage
    {
        "domain": 1,
        "domain_name": "General Security Concepts",
        "question": "What is TOTP (Time-based One-Time Password)?",
        "options": [
            {"id": "a", "text": "A password that changes based on location"},
            {"id": "b", "text": "A password generated based on current time"},
            {"id": "c", "text": "A password for top-level access"},
            {"id": "d", "text": "A static password"}
        ],
        "correct_answer": "b",
        "explanation": "TOTP generates one-time passwords based on the current time. Authenticator apps like Google Authenticator use TOTP to generate codes that change every 30 seconds."
    },
    {
        "domain": 2,
        "domain_name": "Threats, Vulnerabilities & Mitigations",
        "question": "What is a Distributed Denial of Service (DDoS) attack?",
        "options": [
            {"id": "a", "text": "An attack from a single source"},
            {"id": "b", "text": "An attack from multiple compromised systems"},
            {"id": "c", "text": "An encryption attack"},
            {"id": "d", "text": "A physical attack"}
        ],
        "correct_answer": "b",
        "explanation": "A DDoS attack uses multiple compromised systems (botnet) to flood a target with traffic, making it unavailable. It's harder to mitigate than single-source DoS attacks."
    },
    {
        "domain": 3,
        "domain_name": "Security Architecture",
        "question": "What is a next-generation firewall (NGFW)?",
        "options": [
            {"id": "a", "text": "A firewall with application awareness and deep packet inspection"},
            {"id": "b", "text": "A faster traditional firewall"},
            {"id": "c", "text": "A wireless firewall"},
            {"id": "d", "text": "A cloud-only firewall"}
        ],
        "correct_answer": "a",
        "explanation": "NGFWs combine traditional firewall capabilities with application awareness, deep packet inspection, intrusion prevention, and threat intelligence for comprehensive protection."
    },
    {
        "domain": 4,
        "domain_name": "Security Operations",
        "question": "What is a false positive in security monitoring?",
        "options": [
            {"id": "a", "text": "A real threat that was detected"},
            {"id": "b", "text": "A benign activity incorrectly flagged as malicious"},
            {"id": "c", "text": "A missed threat"},
            {"id": "d", "text": "A system error"}
        ],
        "correct_answer": "b",
        "explanation": "A false positive occurs when a security system incorrectly identifies benign activity as malicious. Too many false positives can lead to alert fatigue and missed real threats."
    },
    {
        "domain": 5,
        "domain_name": "Security Program Management",
        "question": "What is risk avoidance?",
        "options": [
            {"id": "a", "text": "Ignoring risks"},
            {"id": "b", "text": "Eliminating risk by not engaging in the risky activity"},
            {"id": "c", "text": "Transferring risk to insurance"},
            {"id": "d", "text": "Accepting all risks"}
        ],
        "correct_answer": "b",
        "explanation": "Risk avoidance eliminates risk by not engaging in the activity that creates the risk. For example, not storing sensitive data online to avoid data breach risk."
    }
]

async def add_questions():
    # Add unique IDs to each question
    for q in additional_questions:
        q["id"] = str(uuid.uuid4())
    
    # Insert questions
    result = await db.questions.insert_many(additional_questions)
    print(f"Added {len(result.inserted_ids)} new questions")
    
    # Get total count
    total = await db.questions.count_documents({})
    print(f"Total questions in database: {total}")

if __name__ == "__main__":
    asyncio.run(add_questions())
