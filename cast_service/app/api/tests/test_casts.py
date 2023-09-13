from fastapi.testclient import TestClient


def test_get(test_app):
    response = test_app.get(f"1/")
    assert response.status_code == 200
    assert response.json() == {
        "name": "Daisy Ridley",
        "nationality": "British",
        "id": 1
    }
