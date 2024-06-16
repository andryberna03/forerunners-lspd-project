from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

"""
Execute this test by running on the terminal (from the app/) the command:
pytest --cov=app --cov-report=html tests/
"""

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
    Test the endpoint "/df_show" to ensure it returns a DataFrame-like JSON structure.

    Sends a GET request to "/df_show" and performs the following checks:
    - Asserts that the response status code is 200.
    - Verifies that the response data is a non-empty list.
    - Checks that the structure of the first item in the response matches the expected keys.
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
    expected_keys = ['AF_ID', 'TEACHING', 'CYCLE', 'PARTITION', 'SITE', 'CREDITS', 'DEGREE_TYPE', 'LECTURE_DAY', 'LECTURE_START', 'LECTURE_END', 'LECTURER_NAME', 'CLASSROOM_NAME', 'LOCATION_NAME', 'ADDRESS', 'DOCENTE_ID', 'URL_DOCENTE', 'URLS_INSEGNAMENTO', 'START_ISO8601', 'END_ISO8601']

    # Check the structure and non-empty values for each item in the response data
    for item in response_data:
        # Ensure all expected keys are present in the item
        assert all(key in item for key in expected_keys)
        
        # Ensure none of the values corresponding to the keys are empty
        assert all(item[key] is not None and item[key] != '' for key in expected_keys)


#not ok
def test_csv_creation_date():
    """
    """
    response = client.get("/csv_creation_date")

    assert response.status_code == 200

    # QUI DEVO CAPIRE CHE ASSERT DEVO FARE, PER IL FORMAT? %A, %d-%b-%Y %H:%M:%S %Z


@patch("app.main.get_all_teachings")  # Mock the get_all_teachings function
def test_get_all_teachings(mock_get_all_teachings):
    # Create sample returned list
    mock_teachings = "{\"MATHEMATICS FOR DECISION SCIENCES 2-PRACTICE\": \"MATHEMATICS FOR DECISION SCIENCES 2-PRACTICE\", \"INTRODUCTION TO DIGITAL MANAGEMENT-1\": \"INTRODUCTION TO DIGITAL MANAGEMENT-1\", \"LAB OF WEB TECHNOLOGIES\": \"LAB OF WEB TECHNOLOGIES\", \"INTRODUCTION TO DIGITAL MANAGEMENT-2\": \"INTRODUCTION TO DIGITAL MANAGEMENT-2\", \"STRATEGIC AND DIGITAL MARKETING\": \"STRATEGIC AND DIGITAL MARKETING\", \"E-BUSINESS, ENTREPRENEURSHIP AND DIGITAL TRANSFORMATION-2\": \"E-BUSINESS, ENTREPRENEURSHIP AND DIGITAL TRANSFORMATION-2\", \"INTRODUCTION TO DIGITAL MANAGEMENT-2 PRACTICE\": \"INTRODUCTION TO DIGITAL MANAGEMENT-2 PRACTICE\", \"MATHEMATICS FOR DECISION SCIENCES-2\": \"MATHEMATICS FOR DECISION SCIENCES-2\", \"MATHEMATICS FOR DECISION SCIENCES 1\": \"MATHEMATICS FOR DECISION SCIENCES 1\", \"LAB OF SOFTWARE PROJECT DEVELOPMENT\": \"LAB OF SOFTWARE PROJECT DEVELOPMENT\", \"MATHEMATICS FOR DECISION SCIENCES 1-PRACTICE\": \"MATHEMATICS FOR DECISION SCIENCES 1-PRACTICE\", \"FUNDAMENTALS OF IT LAW\": \"FUNDAMENTALS OF IT LAW\", \"PLANNING AND MANAGEMENT CONTROL SYSTEMS\": \"PLANNING AND MANAGEMENT CONTROL SYSTEMS\", \"E-BUSINESS, ENTREPRENEURSHIP AND DIGITAL TRANSFORMATION-1\": \"E-BUSINESS, ENTREPRENEURSHIP AND DIGITAL TRANSFORMATION-1\", \"ECONOMICS OF INNOVATION, GROWTH THEORY AND ECONOMICS DEVELOPMENT-2\": \"ECONOMICS OF INNOVATION, GROWTH THEORY AND ECONOMICS DEVELOPMENT-2\", \"ORGANIZING IN A DIGITAL WORLD\": \"ORGANIZING IN A DIGITAL WORLD\", \"ECONOMICS OF INNOVATION, GROWTH THEORY AND ECONOMICS DEVELOPMENT-2 PRACTICE\": \"ECONOMICS OF INNOVATION, GROWTH THEORY AND ECONOMICS DEVELOPMENT-2 PRACTICE\", \"PLANNING AND MANAGEMENT CONTROL SYSTEMS-PRACTICE\": \"PLANNING AND MANAGEMENT CONTROL SYSTEMS-PRACTICE\"}"
    
    # Mock the return value of get_all_teachings
    mock_get_all_teachings.return_value = mock_teachings

    # Define query parameters: testing with digital management courses
    location_str = 'RONCADE'
    degreetype_str = 'Bachelor'
    cycle_str = 'Fall Semester (Sep-Jan)'

    # Send a GET request
    response = client.get(f"/query/{location_str}/{degreetype_str}/{cycle_str}")

    # Assert response status code is 200 when the file exists
    assert response.status_code == 200

    # Parse the JSON response into a dictionary
    actual_teachings = response.json()

    # Check if every key in actual_teachings is in mock_teachings and vice versa
    assert actual_teachings == mock_teachings

    # No need to test "if"s of this query because the options of the filters
    # are generated from the dataframe itself.

# Testing if there are no teachings corrisponding to filters --> PASSED!!!
# If I imput Master and then Roncade it should yield empty list. 
@patch("app.main.get_all_teachings") #Mock the get_all_teaching function
def test_get_all_teachings_empty(mock_get_all_teachings):

    empty_teachings = '{}'
    # Mock the return value to be an empty JSON object
    mock_get_all_teachings.return_value = empty_teachings

    # Define query parameters: testing with digital management courses
    location_str = 'RONCADE'
    degreetype_str = 'Master'
    cycle_str = 'Fall Semester (Sep-Jan)'

    # Send a GET request
    response = client.get(f"/query/{location_str}/{degreetype_str}/{cycle_str}")

    assert response.json() == empty_teachings




def test_get_teaching():
    # Define query parameters: testing with digital management courses
    test_teaching = "MATHEMATICS FOR DECISION SCIENCES 2-PRACTICE"

    # Send a GET request
    response = client.get(f"/query/{test_teaching}")

    # Assert response status code is 200 when the file exists
    assert response.status_code == 200

     # Extract the actual course data from the response
    choosen_teaching = response.json()

    for key, value in choosen_teaching.items():
        assert value["TEACHING"] == test_teaching

    