"""
Frontend module for the Flask application.

This module defines a simple Flask application that serves as the frontend for the project.
"""

from flask import Flask, render_template, jsonify
from flask_cors import CORS
import requests
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, validators

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'

# Configura CORS per consentire tutte le origini (*)
CORS(app)

# Configuration for the FastAPI backend URL
FASTAPI_BACKEND_HOST = 'http://backend'  # Replace with the actual URL of your FastAPI backend
BACKEND_URL = f'{FASTAPI_BACKEND_HOST}/query/'

class DatatimeCSV(object):
    datatime = None

class QueryForm(FlaskForm):
    location = SelectField('Location:', validators=[validators.DataRequired()])
    degreetype = SelectField('Degree type:', validators=[validators.DataRequired()])
    teaching = SelectField('Enter teaching name:', validators=[validators.DataRequired()])
    cycle = SelectField('Cycle:', validators=[validators.DataRequired()])
    credits = SelectField('Credits:', validators=[validators.DataRequired()])
    submit = SubmitField('View your lectures')

@app.route('/')
def index():
    """
    Render the index page.

    Returns:
        str: Rendered HTML content for the index page.
    """
    # Fetch the date from the backend
    return render_template('index.html')


@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    form = QueryForm()
    datatime_csv = DatatimeCSV()
    error_message = None

    creation_csv = f'{FASTAPI_BACKEND_HOST}/csv_creation_date'
    response_creation_csv = requests.get(creation_csv)
    datatime_creation_csv = response_creation_csv.json()
    datatime_csv.datatime = datatime_creation_csv

    # Fetch data from the backend and update form choices
    fastapi_url = f'{FASTAPI_BACKEND_HOST}/df_show'
    response = requests.get(fastapi_url)

    if response.status_code == 200:
        data = response.json()
        form.cycle.choices = get_unique_values(data, 'CYCLE')
        form.degreetype.choices = get_unique_values(data, 'DEGREE_TYPE')
        form.credits.choices = get_unique_values(data, 'CREDITS')
        form.location.choices = get_unique_values(data, 'SITE')
        form.teaching.choices = get_unique_values(data, 'TEACHING')
    else:
        error_message = "Error: Unable to fetch data from the backend."

    if form.validate_on_submit():
        teaching = form.teaching.data
        location_str = form.location.data
        degreetype_str = form.degreetype.data
        #academic_year_str = form.academic_year.data
        #cycle_str = form.cycle.data
        #credits_str = form.credits.data
        
        # Build URL
        fastapi_url = f'{FASTAPI_BACKEND_HOST}/query/{teaching}/{location_str}/{degreetype_str}'#/{cycle_str}/{credits_str}/{academic_year_str}'

        response = requests.get(fastapi_url)

        if response.status_code == 200:
            data = response.json()
            return render_template('calendar.html', datatime_csv=datatime_csv, form=form, result=data, error_message=error_message)
        else:
            error_message = f'Error: Unable to fetch lesson for {teaching} from FastAPI Backend'

    return render_template('calendar.html', datatime_csv=datatime_csv, form=form, result=None, error_message=error_message)


@app.route('/about')
def about():
    """
    """
    return render_template('about.html')


def get_unique_values(data, column_name):
    """
    Extract unique values from a specific column in JSON data.

    Args:
    data (dict or list): JSON data containing the column.
    column_name (str): Name of the column to extract unique values from.

    Returns:
    list: Unique values from the specified column.
    """
    unique_values = set()
    if isinstance(data, list):
        for entry in data:
            if column_name in entry and entry[column_name] is not None:  # Aggiungi questo controllo per evitare valori None
                unique_values.add(entry[column_name])
    elif isinstance(data, dict):
        if column_name in data:
            for entry in data[column_name]:
                if entry is not None:  # Aggiungi questo controllo per evitare valori None
                    unique_values.add(entry)
    return sorted(list(unique_values))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
