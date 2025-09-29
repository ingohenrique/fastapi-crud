import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session
from src.main import app
from src.infra.database.session import get_session
from src.infra.database.models import *

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

connection = engine.connect()
SQLModel.metadata.create_all(connection)

def override_get_session():
    with Session(bind=connection) as session:
        yield session

@pytest.fixture(scope="function")
def client():
    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
