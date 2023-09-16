import json
import pytest

from fastapi.testclient import TestClient

from app.api import db_manager as dbm


def test_create_cast(test_app, mock_add_cast):
    test_request_payload = {"name": "Jane Doe", "nationality": "American"}
    test_response_payload = {
        "name": "Jane Doe",
        "nationality": "American",
        "id": 1
    }

    response = test_app.post("", json=test_request_payload)

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_cast_without_nationality(test_app, mock_add_cast):
    test_request_payload = {"name": "Jane Doe"}
    test_response_payload = {
        "name": "Jane Doe",
        "nationality": None,
        "id": 1
    }

    response = test_app.post("", json=test_request_payload)

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_cast_without_name(test_app, mock_add_cast):
    response = test_app.post("", json={"nationality": "American"})
    assert response.status_code == 422


def test_create_cast_with_wrong_name_data_type(test_app, mock_add_cast):
    response = test_app.post("", json={"name": 2})
    assert response.status_code == 422


def test_create_cast_with_wrong_nationality_data_type(test_app, mock_add_cast):
    response = test_app.post("", json={"nationality": 2})
    assert response.status_code == 422


def test_get(test_app):
    response = test_app.get("1/")
    assert response.status_code == 200
    assert response.json() == {
        "name": "Daisy Ridley",
        "nationality": "British",
        "id": 1
    }
