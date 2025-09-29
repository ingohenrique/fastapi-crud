from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class UserTable(SQLModel, table=True):
    __tablename__ = "usertable"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(min_length=1)
    email: str = Field(min_length=1)
