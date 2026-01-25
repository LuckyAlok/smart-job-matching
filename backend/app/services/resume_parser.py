import re
import PyPDF2
from typing import Dict, List, Any
from io import BytesIO

def extract_text_from_pdf(file_content: bytes) -> str:
    """
    Extracts raw text from a PDF file content.
    """
    try:
        pdf_reader = PyPDF2.PdfReader(BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""

def parse_resume(text: str) -> Dict[str, Any]:
    """
    Parses resume text to extract structured data using heuristics.
    MVP: Extracts email and skills.
    """
    
    # 1. Extract Email
    email_regex = r"[\w\.-]+@[\w\.-]+"
    email = re.search(email_regex, text)
    email_str = email.group(0) if email else None

    # 2. Extract Skills (Keyword Matching)
    # This is a basic list. In a real app, this would come from the DB or a larger dataset.
    known_skills = [
        "Python", "Java", "JavaScript", "React", "Node.js", "SQL", "HTML", "CSS", 
        "Docker", "Kubernetes", "AWS", "Azure", "Git", "Machine Learning", "Data Analysis",
        "C++", "C#", "Go", "Rust", "Swift", "Kotlin", "Flutter", "FastAPI", "Django", "Flask"
    ]
    
    found_skills = []
    text_lower = text.lower()
    
    for skill in known_skills:
        # Use regex to find whole words to avoid partial matches (e.g., "Go" in "Google")
        if re.search(r"\b" + re.escape(skill.lower()) + r"\b", text_lower):
            found_skills.append(skill)
            
    # 3. Simple Heuristic for Name (First line or near top)
    # This is very prone to error but serves as a placeholder
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    name = lines[0] if lines else "Unknown"

    return {
        "name": name,
        "email": email_str,
        "skills": list(set(found_skills)), # Remove duplicates
        "raw_text_length": len(text)
    }
