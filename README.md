# SEC-SY0-701 CompTIA Security+ Study App

A comprehensive study application for the CompTIA Security+ SY0-701 certification exam, featuring practice questions, exam simulation, flashcards, and progress tracking.

## Architecture

- **Frontend**: React app deployed on Vercel
- **Backend**: FastAPI deployed on Render
- **Database**: MongoDB Atlas

## Local Development

### Prerequisites

- Node.js 20.x
- Python 3.11
- MongoDB (local or Atlas)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with the following variables:
   ```
   MONGO_URL=mongodb://localhost:27017  # or your MongoDB Atlas connection string
   DB_NAME=sec_sy0_701_db
   JWT_SECRET=your_jwt_secret_key
   ```

5. Run the backend:
   ```bash
   uvicorn server:app --reload
   ```

The backend will be available at `http://localhost:8000`.

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file:
   ```
   REACT_APP_BACKEND_URL=http://localhost:8000
   ```

4. Run the frontend:
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000`.

## Deployment

### Backend (Render)

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set the following environment variables in Render:
   - `MONGO_URL`: Your MongoDB Atlas connection string
   - `DB_NAME`: Your database name
   - `JWT_SECRET`: A secure random string
   - `PYTHON_VERSION`: 3.11

### Frontend (Vercel)

1. Connect your GitHub repository to Vercel
2. Set the following environment variable in Vercel:
   - `REACT_APP_BACKEND_URL`: Your Render backend URL (e.g., `https://your-backend.onrender.com`)

## Features

- User registration and authentication
- Practice mode with randomized questions
- Exam simulation with time limits
- Flashcard study system
- Progress tracking and analytics
- Domain-specific question categorization
- Weak areas identification

## Tech Stack

- **Frontend**: React, React Router, Tailwind CSS, Radix UI
- **Backend**: FastAPI, MongoDB, JWT authentication
- **Deployment**: Vercel, Render, MongoDB Atlas
