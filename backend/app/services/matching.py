from typing import List, Dict, Set

# Normalization Layer
# Example alias mapping - In a real prod environment this might be a DB table or config file
SKILL_ALIASES = {
    "ms excel": "excel",
    "microsoft excel": "excel",
    "js": "javascript",
    "py": "python",
    "reactjs": "react",
    "react.js": "react",
    "node": "node.js",
    "nodejs": "node.js",
    "golang": "go",
    "postgres": "postgresql"
}

def normalize_skill(skill: str) -> str:
    """
    Normalizes a skill string: lowercased, stripped, and alias-mapped.
    """
    normalized = skill.lower().strip()
    return SKILL_ALIASES.get(normalized, normalized)

def normalize_skill_list(skills: List[str]) -> Set[str]:
    """
    Returns a set of normalized skills from a list.
    """
    return {normalize_skill(s) for s in skills}

def calculate_match(resume_skills: List[str], job_skills: List[str]) -> Dict:
    """
    Calculates the match score between resume skills and job required skills.
    
    Returns:
    {
        "score": float (0.0 - 100.0),
        "matched_skills": List[str],
        "missing_skills": List[str]
    }
    """
    if not job_skills:
        return {
            "score": 0.0,
            "matched_skills": [],
            "missing_skills": []
        }

    norm_resume = normalize_skill_list(resume_skills)
    norm_job = normalize_skill_list(job_skills)
    
    # Matching Logic
    matched = norm_resume.intersection(norm_job)
    missing = norm_job.difference(norm_resume)
    
    # Score Calculation
    # Simple percentage of required skills covered
    score = (len(matched) / len(norm_job)) * 100 if norm_job else 0.0
    
    return {
        "score": round(score, 2),
        "matched_skills": list(matched),
        "missing_skills": list(missing)
    }
