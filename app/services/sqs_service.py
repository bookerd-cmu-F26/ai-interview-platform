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
    ) -> None:
        message = {
            "event_type": "GENERATE_QUESTIONS",
            "interview_id": interview_id,
            "user_id": user_id
        }

        self.sqs.send_message(
            QueueUrl=QUESTION_GENERATION_QUEUE_URL,
            MessageBody=json.dumps(message),
        )

    def receive_question_generation_messages(
    self,
    ) -> list[dict]:
        response = self.sqs.receive_message(
            QueueUrl=QUESTION_GENERATION_QUEUE_URL,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=20,
            VisibilityTimeout=60,
        )

        return response.get(
            "Messages",
            [],
        )


    def delete_message(
        self,
        receipt_handle: str,
        ) -> None:
            self.sqs.delete_message(
                QueueUrl=QUESTION_GENERATION_QUEUE_URL,
                ReceiptHandle=receipt_handle,
        )