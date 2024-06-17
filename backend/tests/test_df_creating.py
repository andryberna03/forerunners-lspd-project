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

# Test the function with an existing file that is more than a day old
def test_existing_file_recent(mocker):
    """
    Test the df_creating function with an existing file that is less than a day old.

    This test mocks the file system and pandas to simulate the presence of a recent file.

    Parameters:
    mocker: The pytest-mock mocker object.

    Asserts:
    The returned DataFrame matches the mock DataFrame.
    """
    # Mock os.path.exists to return True
    mocker.patch('os.path.exists', return_value=True)
    # Mock os.path.getctime to return a timestamp of 1 hour ago
    mocker.patch('os.path.getctime', return_value=(datetime.datetime.now() - datetime.timedelta(hours=1)).timestamp())
    # Mock pandas.read_csv to return a predefined DataFrame
    mock_df = pd.DataFrame({'A': [1, 2, 3]})
    mocker.patch('pandas.read_csv', return_value=mock_df)
    
    # Call the function with a dummy file path
    result_df = df_creating('app/dummy.csv')
    
    # Assert that the result DataFrame matches the mock DataFrame
    assert (result_df == mock_df).all().all()

# Test the function with an existing file that is more than a day old
def test_existing_file_old(mocker):
    """
    Test the df_creating function with an existing file that is more than a day old.

    This test mocks the file system and create_new_dataframe to simulate the presence of an old file.

    Parameters:
    mocker: The pytest-mock mocker object.

    Asserts:
    The returned DataFrame matches the mock DataFrame created by create_new_dataframe.
    """
    # Mock os.path.exists to return True
    mocker.patch('os.path.exists', return_value=True)
    # Mock os.path.getctime to return a timestamp of 2 days ago
    mocker.patch('os.path.getctime', return_value=(datetime.datetime.now() - datetime.timedelta(days=2)).timestamp())
    # Mock create_new_dataframe to return a predefined DataFrame
    mock_df = pd.DataFrame({'A': [4, 5, 6]})
    mocker.patch('app.mymodules.df_creating.create_new_dataframe', return_value=mock_df)
    
    # Call the function with a dummy file path
    result_df = df_creating('app/dummy.csv')
    
    # Assert that the result DataFrame matches the mock DataFrame created by create_new_dataframe
    assert (result_df == mock_df).all().all()

# Test the function when the file does not exist
def test_non_existing_file(mocker):
    """
    Test the df_creating function when the file does not exist.

    This test mocks the file system and create_new_dataframe to simulate the absence of a file.

    Parameters:
    mocker: The pytest-mock mocker object.

    Asserts:
    The returned DataFrame matches the mock DataFrame created by create_new_dataframe.
    """
    # Mock os.path.exists to return False
    mocker.patch('os.path.exists', return_value=False)
    # Mock create_new_dataframe to return a predefined DataFrame
    mock_df = pd.DataFrame({'A': [7, 8, 9]})
    mocker.patch('app.mymodules.df_creating.create_new_dataframe', return_value=mock_df)
    
    # Call the function with a dummy file path
    result_df = df_creating('app/dummy.csv')
    
    # Assert that the result DataFrame matches the mock DataFrame created by create_new_dataframe
    assert (result_df == mock_df).all().all()

#TESTING create_new_dataframe
def test_create_new_dataframe():
    """
    Test the create_new_dataframe function.

    This test checks if the DataFrame created by create_new_dataframe has the expected structure and content.

    Asserts:
    The result is a DataFrame.
    The DataFrame is not empty.
    The DataFrame has the expected headers.
    """
    # Define the expected headers for the DataFrame
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
    Test to verify that the file 'final.csv' was created within the last 24 hours.

    - Checks if the file 'final.csv' exists.
    - Retrieves the creation time of the file.
    - Calculates the current time and the time 24 hours ago.
    - Asserts that the file was created less than 24 hours ago.

    Requires the 'final.csv' file to exist for accurate testing.
    """
    file_path = 'app/final.csv'  # Ensure the correct path to your CSV file

    # Ensure the file exists before proceeding with the test
    assert os.path.exists(file_path), f"File '{file_path}' does not exist."

    # Obtain the creation time of the file
    creation_time = os.path.getctime(file_path)
    creation_time_dt = datetime.datetime.fromtimestamp(creation_time)
    now_dt = datetime.datetime.now()

    # Calculate 24 hours ago from now
    twenty_four_hours_ago = now_dt - datetime.timedelta(days=1)

    # Verify that the file was created less than 24 hours ago
    assert creation_time_dt > twenty_four_hours_ago, "Il file final.csv è stato creato più di 24 ore fa."


