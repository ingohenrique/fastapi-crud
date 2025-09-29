from typing import Optional
from uuid import UUID

from pydantic import EmailStr
from sqlmodel import Session, select

from src.infra.models import UserTable
from src.models.user import User, UserCreate


class UserRepository:

    def __init__(self, session: Session):
        """
        Initialize the UserRepository with a database session.
        :param session: SQLModel Session
        """
        self.session = session

    def create_user(self, user_create: UserCreate) -> User:
        """
        Create a new user in the database.
        :param user_create: UserCreate
        :return: User
        :raises ValueError: If email already exists
        """
        existing_user = self.get_user_by_email(user_create.email)
        if existing_user:
            raise ValueError("Email already exists")
        
        db_user = UserTable.model_validate(user_create)
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)

        return User.model_validate(db_user)

    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """
        Get user by ID.
        :param user_id: User UUID
        :return: User or None
        """
        statement = select(UserTable).where(UserTable.id == user_id)
        db_user = self.session.exec(statement).first()

        if not db_user:
            return None

        return User.model_validate(db_user)

    def get_user_by_email(self, email: EmailStr) -> Optional[User]:
        """
        Get user by email.
        :param email: User email
        :return: User or None
        """
        statement = select(UserTable).where(UserTable.email == email)
        db_user = self.session.exec(statement).first()

        if not db_user:
            return None

        return User.model_validate(db_user)

    def get_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        """
        Get list of users with pagination.
        :param skip: Number of records to skip
        :param limit: Maximum number of records to return
        :return: List of users
        """
        statement = select(UserTable).offset(skip).limit(limit)
        db_users = self.session.exec(statement).all()

        return [User.model_validate(db_user) for db_user in db_users]

    def update_user(self, user_id: UUID, user_update: UserCreate) -> User:
        """
        Update user by ID.
        :param user_id: User UUID
        :param user_update: UserCreate
        :return: Updated User
        :raises ValueError: If user not found or email already exists
        """
        db_user = self.session.get(UserTable, user_id)
        if not db_user:
            raise ValueError("User not found")

        if db_user.email != user_update.email:
            existing_user = self.get_user_by_email(user_update.email)
            if existing_user:
                raise ValueError("Email already exists")

        db_user.name = user_update.name
        db_user.email = str(user_update.email)

        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)

        return User.model_validate(db_user)

    def delete_user(self, user_id: UUID) -> None:
        """
        Delete user by ID.
        :param user_id: User UUID
        :return: None
        """
        statement = select(UserTable).where(UserTable.id == user_id)
        db_user = self.session.exec(statement).first()
        if db_user:
            self.session.delete(db_user)
            self.session.commit()
        return None
