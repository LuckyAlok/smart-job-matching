from typing import Any, List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api import deps
from app.models.all_models import Course
from app.services.recommendation import get_recommendations

router = APIRouter()

@router.get("/")
def read_courses(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve courses.
    """
    courses = db.query(Course).offset(skip).limit(limit).all()
    return courses

@router.get("/recommendations")
def recommend_courses(
    skills: str = Query(..., description="Comma-separated list of skills, e.g. 'python,sql'"),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get course recommendations for specific skills.
    
    Query Param: skills=python,sql
    """
    skill_list = [s.strip() for s in skills.split(",") if s.strip()]
    recommendations = get_recommendations(skill_list, db)
    
    # Remap to requested structure: [{'skill': 'python', 'courses': [...]}]
    response = []
    for skill, courses in recommendations.items():
        response.append({
            "skill": skill,
            "courses": courses
        })
        
    return response
