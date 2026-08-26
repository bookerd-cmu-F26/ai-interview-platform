from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class QuestionType(str, Enum):
    CODING = "CODING"
    BEHAVIORAL = "BEHAVIORAL"
    SYSTEM_DESIGN = "SYSTEM_DESIGN"


class QuestionResponse(BaseModel):
    question_id: str
    interview_id: str
    question_type: QuestionType
    question_text: str
    question_order: int
    created_at: datetime