"""
Backend module for the FastAPI application.

This module defines a FastAPI application that serves
as the backend for the project.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from .mymodules.df_creating import df_creating
import json
from fastapi.responses import JSONResponse

app = FastAPI()

# Configura CORS per consentire tutte le origini (*)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
            
    filtered_df = filtered_df[filtered_df['TEACHING'].str.contains(teaching, case=False, na=False)]
    
    # Creating the JSON structure for FullCalendar
    events = []
    for _, row in filtered_df.iterrows():
        event = {
            "title": f"{row['TEACHING']} - {row['PARTITION']}",
            "start": f"{row['LECTURE_DAY']}T{row['LECTURE_START']}",
            "end": f"{row['LECTURE_DAY']}T{row['LECTURE_END']}",
            "url": row['URLS_INSEGNAMENTO'],
            # You can add more properties here as needed
        }
        events.append(event)

    return events  
# dovremmo vedere json file classico con eventi nelle graffe con chiavi che vuole fullcalendar

@app.get('/get_teachings')
def get_teachings():
    """
    """
    # Crea una lista per memorizzare i risultati
    results = []

    # Itera su ogni riga del DataFrame
    for index, row in final_urls_dataframe.iterrows():
        # Controlla se il valore nella colonna 'partition' è 'null'
        if pd.isna(row['PARTITION']):
            # Se 'partition' è 'null', aggiungi solo il valore di 'TEACHING' a results
            results.append(row['TEACHING'])
        else:
            # Altrimenti, unisci le stringhe di 'TEACHING' e 'partition' con un trattino e aggiungi il risultato a results
            results.append(row['TEACHING'] + ' - ' + row['PARTITION'])

    # Elimina i duplicati dalla lista di risultati
    results_set = set(results)
    result_list = list(results_set)

    # Converti la lista di risultati in un DataFrame
    result_dataframe = pd.DataFrame({'result': result_list})

    return result_dataframe
