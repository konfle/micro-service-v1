import json
import pytest

from fastapi.testclient import TestClient

from app.api import db_manager as dbm


def test_create_cast(test_app, monkeypatch):
    test_request_payload = {"name": "Jane Doe", "nationality": "American"}
    test_response_payload = {"name": "Jane Doe", "nationality": "American", "id": 1}

    async def mock_add_cast(payload):
        return 1

    monkeypatch.setattr(dbm, "add_cast", mock_add_cast)

    response = test_app.post("", content=json.dumps(test_request_payload), )

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_get(test_app):
    response = test_app.get(f"1/")
    assert response.status_code == 200
    assert response.json() == {
        "name": "Daisy Ridley",
        "nationality": "British",
        "id": 1
    }
