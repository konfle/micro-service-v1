import pytest

from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def test_app():
    with TestClient(app, base_url=f"http://localhost:8080/api/v1/casts/") as client:
        yield client
