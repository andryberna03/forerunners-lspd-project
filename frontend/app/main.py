"""
Frontend module for the Flask application.

This module defines a simple Flask application that serves
as the frontend for the project.
"""

from flask import Flask, render_template
from flask_cors import CORS
import requests
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
import json

app = Flask(__name__)
# Replace with a secure secret key
app.config['SECRET_KEY'] = 'your_secret_key'

"""
Configure Cross-Origin Resource Sharing (CORS) for the Flask application.

CORS is a mechanism that allows a server to indicate any other origins
(domain, scheme, or port)that are permitted to access the server's resources.
By default, Flask does not enable CORS,so this line of code is necessary to
allow all origins to access the application.
"""
CORS(app)


# Configuration for the FastAPI backend URL
FASTAPI_BACKEND_HOST = 'http://backend'
BACKEND_URL = f'{FASTAPI_BACKEND_HOST}/query/'


class DatatimeCSV(object):
    """
    A simple class to hold the date and time of a CSV file.

    Attributes:
    datatime (str): The date and time of the CSV file.
    """
    datatime = None


class QueryTeachings(FlaskForm):
    """
    A Flask-WTF form for querying lectures based on various parameters.

    Attributes:
    location (SelectField): A dropdown menu for selecting the location.
    degreetype (SelectField): A dropdown menu for selecting the degree type.
    cycle (SelectField): A dropdown menu for selecting the cycle.
    submit (SubmitField): A button for submitting the form.
    """
    location = SelectField('Location:')
    degreetype = SelectField('Degree type:')
    cycle = SelectField('Cycle:')
    submit = SubmitField('View your teachings')


class QueryLectures(FlaskForm):
    """
    A Flask-WTF form for querying lectures based on various parameters.

    Attributes:
    teaching (SelectField): A dropdown menu for selecting the teaching name.
    submit_teaching (SubmitField): A button for submitting the form.
    """
    teaching = SelectField('Enter teaching name:')
    submit_teaching = SubmitField('View your lectures')


@app.route('/')
def index():
    """
    Render the index page.

    Returns:
        str: Rendered HTML content for the index page.
    """
    # Fetch the date from the backend
    return render_template('index.html')


@app.route('/about')
def about():
    """
    Render the about page.

    Returns:
        str: Rendered HTML content for the about page.
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
            if column_name in entry and entry[column_name] is not None:
                unique_values.add((entry[column_name], entry[column_name]))
    elif isinstance(data, dict):
        if column_name in data:
            for entry in data[column_name]:
                if entry is not None:
                    unique_values.add((entry, entry))
    return sorted(list(unique_values))


@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    """
    Handle the '/calendar' route of the Flask application.

    Fetches data from the backend, updates form choices,
    and processes form submissions.

    Returns:
        str: Rendered HTML content for the '/calendar' page.
    """
    datatime_csv = DatatimeCSV()
    form = QueryTeachings()
    form_lectures = QueryLectures()
    error_message = None

    # Fetch the creation date of the CSV file from the backend
    creation_csv = f'{FASTAPI_BACKEND_HOST}/csv_creation_date'
    response_creation_csv = requests.get(creation_csv)
    datatime_creation_csv = response_creation_csv.json()
    datatime_csv.datatime = datatime_creation_csv

    # Fetch data from the backend and update form choices
    url_csv = f'{FASTAPI_BACKEND_HOST}/df_show'
    response_csv = requests.get(url_csv)

    if response_csv.status_code == 200:
        data = response_csv.json()
        form.cycle.choices = get_unique_values(data, 'CYCLE')
        form.degreetype.choices = get_unique_values(data, 'DEGREE_TYPE')
        form.location.choices = get_unique_values(data, 'SITE')
    else:
        error_message = "Error: Unable to fetch data from the backend."

    # Process form submissions
    if form.validate_on_submit():
        location = form.location.data
        degreetype = form.degreetype.data
        cycle = form.cycle.data

        # Build URL for querying teachings
        url_query = f'{FASTAPI_BACKEND_HOST}/query'
        url_teachings = f'{url_query}/{location}/{degreetype}/{cycle}'
        response_teachings = requests.get(url_teachings)

        if response_teachings.status_code == 200:
            # Extract and display the result from the FastAPI backend
            teachings = response_teachings.json()
            data_dict = json.loads(teachings)
            teachings = sorted([
                (key, value) for key, value in data_dict.items()
            ])
            form_lectures.teaching.choices = teachings

            return render_template(
                'calendar.html', form=form, form_lectures=form_lectures,
                datatime_csv=datatime_csv, error_message=error_message
            )
        else:
            error_message = "Error: Unable to fetch data from the backend."

    # Render the '/calendar' page with the appropriate data and form
    return render_template(
        'calendar.html', form=form, form_lectures=form_lectures,
        datatime_csv=datatime_csv, error_message=error_message
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
