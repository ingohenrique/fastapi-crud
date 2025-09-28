from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.infra.database.deps import get_user_repository
from src.models.user import UserCreate
from src.repositories.user_repository import UserRepository
from src.schemas.user import UserResponse
from src.usecase.user_usecase import UserUseCase

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
        user_create: UserCreate,
        user_repository: UserRepository = Depends(get_user_repository)
) -> UserResponse:
    """
    Create a new user.
    :param user_create: UserCreate
    :param user_repository: UserRepository dependency
    :return: UserResponse
    """
    user_use_case = UserUseCase(user_repository)
    try:
        user = user_use_case.create_user(user_create)
        return UserResponse.model_validate(user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
        user_id: UUID,
        user_repository: UserRepository = Depends(get_user_repository)
) -> UserResponse:
    """
    Get a user by ID.
    :param user_id: User UUID
    :param user_repository: UserRepository dependency
    :return: UserResponse
    """
    user_use_case = UserUseCase(user_repository)
    user = user_use_case.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponse.model_validate(user)


@router.get("/", response_model=list[UserResponse])
async def list_users(
        skip: int = 0,
        limit: int = 100,
        user_repository: UserRepository = Depends(get_user_repository)
) -> list[UserResponse]:
    """
    List users with pagination.
    :param skip: Number of records to skip
    :param limit: Maximum number of records to return
    :param user_repository: UserRepository dependency
    :return: List of UserResponse
    """
    user_use_case = UserUseCase(user_repository)
    try:
        users = user_use_case.get_all_users(skip=skip, limit=limit)
        return [UserResponse.model_validate(user) for user in users]
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: UUID,
        user_repository: UserRepository = Depends(get_user_repository)
) -> None:
    """
    Delete a user by ID.
    :param user_id: User UUID
    :param user_repository: UserRepository dependency
    :return: None
    """
    user_use_case = UserUseCase(user_repository)
    try:
        user_use_case.delete_user(user_id)
        return None
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
