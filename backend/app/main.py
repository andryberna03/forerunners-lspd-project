"""
Backend module for the FastAPI application.

This module defines a FastAPI application that serves
as the backend for the project.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from fastapi.responses import JSONResponse
import pandas as pd

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
    
    teaching_select_dict = teaching_select.to_dict(orient='index')

    #subset_final_json = json.dumps(teaching_select_dict, indent=4)
    subset_final_json = JSONResponse(content=teaching_select_dict)
    
    return subset_final_json
