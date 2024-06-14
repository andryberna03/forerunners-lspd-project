import os
import sys
from fastapi.testclient import TestClient
from app.main import app
import datetime

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








# # testing the query. we will need to change but overall code is correct
# @patch('app.main.get_courses_taught_by_person')  # Mock the get_courses_taught_by_person function
# def test_get_courses_taught_by_person(mock_get_courses_taught_by_person):
#     # Create sample with two random lessons (details are correct)
#     mock_courses = {
#         '2636': {
#             'AF_ID': 472740,
#             'TEACHING': 'STORIA GRECA',
#             'CYCLE': 'Fall Semester (Sep-Jan)',
#             'PARTITION': 'Cognomi M-Z',
#             'SITE': 'VENEZIA',
#             'CREDITS': 12,
#             'DEGREE_TYPE': 'Bachelor',
#             'LECTURE_DAY': '2023-09-11',
#             'LECTURE_START': '08:45',
#             'LECTURE_END': '10:15',
#             'LECTURER_NAME': 'DE VIDO STEFANIA',
#             'CLASSROOM_NAME': 'Aula 24',
#             'LOCATION_NAME': 'San Sebastiano',
#             'ADDRESS': 'Dorsoduro 1686, Campo San Sebastiano, 30123 Venezia',
#             'DOCENTE_ID': 5593153,
#             'URL_DOCENTE': 'https://www.unive.it/data/persone/5593153',
#             'URLS_INSEGNAMENTO': 'https://www.unive.it/data/insegnamento/297018',
#             'START_ISO8601': '2023-09-11T08:45:00',
#             'END_ISO8601': '2023-09-11T11:00:00'}
#         # },
#         # '2410': {
#         #     'AF_ID': 480730,
#         #     'TEACHING': 'FILOLOGIA LATINA',
#         #     'CYCLE': 'Fall Semester (Sep-Jan)',
#         #     'PARTITION': '',
#         #     'SITE': 'VENEZIA',
#         #     'CREDITS': 6,
#         #     'DEGREE_TYPE': 'Master',
#         #     'LECTURE_DAY': '2023-09-12',
#         #     'LECTURE_START': '14:00',
#         #     'LECTURE_END': '15:30',
#         #     'LECTURER_NAME': 'VENUTI MARTINA CHIARA',
#         #     'CLASSROOM_NAME': 'Aula 1D',
#         #     'LOCATION_NAME': 'Polo didattico San Basilio (Magazzino 5)',
#         #     'ADDRESS': 'Dorsoduro Area Portuale, Salizada S. Basegio, Magazzino 5, 30123 Venezia',
#         #     'DOCENTE_ID': 12419991,
#         #     'URL_DOCENTE': 'https://www.unive.it/data/persone/12419991',
#         #     'URLS_INSEGNAMENTO': 'https://www.unive.it/data/insegnamento/448767',
#         #     'START_ISO8601': '2023-09-12T14:10:00',
#         #     'END_ISO8601': '2023-09-12T15:30:00',
#         # },
#     }

#     # Mock the return value of get_courses_taught_by_person to return the parameters object
#     mock_get_courses_taught_by_person.return_value = mock_courses

#     # Define query parameters
#     teaching = 'STORIA GRECA'
#     location_str = 'VENEZIA'
#     degreetype_str = 'Bachelor'
#     cycle_str = 'Fall Semester (Sep-Jan)'
#     credits_str = '12'

#     # Send a GET request
#     response = client.get(f"/query/{teaching}/{location_str}/{degreetype_str}/{cycle_str}/{credits_str}")


#     # Assert response status code is 200 wehn the file exists
#     assert response.status_code == 200

#      # Extract the actual course data from the response
#     assert response.json() == mock_courses

#     # 348959,ESERCITAZIONI DI LINGUA THAI 3 MOD.2A,Spring Semester (Feb-June),,VENEZIA,0,Bachelor,2024-05-23,08:45,10:15,JUNGSUKCHAROEN JUTARMAS,Aula Saoneria,Ca' Dolfin - Saoneria,"Dorsoduro 3825/D, 30123 Venezia",-1.0,https://www.unive.it/data/persone/-1,https://www.unive.it/data/insegnamento/348959,2024-05-23T08:45:00,2024-05-23T10:15:00 
#     # == 472730,STORIA GRECA,Fall Semester (Sep-Jan),Cognomi A-L,VENEZIA,12,Bachelor,2023-09-11,08:45,10:15,ANTONETTI CLAUDIA,Aula 24,San Sebastiano,"Dorsoduro 1686, Campo San Sebastiano, 30123 Venezia",-1.0,https://www.unive.it/data/persone/-1,https://www.unive.it/data/insegnamento/472730,2023-09-11T08:45:00,2023-09-11T10:15:00
#     # test fallisce al secondo assert. con questi parametri mi va a pescare la lezione di thai??? perchè???