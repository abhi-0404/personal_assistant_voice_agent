"""Test setup: run the real FastAPI app against a throwaway in-memory SQLite database."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.api.dependencies import get_db
from src.main import app
from src.models.base import Base


@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    async def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    # No `with` block: the app's startup hook (which creates database.db on disk) is not run.
    yield TestClient(app)
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


def tool_call(name: str, arguments, call_id: str = "call_1") -> dict:
    """Builds the request body Vapi sends when the assistant invokes a tool."""
    return {"message": {"toolCalls": [{"id": call_id, "function": {"name": name, "arguments": arguments}}]}}


def result_of(response) -> dict:
    body = response.json()
    assert len(body["results"]) == 1
    return body["results"][0]
