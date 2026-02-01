import sys
import os
import logging
from sqlalchemy import text # Import text

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import engine
from app.db.base import Base
from app.models.all_models import User, JobRole, Course, Resume, MatchResult

def reset_database():
    print("🗑️  Dropping all tables...")
    # Reflecting all tables and dropping them
    Base.metadata.drop_all(bind=engine)
    print("✅ All tables dropped.")
    
    print("🏗️  Creating new tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ New tables created.")

if __name__ == "__main__":
    reset_database()
