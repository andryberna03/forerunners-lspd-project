"""
Backend module for the FastAPI application.

This module defines a FastAPI application that serves
as the backend for the project.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import os
import pytz
from datetime import datetime
import json

from .mymodules.df_creating import df_creating

app = FastAPI()
file_path_final = 'app/final.csv'

# Add Cross-Origin Resource Sharing (CORS) middleware to the FastAPI application.
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
def read_root():
    """
    Root endpoint for the backend.

    Returns:
        dict: A simple greeting.
    """
    return {"Hello": "World"}


final_urls_dataframe = pd.read_csv('app/final.csv')

@app.get('/df_show')
def read_and_return_df():
    """
    Read and return the dataframe created with df_creating module.

    Returns:
        DataFrame: Lectures dataframe.
    """
    final_urls_dataframe = df_creating(file_path_final)
    final_urls_dataframe = final_urls_dataframe.fillna('null')
    return final_urls_dataframe.to_dict(orient='records')


def get_csv_creation_date():
    """
    Returns the creation date of the 'final.csv' file.
    
    Returns:
        datetime: The creation date of the file if it exists, otherwise None.
    """
    if os.path.exists(file_path_final):
        creation_time = os.path.getctime(file_path_final)
        file_creation_date = datetime.fromtimestamp(creation_time)
        return file_creation_date
    else:
        return None

# Endpoint to return the creation date of the CSV file
@app.get("/csv_creation_date")
async def csv_creation_date():
    """
    Endpoint to get the creation date of the 'final.csv' file.
    
    Returns:
        str: The creation date of the file in the format 'A, dd-mmm-YYYY HH:MM:SS TZ'.
    
    Raises:
        HTTPException: If the CSV file is not found.
    """
    creation_date = get_csv_creation_date()
    if creation_date:
        # Set the timezone to Rome
        rome_tz = pytz.timezone('Europe/Rome')
        # Convert the creation date to Rome timezone
        creation_date_rome = creation_date.astimezone(rome_tz)
        # Format the date in the required format
        date_format = creation_date_rome.strftime('%A, %d-%b-%Y %H:%M:%S %Z')
        return date_format
    else:
        raise HTTPException(status_code=404, detail="CSV file not found")


@app.get("/query/{location}/{degreetype}/{cycle}")
def get_courses_taught_by_person(location, degreetype, cycle):
    """
    This function retrieves and returns a list of teachings based on the provided location, degree type, and cycle.

    Parameters:
    location (str): A comma-separated string of locations (MESTRE, VENEZIA, RONCADE, TREVISO). If empty, all locations are considered.
    degreetype (str): A comma-separated string of degree types (Bachelor, Master). If empty, all degree types are considered.
    cycle (str): The cycle to filter the teachings.

    Returns:
    str: A JSON string containing a dictionary of unique teachings.

    Note:
    The function filters the dataframe based on the provided parameters and returns a list of unique teachings.
    The degree types are mapped to their corresponding codes in the DataFrame.
    The function fills any missing values in the dataframe with the string 'null'.
    """
    filtered_df = final_urls_dataframe

    # Filter by location
    site_list = location.split(",") if location else []
    if site_list:
        filtered_df = filtered_df[filtered_df['SITE'].isin(site_list)]

    # Filter by degreetype
    # Dictionary to map the degree types to the corresponding codes in the DataFrame
    degree_mapping = {
        'Bachelor': 'Bachelor',
        'Master': 'Master'}

    # Convert the degreetype_list from friendly names to codes
    degreetype_list = degreetype.split(",") if degreetype else []
    code_list = []
    for degreetype in degreetype_list:
        code_list.append(degree_mapping[degreetype])
 
#     if code_list:
#         filtered_df = filtered_df[filtered_df['DEGREE_TYPE'].isin(code_list)]

    filtered_df = filtered_df[filtered_df['CYCLE'] == cycle]

    filtered_df.fillna("null", inplace=True)

    teachings = filtered_df['TEACHING']

    final_teachings = dict()
    for teaching in teachings:
        final_teachings[teaching] = teaching

    final_teachings = json.dumps(final_teachings)

    return final_teachings


@app.get("/query/{final_teaching}")
def get_teaching(final_teaching):
    """
    This function retrieves and returns a specific teaching record from the dataframe.

    Parameters:
    final_teaching (str): The unique identifier of the teaching record to retrieve.

    Returns:
    JSONResponse: A JSON response containing the details of the specified teaching record.

    Note:
    The function filters the dataframe based on the 'TEACHING' column and the provided 'final_teaching' parameter.
    It then fills any missing values in the dataframe with the string 'null'.
    The filtered dataframe is converted to a dictionary with 'index' orientation, and a JSON response is created using the dictionary.
    The JSON response is then returned.
    """

    # Filter the dataframe based on the 'TEACHING' column and the provided 'final_teaching' parameter
    filtered_df = final_urls_dataframe[final_urls_dataframe['TEACHING'] == final_teaching]

    # Fill any missing values in the dataframe with the string 'null'
    filtered_df.fillna("null", inplace=True)

    # Convert the filtered dataframe to a dictionary with 'index' orientation
    filtered_dict = filtered_df.to_dict(orient='index')

    # Create a JSON response using the dictionary
    subset_final_json = JSONResponse(content=filtered_dict)

    # Return the JSON response
    return subset_final_json
