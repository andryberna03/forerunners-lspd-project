"""
Backend module for the FastAPI application.

This module defines a FastAPI application that serves
as the backend for the project.
"""

from fastapi import FastAPI
from fastapi import FastAPI
from .mymodules.df_creating import df_creating
import json

app = FastAPI()



@app.get('/csv_show')
def read_and_return_df():
    """
    """
    df = df_creating()
    return df

@app.get('/')
def read_root():
    """
    Root endpoint for the backend.

    Returns:
        dict: A simple greeting.
    """
    return {"Hello": "World"}

@app.get("/query/{insegnamento_name}/{location_str}")
def get_courses_taught_by_person(insegnamento_name, location_str):
    """

    """

    # Convert to title case for consistency

    insegnamento_name = insegnamento_name.title()  
    
    # Convert the comma-separated location string into a list
    luoghi_list = location_str.split(",") if location_str else []
    
    filtered_df = df_creating()

    
    if luoghi_list:
        filtered_df = filtered_df[filtered_df['LUOGO'].isin(luoghi_list)]
            
    insegnamenti = filtered_df[filtered_df['NOME_INSEGNAMENTO'].str.contains(insegnamento_name, case=False, na=False)]
    
    insegnamenti_dict = insegnamenti.to_dict(orient='index')

    subset_final_json = json.dumps(insegnamenti_dict, indent=4)

    return subset_final_json