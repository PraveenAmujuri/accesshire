# AccessHire AI

> **Final-Year B.Tech Artificial Intelligence & Machine Learning Project**  
> An Agentic AI-powered accessible mock interview platform designed to help candidates practice job interviews through adaptive, closed-loop orchestration.

---

## 🏗️ Architecture Overview

AccessHire AI is decoupled into three independent applications:

1. **`frontend-marketing/`**: Public-facing marketing and architecture showcase application built with React, Vite (JavaScript), Tailwind CSS, and Framer Motion.
2. **`frontend-interview/`**: Authenticated candidate mock interview workspace with accessibility controls (High Contrast, font scaling, simplified question phrasing), voice/text interaction components, and performance reports.
3. **`backend/`**: Python 3.11+ FastAPI service with Motor async MongoDB drivers, JWT auth, LangGraph multi-agent orchestration, and a Central Orchestrator / Supervisor resilience layer.

---

## 🚀 Quickstart Guide

### 1. Backend (FastAPI)
```bash
cd backend
# Create and activate virtual environment
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows PowerShell
# source .venv/bin/activate    # Linux / macOS

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run FastAPI server
uvicorn app.main:app --reload --port 8000
```
- API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
- Health Check: [http://localhost:8000/api/health](http://localhost:8000/api/health)

### 2. Marketing Frontend
```bash
cd frontend-marketing
npm install
npm run dev
```
- Accessible on: [http://localhost:5173](http://localhost:5173)

### 3. Interview Frontend
```bash
cd frontend-interview
npm install
npm run dev
```
- Accessible on: [http://localhost:5174](http://localhost:5174)

---

## 🔬 Core Research Contribution
The main research contribution is an **Adaptive Closed-Loop Decision Policy Engine**:
```
Interview State -> Policy Decision -> Next Question -> Candidate Answer -> Evaluation -> Update State -> Policy Decision
```
State vectors track topic mastery and dynamically calibrate question difficulty, probe follow-ups, and provide cognitive accessibility accommodations.
