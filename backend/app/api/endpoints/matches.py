from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.all_models import JobRole, Resume, MatchResult
from app.services.matching import calculate_match
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

@router.post("/{job_role_id}")
def match_job(
    job_role_id: int,
    db: Session = Depends(deps.get_db),
    current_user_id: int = Depends(get_current_user_id),
) -> Any:
    # 1. Get Job Role
    job_role = db.query(JobRole).filter(JobRole.id == job_role_id).first()
    if not job_role:
        raise HTTPException(status_code=404, detail="Job Role not found")
        
    # 2. Get User's Latest Resume
    resume = db.query(Resume).filter(Resume.user_id == current_user_id).first()
    if not resume:
        raise HTTPException(status_code=400, detail="No resume found for user. Please upload one first.")
        
    # 3. Calculate Match
    # Resume skills are stored as JSON list in DB
    resume_skills = resume.parsed_skills if resume.parsed_skills else []
    job_skills = job_role.required_skills
    
    result = calculate_match(resume_skills, job_skills)
    
    # 4. Save Match Result
    # Check if exists to update or create new
    match_entry = db.query(MatchResult).filter(
        MatchResult.user_id == current_user_id,
        MatchResult.job_role_id == job_role_id
    ).first()
    
    if match_entry:
        match_entry.score = result["score"]
        match_entry.details = result
    else:
        match_entry = MatchResult(
            user_id=current_user_id,
            job_role_id=job_role_id,
            score=result["score"],
            details=result
        )
        db.add(match_entry)
        
    db.commit()
    
    return result

@router.get("/latest")
def get_latest_matches(
    db: Session = Depends(deps.get_db),
    current_user_id: int = Depends(get_current_user_id),
    limit: int = 5
) -> Any:
    matches = db.query(MatchResult).filter(MatchResult.user_id == current_user_id)\
        .order_by(MatchResult.score.desc()).limit(limit).all()
        
    return matches
