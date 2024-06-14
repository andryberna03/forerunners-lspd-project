import os
import datetime
from app.mymodules.df_creating import df_creating, create_new_dataframe
import pandas as pd
import pytest
"""
Execute this test by running on the terminal (from the app/) the command:
pytest --cov=app --cov-report=html tests/
 """
file_path = 'app/final.csv'

#TESTING df_creating

# Test the function with an existing file that is less than a day old
def test_existing_file_recent(mocker):
    mocker.patch('os.path.exists', return_value=True)
    mocker.patch('os.path.getctime', return_value=(datetime.datetime.now() - datetime.timedelta(hours=1)).timestamp())
    mock_df = pd.DataFrame({'A': [1, 2, 3]})
    mocker.patch('pandas.read_csv', return_value=mock_df)
    
    result_df = df_creating('app/dummy.csv')
    
    assert (result_df == mock_df).all().all()

# Test the function with an existing file that is more than a day old
def test_existing_file_old(mocker):
    mocker.patch('os.path.exists', return_value=True)
    mocker.patch('os.path.getctime', return_value=(datetime.datetime.now() - datetime.timedelta(days=2)).timestamp())
    mock_df = pd.DataFrame({'A': [4, 5, 6]})
    mocker.patch('app.mymodules.df_creating.create_new_dataframe', return_value=mock_df)
    
    result_df = df_creating('app/dummy.csv')
    
    assert (result_df == mock_df).all().all()

# Test the function when the file does not exist
def test_non_existing_file(mocker):
    mocker.patch('os.path.exists', return_value=False)
    mock_df = pd.DataFrame({'A': [7, 8, 9]})
    mocker.patch('app.mymodules.df_creating.create_new_dataframe', return_value=mock_df)
    
    result_df = df_creating('app/dummy.csv')
    
    assert (result_df == mock_df).all().all()

#TESTING create_new_dataframe
def test_create_new_dataframe():
    expected_header = [
        "AF_ID", "TEACHING", "CYCLE", "PARTITION", "SITE", "CREDITS", "DEGREE_TYPE",
        "LECTURE_DAY", "LECTURE_START", "LECTURE_END", "LECTURER_NAME", "CLASSROOM_NAME",
        "LOCATION_NAME", "ADDRESS", "DOCENTE_ID", "URL_DOCENTE", "URLS_INSEGNAMENTO",
        "START_ISO8601", "END_ISO8601"
    ]
    
    # Call the function to create the DataFrame
    result_df = create_new_dataframe('app/dummy.csv')
    
    # Assert that the result is a DataFrame
    assert isinstance(result_df, pd.DataFrame), "The result should be a DataFrame."
    
    # Assert that the DataFrame is not empty
    assert not result_df.empty, "The DataFrame should not be empty."
    
    # Assert that the DataFrame has the expected headers
    assert list(result_df.columns) == expected_header, "The DataFrame headers do not match the expected headers."
    
    # # Define the expected types for each column
    # expected_types = {
    #     "AF_ID": int,
    #     "TEACHING": str,
    #     "CYCLE": str,
    #     "SITE": str,
    #     "CREDITS": int,
    #     "DEGREE_TYPE": str,
    #     "LECTURE_DAY": str,
    #     "LECTURE_START": str,
    #     "LECTURE_END": str,
    #     "CLASSROOM_NAME": str,
    #     "LOCATION_NAME": str,
    #     "DOCENTE_ID": int,
    #     "URL_DOCENTE": str,
    #     "URLS_INSEGNAMENTO": str,
    #     "START_ISO8601": str,
    #     "END_ISO8601": str
    # }
    
    # # Assert that the columns have the expected types
    # for column, expected_type in expected_types.items():
    #     for item in result_df[column]:
    #         assert isinstance(item, expected_type), f"Column {column} should be of type {expected_type}."


#TESTING final.csv
def test_file_is_csv():
    """
    Test to verify that the file at 'app/final.csv' is a valid CSV file with the expected header.

    - Checks if the file exists.
    - Attempts to read the file using pandas to ensure it's a valid CSV.
    - Asserts that the header row of the CSV matches the expected header list.
    """
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
    """
    Test to verify that the file 'app/final.csv' was created within the last 24 hours.

    - Checks if the file 'app/final.csv' exists.
    - Retrieves the creation time of the file.
    - Calculates the current time and the time 24 hours ago.
    - Asserts that the file was created less than 24 hours ago.

    Requires the 'app/final.csv' file to exist for accurate testing.
    """
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
