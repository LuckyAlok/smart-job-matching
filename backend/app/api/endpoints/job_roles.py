from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.models.all_models import JobRole
from app.schemas.content import JobRole as JobRoleSchema

router = APIRouter()

@router.get("/", response_model=List[JobRoleSchema])
def read_job_roles(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve job roles.
    """
    roles = db.query(JobRole).offset(skip).limit(limit).all()
    return roles
