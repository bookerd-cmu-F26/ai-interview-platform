import json

from app.models.interview import InterviewStatus
from app.repositories.interview_repository import (
    InterviewRepository,
)
from app.repositories.question_generation_repository import (
    QuestionGenerationRepository,
)
from app.services.ai_question_service import (
    AIQuestionService,
)
from app.services.sqs_service import SQSService


class QuestionGenerationConsumer:
    def __init__(self) -> None:
        self.sqs_service = SQSService()
        self.interview_repository = InterviewRepository()
        self.question_service = AIQuestionService()
        self.question_generation_repository = (
            QuestionGenerationRepository()
        )

    def process_message(
        self,
        message: dict,
    ) -> None:
        body = json.loads(
            message["Body"]
        )

        interview_id = body[
            "interview_id"
        ]

        interview = (
            self.interview_repository.find_by_id(
                interview_id
            )
        )

        if interview is None:
            self.sqs_service.delete_message(
                message["ReceiptHandle"]
            )
            return

        if (
            interview.status
            != InterviewStatus.QUESTION_GENERATING
        ):
            self.sqs_service.delete_message(
                message["ReceiptHandle"]
            )
            return

        questions = (
            self.question_service.generate_questions(
            interview
            )
        )

        transaction_succeeded = (
            self.question_generation_repository
            .create_questions_and_mark_ready(
                questions
            )
        )

        if transaction_succeeded:
            self.sqs_service.delete_message(
                message["ReceiptHandle"]
            )
            return

        latest_interview = (
            self.interview_repository.find_by_id(
                interview_id
            )
        )

        if (
            latest_interview is not None
            and latest_interview.status
            == InterviewStatus.INTERVIEW_READY
        ):
            self.sqs_service.delete_message(
                message["ReceiptHandle"]
            )