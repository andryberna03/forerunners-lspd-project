# **Ca’ Foscari Exchange Calendar by Forerunners**

## **Scope**
Ca’ Foscari Exchange Calendar website is an intuitive and user-friendly platform designed to help exchange students navigate challenges of scheduling their teachings calendars. By simply implementing some filters, students can easily organise their schedules and collect relevant information about their courses.

## **Features**
Our website offers three main sections: `Home`, `About the Project`, and `Calendar`. The `Home` and `About the Project` pages provide a clear overview of the project's purpose and functionality. The `Calendar` page serves as user interactive hub, allowing to submit queries to the project's backend:
- **User-friendly Interface**: Enjoy a seamless user experience with an intuitive design that makes navigation and information retrieval straightforward and efficient.
- **Advanced Filtering**: Filter teachings based on specific criteria such as the degree type and the semester in which the teaching occurs.
- **Dynamic Filtering**: According to Advanced Filtering, only suitable teachings will be displayed to be chosen and this selection will vary at each modification of the Advanced Filtering.
- **Calendar Download**: After filtering the relevant teaching, the user can download the information in iCal to add it directly to their preferred calendar client.

## **Preview of the website**
### *Home Page*
The Home page of the website explains why we decided to undertake this project and displays a map created with Leaflet and OpenStreetMap that shows all the sites in the dataset.

![Index Page pt1](frontend/app/static/img/readme/imageindex1.png)
![Index Page pt2](frontend/app/static/img/readme/imageindex2.png)

### *Calendar Page*
The Calendar page allows users to apply filters to request specific teachings and generate a personalised schedule. This schedule can also be downloaded in iCal via a dedicated button, allowing users to insert it into their preferred calendar client.

![Calendar Page pt1](frontend/app/static/img/readme/imagecalendar1.png)
![Calendar Page pt2](frontend/app/static/img/readme/imagecalendar2.png)

### *About Page*
The about page provides more detailed information regarding the development of the project, its composition and the team of contributors.

![About Page](frontend/app/static/img/readme/imageabout.png)

## **Datasets Used in the Project**
Our database was built upon the [open data published on the website of Ca’ Foscari University of Venice](https://www.unive.it/pag/13488/). We started by studying the [”Webservice corsi e orari” datasets](https://www.unive.it/pag/fileadmin/user_upload/ateneo/mobile/documenti/WebserviceCorsi-Insegnamenti-Orari-Aule-Sedi.pdf), discovering that data is exposed in JSON format and is updated every 24 hours at 8:00 AM CEST.

Then, we retrieved data in different dataframes and merged them in order to have a unique CSV dataset. Columns of the final dataframe are:
- *TEACHING*: Name of the teaching.
- *CYCLE*: Semester (Fall-Spring) during the year in which the teaching is offered.
- *PARTITION*: Teaching division by surname if there are too many students.
- *SITE*: Where the teaching is conducted.
- *CREDITS*: Number of Italian credits (CFU) granted after passing the exam.
- *DEGREE_TYPE*: Degree type of the teaching as "Bachelor" or "Master".
- *LECTURE_DAY*: Day on which a lecture of the teaching is held.
- *LECTURE_START*: Starting time on the day the lecture is held.
- *LECTURE_END*: Ending time on the day the lecture is held.
- *LECTURER_NAME*: Name of the professor who teaches the lecture.
- *CLASSROOM_NAME*: Name of the room where the lecture is held.
- *LOCATION_NAME*: Name of the location where the room is situated.
- *ADDRESS*: Address of the location.
- *URL_DOCENTE*: University webpage of the lecturer.
- *URLS_INSEGNAMENTO*: University webpage of the teaching.
- *START_ISO8601*: ISO8601 format of LECTURE_START.
- *END_ISO8601*: ISO8601 format of LECTURE_END.

## **Technologies Used**
- HTML/CSS/JavaScript/Python
- [Flask](https://flask.palletsprojects.com/en/3.0.x/) (Frontend) - [FastAPI](https://fastapi.tiangolo.com) (Backend)
- [Bootstrap](https://getbootstrap.com/docs/5.3/getting-started/introduction/) for responsive design
- [Docker](https://www.docker.com/) to deploy the application

## **Architecture**
The project follows a simple client-server architecture:

1. **Frontend (Flask):**
   - Represents the user interface or client side.
   - Built with Flask, a lightweight web framework for Python.
   - Responsible for rendering web pages and user interaction, including the form for querying the backend.

2. **Backend (FastAPI):**
   - Represents the server or backend of the application.
   - Built with FastAPI, a modern web framework for building APIs with Python.
   - Handles requests from the frontend, including querying birthdays and providing the current date.

3. **Docker Compose:**
   - Orchestrates the deployment of both frontend and backend as separate containers.
   - Ensures seamless communication between frontend and backend containers.
   - Simplifies the deployment and management of the entire application.

Bidirectional communication is established between the Frontend (Flask) and Backend (FastAPI). Docker Compose facilitates this communication, allowing the components to work together seamlessly.

## Project Structure

- `backend/`: FastAPI backend implementation.
   - Dockerfile: Dockerfile for building the backend image.
   - requirements.txt: List of Python dependencies for the backend.
   - app/: Folder for dataset, Python modules, and Python main backend application
      - mymodules/: Folder for Python modules.
         - df_creating.py: Python module for creating dataset.
      - dummy.csv: dataset used in testing phase.
      - final.csv: dataset created by df_creating.py.
      - main.py: Main backend application file.
   - test/: Folder for Python test of main backend application.
      - test_main.py: Python test of main backend application.
      - test_df_creation.py: Python test of Python module for creating dataset.
- `frontend/`: Flask frontend implementation.
   - Dockerfile: Dockerfile for building the frontend image.
   - requirements.txt: List of Python dependencies for the frontend.
   - app/: Folder for static files, templates, and Python main frontend application
        - static/: Folder for static files (CSS, JavaScript, Images).
        - templates/: Folder for HTML templates.
        - main.py: Main frontend application file.
- `docker-compose.yml`: Docker Compose configuration for running both frontend and backend.

## **How to run the project**

### *Prerequisites*

- Docker
- Visual Studio Code (or any other IDE)

### *Usage*

1. Clone the repository and navigate in the directory:

    ```bash
    git clone REPO_URL
    cd forerunners-lspd-project
    ```

> **NOTE:** Uncomment the lines in the Dockerfiles that follow the section labeled `Command to run the application` and comment out the ones labeled `Command to keep the container running`. This will allow you to access the backend and frontend, as described in Point 3.

2. Build and run the Docker containers:

    ```bash
    docker-compose up --build
    ```

    This will start both the frontend and backend containers.

3. Open your web browser and navigate to [http://localhost:8080](http://localhost:8080) to access the `frontend` and [http://localhost:8081](http://localhost:8081) to access the `backend`.

4. Use the form on the frontend [http://localhost:8080/calendar](http://localhost:8080/calendar) to query teachings from the backend using filters.

## **Example Data Flow**

### *User accesses the calendar webpage:*
The `calendar.html` page is loaded, and meanwhile, the backend checks if 24 hours have passed since the last website dataset update. If not, nothing happens. However, if 24 hours have passed, the FastAPI updates the dataset with new data from Ca' Foscari's open data. After the update, the page loads correctly, and the last update date of the dataset is refreshed. This way, users always have up-to-date data available in the backend for frontend requests.

### *First user’s query:*
The user chooses their teaching features using filters and then asks for data. Flask sends a query to the FastAPI to retrieve the relevant data. FastAPI processes the query and responds with the requested information in JSON format. Upon receiving the data, Flask extracts and transforms it as necessary, making them available and ready for the second user's query when `calendar.html` template will be rendered again.

### *Calendar display:*
The user select their specific teaching and JavaScript makes two AJAX calls to retrieve data. The first one is used to populate the calendar design showing classess. By moving the cursor over the slot the user gains detailed information about each lecture, including the course title, lecturer, time, and location. This detailed view provides users with a clear and organised schedule, making it easy to manage their academic commitment. Additionally, if the user clicks on the time slot it will take the user to Ca’ Foscari official web page for that teaching. The second one is used to create the iCal file.

### *User download teaching in iCal format:*
When the download button is clicked by the user, `calendar.ics` file is created based on information retrived in the most recent query using JavaScript AJAX call. As soon as the file is created, it is immediately downloaded by the browser using timezone CET. This allows the user to directly add the lectures to their preferred calendar client.

## **Shutting Down the Docker Containers**

To shut down the running Docker containers, you can use the following steps:

1. Open a terminal.

2. Navigate to the project root directory.

3. Run the following command to stop and remove the Docker containers:

    ```bash
    docker-compose down
    ```

## **Starting and Stopping Containers Individually**

If you need to start or stop the containers individually, you can use the following commands:

- **Start Frontend Container:**

    ```bash
    docker-compose up frontend
    ```

- **Stop Frontend Container:**

    ```bash
    docker-compose stop frontend
    ```

- **Start Backend Container:**

    ```bash
    docker-compose up backend
    ```

- **Stop Backend Container:**

    ```bash
    docker-compose stop backend
    ```

Make sure to replace `frontend` and `backend` with the appropriate service names from your `docker-compose.yml` file.

> **NOTE:** When stopping containers individually, the `docker-compose down` command is not required. Now you can manage the lifecycle of your Docker containers more flexibly.

## **Testing**

The tests focus on the backend of the project, including the handling of data, file operations, and API endpoint responses. These tests are needed to meet the project's requirements and to guarantee that the system behaves as expected under different conditions.

The tests cover the following scenarios:

1. **DataFrame Creation (`df_creating` function)**:
   - **Existing File (Recent)**: Verifies that the `df_creating` function correctly loads a DataFrame from a CSV file that was created less than a day ago.
   - **Existing File (Old)**: Ensures that the function creates a new DataFrame if the existing file is older than a day.
   - **Non-Existing File**: Checks that the function creates a new DataFrame when the specified file does not exist.

2. **DataFrame Structure (`create_new_dataframe` function)**:
   - Validates that the `create_new_dataframe` function produces a DataFrame with the expected structure and content.

3. **File Validation**:
   - **CSV Format Check**: Ensures that the `final.csv` file is a valid CSV with the correct headers.
   - **File Creation Date**: Confirms that the `final.csv` file was created within the last 24 hours.

4. **API Endpoints**:
   - **Main Endpoint (`/`)**: Tests the root endpoint to ensure it returns the expected response.
   - **DataFrame Endpoint (`/df_show`)**: Verifies that the endpoint returns a JSON representation of the DataFrame.
   - **CSV Creation Date Endpoint**: Check if the HTTPException is correctly thrown.
   - **Teaching Query Endpoint (`/query`)**:
     - Checks the response for valid teaching queries.
     - Ensures correct behavior when no teachings match the query filters.
   - **Single Teaching Query (`/query/{teaching_name}`)**: Validates the response for a specific teaching query.

To execute these tests, navigate to the `backend/` directory and run the following command in the terminal:

```
pytest --cov=app --cov-report=html tests/
```

These tests utilize `pytest` for testing functionalities and `pytest-mock` for mocking dependencies, be sure you have them installed. The `TestClient` from FastAPI is used for testing API endpoints, allowing for the simulation of HTTP requests and responses. This approach ensures that the application is robust, reliable, and meets the specified requirements.

## **Limitations**
Despite our efforts to create an excellent website, it has some limitations:
- It is not possible to search for more than one teaching at a time; therefore, the user must make a separate query for each course users intend to search for.
- If "Enter teaching name:" filter has no values, the previous query was wrong (ex. RONCADE has no master degrees).
- The dataset contains 20,000 rows with NaN values in the "SITE" column; consequently, these values have been filled with 'Not defined yet'.

## **Contact**
Ca’ Foscari Exchange Calendar software development team:
- Bernardo Andrea (894305) - [andrea.bernardo@student.h-farm.com](mailto:andrea.bernardo@student.h-farm.com)
- Gnoni Mavarelli Antonio (894314) - [antonio.gnonimavarelli@student.h-farm.com](mailto:antonio.gnonimavarelli@student.h-farm)
- Griselin Marta (894571) - [marta.griselin@student.h-farm.com](mailto:marta.griselin@student.h-farm.com)
- Piscopello Francesco (893994) - [francesco.piscopello@student.h-farm.com](mailto:francesco.piscopello@student.h-farm.com)
- Sartori Carlo Alberto (894176) - [carlo.sartori@student.h-farm.com](mailto:carlo.sartori@student.h-farm.com)