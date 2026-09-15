from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException, status

from app.models.interview import (
    CreateInterviewRequest,
    InterviewResponse,
    InterviewStatus,
)
from app.repositories.interview_repository import (
    InterviewRepository,
)
from app.repositories.user_repository import UserRepository
from app.services.sqs_service import SQSService


class InterviewService:
    def __init__(
        self,
        interview_repository: InterviewRepository,
        user_repository: UserRepository,
        sqs_service: SQSService,
    ) -> None:
        self.interview_repository = interview_repository
        self.user_repository = user_repository
        self.sqs_service = sqs_service

    def create_interview(
        self,
        request: CreateInterviewRequest,
    ) -> InterviewResponse:
        user = self.user_repository.find_by_id(
            request.user_id
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        now = datetime.now(timezone.utc)

        interview = InterviewResponse(
            interview_id=str(uuid4()),
            user_id=request.user_id,
            interview_types=request.interview_types,
            job_title=request.job_title,
            job_description=request.job_description,
            status=InterviewStatus.QUESTION_GENERATING,
            created_at=now,
            updated_at=now,
        )

        self.interview_repository.save(
            interview
        )

        self.sqs_service.send_question_generation_message(
            interview_id=interview.interview_id,
            user_id=interview.user_id,
        )

        return interview

    def get_interview(
        self,
        interview_id: str,
    ) -> InterviewResponse:
        interview = (
            self.interview_repository.find_by_id(
                interview_id
            )
        )

        if interview is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview not found",
            )

        return interview

    def get_interviews_by_user(
        self,
        user_id: str,
    ) -> list[InterviewResponse]:
        user = self.user_repository.find_by_id(
            user_id
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return (
            self.interview_repository.find_by_user_id(
                user_id
            )
        )