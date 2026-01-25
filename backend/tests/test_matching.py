import unittest
from app.services.matching import normalize_skill, calculate_match

class TestMatchingService(unittest.TestCase):
    
    def test_normalization(self):
        self.assertEqual(normalize_skill("MS Excel"), "excel")
        self.assertEqual(normalize_skill("JS"), "javascript")
        self.assertEqual(normalize_skill("Python"), "python")
        self.assertEqual(normalize_skill("Unknown Skill"), "unknown skill")

    def test_perfect_match(self):
        resume = ["Python", "FastAPI"]
        job = ["Python", "FastAPI"]
        result = calculate_match(resume, job)
        self.assertEqual(result["score"], 100.0)
        self.assertEqual(len(result["missing_skills"]), 0)

    def test_partial_match(self):
        resume = ["Python", "React"]
        job = ["Python", "FastAPI", "Docker"]
        result = calculate_match(resume, job)
        # 1 match (Python) out of 3 required -> 33.33%
        self.assertEqual(result["score"], 33.33)
        self.assertIn("fastapi", result["missing_skills"])
        self.assertIn("docker", result["missing_skills"])
        self.assertIn("python", result["matched_skills"])

    def test_no_match(self):
        resume = ["Java"]
        job = ["Python"]
        result = calculate_match(resume, job)
        self.assertEqual(result["score"], 0.0)

    def test_alias_matching(self):
        resume = ["JS", "Py"] # Should map to javascript, python
        job = ["JavaScript", "Python"]
        result = calculate_match(resume, job)
        self.assertEqual(result["score"], 100.0)

if __name__ == '__main__':
    unittest.main()
