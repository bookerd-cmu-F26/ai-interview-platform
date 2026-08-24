from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class InterviewStatus(str, Enum):
    QUESTION_GENERATING = "QUESTION_GENERATING"
    INTERVIEW_READY = "INTERVIEW_READY"
    FAILED = "FAILED"


class InterviewType(str, Enum):
    CODING = "CODING"
    BEHAVIORAL = "BEHAVIORAL"
    SYSTEM_DESIGN = "SYSTEM_DESIGN"


class CreateInterviewRequest(BaseModel):
    user_id: str
    interview_type: InterviewType
    job_title: str = Field(min_length=1, max_length=200)
    job_description: str | None = None


class InterviewResponse(BaseModel):
    interview_id: str
    user_id: str
    interview_type: InterviewType
    job_title: str
    job_description: str | None = None
    status: InterviewStatus
    created_at: datetime
    updated_at: datetime