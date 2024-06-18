"""
Test module of backend main module.

Execute this test by running on the terminal (from the app/) the command:
pytest --cov=app --cov-report=html tests/
"""

from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
import pytest
import os
import pandas as pd
from datetime import datetime

pd.options.mode.chained_assignment = None

client = TestClient(app)


def test_read_main():
    """
    Test the main endpoint ("/") of the application.

    Sends a GET request to the root endpoint and asserts:
    - The response status code is 200.
    - The JSON response matches {"Hello": "World"}.
    """
    # Send a GET request to the root endpoint
    response = client.get("/")

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Assert that the JSON response matches {"Hello": "World"}
    assert response.json() == {"Hello": "World"}


def test_read_and_return_df():
    """
    Test the endpoint "/df_show" to ensure
    it returns a DataFrame-like JSON structure.

    Sends a GET request to "/df_show" and performs the following checks:
    - Asserts that the response status code is 200.
    - Verifies that the response data is a non-empty list.
    - Checks that the structure of the first item in
      the response matches the expected keys.
    - Ensures that none of the items in the response data are empty.
    """
    # Send a GET request to the endpoint
    response = client.get("/df_show")

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Get the JSON response data
    response_data = response.json()

    # Ensure that the response data is a non-empty list
    assert isinstance(response_data, list)
    assert len(response_data) > 0

    # Expected keys in the response data
    expected_keys = ['AF_ID', 'TEACHING', 'CYCLE', 'PARTITION', 'SITE',
                     'CREDITS', 'DEGREE_TYPE', 'LECTURE_DAY', 'LECTURE_START',
                     'LECTURE_END', 'LECTURER_NAME', 'CLASSROOM_NAME',
                     'LOCATION_NAME', 'ADDRESS', 'DOCENTE_ID', 'URL_DOCENTE',
                     'URLS_INSEGNAMENTO', 'START_ISO8601', 'END_ISO8601'
                     ]

    # Check the structure and non-empty values for each item
    for item in response_data:
        # Ensure all expected keys are present in the item
        assert all(key in item for key in expected_keys)

        # Ensure none of the values corresponding to the keys are empty
        for key in expected_keys:
            assert item[key] is not None and item[key] != ''


def test_csv_creation_date():
    """
    This function tests the endpoint "/csv_creation_date"
    to ensure it returns the creation date of the CSV file.

    Parameters:
    None

    Returns:
    None

    Raises:
    None

    Note:
    - The function sends a GET request to "/csv_creation_date" endpoint.
    - It asserts the response status code is 200 when the function works.
    - It asserts the response is in the right date format.
    - It asserts the date has the correct timezone (Europe/Rome).
    """
    response = client.get("/csv_creation_date")

    date = response.json()

    # Assert response status code is 200 when the function works
    assert response.status_code == 200
    # Assert response in the right date format
    assert datetime.strptime(date, '%A, %d-%b-%Y %H:%M:%S %Z')
    # Assert date with the correct timezone (Europe/Rome)
    assert date.endswith('CEST')


@pytest.mark.asyncio
async def test_csv_creation_date_not_exists(monkeypatch):
    """
    Test the endpoint "/csv_creation_date" when the CSV file does not exist.

    Parameters:
    monkeypatch (pytest.MonkeyPatch): A pytest fixture for patching objects
                                      in the test environment.

    Returns:
    None

    Raises:
    None

    Note:
    - This function simulates the absence of the CSV file
      by patching the 'os.path.exists' function.
    - It sends a GET request to the "/csv_creation_date" endpoint.
    - It asserts the response status code is 404 when the file does not exist.
    - It asserts the response JSON matches the expected error message.
    """
    # Simulate the absence of the CSV file
    monkeypatch.setattr(os.path, 'exists', lambda x: False)

    # Send a GET request to the endpoint
    response = client.get("/csv_creation_date")

    # Assert response status code is 404 when the file does not exist
    assert response.status_code == 404

    # Assert response JSON matches the expected error message
    assert response.json() == {"detail": "File CSV not found"}


def test_get_all_teachings():
    """
    Test the endpoint "/query/{location_str}/{degreetype_str}/{cycle_str}"
    to ensure it returns a dictionary of all teachings
    that match the query parameters.

    Parameters:
    location_str (str): The location of the courses to be queried.
    degreetype_str (str): The degree type of the courses to be queried.
    cycle_str (str): The cycle of the courses to be queried.

    Returns:
    None

    Raises:
    None

    Note:
    - This function sends a GET request to
      the "/query/{location_str}/{degreetype_str}/{cycle_str}" endpoint.
    - It asserts the response status code is 200 when the function works.
    - It asserts the response JSON matches
      the expected dictionary of teachings.
    """
    # Create sample returned list
    mock_teachings = "{\"E-BUSINESS, ENTREPRENEURSHIP AND DIGITAL TRANSFORMATION-1\": \"E-BUSINESS, ENTREPRENEURSHIP AND DIGITAL TRANSFORMATION-1\", \"E-BUSINESS, ENTREPRENEURSHIP AND DIGITAL TRANSFORMATION-2\": \"E-BUSINESS, ENTREPRENEURSHIP AND DIGITAL TRANSFORMATION-2\", \"ECONOMICS OF INNOVATION, GROWTH THEORY AND ECONOMICS DEVELOPMENT-2\": \"ECONOMICS OF INNOVATION, GROWTH THEORY AND ECONOMICS DEVELOPMENT-2\", \"ECONOMICS OF INNOVATION, GROWTH THEORY AND ECONOMICS DEVELOPMENT-2 PRACTICE\": \"ECONOMICS OF INNOVATION, GROWTH THEORY AND ECONOMICS DEVELOPMENT-2 PRACTICE\", \"FUNDAMENTALS OF IT LAW\": \"FUNDAMENTALS OF IT LAW\", \"INTRODUCTION TO DIGITAL MANAGEMENT-1\": \"INTRODUCTION TO DIGITAL MANAGEMENT-1\", \"INTRODUCTION TO DIGITAL MANAGEMENT-2\": \"INTRODUCTION TO DIGITAL MANAGEMENT-2\", \"INTRODUCTION TO DIGITAL MANAGEMENT-2 PRACTICE\": \"INTRODUCTION TO DIGITAL MANAGEMENT-2 PRACTICE\", \"LAB OF SOFTWARE PROJECT DEVELOPMENT\": \"LAB OF SOFTWARE PROJECT DEVELOPMENT\", \"LAB OF WEB TECHNOLOGIES\": \"LAB OF WEB TECHNOLOGIES\", \"MATHEMATICS FOR DECISION SCIENCES 1\": \"MATHEMATICS FOR DECISION SCIENCES 1\", \"MATHEMATICS FOR DECISION SCIENCES 1-PRACTICE\": \"MATHEMATICS FOR DECISION SCIENCES 1-PRACTICE\", \"MATHEMATICS FOR DECISION SCIENCES 2-PRACTICE\": \"MATHEMATICS FOR DECISION SCIENCES 2-PRACTICE\", \"MATHEMATICS FOR DECISION SCIENCES-2\": \"MATHEMATICS FOR DECISION SCIENCES-2\", \"ORGANIZING IN A DIGITAL WORLD\": \"ORGANIZING IN A DIGITAL WORLD\", \"PLANNING AND MANAGEMENT CONTROL SYSTEMS\": \"PLANNING AND MANAGEMENT CONTROL SYSTEMS\", \"PLANNING AND MANAGEMENT CONTROL SYSTEMS-PRACTICE\": \"PLANNING AND MANAGEMENT CONTROL SYSTEMS-PRACTICE\", \"STRATEGIC AND DIGITAL MARKETING\": \"STRATEGIC AND DIGITAL MARKETING\"}"

    # Define query parameters: testing with digital management courses
    location_str = 'RONCADE'
    degreetype_str = 'Bachelor'
    cycle_str = 'Fall Semester (Sep-Jan)'

    # Send a GET request
    query = f"/query/{location_str}/{degreetype_str}/{cycle_str}"
    response = client.get(query)

    # Assert response status code is 200 when the function works
    assert response.status_code == 200

    # Parse the JSON response into a dictionary
    actual_teachings = response.json()

    # Check if every keys are equal in teachings
    assert actual_teachings == mock_teachings


def test_get_all_teachings_empty():
    """
    Test the endpoint "/query/{location_str}/{degreetype_str}/{cycle_str}"
    to ensure it returns an empty dictionary
    when no courses match the query parameters.

    Parameters:
    location_str (str): The location of the courses to be queried.
    degreetype_str (str): The degree type of the courses to be queried.
    cycle_str (str): The cycle of the courses to be queried.

    Returns:
    None

    Raises:
    None

    Note:
    - This function sends a GET request to
      the "/query/{location_str}/{degreetype_str}/{cycle_str}" endpoint.
    - It asserts the response status code is 200 when the function works.
    - It asserts the response JSON matches an empty dictionary.
    """

    # Define query parameters: testing with digital management courses
    location_str = 'RONCADE'
    degreetype_str = 'Master'
    cycle_str = 'Fall Semester (Sep-Jan)'

    # Send a GET request
    query = f"/query/{location_str}/{degreetype_str}/{cycle_str}"
    response = client.get(query)

    # Assert response status code is 200 when the file exists
    assert response.status_code == 200

    # Check if the returned dictionary is empty
    empty_teachings = '{}'
    assert response.json() == empty_teachings


def test_get_teaching():
    """
    Test the endpoint "/query/{teaching_str}" to ensure it returns the correct
    course data based on the query parameter.

    Parameters:
    teaching_str (str): The name of the teaching to be queried.

    Returns:
    None

    Raises:
    None

    Note:
    - This function sends a GET request to
      the "/query/{teaching_str}" endpoint.
    - It asserts the response status code is 200 when the function works.
    - It asserts the response JSON matches the expected course data.
    """

    # Define query parameters: testing with a specific course
    test_teaching = "MATHEMATICS FOR DECISION SCIENCES 2-PRACTICE"

    # Send a GET request
    response = client.get(f"/query/{test_teaching}")

    # Assert response status code is 200 when the file exists
    assert response.status_code == 200

    # Extract the actual course data from the response
    choosen_teaching = response.json()

    # Check if the returned course data matches the expected course
    for key, value in choosen_teaching.items():
        assert value["TEACHING"] == test_teaching
