from src.models.user import User, UserCreate
from src.repositories.user_repository import UserRepository


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        """
        Initialize the CreateUserUseCase with a UserRepository.
        :param user_repository: UserRepository
        """
        self.user_repository = user_repository

    def execute(self, user_create: UserCreate) -> User:
        """
        Execute the use case to create a new user.
        :param user_create: UserCreate
        :return: User
        """
        return self.user_repository.create_user(user_create)
