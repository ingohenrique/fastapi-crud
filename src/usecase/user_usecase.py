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
        Create a new user.
        :param user_create: UserCreate
        :return: User
        """
        return self.user_repository.create_user(user_create)

    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """
        Get user by ID.
        :param user_id: User UUID
        :return: User or None
        """
        return self.user_repository.get_user_by_id(user_id)

    def get_all_users(self) -> List[User]:
        """
        Get all users.
        :return: List of Users
        """
        return self.user_repository.get_users()

    def delete_user(self, user_id: UUID) -> None:
        """
        Delete user by ID.
        :param user_id:
        :return:
        """
        return self.user_repository.delete_user(user_id)
