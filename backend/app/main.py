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

from .mymodules.df_creating import df_creating

app = FastAPI()

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
    final_urls_dataframe = df_creating()
    final_urls_dataframe = final_urls_dataframe.fillna('null')
    return final_urls_dataframe.to_dict(orient='records')


# Funzione per ottenere la data di creazione del file CSV
def get_csv_creation_date():
    """
    This function retrieves the creation date of a CSV file.

    Parameters:
    None

    Returns:
    datetime.datetime: The creation date of the CSV file if it exists, otherwise None.

    Raises:
    None

    Note:
    The CSV file path is hardcoded as 'app/final.csv'.
    The function uses the os.path.exists() and os.path.getctime() methods to retrieve the file creation date.
    The creation date is converted from a timestamp to a datetime object using datetime.datetime.fromtimestamp().
    """
    file_path_final = 'app/final.csv'
    if os.path.exists(file_path_final):
        creation_time = os.path.getctime(file_path_final)
        file_creation_date = datetime.fromtimestamp(creation_time)
        return file_creation_date
    else:
        return None

# Endpoint per restituire la data di creazione del file CSV
@app.get("/csv_creation_date")
async def csv_creation_date(response: Response):
    """
    This function retrieves the creation date of the CSV file and sets a cookie with the date.

    Parameters:
    response (Response): The FastAPI Response object to set the cookie.

    Returns:
    str: The formatted creation date of the CSV file in 'Day, DD-MMM-YYYY HH:MM:SS TZ' format.

    Raises:
    HTTPException: If the CSV file does not exist, a 404 Not Found exception is raised.

    Note:
    The CSV file path is hardcoded as 'app/final.csv'.
    The function uses the os.path.exists() and os.path.getctime() methods to retrieve the file creation date.
    The creation date is converted from a timestamp to a datetime object using datetime.datetime.fromtimestamp().
    The datetime object is then converted to the 'Europe/Rome' timezone using pytz.timezone().
    The formatted date is set as a cookie with the name 'creation_date' using the Response.set_cookie() method.
    """
    creation_date = get_csv_creation_date()
    if creation_date:
        # Set the timezone to Rome
        rome_tz = pytz.timezone('Europe/Rome')
        # Convert the creation date to Rome timezone
        creation_date_rome = creation_date.astimezone(rome_tz)
        # Format the date in the required format
        cookie_date_format = creation_date_rome.strftime('%A, %d-%b-%Y %H:%M:%S %Z')
        # Set the cookie with the formatted date
        response.set_cookie(key='creation_date', value=cookie_date_format)
        return cookie_date_format
    else:
        raise HTTPException(status_code=404, detail="File CSV non trovato")


@app.get("/query/{teaching}/{location_str}/{degreetype_str}/{cycle_str}/{credits_str}")
def get_courses_taught_by_person(teaching, location_str, degreetype_str, cycle_str, credits_str):
    """
    """

    teaching = teaching.title()  # Convert to title case for consistency
    # Filter the DataFrame to rows where the person's name appears in the 'DOCENTI' column

    filtered_df = final_urls_dataframe

    # Filter by location: MESTRE, VENEZIA, RONCADE, TREVISO
    site_list = location_str.split(",") if location_str else []
    if site_list:
        filtered_df = filtered_df[filtered_df['SITE'].isin(site_list)]

    # Filter by DEGREE_TYPE
    # Dictionary to map the degree types to the corresponding codes in the DataFrame
    degree_mapping = {
        'Bachelor': 'Bachelor',
        'Master': 'Master'}

    # Convert the degreetype_list from friendly names to codes
    degreetype_list = degreetype_str.split(",") if degreetype_str else []
    code_list = []
    for degreetype in degreetype_list:
        code_list.append(degree_mapping[degreetype])
 
    if code_list:
        filtered_df = filtered_df[filtered_df['DEGREE_TYPE'].isin(code_list)]

    filtered_df = filtered_df[filtered_df['TEACHING'].str.contains(teaching, case=False, na=False)]

    filtered_df = filtered_df[filtered_df['CYCLE']==cycle_str]
    
    filtered_df = filtered_df[filtered_df['CREDITS']==int(credits_str)]

    filtered_df.fillna("null", inplace=True)

    filtered_dict = filtered_df.to_dict(orient='index')

    subset_final_json = JSONResponse(content=filtered_dict)

    return subset_final_json
