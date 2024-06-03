"""
Frontend module for the Flask application.

This module defines a simple Flask application that serves as the frontend for the project.
"""

from flask import Flask, render_template, send_file
from flask_cors import CORS
import requests
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, validators
import os
from ics import Calendar, Event
from fastapi.responses import FileResponse
from datetime import datetime
import pytz

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure secret key

"""
Configure Cross-Origin Resource Sharing (CORS) for the Flask application.

CORS is a mechanism that allows a server to indicate any other origins (domain, scheme, or port) 
that are permitted to access the server's resources. By default, Flask does not enable CORS, 
so this line of code is necessary to allow all origins to access the application.
"""
CORS(app)

# Configuration for the FastAPI backend URL
FASTAPI_BACKEND_HOST = 'http://backend'  # Replace with the actual URL of your FastAPI backend
BACKEND_URL = f'{FASTAPI_BACKEND_HOST}/query/'

class DatatimeCSV(object):
    """
    A simple class to hold the date and time of a CSV file.

    Attributes:
    datatime (str): The date and time of the CSV file.
    """

    datatime = None


class QueryForm(FlaskForm):
    """
    A Flask-WTF form for querying lectures based on various parameters.

    Attributes:
    location (SelectField): A dropdown menu for selecting the location.
    degreetype (SelectField): A dropdown menu for selecting the degree type.
    teaching (SelectField): A dropdown menu for selecting the teaching name.
    cycle (SelectField): A dropdown menu for selecting the cycle.
    credits (SelectField): A dropdown menu for selecting the credits.
    submit (SubmitField): A button for submitting the form.
    """

    location = SelectField('Location:', validators=[validators.DataRequired()])
    degreetype = SelectField('Degree type:', validators=[validators.DataRequired()])
    teaching = SelectField('Enter teaching name:') #, validators=[validators.DataRequired()]
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
                unique_values.add(entry[column_name])
    elif isinstance(data, dict):
        if column_name in data:
            for entry in data[column_name]:
                if entry is not None:  
                    unique_values.add(entry)
    return sorted(list(unique_values))

def get_teaching_values(location_str, degreetype_str, cycle_str, credits_str, data, column_name):
    # Filter the data based on the given parameters
    filtered_data = [
        item for item in data
        if location_str in item.get('SITE', '') and
           degreetype_str in item.get('DEGREE_TYPE', '') and
           cycle_str in item.get('CYCLE', '') and
           credits_str in item.get('CREDITS', '')
    ]
    
    # Extract the unique values from the specified column, ignoring None values
    unique_values = {item[column_name] for item in filtered_data if column_name in item and item[column_name] is not None}
    
    # Return the sorted list of unique values
    return sorted(list(unique_values))
    


@app.route('/create_ics')
def export_ics(response):
    """
    Exports the provided lesson data into an ICS calendar file.

    Parameters:
    response (dict): A dictionary containing lesson data. Each lesson is represented as a dictionary with keys such as 'TEACHING', 'LECTURE_DAY', 'LECTURE_START', 'LECTURE_END', etc.

    Returns:
    flask.Response: A Flask response object containing the ICS file as an attachment.

    Raises:
    None

    """
    # Create an ICS calendar
    calendar = Calendar()

    # Iterate over each lesson in the response
    for key, lesson in response.items():
        # Create a new event for the lesson
        event = Event()

        # Set the event name to the teaching name
        event.name = lesson.get("TEACHING")

        # Parse the lecture day and time
        year, month, day = lesson['LECTURE_DAY'].split('-')
        hour_start, minute_start = lesson['LECTURE_START'].split(':')

        # Set the event start time with CET timezone
        event.begin = str(datetime(int(year), int(month), int(day), int(hour_start), int(minute_start), 0, tzinfo=pytz.timezone("CET")))
        
        # Parse the lecture end time
        hour_end, minute_end = lesson['LECTURE_END'].split(':')

        # Set the event end time with CET timezone
        event.end = str(datetime(int(year), int(month), int(day), int(hour_end), int(minute_end), 0, tzinfo=pytz.timezone("CET")))
        
        # Set the event description with relevant lesson details
        event.description = (
            f"Lecturer: {lesson.get('LECTURER_NAME', 'No Lecturer')}\n"
            f"Classroom: {lesson.get('CLASSROOM_NAME', 'No Classroom')}\n"
            f"Degree Name: {lesson.get('DEGREE_NAME', 'No Degree Name')}\n"
            f"URL Lecturer: {lesson.get('URL_DOCENTE', 'No URL')}\n"
            f"URL Teaching: {lesson.get('URLS_INSEGNAMENTO', 'No URL')}"
        )

        # Add the event to the calendar
        calendar.events.add(event)

    # Specify the path for the ICS file
    ical_path = 'app/calendar.ics'

    # Check if the file already exists
    if os.path.exists(ical_path):
       # Open the file in write mode and write the calendar data
       with open(ical_path, 'w') as f:
        f.writelines(calendar.serialize_iter())

    # Return the ICS file as a Flask response
    return FileResponse('calendar.ics', media_type='text/calendar', filename='calendar.ics')

@app.route('/download_ics')
def get_ics():
    """
    This function is responsible for downloading the generated ICS file.

    The function uses Flask's send_file method to send the 'calendar.ics' file to the client.
    The file is sent as an attachment, which means the client will be prompted to download it.

    Parameters:
    None

    Returns:
    flask.Response: A Flask response object containing the ICS file as an attachment.
    """
    return send_file('calendar.ics', as_attachment=True)

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
    else:
        error_message = "Error: Unable to fetch data from the backend."

    if form.validate_on_submit():
        location_str = form.location.data
        degreetype_str = form.degreetype.data
        cycle_str = form.cycle.data
        credits_str = form.credits.data

        form.teaching.choices = get_teaching_values(location_str, degreetype_str, cycle_str, credits_str, data, 'TEACHING')
        teaching = form.teaching.data


        # Build URL
        fastapi_url = f'{FASTAPI_BACKEND_HOST}/query/{teaching}/{location_str}/{degreetype_str}/{cycle_str}/{credits_str}'

        response = requests.get(fastapi_url)

        export_ics(response.json())

        if response.status_code == 200:
            # Extract and display the result from the FastAPI backend
            data = response.json() # data è nel formato che ci piace
            return render_template('calendar.html', datatime_csv=datatime_csv, form=form, result=data, error_message=error_message)
        else:
            error_message = f'Error: Unable to fetch lesson for {teaching} from FastAPI Backend'

    return render_template('calendar.html', datatime_csv=datatime_csv, form=form, result=None, error_message=error_message)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)