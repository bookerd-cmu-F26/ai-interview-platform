import boto3
from botocore.exceptions import ClientError

from app.config import (
    AWS_REGION,
    INTERVIEWS_TABLE_NAME,
    QUESTIONS_TABLE_NAME,
)

from app.models.question import QuestionResponse


class QuestionGenerationRepository:
    def __init__(self) -> None:
        self.client = boto3.client(
            "dynamodb",
            region_name=AWS_REGION,
        )

    def create_question_and_mark_ready(
        self,
        question: QuestionResponse,
    ) -> bool:
        try:
            self.client.transact_write_items(
                TransactItems=[
                    {
                        "Put": {
                            "TableName": QUESTIONS_TABLE_NAME,
                            "Item": {
                                "question_id": {
                                    "S": question.question_id
                                },
                                "interview_id": {
                                    "S": question.interview_id
                                },
                                "question_type": {
                                    "S": question.question_type.value
                                },
                                "question_text": {
                                    "S": question.question_text
                                },
                                "question_order": {
                                    "N": str(question.question_order)
                                },
                                "created_at": {
                                    "S": question.created_at.isoformat()
                                },
                            },
                            "ConditionExpression": (
                                "attribute_not_exists(question_id)"
                            ),
                        }
                    },
                    {
                        "Update": {
                            "TableName": INTERVIEWS_TABLE_NAME,
                            "Key": {
                                "interview_id": {
                                    "S": question.interview_id
                                }
                            },
                            "UpdateExpression": (
                                "SET #status = :ready"
                            ),
                            "ConditionExpression": (
                                "#status = :generating"
                            ),
                            "ExpressionAttributeNames": {
                                "#status": "status"
                            },
                            "ExpressionAttributeValues": {
                                ":generating": {
                                    "S": "QUESTION_GENERATING"
                                },
                                ":ready": {
                                    "S": "INTERVIEW_READY"
                                },
                            },
                        }
                    },
                ]
            )

            return True

        except ClientError as error:
            if (
                error.response["Error"]["Code"]
                == "TransactionCanceledException"
            ):
                return False

            raise