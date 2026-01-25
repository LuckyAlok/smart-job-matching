from fastapi import FastAPI
from app.core.config import settings
from app.api.api import api_router
from app.db.base import Base
from app.db.session import engine

# Create tables on startup
Base.metadata.create_all(bind=engine)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=settings.PROJECT_NAME)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "Welcome to Smart Job Matching API"}

from sqlalchemy.orm import Session
from fastapi import Depends
from app.api import deps
from scripts.seed_db import seed_data

@app.get("/seed")
def seed_db(db: Session = Depends(deps.get_db)):
    """
    WARNING: Use this only for initial setup!
    """
    try:
        seed_data(db)
        return {"message": "Database seeded successfully"}
    except Exception as e:
        return {"error": str(e)}
