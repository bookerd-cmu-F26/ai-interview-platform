import json

import boto3

from app.config import (
    AWS_REGION,
    QUESTION_GENERATION_QUEUE_URL,
)


class SQSService:
    def __init__(self) -> None:
        self.sqs = boto3.client(
            "sqs",
            region_name=AWS_REGION,
        )

    def send_question_generation_message(
        self,
        interview_id: str,
        user_id: str,
        interview_type: str,
    ) -> None:
        message = {
            "event_type": "GENERATE_QUESTIONS",
            "interview_id": interview_id,
            "user_id": user_id,
            "interview_type": interview_type,
        }

        self.sqs.send_message(
            QueueUrl=QUESTION_GENERATION_QUEUE_URL,
            MessageBody=json.dumps(message),
        )