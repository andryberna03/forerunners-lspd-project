import datetime
import requests
import pandas as pd
import os
import datetime


def df_creating(file_path_final) -> pd.DataFrame:
    """
    Create or load a DataFrame from a CSV file.

    This is the main function which orchestrates the entire process of creating
    the final dataframe. It checks if a file exists and is less than a day old.
    If so, it loads the data from the file. Otherwise, it calls the create_new_dataframe
    function to generate a new dataframe.
    
    Parameters:
    file_path_final (str): The path to the CSV file.

    Returns:
    pd.DataFrame: The final dataframe containing all the required data.
    """
    # Check if the file exists and was created within the last 24 hours
    if os.path.exists(file_path_final):
        # Get the creation time of the file
        creation_time = os.path.getctime(file_path_final)
        file_creation_date = datetime.datetime.fromtimestamp(creation_time)
        current_date = datetime.datetime.now()

        # If the file was created within the last 24 hours, load it
        if current_date - file_creation_date < datetime.timedelta(days=1):
            final_urls_dataframe = pd.read_csv(file_path_final)
            return final_urls_dataframe
        # If the file was not created within the last 24 hours, create a new dataframe
        else:
            return create_new_dataframe(file_path_final)
    # If the file does not exist, create a new dataframe
    else:
        return create_new_dataframe(file_path_final)


def create_new_dataframe(file_path_final: str) -> pd.DataFrame:
    """
    This function creates a new DataFrame by calling the necessary functions,
    preprocesses the data, merges it, orders it, adds URLs, and handles problematic values.
    It then saves the DataFrame to a CSV file and returns it.

    Args:
    file_path_final (str): The path to the final CSV file.

    Returns:
    pd.DataFrame: The new DataFrame.
    """
    # Define the URLs from which to retrieve data
    urls = {
        "degrees": "http://apps.unive.it/sitows/didattica/corsi",
        "teachings": "http://apps.unive.it/sitows/didattica/insegnamenti",
        "degrees_teachings": "http://apps.unive.it/sitows/didattica/corsiinsegnamenti",
        "degrees_teachings": "http://apps.unive.it/sitows/didattica/corsiinsegnamenti",
        "lecturers": "http://apps.unive.it/sitows/didattica/docenti",
        "teachings_lecturers": "http://apps.unive.it/sitows/didattica/insegnamentidocenti",
        "teachings_lecturers": "http://apps.unive.it/sitows/didattica/insegnamentidocenti",
        "lectures": "http://apps.unive.it/sitows/didattica/lezioni",
        "classrooms": "http://apps.unive.it/sitows/didattica/aule",
        "locations": "http://apps.unive.it/sitows/didattica/sedi",
    }

    # Use defined function to get urls_dataframe
    urls_dataframes = get_data(urls)

    # Use the function to preprocess the data
    preprocessed_urls_dataframes = preprocess_data(urls_dataframes)

    # Use the function to merge the data
    merged_urls_dataframe = merge_data(preprocessed_urls_dataframes)

    # Use the function to order
    ordered_dataframe = rename_and_convert(merged_urls_dataframe)

    # Add prof URL
    final_urls_dataframe = unive_lecturer_urls(ordered_dataframe)

    # Add course URL
    final_urls_dataframe = unive_teaching_urls(final_urls_dataframe)

    final_urls_dataframe = format_iso8601(final_urls_dataframe)

    final_urls_dataframe = modify_values(final_urls_dataframe)

    # Save the DataFrame to CSV
    final_urls_dataframe.to_csv(file_path_final, index=False)

    # Read the DataFrame from CSV
    final_urls_dataframe = pd.read_csv(file_path_final)

    return final_urls_dataframe


# Retrieve JSON data from a URL and convert it to a Pandas DataFrame
def get_data(urls: dict) -> dict:
    """
    Retrieve data from the URL, convert it to a Pandas DataFrame,
    modify the URLs dictionary in place, and assign it to a new variable.

    Args:
        urls (dict[str: str]): Dictionary containing
        URLs to retrieve data from.

    Returns:
        dict[str: pd.DataFrame]: Dictionary with retrieved
        dict[str: pd.DataFrame]: Dictionary with retrieved
        data as Pandas DataFrames.
    """
    # Loop through each URL in the URLs dictionary
    for url in urls.keys():
        # Retrieve data from the URL
        url_response = requests.get(urls[url])
        # Convert the response into a JSON object and store it in a list
        url_data = url_response.json()
        # Convert the JSON object into a Pandas DataFrame
        url_df = pd.DataFrame(url_data)
        # Replace in place URLs within dictionary
        urls[url] = url_df

    # Assign the modified URLs dictionary to a new variable
    urls_dfs = urls

    return urls_dfs


# Process data changing columns names and converting to uppercase
def preprocess_data(urls_dataframes: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocesses multiple DataFrames from the provided dictionary by converting
    specified columns to uppercase and renaming specific columns.

    Args:
    urls_dataframes (dict[str, pd.DataFrame]):
    A dictionary containing DataFrames to preprocess.

    Returns:
    dict[str, pd.DataFrame]: The preprocessed DataFrames.
    """
    # Convert specified columns to uppercase
    urls_dataframes["lecturers"]['NOME'] = \
        urls_dataframes["lecturers"]['NOME'].str.upper()
    urls_dataframes["lecturers"]['COGNOME'] = \
        urls_dataframes["lecturers"]['COGNOME'].str.upper()

    # Rename specific columns
    urls_dataframes["teachings"].rename(columns={
        "NOME": "TEACHING", "SEDE": "SITE"}, inplace=True)
    urls_dataframes["lecturers"].rename(columns={
        "NOME": "LECTURER_NAME"}, inplace=True)
    urls_dataframes["classrooms"].rename(columns={
        "NOME": "CLASSROOM_NAME"}, inplace=True)
    urls_dataframes["locations"].rename(columns={
        "NOME": "LOCATION_NAME"}, inplace=True)

    preprocessed_urls_dataframes = urls_dataframes

    return preprocessed_urls_dataframes


# Merge all dataframes in one using dictionary with dataframes
def merge_data(urls_dataframes: pd.DataFrame) -> pd.DataFrame:
    """
    Merges multiple DataFrames from the provided dictionary
    using various columns and methods.

    Args:
    urls_dataframes (dict[str, pd.DataFrame]):
    A dictionary containing DataFrames to merge.

    Returns:
    pd.DataFrame: The merged DataFrame.
    """
    # Merge insegnamenti_df and corsi_insegnamenti_df
    # on the common column 'AF_ID' and
    # use intersection of keys from both frames
    merged_df = pd.merge(urls_dataframes["teachings"],
                         urls_dataframes["degrees_teachings"],
                         on='AF_ID', how='inner')

    # Drop duplicate rows based on
    # the combination of columns 'AR_ID' and 'AF_ID'
    merged_df = merged_df.drop_duplicates(
        subset=['AR_ID', "AF_ID"])

    # Merge merged_df and corsi_df on the columns [CDS_COD,"PDS_COD]
    # and use intersection of keys from both frames
    merged_df = pd.merge(merged_df, urls_dataframes["degrees"], on=[
        "CDS_COD", "PDS_COD"], how='inner')

    # Merge merged_df and lezioni_df on the columns 'AR_ID' and
    # use intersection of keys from both frames
    merged_df = pd.merge(merged_df, urls_dataframes["lectures"],
                         on="AR_ID", how='inner')

    # Drops duplicate rows based on the 'IMPEGNO_ID' column
    merged_df = merged_df.drop_duplicates(subset=['IMPEGNO_ID'])

    # Merge the DataFrame with aule_df DataFrame on the column 'AULA_ID'
    # and use intersection of keys from both frames
    merged_df = pd.merge(merged_df, urls_dataframes["classrooms"],
                         on="AULA_ID", how='inner')

    # Merge the DataFrame with aule_df DataFrame on the column 'SEDE_ID'
    # and use intersection of keys from both frames
    final_urls_df = pd.merge(merged_df, urls_dataframes["locations"],
                             on="SEDE_ID", how='inner')

    # Dropping unnecessary columns such as 'CDS_COD' and 'PDS_COD'
    final_urls_df = final_urls_df.drop([
        'CDS_COD', 'PDS_COD', "PDS_DES", "AR_ID",
        "IMPEGNO_ID", "AULA_ID", "SEDE_ID"], axis=1)

    return final_urls_df


def rename_and_convert(merged_dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Reorders the columns of the DataFrame according to the provided order
    and converts the 'DOCENTI' column values to uppercase.

    Args:
    merged_dataframe (pd.DataFrame): The DataFrame to process.
    merged_dataframe (pd.DataFrame): The DataFrame to process.

    Returns:
    pd.DataFrame: The processed DataFrame.
    """
    drop_columns = [
        'CODICE', 'SETTORE', 'CREDITI', 'PESO_TOTALE',
        'TIPO_CORSO_DES', 'TIPO_ATTIVITA', 'POSTI', 
        'NOTE', 'ANNO_CORSO', 'CDS_DES','COORDINATE']

    merged_dataframe.drop(columns=drop_columns, inplace=True)

    new_column_names = {'CICLO': "CYCLE", 'CODICE': 'CODE',
                        'PARTIZIONE': 'PARTITION',
                        'SETTORE': "SECTOR", 'PESO': "CREDITS",
                        'TIPO_CORSO_COD': "DEGREE_TYPE",
                        'GIORNO': "LECTURE_DAY", 'INIZIO': "LECTURE_START",
                        'FINE': "LECTURE_END", 'DOCENTI': 'LECTURER_NAME',
                        'INDIRIZZO': 'ADDRESS'}

    merged_dataframe.rename(columns=new_column_names, inplace=True)

    # Converts the 'DOCENTI' column values to uppercase
    merged_dataframe['LECTURER_NAME'] = merged_dataframe[
        'LECTURER_NAME'].str.upper()

    # Drop rows where DEGREE_TYPE is different from 'L' or 'LM'
    merged_dataframe = merged_dataframe[(merged_dataframe['DEGREE_TYPE'] == 'L') | (merged_dataframe['DEGREE_TYPE'] == 'LM')]

    return merged_dataframe


def unive_lecturer_urls(ordered_dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Enriches the main DataFrame with URLs of lecturers.

    Parameters:
    ordered_dataframe (pd.DataFrame): The main DataFrame containing lecturer names.

    Returns:
    pd.DataFrame: The updated DataFrame with added URLs of lecturers.

    The function performs the following steps:
    1. Retrieves data about lecturers from a JSON URL.
    2. Creates a new column 'LECTURER_NAME' by concatenating 'COGNOME' and 'NOME' columns.
    3. Selects only 'LECTURER_NAME' and 'DOCENTE_ID' columns from the lecturers DataFrame.
    4. Merges the main DataFrame with the lecturers DataFrame on 'LECTURER_NAME'.
    5. Fills NaN values in 'DOCENTE_ID' column with -1.
    6. Creates a new column 'URL_DOCENTE' by concatenating a base URL and 'DOCENTE_ID' column.
    7. Returns the updated DataFrame.
    """
    lecturers = pd.read_json("http://apps.unive.it/sitows/didattica/docenti")
    lecturers['LECTURER_NAME'] = (lecturers['COGNOME'] + '' + lecturers['NOME']).str.upper()
    lecturers = lecturers[['LECTURER_NAME','DOCENTE_ID']]

    # Merge of the main DataFrame with lecturer's data
    final_urls_dataframe = pd.merge(ordered_dataframe, lecturers, on='LECTURER_NAME', how='left')
    final_urls_dataframe['DOCENTE_ID'] = final_urls_dataframe['DOCENTE_ID'].fillna(-1)
    
    # Convert to integer and then to string
    url_lecturers = 'https://www.unive.it/data/persone/'
    final_urls_dataframe['URL_DOCENTE'] = url_lecturers + final_urls_dataframe[
        'DOCENTE_ID'].astype(int).astype(str)
    
    return final_urls_dataframe


def unive_teaching_urls(final_urls_dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    This function adds a new column to the DataFrame containing URLs of teachings.

    Parameters:
    final_urls_dataframe (pd.DataFrame): The DataFrame to which the new column will be added.
        The DataFrame should contain a column named 'AF_ID' which contains the IDs of the teachings.

    Returns:
    pd.DataFrame: The updated DataFrame with a new column 'URLS_INSEGNAMENTO' containing the URLs of teachings.
        The URLs are constructed by concatenating the base URL 'https://www.unive.it/data/insegnamento/'
        with the IDs from the 'AF_ID' column, converted to strings.

    Raises:
    ValueError: If the 'AF_ID' column is not found in the DataFrame.

    """
    # Check if 'AF_ID' column exists in the DataFrame
    if 'AF_ID' not in final_urls_dataframe.columns:
        raise ValueError("'AF_ID' column not found in the DataFrame")

    # Construct the URLs by concatenating the base URL and the IDs from 'AF_ID' column
    final_urls_dataframe["URLS_INSEGNAMENTO"] = 'https://www.unive.it/data/insegnamento/' + final_urls_dataframe['AF_ID'].astype(str)

    return final_urls_dataframe

def format_iso8601(final_urls_dataframe):
    def format_to_iso8601(date_str, time_str):
        # Create a datetime object from date and time strings
        full_datetime = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        return full_datetime.isoformat()

    # Apply the formatting function to create new columns for ISO 8601 formatted dates
    final_urls_dataframe['START_ISO8601'] = final_urls_dataframe.apply(
        lambda row: format_to_iso8601(row['LECTURE_DAY'], row['LECTURE_START']), axis=1)
    final_urls_dataframe['END_ISO8601'] = final_urls_dataframe.apply(
        lambda row: format_to_iso8601(row['LECTURE_DAY'], row['LECTURE_END']), axis=1)
    return final_urls_dataframe


def modify_values(final_urls_dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Modify values in the DataFrame according to specified rules.

    This function performs several modifications on the input DataFrame:
    - Replaces 'L' with 'Bachelor' and 'LM' with 'Master' in the 'DEGREE_TYPE' column.
    - Replaces 'PADOVA' with 'VENEZIA' in the 'SITE' column.
    - Fills missing values in the 'SITE' column with 'Not defined yet'.
    - Fills missing values in the 'PARTITION' column with an empty string.
    - Removes rows where 'CYCLE' is 'Precorsi'.
    - Translates semester names in the 'CYCLE' column to English equivalents.

    Parameters:
    final_urls_dataframe (pd.DataFrame): The input DataFrame to be modified.

    Returns:
    pd.DataFrame: The modified DataFrame.
    """
    # Replace degree types with their full names
    final_urls_dataframe['DEGREE_TYPE'] = final_urls_dataframe['DEGREE_TYPE'].replace({'L': 'Bachelor', 'LM': 'Master'})

    # Replace 'PADOVA' with 'VENEZIA' in the 'SITE' column
    final_urls_dataframe['SITE'] = final_urls_dataframe['SITE'].replace({'PADOVA': 'VENEZIA'})

    # Fill missing values in the 'SITE' column
    final_urls_dataframe['SITE'] = final_urls_dataframe['SITE'].fillna("Not defined yet")

    # Fill missing values in the 'PARTITION' column with an empty string
    final_urls_dataframe['PARTITION'] = final_urls_dataframe['PARTITION'].fillna("")

    # Remove rows where 'CYCLE' is 'Precorsi'
    final_urls_dataframe = final_urls_dataframe[final_urls_dataframe['CYCLE'] != 'Precorsi']

    # Iterate over the DataFrame using the index and semester value
    for index, semester in final_urls_dataframe['CYCLE'].items():

        # Check if the semester is in the list of Spring semesters
        if semester in ['II Semestre', "3° Periodo", "4° Periodo"]:
            # Replace the semester name with the English equivalent
            new_semester = 'Spring Semester (Feb-June)'
            # Update the DataFrame at the current index
            final_urls_dataframe.at[index, 'CYCLE'] = new_semester

        # Check if the semester is 'Annuale'
        elif semester == 'Annuale':
            # Replace the semester name with the English equivalent
            new_semester = 'Annual'
            # Update the DataFrame at the current index
            final_urls_dataframe.at[index, 'CYCLE'] = new_semester

        # If the semester is not in the list of Spring or Annual semesters,
        # it must be a Fall semester
        else:
            # Replace the semester name with the English equivalent
            new_semester = 'Fall Semester (Sep-Jan)'
            # Update the DataFrame at the current index
            final_urls_dataframe.at[index, 'CYCLE'] = new_semester

    return final_urls_dataframe


if __name__ == "__main__":
    final_urls_dataframe = df_creating('app/final.csv')