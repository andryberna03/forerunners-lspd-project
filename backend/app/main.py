"""
Backend module for the FastAPI application.

This module defines a FastAPI application that serves
as the backend for the project.
"""

from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime
import pandas as pd
from fastapi import Query
from .mymodules.df_creating import df_creating
import json

app = FastAPI()


@app.get('/')
def read_root():
    """
    Root endpoint for the backend.

    Returns:
        dict: A simple greeting.
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
    return final_urls_dataframe


@app.get("/query/{insegnamento_name}/{location_str}/{degreetype_str}")
def get_courses_taught_by_person(insegnamento_name, location_str,degreetype_str):
    """
    """
    
    insegnamento_name = insegnamento_name.title()  # Convert to title case for consistency
    # Filter the DataFrame to rows where the person's name appears in the 'DOCENTI' column
    
    filtered_df = final_urls_dataframe
    
    # Filter by location: MESTRE, VENEZIA, RONCADE, TREVISO
    luoghi_list = location_str.split(",") if location_str else []
    if luoghi_list:
        filtered_df = filtered_df[filtered_df['SITE'].isin(luoghi_list)]

    # Filter by DEGREE_TYPE
    # Dictionary to map the degree types to the corresponding codes in the DataFrame
    degree_mapping = {
        'MASTER': 'LM',
        'BACHELOR': 'L',
        'OTHER': ['MINOR', 'CP', 'CF-270', 'M2-270', 'M-CR', 'D2', 'ADCO']
    }

    # Convert the degreetype_list from friendly names to codes
    degreetype_list = degreetype_str.split(",") if degreetype_str else []
    code_list = []
    for degreetype in degreetype_list:
        code_list.append(degree_mapping[degreetype])
 
    if code_list:
        filtered_df = filtered_df[filtered_df['DEGREE_TYPE'].isin(code_list)]
            
    insegnamenti = filtered_df[filtered_df['TEACHING'].str.contains(insegnamento_name, case=False, na=False)]
    
    insegnamenti_dict = insegnamenti.to_dict(orient='index')

    subset_final_json = json.dumps(insegnamenti_dict, indent=4)

    return subset_final_json

