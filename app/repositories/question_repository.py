import boto3
from boto3.dynamodb.conditions import Key

from app.config import (
    AWS_REGION,
    QUESTIONS_INTERVIEW_INDEX_NAME,
    QUESTIONS_TABLE_NAME,
)

from app.models.question import QuestionResponse


class QuestionRepository:
    def __init__(self) -> None:
        dynamodb = boto3.resource(
            "dynamodb",
            region_name=AWS_REGION,
        )

        self.table = dynamodb.Table(
            QUESTIONS_TABLE_NAME
        )

    def find_by_interview_id(
        self,
        interview_id: str,
    ) -> list[QuestionResponse]:
        response = self.table.query(
            IndexName=QUESTIONS_INTERVIEW_INDEX_NAME,
            KeyConditionExpression=Key(
                "interview_id"
            ).eq(interview_id),
            ScanIndexForward=True,
        )

        return [
            QuestionResponse(**item)
            for item in response.get("Items", [])
        ]