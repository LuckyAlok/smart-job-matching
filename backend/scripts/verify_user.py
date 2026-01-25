from app.db.session import SessionLocal
from app.models.all_models import User

db = SessionLocal()
email = "match_verif_user@example.com"
user = db.query(User).filter(User.email == email).first()

from app.core.security import get_password_hash

if user:
    print(f"User found: {user.email} (ID: {user.id})")
else:
    print(f"User {email} NOT FOUND. Creating...")
    new_user = User(
        email=email,
        hashed_password=get_password_hash("password"),
        is_active=True
    )
    db.add(new_user)
    db.commit()
    print(f"User {email} created successfully.")
