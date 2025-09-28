from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.infra.database.deps import get_user_repository
from src.models.user import UserCreate
from src.repositories.user_repository import UserRepository
from src.schemas.user import UserResponse
from src.usecase.create_user import CreateUserUseCase

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
    use_case = CreateUserUseCase(user_repository)
    user = use_case.execute(user_create)
    return UserResponse.model_validate(user)


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
    user = user_repository.get_user_by_id(user_id)
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
    users = user_repository.get_users(skip=skip, limit=limit)
    return [UserResponse.model_validate(user) for user in users]
