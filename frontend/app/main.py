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
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure secret key

# Configuration for the FastAPI backend URL
FASTAPI_BACKEND_HOST = 'http://backend'  # Replace with the actual URL of your FastAPI backend
BACKEND_URL = f'{FASTAPI_BACKEND_HOST}/query/'

class QueryForm(FlaskForm):
    insegnamento_name = StringField('Nome Insegnamento:')
    submit = SubmitField('Visualizza le tue lezioni')


@app.route('/')
def index():
    """
    Render the index page.

    Returns:
        str: Rendered HTML content for the index page.
    """
    return render_template('index.html')

@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    """
<<<<<<< HEAD
=======
    Function to fetch the current date from the backend.

    Returns:
        str: Current date in ISO format.
    """
    backend_url = 'http://backend/get-date'  # Adjust the URL based on your backend configuration
    try:
        response = requests.get(backend_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json().get('date', 'Date not available')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching date from backend: {e}")
        return 'Date not available'


@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    """
>>>>>>> develop-indexhtml
    Render the calendar page.

    Returns:
        str: Rendered HTML content for the index page.
    """
    form = QueryForm()
    error_message = None  # Initialize error message

    if form.validate_on_submit():
        insegnamento_name = form.insegnamento_name.data

        # Costruisce l'URL 
        fastapi_url = f'{FASTAPI_BACKEND_HOST}/query/{insegnamento_name}'
        response = requests.get(fastapi_url)

        if response.status_code == 200:
            # Extract and display the result from the FastAPI backend
            data = response.json()
            # result = data.get('birthday', f'Error: Birthday not available for {person_name}')
            return render_template('calendar.html', form=form, result=data, error_message=error_message)
        else:
            error_message = f'Error: Unable to fetch birthday for {insegnamento_name} from FastAPI Backend'

    return render_template('calendar.html', form=form, result=None, error_message=error_message)

@app.route('/about')
def about():
<<<<<<< HEAD
    """
    Render the about page.

    Returns:
        str: Rendered HTML content for the about page.
    """
=======
>>>>>>> develop-indexhtml
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

