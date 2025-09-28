from uuid import UUID

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    """
    User domain entity.
    """
    id: UUID
    name: str
    email: EmailStr

    model_config = {'from_attributes': True}


class UserCreate(BaseModel):
    """
    User creation model for creating a new user.
    """
    name: str
    email: EmailStr
