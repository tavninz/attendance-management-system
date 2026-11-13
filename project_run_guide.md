# School Leave Management System - Setup & Run Guide

This full-stack application consists of a **FastAPI** backend (Python), a **React / Vite** frontend (Node.js), and containerized services using **Docker**.

---

## Prerequisites

Make sure you have the following installed on your machine:

- **Node.js** (v18+ or v22+) & `npm`
- **Python** (v3.10+)
- **Docker & Docker Compose** (optional, for containerized execution)
- **PostgreSQL** (if running locally without Docker)

---

## 1. Local Development Setup (Without Docker)

### Backend Setup (FastAPI)

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the `backend/` directory with your configurations (e.g., database URL, secret keys).
5. Run the FastAPI development server:
   ```bash
   uvicorn app.main:app --reload
   ```
   _The API will be available at `http://localhost:8000`, and documentation at `http://localhost:8000/docs`._

---

### Frontend Setup (React & Vite)

1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
   _The frontend will be available at `http://localhost:5173`._

---

## 2. Running with Docker Containerization

If you want to run the entire stack using Docker Compose, follow these steps:

1. Ensure your root directory contains a `docker-compose.yml` file along with individual `Dockerfile` configurations for both backend and frontend.
2. Build and start all containers in detached mode:
   ```bash
   docker-compose up --build -d
   ```
3. Check running containers:
   ```bash
   docker ps
   ```
4. To view application logs:
   ```bash
   docker-compose logs -f
   ```
5. To stop and remove containers:
   ```bash
   docker-compose down
   ```
