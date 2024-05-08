"""
Frontend module for the Flask application.

This module defines a simple Flask application that serves as the frontend for the project.
"""

from flask import Flask, render_template
from flask_cors import CORS
import requests
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, SelectField
from wtforms.widgets import ListWidget, CheckboxInput

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'

# Configura CORS per consentire tutte le origini (*)
CORS(app)

# Configuration for the FastAPI backend URL
FASTAPI_BACKEND_HOST = 'http://backend'  # Replace with the actual URL of your FastAPI backend
BACKEND_URL = f'{FASTAPI_BACKEND_HOST}/query/'

class QueryForm(FlaskForm):
    location = SelectMultipleField('Location:', choices=[('VENEZIA', 'VENEZIA'), ('RONCADE', 'RONCADE'), ('TREVISO', 'TREVISO'), ('PADOVA', 'PADOVA')],
                                    widget=ListWidget(prefix_label=False), option_widget=CheckboxInput())
    degreetype = SelectMultipleField('Degree type:', choices=[('MASTER', 'MASTER'), ('BACHELOR', 'BACHELOR'), ('OTHER', 'OTHER')],
                                    widget=ListWidget(prefix_label=False), option_widget=CheckboxInput())
    teaching = SelectField('Enter teaching name:')
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
    error_message = None

    # Fetch teachings from the backend and update form choices
    fastapi_url = f'{FASTAPI_BACKEND_HOST}/get_teachings'
    response = requests.get(fastapi_url)

    if response.status_code == 200:
        data = response.json()
        form.teaching.choices = [(teaching, teaching) for teaching in data['teachings']]
    else:
        error_message = "Error: Unable to fetch teaching data from the backend."

    if form.validate_on_submit():
        teaching = form.teaching.data
        selected_location = form.location.data
        selected_degreetype = form.degreetype.data
        
        # Convert location list into string
        location_str = ",".join(selected_location)
        degreetype_str = ",".join(selected_degreetype)
        
        # Build URL
        fastapi_url = f'{FASTAPI_BACKEND_HOST}/query/{teaching}/{location_str}/{degreetype_str}'
        response = requests.get(fastapi_url)

        if response.status_code == 200:
            data = response.json()
            return render_template('calendar.html', form=form, result=data, error_message=error_message)
        else:
            error_message = f'Error: Unable to fetch lesson for {teaching} from FastAPI Backend'

    return render_template('calendar.html', form=form, result=None, error_message=error_message)



@app.route('/about')
def about():
    """
    """
    return render_template('about.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
