from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException, status

from app.models.user import (
    CreateUserRequest,
    UpdateUserRequest,
    UserResponse,
)
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        self.user_repository = user_repository

    def create_user(
        self,
        request: CreateUserRequest,
    ) -> UserResponse:
        existing_user = self.user_repository.find_by_email(
            request.email
        )

        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this email already exists",
            )

        now = datetime.now(timezone.utc)

        user = UserResponse(
            user_id=str(uuid4()),
            name=request.name,
            email=request.email,
            resume_url=request.resume_url,
            created_at=now,
            updated_at=now,
        )

        return self.user_repository.save(user)

    def get_user(
        self,
        user_id: str,
    ) -> UserResponse:
        user = self.user_repository.find_by_id(
            user_id
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return user

    def get_users(
        self,
        limit: int,
    ) -> list[UserResponse]:
        return self.user_repository.find_all(
            limit=limit
        )

    def update_user(
        self,
        user_id: str,
        request: UpdateUserRequest,
    ) -> UserResponse:
        existing_user = self.get_user(user_id)

        update_data = request.model_dump(
            exclude_unset=True
        )

        new_email = update_data.get("email")

        if new_email is not None:
            user_with_email = (
                self.user_repository.find_by_email(
                    new_email
                )
            )

            if (
                user_with_email is not None
                and user_with_email.user_id != user_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="A user with this email already exists",
                )

        updated_user = UserResponse(
            user_id=existing_user.user_id,
            name=update_data.get(
                "name",
                existing_user.name,
            ),
            email=update_data.get(
                "email",
                existing_user.email,
            ),
            resume_url=update_data.get(
                "resume_url",
                existing_user.resume_url,
            ),
            created_at=existing_user.created_at,
            updated_at=datetime.now(timezone.utc),
        )

        return self.user_repository.save(
            updated_user
        )

    def delete_user(
        self,
        user_id: str,
    ) -> None:
        self.get_user(user_id)

        self.user_repository.delete(
            user_id
        )