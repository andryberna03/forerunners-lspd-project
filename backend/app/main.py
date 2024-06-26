"""
Backend module for the FastAPI application.

This module defines a FastAPI application that serves
as the backend for the project.
"""


from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from fastapi.responses import JSONResponse
import pandas as pd
import os
import pytz
from datetime import datetime
import json

from .mymodules.df_creating import df_creating

app = FastAPI()

# Add Cross-Origin Resource Sharing (CORS) middleware to the FastAPI app.
# This middleware allows all origins to access the API endpoints.
# It also allows credentials, all HTTP methods, and all headers.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,  # Allow credentials
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


@app.get('/')
def read_root() -> dict:
    """
    Root endpoint for the backend.

    Returns:
        dict: A simple greeting.
    """
    return {"Hello": "World"}


final_path_csv = 'app/final.csv'
final_urls_dataframe = pd.read_csv(final_path_csv)


@app.get('/df_show')
def read_and_return_df():
    """
    Read and return the dataframe created with the df_creating module.

    Returns:
        list: A list of dictionaries representing the lectures dataframe.
    """
    # Create or load the DataFrame using the df_creating module
    final_urls_dataframe = df_creating(final_path_csv)
    # Fill NaN values with 'null'
    final_urls_dataframe = final_urls_dataframe.fillna('null')
    # Convert DataFrame to a list of dictionaries and return
    return final_urls_dataframe.to_dict(orient='records')


def get_csv_creation_date():
    """
    Retrieve the creation date of a CSV file.

    This function checks if a CSV file exists
    at the hardcoded path 'app/final.csv'.
    If the file exists, it retrieves and returns
    the creation dateas a datetime object.
    Returns:
        datetime: The creation date of the CSV file
        if it exists, otherwise None.
    Note:
        The function uses os.path.exists() and os.path.getctime() to check
        the file existenceand get the creation time.
        The creation time is converted from a timestamp
        to a datetime object using datetime.fromtimestamp().
    """
    file_path_final = 'app/final.csv'
    if os.path.exists(file_path_final):
        # Get the creation time of the file
        creation_time = os.path.getctime(file_path_final)
        # Convert the creation time from a timestamp to a datetime object
        file_creation_date = datetime.fromtimestamp(creation_time)
        return file_creation_date
    else:
        return None


@app.get("/csv_creation_date")
async def csv_creation_date():
    """
    Retrieve the creation date of the CSV file
    and set a cookie with the date.

    This endpoint retrieves the creation date of the CSV file
    at the hardcoded path 'app/final.csv'.If the file exists,
    it formats the creation date in 'Day, DD-MMM-YYYY HH:MM:SS TZ' format,
    sets it as a cookie named 'creation_date', and returns the formatted date.

    Returns:
        str: The formatted creation date of the CSV file in 'Day,
        DD-MMM-YYYY HH:MM:SS TZ' format.

    Raises:
        HTTPException: If the CSV file does not exist,
        a 404 Not Found exception is raised.

    Note:
        The function uses os.path.exists() and os.path.getctime() to check
        the file existence and get the creation time.
        The creation time is converted from a timestamp to a datetime
        object using datetime.fromtimestamp().
        The datetime object is then converted to the
        'Europe/Rome' timezone using pytz.timezone().
        The formatted date is set as a cookie using Response.set_cookie().
    """
    # Get the creation date of the CSV file
    creation_date = get_csv_creation_date()
    if creation_date:
        # Set the timezone to Rome
        rome_tz = pytz.timezone('Europe/Rome')
        # Convert the creation date to Rome timezone
        creation_date_rome = creation_date.astimezone(rome_tz)
        # Format the date in the required format
        cookie_date_format = creation_date_rome.strftime(
            '%A, %d-%b-%Y %H:%M:%S %Z'
        )
        return cookie_date_format
    else:
        # Raise a 404 Not Found exception if the CSV file does not exist
        raise HTTPException(status_code=404, detail="File CSV not found")


@app.get("/query/{location}/{degreetype}/{cycle}")
def get_all_teachings(location: str, degreetype: str, cycle: str) -> str:
    """
    Retrieve and return a list of unique teachings
    based on location, degree type, and cycle.

    Parameters:
    location (str): The location of the teachings.
    degreetype (str): The type of degree.
    cycle (str): The cycle of the teachings.

    Returns:
    str: A JSON string containing a list of unique teachings.

    Note:
    This function filters the dataframe based on the provided parameters,
    extracts the unique teachings, and returns them as a sorted JSON string.
    """
    # Filter the dataframe based on the provided parameters
    filtered_df = final_urls_dataframe[
        final_urls_dataframe['DEGREE_TYPE'] == degreetype
    ]
    filtered_df = filtered_df[filtered_df['SITE'] == location]
    filtered_df = filtered_df[filtered_df['CYCLE'] == cycle]

    # Fill any missing values in the dataframe with the string 'null'
    filtered_df.fillna("null", inplace=True)

    # Extract the unique teachings from the filtered dataframe
    teachings = filtered_df['TEACHING']

    # Create a dictionary with unique teachings
    final_teachings = dict()
    for teaching in teachings:
        final_teachings[teaching] = teaching

    # Sort the dictionary
    final_teachings = dict(sorted(final_teachings.items()))

    # Convert the dictionary to a JSON string
    final_teachings = json.dumps(final_teachings)

    # Return the JSON string
    return final_teachings


@app.get("/query/{final_teaching}")
def get_teaching(final_teaching: str):
    """
    Retrieve and return a specific teaching record from the dataframe.

    Parameters:
    final_teaching (str):
    The unique identifier of the teaching record to retrieve.

    Returns:
    JSONResponse:
    A JSON response containing the details of the specified teaching record.

    Note:
    The function filters the dataframe based on the 'TEACHING' column
    and the provided 'final_teaching' parameter.
    It then fills any missing values in the dataframe with the string 'null'.
    The filtered dataframe is converted to a dictionary
    with 'index' orientation,and a JSON response is created
    using the dictionary.The JSON response is then returned.
    """
    # Filter the dataframe based on the 'TEACHING' column
    # and on provided 'final_teaching' parameter
    filtered_df = final_urls_dataframe[
        final_urls_dataframe['TEACHING'] == final_teaching
    ]

    # Fill any missing values in the dataframe with the string 'null'
    filtered_df.fillna("null", inplace=True)

    # Convert the filtered dataframe to a dictionary with 'index' orientation
    filtered_dict = filtered_df.to_dict(orient='index')

    # Create a JSON response using the dictionary
    subset_final_json = JSONResponse(content=filtered_dict)

    # Return the JSON response
    return subset_final_json
