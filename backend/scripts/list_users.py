import sys
import os

# Add parent directory to path to resolve 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.all_models import User

def list_users():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print(f"--- Database User Report ---")
        print(f"Total Users Registered: {len(users)}\n")
        
        print(f"{'ID':<5} | {'Email':<30} | {'Full Name':<20} | {'Active'}")
        print("-" * 70)
        for user in users:
            print(f"{user.id:<5} | {user.email:<30} | {str(user.full_name):<20} | {user.is_active}")
            
        print("-" * 70)
        print("Note: Passwords are hashed and stored securely (not shown here).")
        
    except Exception as e:
        print(f"Error reading database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    list_users()
