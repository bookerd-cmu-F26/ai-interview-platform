from datetime import datetime, timezone
from uuid import uuid4

from app.models.interview import InterviewResponse
from app.models.question import (
    QuestionResponse,
    QuestionType,
)


class QuestionService:
    def generate_question(
        self,
        interview: InterviewResponse,
    ) -> QuestionResponse:
        question_text_by_type = {
            "CODING": (
                "Design and implement an LRU cache with "
                "O(1) get and put operations."
            ),
            "BEHAVIORAL": (
                "Tell me about a time you had a disagreement "
                "with a teammate. How did you handle it?"
            ),
            "SYSTEM_DESIGN": (
                "Design a URL shortening service."
            ),
        }

        question_text = question_text_by_type[
            interview.interview_type.value
        ]

        return QuestionResponse(
            question_id=str(uuid4()),
            interview_id=interview.interview_id,
            question_type=QuestionType(
                interview.interview_type.value
            ),
            question_text=question_text,
            question_order=1,
            created_at=datetime.now(timezone.utc),
        )