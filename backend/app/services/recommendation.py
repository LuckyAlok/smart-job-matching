from typing import List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.all_models import Course
from app.services.matching import normalize_skill

def get_recommendations(skills: List[str], db: Session) -> Dict[str, List[Dict]]:
    """
    Get course recommendations for the given list of skills.
    Returns top 3 courses per skill with mixed difficulty.
    """
    recommendations = {}
    
    # Normalize input skills first
    normalized_skills = {normalize_skill(s) for s in skills}
    
    # Pre-fetch all courses to filter in Python (since skills_covered is JSON)
    # Note: In a large production DB, this would be a specialized JSONB query.
    all_courses = db.query(Course).all()
    
    for skill in normalized_skills:
        skill_courses = []
        for course in all_courses:
            # Normalize course skills to match
            if any(normalize_skill(cs) == skill for cs in course.skills_covered):
                skill_courses.append(course)
        
        if not skill_courses:
            continue
            
        # Select top 3 with mixed difficulty logic
        # Ideally we want 1 Beginner, 1 Intermediate, 1 Advanced if available
        selected = []
        by_difficulty = {"Beginner": [], "Intermediate": [], "Advanced": []}
        
        for c in skill_courses:
            if c.difficulty in by_difficulty:
                by_difficulty[c.difficulty].append(c)
        
        # Strategy: Pick one from each if possible, fill remaining with any
        for diff in ["Beginner", "Intermediate", "Advanced"]:
            if by_difficulty[diff]:
                selected.append(by_difficulty[diff].pop(0))
                
        # Fill strictly up to 3 if we have gaps
        all_remaining = by_difficulty["Beginner"] + by_difficulty["Intermediate"] + by_difficulty["Advanced"]
        
        while len(selected) < 3 and all_remaining:
            selected.append(all_remaining.pop(0))
            
        recommendations[skill] = [
            {
                "title": c.title,
                "platform": c.provider,
                "link": c.url,
                "difficulty": c.difficulty
            }
            for c in selected[:3]
        ]
        
    return recommendations
