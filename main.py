from fastapi import FastAPI
from sqlmodel import SQLModel

from src.api.v1.endpoints import users
from src.infra.database.session import engine

app = FastAPI(title="FastAPI CRUD", version="0.1.0")

# Create tables
SQLModel.metadata.create_all(engine)

app.include_router(users.router, prefix="/api/v1")
