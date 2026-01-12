# CompTIA Security+ (SY0-701) Study App PRD

## Original Problem Statement
Create an app that helps you study for the CompTIA Cybersecurity Security+ (SY0-701) exam. Full with question and progress meter allow you to review correct answers. Make Intuitive and productive.

## User Choices
- Pre-populated question bank (884 questions across 5 domains)
- All study modes: Practice, Exam Simulation, Flashcard, Smart Review (SM-2 Spaced Repetition)
- Basic + Advanced progress tracking
- Dark/Light theme toggle
- JWT-based user authentication

## Architecture
- **Backend**: FastAPI with MongoDB (motor async driver)
- **Frontend**: React with Tailwind CSS, shadcn/ui, Phosphor Icons
- **Auth**: JWT-based authentication with bcrypt password hashing
- **Database**: MongoDB for users, questions, progress, and SRS items
- **Algorithm**: SM-2 for spaced repetition

## User Personas
1. **IT Certification Seekers**: Professionals preparing for Security+ certification
2. **Career Changers**: Students entering cybersecurity field
3. **Security Professionals**: Those needing formal certification validation

## Core Requirements (Static)
- User authentication (register/login)
- Question bank with all 5 SY0-701 domains
- Multiple study modes with immediate feedback
- Progress tracking and analytics
- Theme switching

## What's Been Implemented (January 2026)
- ✅ JWT authentication with register/login
- ✅ **884 pre-seeded Security+ questions** covering all 5 domains
- ✅ Practice Mode with immediate feedback and explanations
- ✅ Exam Simulation Mode (90 questions, 90 minutes, question navigator)
- ✅ Flashcard Mode with flip cards and known/unknown tracking
- ✅ Smart Review Mode (SM-2 spaced repetition algorithm)
- ✅ Dashboard with readiness score, accuracy, streaks
- ✅ Domain progress breakdown
- ✅ Weak areas identification
- ✅ Dark/Light theme toggle
- ✅ Results page with score breakdown and question review
- ✅ Session history tracking
- ✅ **PWA Support** - Installable on mobile devices
- ✅ **Mobile-optimized responsive design**

## Question Bank Distribution
| Domain | Name | Questions |
|--------|------|-----------|
| 1 | General Security Concepts | 148 |
| 2 | Threats, Vulnerabilities & Mitigations | 190 |
| 3 | Security Architecture | 181 |
| 4 | Security Operations | 182 |
| 5 | Security Program Management | 183 |
| **Total** | | **884** |

## Domain Coverage (SY0-701)
1. General Security Concepts (12%)
2. Threats, Vulnerabilities & Mitigations (22%)
3. Security Architecture (18%)
4. Security Operations (28%)
5. Security Program Management (20%)

## Prioritized Backlog
### P0 (Completed)
- ✅ All core study modes
- ✅ Authentication
- ✅ Progress tracking
- ✅ Expand question bank to 600+ (achieved 884)
- ✅ SM-2 Spaced Repetition (Smart Review)

### P1 (Next)
- Add "Review Forecast" chart to dashboard (upcoming due cards)
- Performance-based questions (simulations)
- Detailed exam simulation analytics (per-domain breakdown)
- Study plan recommendations based on weak areas

### P2 (Future)
- Export progress reports (PDF)
- Social features (leaderboards)
- Mobile-responsive improvements
- Bookmark/favorite questions feature

## Key Files
- `/app/backend/server.py`: Main FastAPI backend
- `/app/frontend/src/pages/Dashboard.js`: Main user dashboard
- `/app/frontend/src/pages/SmartReview.js`: Spaced repetition page
- `/app/frontend/src/pages/Practice.js`: Practice mode
- `/app/frontend/src/pages/Exam.js`: Exam simulation
- `/app/frontend/src/pages/Flashcards.js`: Flashcard mode

## API Endpoints
- **Auth**: POST /api/auth/register, POST /api/auth/login, GET /api/auth/me
- **Questions**: GET /api/questions/{mode}, POST /api/questions/submit
- **Progress**: GET /api/progress
- **SRS**: GET /api/srs/review, POST /api/srs/update
