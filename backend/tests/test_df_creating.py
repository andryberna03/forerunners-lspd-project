
import os
import datetime
from unittest.mock import patch
from app.mymodules.df_creating import df_creating
import pandas as pd
import pytest
"""
Execute this test by running on the terminal (from the app/) the command:
pytest --cov=app --cov-report=html tests/
 """
file_path = 'app/final.csv'



def test_file_is_csv():
    expected_header = [
    "AF_ID", "TEACHING", "CYCLE", "PARTITION", "SITE", "CREDITS", "DEGREE_TYPE",
    "LECTURE_DAY", "LECTURE_START", "LECTURE_END", "LECTURER_NAME", "CLASSROOM_NAME",
    "LOCATION_NAME", "ADDRESS", "DOCENTE_ID", "URL_DOCENTE", "URLS_INSEGNAMENTO",
    "START_ISO8601", "END_ISO8601"]

    # Check if the file exists
    assert os.path.exists(file_path), f"File {file_path} does not exist."

    # Check if the file is a CSV by attempting to read it with pandas
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        pytest.fail(f"File {file_path} is not a valid CSV file. Error: {e}")

    # Check if the header row matches the expected header
    assert list(df.columns) == expected_header, \
        f"CSV header does not match expected header. Found: {list(df.columns)}, Expected: {expected_header}"



def test_file_created_within_24_hours():
    # Verificare che il file esiste
    assert os.path.exists(file_path), "Il file final.csv non esiste."

    # Ottenere il tempo di creazione del file
    file_stat = os.stat(file_path)
    creation_time = file_stat.st_ctime

    # Calcolare l'ora corrente e l'intervallo di 24 ore fa
    now = datetime.datetime.now().timestamp()
    twenty_four_hours_ago = now - 24 * 60 * 60

    # Verificare che il file sia stato creato meno di 24 ore fa
    assert creation_time > twenty_four_hours_ago, "Il file final.csv è stato creato più di 24 ore fa."


# # Test 2: Test for non-existing file

# # Test 3: Test for outdated file


# # Test 4: Test for API requests
# @patch('app.mymodules.df_creating.requests.get')
# def test_api_requests(mock_get):
#     # Mock API responses
#     mock_responses = {
#         'degrees': {'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']},
#         # Add mock responses for other URLs as needed
#     }
#     mock_get.side_effect = lambda url: mock_responses[url.split('/')[-1]]
#     # Call df_creating and assert it retrieves data from mocked responses
#     final_df = df_creating()
#     expected_df = pd.DataFrame(mock_responses['degrees'])
#     assert final_df.equals(expected_df)

# # Test 5: Test for data consistency and correctness
# def test_data_consistency_and_correctness():
#     # Call df_creating
#     final_df = df_creating()
#     # Perform assertions to check data consistency and correctness
#     # For example, check column names, data types, presence of expected data, etc.

import csv
import os
import pytest

# Define the path to your CSV file relative to the location of this script
CSV_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'app', 'final.csv')

def test_csv_file_exists():
    assert os.path.isfile(CSV_FILE_PATH), f"CSV file not found at: {CSV_FILE_PATH}"

def test_csv_file_format():
    # Assuming the CSV file should have at least one row and one column
    with open(CSV_FILE_PATH, 'r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader, None)  # Read the header row
        assert header is not None, "CSV file is empty"
        assert len(header) > 0, "CSV file should have at least one column"
        # You can add more specific format checks if needed
        # For example, check if the header contains specific column names

# Additional setup if required by pytest
# if __name__ == "__main__":
#   pytest.main()

