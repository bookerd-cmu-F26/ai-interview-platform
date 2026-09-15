from datetime import datetime, timezone

from app.models.interview import (
    InterviewResponse,
    InterviewStatus,
    InterviewType,
)
from app.services.ai_question_service import (
    AIQuestionService,
)


interview = InterviewResponse(
    interview_id="test-interview",
    user_id="test-user",
    interview_types=[
        InterviewType.CODING,
        InterviewType.BEHAVIORAL,
    ],
    job_title="Software Engineer",
    job_description=(
        "Backend engineering role using Python, "
        "distributed systems, and AWS."
    ),
    status=InterviewStatus.QUESTION_GENERATING,
    created_at=datetime.now(timezone.utc),
    updated_at=datetime.now(timezone.utc),
)


service = AIQuestionService()

questions = service.generate_questions(
    interview
)


for question in questions:
    print(
        question.question_order,
        question.question_type,
        question.question_text,
    )