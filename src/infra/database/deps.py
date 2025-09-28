from fastapi import Depends
from sqlmodel import Session

from src.repositories.user_repository import UserRepository
from .session import get_session


def get_user_repository(session: Session = Depends(get_session)) -> UserRepository:
    """Get user repository with database session."""
    return UserRepository(session)
