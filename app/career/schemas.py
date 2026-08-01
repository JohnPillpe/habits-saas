from pydantic import BaseModel
from typing import List


class CareerAnalysis(BaseModel):
    match_score: int
    strengths: List[str]
    missing_skills: List[str]
    recommendations: List[str]
    interview_questions: List[str]