import boto3
from boto3.dynamodb.conditions import Key

from app.config import (
    AWS_REGION,
    INTERVIEWS_TABLE_NAME,
    INTERVIEWS_USER_INDEX_NAME,
)

from app.models.interview import InterviewResponse


class InterviewRepository:
    def __init__(self) -> None:
        dynamodb = boto3.resource(
            "dynamodb",
            region_name=AWS_REGION,
        )

        self.table = dynamodb.Table(
            INTERVIEWS_TABLE_NAME
        )

    def save(
        self,
        interview: InterviewResponse,
    ) -> InterviewResponse:
        self.table.put_item(
            Item={
                "interview_id": interview.interview_id,
                "user_id": interview.user_id,
                "interview_types": [
                    interview_type.value
                    for interview_type in interview.interview_types
                ],  
                "job_title": interview.job_title,
                "job_description": interview.job_description,
                "status": interview.status.value,
                "created_at": interview.created_at.isoformat(),
                "updated_at": interview.updated_at.isoformat(),
            }
        )

        return interview

    def find_by_id(
        self,
        interview_id: str,
    ) -> InterviewResponse | None:
        response = self.table.get_item(
            Key={
                "interview_id": interview_id,
            }
        )

        item = response.get("Item")

        if item is None:
            return None

        return InterviewResponse(**item)

    def find_by_user_id(
        self,
        user_id: str,
    ) -> list[InterviewResponse]:
        response = self.table.query(
            IndexName=INTERVIEWS_USER_INDEX_NAME,
            KeyConditionExpression=Key("user_id").eq(
                user_id
            ),
            ScanIndexForward=False,
        )

        return [
            InterviewResponse(**item)
            for item in response.get("Items", [])
        ]

    def update_status(
        self,
        interview_id: str,
        status: str,
        ) -> None:
            self.table.update_item(
                Key={
                    "interview_id": interview_id,
                },
                UpdateExpression=(
                    "SET #status = :status"
                ),
                ExpressionAttributeNames={
                    "#status": "status",
                },
                ExpressionAttributeValues={
                    ":status": status,
                },
            )