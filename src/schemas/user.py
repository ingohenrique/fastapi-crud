from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    """
    User response model for returning user data.
    """
    id: UUID
    name: str
    email: EmailStr
    model_config = {'from_attributes': True}
