from fastapi import (
    APIRouter,
    Query,
    Response,
    status,
)

from app.models.user import (
    CreateUserRequest,
    UpdateUserRequest,
    UserResponse,
)
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


user_repository = UserRepository()

user_service = UserService(
    user_repository
)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    request: CreateUserRequest,
) -> UserResponse:
    return user_service.create_user(
        request
    )


@router.get(
    "",
    response_model=list[UserResponse],
)
def get_users(
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
) -> list[UserResponse]:
    return user_service.get_users(
        limit
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: str,
) -> UserResponse:
    return user_service.get_user(
        user_id
    )


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
)
def update_user(
    user_id: str,
    request: UpdateUserRequest,
) -> UserResponse:
    return user_service.update_user(
        user_id,
        request,
    )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(
    user_id: str,
) -> Response:
    user_service.delete_user(
        user_id
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )