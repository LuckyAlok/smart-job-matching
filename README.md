# Smart Job Matching Backend

FastAPI backend with PostgreSQL integration, SQLAlchemy ORM, and JWT Authentication.

## Features
- **Authentication**: Secure User Registration and Login (Argon2 + JWT).
- **Job Roles**: List available job roles with required skills.
- **Courses**: List available courses mapped to skills with difficulty levels.
- **Resume Parsing**: Upload PDF resumes to extract text and skills.
- **Skill Matching**: Auto-calculate match scores between Resumes and Job Roles.
- **Course Recommendations**: Smart course suggestions based on skill gaps.
- **Database**: PostgreSQL with SQLAlchemy.

## Setup

### Prerequisites
- Python 3.8+
- PostgreSQL installed and running.

### 1. Environment Setup

Create a virtual environment (optional but recommended):
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r backend/requirements.txt
```

### 2. Database Configuration

Ensure PostgreSQL is running.
Create a database named `smart_job_matching` (or change in `.env` or `config.py`).

You can set environment variables or rely on the defaults in `backend/app/core/config.py`:
- `POSTGRES_USER`: postgres
- `POSTGRES_PASSWORD`: password
- `POSTGRES_SERVER`: localhost
- `POSTGRES_DB`: smart_job_matching

### 3. Run Migrations / Initialize DB
The application automatically creates tables on startup.

### 4. Seed Data
Populate the database with initial Job Roles and Courses:
```bash
python backend/scripts/seed_db.py
```

### 5. Run the Server
From the root directory:
```bash
cd backend
uvicorn app.main:app --reload
```

## API Documentation
Once running, visit:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Project Structure
- `backend/app/main.py`: Entry point.
- `backend/app/models`: Database models.
- `backend/app/schemas`: Pydantic schemas.
- `backend/app/api`: API endpoints.
- `backend/app/core`: Configuration and Security.
