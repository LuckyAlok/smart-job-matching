import sys
import os
import logging
from sqlalchemy.orm import Session

# Add the parent directory to sys.path to resolve 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.models.all_models import JobRole, Course

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_data(db: Session):
    # Job Roles
    job_roles_data = [
        {"title": "Frontend Developer", "skills": ["HTML", "CSS", "JavaScript", "React"]},
        {"title": "Backend Developer", "skills": ["Python", "FastAPI", "SQL", "Docker"]},
        {"title": "Full Stack Developer", "skills": ["HTML", "CSS", "JavaScript", "Python", "SQL"]},
        {"title": "Data Scientist", "skills": ["Python", "Pandas", "Scikit-Learn", "Machine Learning"]},
        {"title": "DevOps Engineer", "skills": ["AWS", "Docker", "Kubernetes", "CI/CD"]},
        {"title": "UI/UX Designer", "skills": ["Figma", "Sketch", "Prototyping"]},
        {"title": "Mobile Developer", "skills": ["React Native", "Flutter", "iOS"]},
        {"title": "Cloud Architect", "skills": ["AWS", "Azure", "Cloud Design Patterns"]},
        {"title": "Security Analyst", "skills": ["Network Security", "Penetration Testing", "Cryptography"]},
        {"title": "Product Manager", "skills": ["Agile", "Scrum", "Roadmapping"]},
        {"title": "QA Engineer", "skills": ["Selenium", "Test Automation", "Bug Tracking"]},
        {"title": "Database Administrator", "skills": ["PostgreSQL", "Oracle", "Performance Tuning"]},
        {"title": "Machine Learning Engineer", "skills": ["TensorFlow", "PyTorch", "Deep Learning"]},
        {"title": "Technical Writer", "skills": ["Documentation", "Technical Writing", "Markdown"]},
        {"title": "Systems Administrator", "skills": ["Linux", "Bash Scripting", "Networking"]}
    ]

    logger.info("Seeding Job Roles...")
    for role in job_roles_data:
        db_role = JobRole(title=role["title"], required_skills=role["skills"], description=f"Role for {role['title']}")
        db.add(db_role)
    
    # Courses
    # Generating 40 courses mapped to above skills
    courses_data = [
        {"title": "Complete React Guide", "provider": "Udemy", "skills": ["React", "JavaScript", "HTML", "CSS"]},
        {"title": "FastAPI - The Complete Course", "provider": "Udemy", "skills": ["FastAPI", "Python", "SQL"]},
        {"title": "Python for Data Science", "provider": "Coursera", "skills": ["Python", "Pandas"]},
        {"title": "Machine Learning A-Z", "provider": "Udemy", "skills": ["Machine Learning", "Scikit-Learn"]},
        {"title": "Docker & Kubernetes: The Practical Guide", "provider": "Udemy", "skills": ["Docker", "Kubernetes"]},
        {"title": "AWS Certified Solutions Architect", "provider": "A Cloud Guru", "skills": ["AWS", "Cloud Design Patterns"]},
        {"title": "Figma UI Design Masterclass", "provider": "Udemy", "skills": ["Figma", "Prototyping"]},
        {"title": "Flutter & Dart - The Complete Guide", "provider": "Udemy", "skills": ["Flutter", "Mobile Development"]},
        {"title": "Ethical Hacking Bootcamp", "provider": "Udemy", "skills": ["Penetration Testing", "Network Security"]},
        {"title": "Agile Crash Course", "provider": "Udemy", "skills": ["Agile", "Scrum"]},
        {"title": "Selenium WebDriver with Java", "provider": "Udemy", "skills": ["Selenium", "Test Automation"]},
        {"title": "PostgreSQL Bootcamp", "provider": "Udemy", "skills": ["PostgreSQL", "SQL"]},
        {"title": "Deep Learning Specialization", "provider": "Coursera", "skills": ["Deep Learning", "TensorFlow"]},
        {"title": "Technical Writing One", "provider": "Udemy", "skills": ["Technical Writing"]},
        {"title": "Linux Administration", "provider": "Coursera", "skills": ["Linux", "Bash Scripting"]},
        {"title": "Modern JavaScript Bootcamp", "provider": "Udemy", "skills": ["JavaScript"]},
        {"title": "Advanced CSS and Sass", "provider": "Udemy", "skills": ["CSS", "HTML"]},
        {"title": "Python Bootcamp", "provider": "Udemy", "skills": ["Python"]},
        {"title": "SQL for Data Science", "provider": "Coursera", "skills": ["SQL"]},
        {"title": "Intro to DevOps", "provider": "Udacity", "skills": ["CI/CD", "DevOps"]},
        {"title": "Azure Fundamentals", "provider": "Microsoft", "skills": ["Azure"]},
        {"title": "Google Cloud Engineer", "provider": "Google", "skills": ["Cloud"]},
        {"title": "Sketch for Designers", "provider": "Udemy", "skills": ["Sketch"]},
        {"title": "iOS Development Bootcamp", "provider": "Udemy", "skills": ["iOS", "Swift"]},
        {"title": "Cybersecurity Fundamentals", "provider": "Coursera", "skills": ["Security"]},
        {"title": "Product Management 101", "provider": "Udemy", "skills": ["Product Management"]},
        {"title": "Manual Testing Guide", "provider": "Udemy", "skills": ["QA"]},
        {"title": "Oracle DBA Course", "provider": "Udemy", "skills": ["Oracle"]},
        {"title": "PyTorch for Deep Learning", "provider": "Udemy", "skills": ["PyTorch"]},
        {"title": "Markdown Mastery", "provider": "Udemy", "skills": ["Markdown"]},
        {"title": "Bash Scripting Guide", "provider": "Udemy", "skills": ["Bash Scripting"]},
        {"title": "Networking Basics", "provider": "Cisco", "skills": ["Networking"]},
        {"title": "React Native - The Practical Guide", "provider": "Udemy", "skills": ["React Native"]},
        {"title": "Scikit-Learn for ML", "provider": "Udemy", "skills": ["Scikit-Learn"]},
        {"title": "Pandas for Data Analysis", "provider": "Udemy", "skills": ["Pandas"]},
        {"title": "Cryptography 101", "provider": "Coursera", "skills": ["Cryptography"]},
        {"title": "Agile Project Management", "provider": "Google", "skills": ["Agile"]},
        {"title": "Automated Testing with Python", "provider": "Udemy", "skills": ["Test Automation", "Python"]},
        {"title": "Performance Tuning in SQL", "provider": "Udemy", "skills": ["Performance Tuning"]},
        {"title": "Intro to HTML5", "provider": "freeCodeCamp", "skills": ["HTML"]}
    ]

    logger.info("Seeding Courses...")
    import random
    difficulties = ["Beginner", "Intermediate", "Advanced"]
    
    for i, course in enumerate(courses_data):
        # Deterministic difficulty based on index for stability
        difficulty = difficulties[i % 3]
        db_course = Course(
            title=course["title"], 
            provider=course["provider"], 
            skills_covered=course["skills"], 
            url="http://example.com",
            difficulty=difficulty
        )
        db.add(db_course)

    db.commit()
    logger.info("Seeding Completed.")

def main():
    logger.info("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    logger.info("Creating tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()

if __name__ == "__main__":
    main()
