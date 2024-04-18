"""
Frontend module for the Flask application.

This module defines a simple Flask application that serves as the frontend for the project.
"""

from flask import Flask, render_template
import requests  # Import the requests library to make HTTP requests
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput

app = Flask(__name__)

# Configuration for the FastAPI backend URL
FASTAPI_BACKEND_HOST = 'http://backend'  # Replace with the actual URL of your FastAPI backend
BACKEND_URL = f'{FASTAPI_BACKEND_HOST}/query/'

class QueryForm(FlaskForm):
    # Adding locations checkbox
    location = SelectMultipleField('Luoghi:', choices=[('MESTRE', 'MESTRE'), ('VENEZIA', 'VENEZIA'), ('RONCADE', 'RONCADE'), ('TREVISO', 'TREVISO')],
                                    widget=ListWidget(prefix_label=False), option_widget=CheckboxInput())
    insegnamento_name = StringField('Enter teaching name:')
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
    """
    Render the calendar page.

    Returns:
        str: Rendered HTML content for the index page.
    """
    form = QueryForm()
    error_message = None  # Initialize error message

    if form.validate_on_submit():
        insegnamento_name = form.insegnamento_name.data

        selected_location = form.location.data
        # Convert location list into string
        location_str = ",".join(selected_location)
        
        # Build URL
        fastapi_url = f'{FASTAPI_BACKEND_HOST}/query/{insegnamento_name}/{location_str}'
        response = requests.get(fastapi_url)

        if response.status_code == 200:
            # Extract and display the result from the FastAPI backend
            data = response.json()
            # result = data.get('birthday', f'Error: Birthday not available for {person_name}')
            return render_template('calendar.html', form=form, result=data, error_message=error_message)
        else:
            error_message = f'Error: Unable to fetch lesson for {insegnamento_name} from FastAPI Backend'

    return render_template('calendar.html', form=form, result=None, error_message=error_message)


@app.route('/about')
def about():
    """
    """
    return render_template('about.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
