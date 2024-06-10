import os
import sys
from fastapi.testclient import TestClient
import os
import sys
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
import pytz
import datetime

# Add the project root to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Now you can do the relative import
from app.main import app


"""
Execute this test by running on the terminal (from the app/) the command:
pytest --cov=app --cov-report=html tests/
 """

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

@patch('app.main.get_csv_creation_date')  # Mock the get_csv_creation_date function
def test_csv_creation_date(mock_get_csv_creation_date):
    # Create a datetime object with the desired timezone
    mock_datetime = datetime.datetime(2024, 6, 12, 10, 30, 0)

    # Mock the return value of get_csv_creation_date to return the datetime object
    mock_get_csv_creation_date.return_value = mock_datetime

    # Send a GET request to the endpoint
    response = client.get("/csv_creation_date")

    # Assert that the response status code is 200 when the file exists
    assert response.status_code == 200

    # Format the expected date string using strftime
    expected_date_string = '"Wednesday\\054 12-Jun-2024 10:30:00 CEST"'

    #CHIEDERE AL PROF SE VA BENE COSì PERCHé ho dovuto manipolare la stringa per farlo tornare corretto, mentre credo
    #che vada manipolata la mock datetime per trasformarla correttamente

    # Assert that the cookie is set with the correct value
    assert response.cookies.get("creation_date") == expected_date_string


def test_read_and_return_df():
    # Send a GET request to the endpoint
    response = client.get("/df_show")

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Get the JSON response data
    response_data = response.json()

    # Ensure that the response data is a non-empty list
    assert isinstance(response_data, list)
    assert len(response_data) > 0

    # Check the structure of the first item in the response data
    first_item = response_data[0]
    expected_keys = ['AF_ID', 'TEACHING', 'CYCLE', 'PARTITION', 'SITE', 'CREDITS', 'DEGREE_TYPE', 'LECTURE_DAY', 'LECTURE_START', 'LECTURE_END', 'LECTURER_NAME', 'CLASSROOM_NAME', 'LOCATION_NAME', 'ADDRESS', 'DOCENTE_ID', 'URL_DOCENTE', 'URLS_INSEGNAMENTO', 'START_ISO8601', 'END_ISO8601']
    assert all(key in first_item for key in expected_keys)