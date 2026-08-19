import boto3
from boto3.dynamodb.conditions import Key

from app.config import (
    AWS_REGION,
    USERS_EMAIL_INDEX_NAME,
    USERS_TABLE_NAME,
)

from app.models.user import UserResponse


class UserRepository:
    def __init__(self) -> None:
        dynamodb = boto3.resource(
            "dynamodb",
            region_name=AWS_REGION,
        )

        self.table = dynamodb.Table(USERS_TABLE_NAME)

    def save(self, user: UserResponse) -> UserResponse:
        self.table.put_item(
            Item={
                "user_id": user.user_id,
                "name": user.name,
                "email": user.email,
                "resume_url": user.resume_url,
                "created_at": user.created_at.isoformat(),
                "updated_at": user.updated_at.isoformat(),
            }
        )

        return user

    def find_by_id(
        self,
        user_id: str,
    ) -> UserResponse | None:
        response = self.table.get_item(
            Key={
                "user_id": user_id,
            }
        )

        item = response.get("Item")

        if item is None:
            return None

        return UserResponse(**item)

    def find_by_email(
        self,
        email: str,
    ) -> UserResponse | None:
        response = self.table.query(
            IndexName=USERS_EMAIL_INDEX_NAME,
            KeyConditionExpression=Key("email").eq(email),
            Limit=1,
        )

        items = response.get("Items", [])

        if not items:
            return None

        return UserResponse(**items[0])

    def find_all(
        self,
        limit: int = 10,
    ) -> list[UserResponse]:
        response = self.table.scan(
            Limit=limit,
        )

        items = response.get("Items", [])

        return [
            UserResponse(**item)
            for item in items
        ]

    def delete(
        self,
        user_id: str,
    ) -> None:
        self.table.delete_item(
            Key={
                "user_id": user_id,
            }
        )