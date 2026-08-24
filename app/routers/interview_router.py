from fastapi import APIRouter, status

from app.models.interview import (
    CreateInterviewRequest,
    InterviewResponse,
)

from app.repositories.interview_repository import (
    InterviewRepository,
)

from app.repositories.user_repository import UserRepository
from app.services.interview_service import InterviewService
from app.services.sqs_service import SQSService


router = APIRouter(
    prefix="/interviews",
    tags=["interviews"],
)


interview_repository = InterviewRepository()
user_repository = UserRepository()
sqs_service = SQSService()

interview_service = InterviewService(
    interview_repository=interview_repository,
    user_repository=user_repository,
    sqs_service=sqs_service,
)


@router.post(
    "",
    response_model=InterviewResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_interview(
    request: CreateInterviewRequest,
) -> InterviewResponse:
    return interview_service.create_interview(
        request
    )


@router.get(
    "/{interview_id}",
    response_model=InterviewResponse,
)
def get_interview(
    interview_id: str,
) -> InterviewResponse:
    return interview_service.get_interview(
        interview_id
    )