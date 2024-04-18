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


@app.get('/df_show')
def read_and_return_df():
    """
    Read and return the dataframe created with df_creating module.

    Returns:
        DataFrame: Lectures dataframe.
    """
    df = df_creating()
    return df


@app.get("/query/{insegnamento_name}/{location_str}")
def get_courses_taught_by_person(insegnamento_name, location_str):
    """
    """
    
    insegnamento_name = insegnamento_name.title()  # Convert to title case for consistency
    # Filter the DataFrame to rows where the person's name appears in the 'DOCENTI' column
    
    # Convert the comma-separated locations string into a list
    luoghi_list = location_str.split(",") if location_str else []

    filtered_df = final_urls_dataframe

    if luoghi_list:
        filtered_df = filtered_df[filtered_df['LOCATION_NAME'].isin(luoghi_list)]
            
    insegnamenti = filtered_df[filtered_df['TEACHING'].str.contains(insegnamento_name, case=False, na=False)]
    
    insegnamenti_dict = insegnamenti.to_dict(orient='index')

    subset_final_json = json.dumps(insegnamenti_dict, indent=4)

    return subset_final_json

