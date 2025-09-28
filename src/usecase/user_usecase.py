from typing import List, Optional
from uuid import UUID

from src.models.user import User, UserCreate
from src.repositories.user_repository import UserRepository


class UserUseCase:
    def __init__(self, user_repository: UserRepository):
        """
        Initialize the UserUseCase with a UserRepository.
        :param user_repository: UserRepository
        """
        self.user_repository = user_repository

    def create_user(self, user_create: UserCreate) -> User:
        """
        Create a new user with basic validation.
        :param user_create: UserCreate
        :return: User
        :raises ValueError: If validation fails
        """
        # Basic validation: Name must not be empty
        if not user_create.name.strip():
            raise ValueError("Name cannot be empty")
        
        return self.user_repository.create_user(user_create)

    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """
        Get user by ID.
        :param user_id: User UUID
        :return: User or None
        """
        return self.user_repository.get_user_by_id(user_id)

    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get all users with pagination validation.
        :param skip: Number of records to skip
        :param limit: Maximum number of records to return
        :return: List of Users
        :raises ValueError: If pagination is invalid
        """
        if skip < 0:
            raise ValueError("Skip cannot be negative")

        if limit <= 0:
            raise ValueError("Limit must be positive")
            
        return self.user_repository.get_users(skip=skip, limit=limit)

    def delete_user(self, user_id: UUID) -> None:
        """
        Delete user by ID.
        :param user_id: User UUID
        :raises ValueError: If user not found
        """
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        self.user_repository.delete_user(user_id)
