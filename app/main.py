from fastapi import FastAPI, HTTPException
from app.models import StudentRequest, StudentSummary
from typing import Dict

app = FastAPI()

GRADE_MAP: Dict[str, float] = {
    "A+": 4.5, "A": 4.0, "B+": 3.5, "B": 3.0,
    "C+": 2.5, "C": 2.0, "D+": 1.5, "D": 1.0, "F": 0.0
}

@app.post("/score")
def calculate_score(data: StudentRequest):
    total_credits = sum(course.credits for course in data.courses)
    if total_credits == 0:
        raise HTTPException(status_code=400, detail="No credits found")

    weighted_sum = sum(GRADE_MAP.get(course.grade, 0) * course.credits for course in data.courses)
    gpa = round(weighted_sum / total_credits, 2)

    return {
        "student_summary": StudentSummary(
            student_id=data.student_id,
            name=data.name,
            gpa=gpa,
            total_credits=total_credits
        )
    }
