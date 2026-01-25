from typing import Any, List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.all_models import Resume, User
from app.services.resume_parser import extract_text_from_pdf, parse_resume
from app.core import security
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from jose import jwt, JWTError

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR if hasattr(settings, 'API_V1_STR') else ''}/auth/login")

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return int(user_id)

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user_id: int = Depends(get_current_user_id),
) -> Any:
    # 1. State: Uploaded
    stages = ["uploaded"]
    
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # 2. Extract Text
    content = await file.read()
    raw_text = extract_text_from_pdf(content)
    stages.append("extracted_text")

    if not raw_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from PDF")

    # 3. Parse JSON
    parsed_data = parse_resume(raw_text)
    stages.append("parsed_json")

    # 4. Save to DB
    # Check if resume exists
    existing_resume = db.query(Resume).filter(Resume.user_id == current_user_id).first()
    if existing_resume:
        existing_resume.content = raw_text
        existing_resume.parsed_skills = parsed_data.get("skills", [])
        # In a real app we might update other fields too
        db.add(existing_resume)
    else:
        new_resume = Resume(
            user_id=current_user_id,
            content=raw_text,
            parsed_skills=parsed_data.get("skills", [])
        )
        db.add(new_resume)
    
    db.commit()
    stages.append("parsed_json_saved")

    return {
        "filename": file.filename,
        "parsed_data": parsed_data,
        "progress": stages
    }
