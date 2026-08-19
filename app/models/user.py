from datetime import datetime

from pydantic import BaseModel, Field


class CreateUserRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str
    resume_url: str | None = None


class UpdateUserRequest(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    email: str | None = None
    resume_url: str | None = None


class UserResponse(BaseModel):
    user_id: str
    name: str
    email: str
    resume_url: str | None = None
    created_at: datetime
    updated_at: datetime
