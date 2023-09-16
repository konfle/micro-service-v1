import json
import pytest
import random

from fastapi.testclient import TestClient

from app.api import db_manager as dbm


class TestEndpointGetAllCast:
    """
    Test class for the 'get_all_casts' endpoint.

    This class contains tests related to retrieving a list of all cast members.
    It uses the FastAPI TestClient to send requests and validate responses.
    """
    def test_get_all_casts(self, test_app, mock_get_all_casts):
        """
        Test successful retrieval of all cast members.

        This test case sends a GET request to the 'get_all_cast' endpoint to retrieve
        a list of cast members. It checks that the response status code is 200, that
        the response contains a JSON list, and that the list is not empty.

        Args:
            test_app: Pytest fixture providing the FastAPI TestClient.
            mock_get_all_casts: Fixture for mocking 'db_manager.get_all_casts'.
        """
        response = test_app.get("")

        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) > 0

    def test_get_all_cast_empty_database(self, test_app, mock_get_all_casts_empty):
        """
        Test retrieval of all cast members from an empty database.

        This test case sends a GET request to the 'get_all_cast' endpoint when the
        database is empty. It checks that the response status code is 200 and that
        the response contains an empty JSON list.

        Args:
            test_app: Pytest fixture providing the FastAPI TestClient.
            mock_get_all_casts_empty: Fixture for mocking 'db_manager.get_all_casts' for an empty database.
        """
        response = test_app.get("")

        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == 0

    def test_get_all_cast_with_query_parameter(self, test_app):
        """
        Test handling of query parameters when provided to the 'get_all_cast' endpoint.

        This test case sends a GET request to the 'get_all_cast' endpoint with an
        invalid query parameter ('invalid_param=123'). It checks that the response
        status code is 400, indicating a bad request, and that the response contains
        an appropriate error message indicating that the endpoint does not support
        query parameters.

        Args:
            test_app: Pytest fixture providing the FastAPI TestClient.
        """
        response = test_app.get("?invalid_param=123")
        assert response.status_code == 400
        assert "This endpoint does not support query parameters." in response.text


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
    """
    Test class for the 'get_cast_by_id' endpoint.

    This class contains tests related to retrieving a cast member by their ID.
    It uses the FastAPI TestClient to send requests and validate responses.
    """

    def test_get_cast_by_id_success(self, test_app, mock_get_cast_by_id):
        """
        Test retrieving a cast member by their ID successfully.

        This test case sends a GET request to the 'get_cast_by_id' endpoint with a
        valid cast ID and checks that the response status code is 200 and that the
        response JSON matches the expected data.

        Args:
            test_app: Pytest fixture providing the FastAPI TestClient.
            mock_get_cast_by_id: Fixture for mocking 'db_manager.get_cast_by_id'.
        """
        cast_id = random.randint(1, 100)
        response = test_app.get(f"{cast_id}/")

        assert response.status_code == 200
        assert response.json() == {
            "name": "Jane Doe",
            "nationality": "British",
            "id": cast_id
        }

    def test_get_cast_by_id_not_found(self, test_app):
        """
        Test retrieving a cast member by a non-existent ID.

        This test case sends a GET request to the 'get_cast_by_id' endpoint with a
        cast ID that does not exist in the database and checks that the response
        status code is 404 (Not Found).

        Args:
            test_app: Pytest fixture providing the FastAPI TestClient.
        """
        cast_id = random.randint(1, 100)
        response = test_app.get(f"{cast_id}/")

        assert response.status_code == 404

    def test_get_cast_by_id_with_bad_data_type(self, test_app):
        """
        Test retrieving a cast member with an invalid cast ID data type.

        This test case sends a GET request to the 'get_cast_by_id' endpoint with an
        invalid cast ID data type (e.g., a non-integer value) and checks that the
        response status code is 422 (Unprocessable Entity), indicating a validation
        failure.

        Args:
            test_app: Pytest fixture providing the FastAPI TestClient.
        """
        response = test_app.get("z")
        assert response.status_code == 422
