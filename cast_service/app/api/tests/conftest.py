import pytest

from fastapi.testclient import TestClient

from app.main import app
from app.api import db_manager as dbm


@pytest.fixture(scope="module")
def test_app():
    with TestClient(app, base_url=f"http://localhost:8080/api/v1/casts/") as client:
        yield client


@pytest.fixture
def mock_add_cast(monkeypatch):
    async def mock_add_cast(payload):
        return 1
    monkeypatch.setattr(dbm, "add_cast", mock_add_cast)
