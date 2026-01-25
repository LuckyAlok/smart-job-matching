from typing import List, Optional
from pydantic import BaseModel

# Job Roles
class JobRoleBase(BaseModel):
    title: str
    description: Optional[str] = None
    required_skills: List[str]

class JobRoleCreate(JobRoleBase):
    pass

class JobRole(JobRoleBase):
    id: int

    class Config:
        from_attributes = True

# Courses
class CourseBase(BaseModel):
    title: str
    provider: Optional[str] = None
    url: Optional[str] = None
    skills_covered: List[str]

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int

    class Config:
        from_attributes = True
