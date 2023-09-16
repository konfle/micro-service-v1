import pytest

from fastapi.testclient import TestClient

from app.main import app
from app.api import db_manager as dbm


@pytest.fixture(scope="module")
def test_app():
    """
    Pytest fixture providing a TestClient for the FastAPI app.

    This fixture sets up a TestClient for the FastAPI app to simulate HTTP requests
    during testing. It configures the client to use the specified base URL for API
    endpoints under '/api/v1/casts/'.

    Usage:
    ```
    def test_example(test_app):
        response = test_app.get("/some_endpoint")
        assert response.status_code == 200
    ```

    Returns:
        TestClient: A TestClient instance for making HTTP requests to the app.
    """
    with TestClient(app, base_url=f"http://localhost:8080/api/v1/casts/") as client:
        yield client


@pytest.fixture
def mock_add_cast(monkeypatch):
    """
    Pytest fixture for mocking the 'db_manager.add_cast' function.

    This fixture replaces the actual 'db_manager.add_cast' function with a mock
    implementation to isolate tests from the database. It allows you to control
    the behavior of 'add_cast' during testing and simulate successful cast member
    additions.

    Args:
        monkeypatch: Pytest fixture for patching modules and objects during testing.

    Returns:
        callable: A callable mock function for 'db_manager.add_cast'.
            The mock function takes a 'payload' parameter and returns a predefined
            cast ID (e.g., 1) to simulate a successful cast member addition.
    """
    async def mock_add_cast(payload):
        return 1
    monkeypatch.setattr(dbm, "add_cast", mock_add_cast)


@pytest.fixture
def mock_get_cast_by_id(monkeypatch):
    """
    Pytest fixture for mocking the 'db_manager.get_cast_by_id' function.

    This fixture replaces the actual 'db_manager.get_cast_by_id' function with a
    mock implementation to isolate tests from the database. It allows you to control
    the behavior of 'get_cast_by_id' during testing.

    Args:
        monkeypatch: Pytest fixture for patching modules and objects during testing.

    Returns:
        callable: A callable mock function for 'db_manager.get_cast_by_id'.
            The mock function takes a 'cast_id' parameter and returns a predefined
            cast member dictionary based on the provided 'cast_id'.
    """
    async def mock_get_cast_by_id(cast_id: int):
        return {
            "name": "Jane Doe",
            "nationality": "British",
            "id": cast_id
        }
    monkeypatch.setattr(dbm, "get_cast_by_id", mock_get_cast_by_id)
