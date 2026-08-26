from fastapi import APIRouter

from app.models.question import QuestionResponse
from app.repositories.question_repository import (
    QuestionRepository,
)


router = APIRouter(
    prefix="/interviews",
    tags=["questions"],
)


question_repository = QuestionRepository()


@router.get(
    "/{interview_id}/questions",
    response_model=list[QuestionResponse],
)
def get_questions(
    interview_id: str,
) -> list[QuestionResponse]:
    return (
        question_repository.find_by_interview_id(
            interview_id
        )
    )