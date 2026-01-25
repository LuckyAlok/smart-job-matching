import unittest
from unittest.mock import MagicMock
from app.services.recommendation import get_recommendations
from app.models.all_models import Course

class TestRecommendationService(unittest.TestCase):
    
    def test_recommendation_logic(self):
        # Mock DB session
        db = MagicMock()
        
        # Mock Courses
        courses = [
            Course(id=1, title="Intro to Python", provider="Udemy", difficulty="Beginner", skills_covered=["Python"]),
            Course(id=2, title="Advanced Python", provider="Coursera", difficulty="Advanced", skills_covered=["Python"]),
            Course(id=3, title="Intermediate Python", provider="Udemy", difficulty="Intermediate", skills_covered=["Python"]),
            Course(id=4, title="Another Python", provider="Udemy", difficulty="Beginner", skills_covered=["Python"]),
            Course(id=5, title="JS Basics", provider="Udemy", difficulty="Beginner", skills_covered=["JavaScript"])
        ]
        
        # Mock query result
        db.query.return_value.all.return_value = courses
        
        # Call service
        result = get_recommendations(["Python", "JavaScript"], db)
        
        # Assertions
        self.assertIn("python", result)
        self.assertIn("javascript", result)
        
        # Check Python courses (Should pick 3 with mixed difficulty if possible)
        py_courses = result["python"]
        self.assertEqual(len(py_courses), 3)
        
        difficulties = {c["difficulty"] for c in py_courses}
        self.assertIn("Beginner", difficulties)
        self.assertIn("Intermediate", difficulties)
        self.assertIn("Advanced", difficulties)
        
        # Check JS courses
        js_courses = result["javascript"]
        self.assertEqual(len(js_courses), 1)
        self.assertEqual(js_courses[0]["title"], "JS Basics")

if __name__ == '__main__':
    unittest.main()
