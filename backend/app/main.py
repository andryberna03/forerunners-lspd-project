"""
Backend module for the FastAPI application.

This module defines a FastAPI application that serves
as the backend for the project.
"""

from fastapi import FastAPI
from .mymodules.df_creating import df_creating
import json
from fastapi.responses import JSONResponse

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
            
    teaching_select = filtered_df[filtered_df['TEACHING'].str.contains(teaching, case=False, na=False)]
    
    teaching_select_dict = teaching_select.to_dict(orient='index')

    #subset_final_json = json.dumps(teaching_select_dict, indent=4)
    subset_final_json = JSONResponse(content=teaching_select_dict)
    
    return subset_final_json

