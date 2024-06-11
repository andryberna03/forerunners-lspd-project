from app.mymodules.df_creating import df_creating

"""
Execute this test by running on the terminal (from the app/) the command:
pytest --cov=app --cov-report=html tests/
 """


#def test_dfcreating():

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

# now run pytest test_df_creating in the terminal 