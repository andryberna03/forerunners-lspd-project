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
import datetime
import pytz

from .mymodules.df_creating import df_creating

app = FastAPI()

# Configura CORS per consentire tutte le origini (*)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)


@app.get('/')
def read_root():
    """
    Root endpoint for the backend.

    Returns:
        dict: A simple greeting.+
    """
    return {"Hello": "World"}

final_urls_dataframe = df_creating()

@app.get('/df_show')
def read_and_return_df():
    """
    Read and return the dataframe created with df_creating module.

    Returns:
        DataFrame: Lectures dataframe.
    """
    final_urls_dataframe = df_creating()
    final_urls_dataframe = final_urls_dataframe.fillna('')
    return final_urls_dataframe.to_dict(orient='records')

# Funzione per ottenere la data di creazione del file CSV
def get_csv_creation_date():
    file_path_final = 'app/final.csv'
    if os.path.exists(file_path_final):
        creation_time = os.path.getctime(file_path_final)
        file_creation_date = datetime.datetime.fromtimestamp(creation_time)
        return file_creation_date
    else:
        return None

# Endpoint per restituire la data di creazione del file CSV
@app.get("/csv_creation_date")
async def csv_creation_date(response: Response):
    creation_date = get_csv_creation_date()
    if creation_date:
        # Impostiamo il fuso orario di Roma
        rome_tz = pytz.timezone('Europe/Rome')
        # Convertiamo la data nel fuso orario di Roma
        creation_date_rome = creation_date.astimezone(rome_tz)
        # Formattiamo la data nel formato richiesto per il cookie
        cookie_date_format = creation_date_rome.strftime('%A, %d-%b-%Y %H:%M:%S %Z')
        # Impostiamo il cookie con il nome 'creation_date' e il valore della data formattata
        response.set_cookie(key='creation_date', value=cookie_date_format)
        return cookie_date_format
    else:
        raise HTTPException(status_code=404, detail="File CSV non trovato")


@app.get("/query/{teaching}/{location_str}/{degreetype_str}")
def get_courses_taught_by_person(teaching, location_str,degreetype_str):
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
        'LM': 'LM',
        'L': 'L'}

    # Convert the degreetype_list from friendly names to codes
    degreetype_list = degreetype_str.split(",") if degreetype_str else []
    code_list = []
    for degreetype in degreetype_list:
        code_list.append(degree_mapping[degreetype])
 
    if code_list:
        filtered_df = filtered_df[filtered_df['DEGREE_TYPE'].isin(code_list)]
            
    teaching_select = filtered_df[filtered_df['TEACHING'].str.contains(teaching, case=False, na=False)]
    
    teaching_select.fillna("null", inplace=True)

    teaching_select_dict = teaching_select.to_dict(orient='index')

    #subset_final_json = json.dumps(teaching_select_dict, indent=4)
    subset_final_json = JSONResponse(content=teaching_select_dict)
    
    return subset_final_json
