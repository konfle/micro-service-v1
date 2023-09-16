import json
import pytest

from fastapi.testclient import TestClient

from app.api import db_manager as dbm


class TestEndpointCreateCast:
    """
    Test class for the 'create_cast' endpoint.

    This class contains tests related to the 'create_cast' endpoint of the cast service API.
    It uses the FastAPI TestClient to send requests and validate responses.
    """
    def test_create_cast(self, test_app, mock_add_cast):
        """
        Test the successful creation of a cast member.

        This test case sends a POST request to the 'create_cast' endpoint with a valid
        payload and verifies that the response status code is 201 and the response JSON
        matches the expected data.

        Args:
            test_app: Pytest fixture providing the FastAPI TestClient.
            mock_add_cast: Fixture for mocking 'db_manager.add_cast'.
        """
        test_request_payload = {"name": "Jane Doe", "nationality": "American"}
        test_response_payload = {
            "name": "Jane Doe",
            "nationality": "American",
            "id": 1
        }

        response = test_app.post("", json=test_request_payload)

        assert response.status_code == 201
        assert response.json() == test_response_payload

    def test_create_cast_without_nationality(self, test_app, mock_add_cast):
        """
        Test creating a cast member without specifying nationality.

        This test case verifies that the 'create_cast' endpoint correctly handles the case
        where the 'nationality' field is not provided in the request payload. It sends a POST
        request with a payload missing the 'nationality' field and checks that the response
        status code is 201 (Created) and that the response JSON includes 'nationality' set to
        None.

        Args:
            test_app: Pytest fixture providing the FastAPI TestClient.
            mock_add_cast: Fixture for mocking 'db_manager.add_cast'.
        """
        test_request_payload = {"name": "Jane Doe"}
        test_response_payload = {
            "name": "Jane Doe",
            "nationality": None,
            "id": 1
        }

        response = test_app.post("", json=test_request_payload)

        assert response.status_code == 201
        assert response.json() == test_response_payload

    def test_create_cast_without_name(self, test_app, mock_add_cast):
        """
        Test creating a cast member without specifying a name.

        This test case verifies that the 'create_cast' endpoint correctly handles the case
        where the 'name' field is missing from the request payload. It sends a POST request
        with a payload missing the 'name' field and checks that the response status code is
        422 (Unprocessable Entity), indicating a validation failure.

        Args:
            test_app: Pytest fixture providing the FastAPI TestClient.
            mock_add_cast: Fixture for mocking 'db_manager.add_cast'.
        """
        response = test_app.post("", json={"nationality": "American"})
        assert response.status_code == 422

    def test_create_cast_with_wrong_name_data_type(self, test_app, mock_add_cast):
        """
        Test creating a cast member with an incorrect data type for the 'name' field.

        This test case verifies that the 'create_cast' endpoint correctly handles the case
        where the 'name' field in the request payload has an incorrect data type. It sends a
        POST request with a payload where 'name' is an integer, and it checks that the
        response status code is 422 (Unprocessable Entity), indicating a validation failure.

        Args:
            test_app: Pytest fixture providing the FastAPI TestClient.
            mock_add_cast: Fixture for mocking 'db_manager.add_cast'.
        """
        response = test_app.post("", json={"name": 2})
        assert response.status_code == 422

    def test_create_cast_with_wrong_nationality_data_type(self, test_app, mock_add_cast):
        """
        Test creating a cast member with an incorrect data type for the 'nationality' field.

        This test case verifies that the 'create_cast' endpoint correctly handles the case
        where the 'nationality' field in the request payload has an incorrect data type. It sends
        a POST request with a payload where 'nationality' is an integer, and it checks that the
        response status code is 422 (Unprocessable Entity), indicating a validation failure.

        Args:
            test_app: Pytest fixture providing the FastAPI TestClient.
            mock_add_cast: Fixture for mocking 'db_manager.add_cast'.
        """
        response = test_app.post("", json={"nationality": 2})
        assert response.status_code == 422


class TestEndpointGetCastById:
    def test_get(self, test_app):
        response = test_app.get("1/")
        assert response.status_code == 200
        assert response.json() == {
            "name": "Daisy Ridley",
            "nationality": "British",
            "id": 1
        }
