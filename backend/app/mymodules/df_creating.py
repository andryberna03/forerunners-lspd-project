import requests
import pandas as pd
import numpy as np
import os
import datetime


def df_creating():
    """
    This is the main function which orchestrates the entire process of creating
    the final dataframe. It checks if a file exists and is less than a day old.
    If so, it loads the data from the file. Otherwise, it calls the create_new_dataframe
    function to generate a new dataframe.

    Returns:
    pd.DataFrame: The final dataframe containing all the required data.
    """
    # Define the path to the final CSV file
    file_path_final = 'app/final.csv'

    # Check if the file exists and was created within the last 24 hours
    if os.path.exists(file_path_final):
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


def create_new_dataframe(file_path_final):
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
        "lecturers": "http://apps.unive.it/sitows/didattica/docenti",
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

    final_urls_dataframe = semesters(final_urls_dataframe)

    # Handle problematic values
    final_urls_dataframe.fillna("null", inplace=True)

    # Save the DataFrame to CSV
    final_urls_dataframe.to_csv(file_path_final, index=False)

    # Read the DataFrame from CSV
    final_urls_dataframe = pd.read_csv(file_path_final)

    return final_urls_dataframe


# Retrieve JSON data from a URL and convert it to a Pandas DataFrame
def get_data(urls):
    """
    Retrieve data from the URL, convert it to a Pandas DataFrame,
    modify the URLs dictionary in place, and assign it to a new variable.

    Args:
        urls (dict[str: str]): Dictionary containing
        URLs to retrieve data from.

    Returns:
        (dict[str: pd.DataFrame]): Dictionary with retrieved
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
def preprocess_data(urls_dataframes):
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
def merge_data(urls_dataframes):
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


def rename_and_convert(merged_dataframe):
    """
    Reorders the columns of the DataFrame according to the provided order
    and converts the 'DOCENTI' column values to uppercase.

    Args:
    merged_dataframe (pd.DataFrame): The DataFrame to process.

    Returns:
    pd.DataFrame: The processed DataFrame.
    """
    drop_columns = [
        'CODICE', 'SETTORE', 'CREDITI', 'PESO_TOTALE',
        'TIPO_CORSO_DES', 'TIPO_ATTIVITA', 'POSTI', 'NOTE']

    merged_dataframe.drop(columns=drop_columns, inplace=True)

    new_column_names = {'CICLO': "CYCLE", 'CODICE': 'CODE',
                        'ANNO_CORSO': 'STUDY_YEAR', 'PARTIZIONE': 'PARTITION',
                        'SETTORE': "SECTOR", 'PESO': "CREDITS",
                        'TIPO_CORSO_COD': "DEGREE_TYPE",
                        'CDS_DES': 'DEGREE_NAME',
                        'GIORNO': "LECTURE_DAY", 'INIZIO': "LECTURE_START",
                        'FINE': "LECTURE_END", 'DOCENTI': 'LECTURER_NAME',
                        'INDIRIZZO': 'ADDRESS', 'COORDINATE': 'COORDINATES'}

    merged_dataframe.rename(columns=new_column_names, inplace=True)

    # Converts the 'DOCENTI' column values to uppercase
    merged_dataframe['LECTURER_NAME'] = merged_dataframe[
        'LECTURER_NAME'].str.upper()

    # Drop rows where DEGREE_TYPE is different from 'L' or 'LM'
    merged_dataframe = merged_dataframe[(merged_dataframe['DEGREE_TYPE'] == 'L') | (merged_dataframe['DEGREE_TYPE'] == 'LM')]

    return merged_dataframe


def unive_lecturer_urls(ordered_dataframe):
    """
    Returns enriched "final_urls_dataframe"
    """
    lecturers = pd.read_json("http://apps.unive.it/sitows/didattica/docenti")
    lecturers['LECTURER_NAME'] = (lecturers['COGNOME'] + ' ' + lecturers['NOME']).str.upper()
    lecturers = lecturers[['LECTURER_NAME','DOCENTE_ID']]
    # Merge of the main DataFrame with lecturer's data
    final_urls_dataframe = pd.merge(ordered_dataframe, lecturers, on='LECTURER_NAME', how='left')
    final_urls_dataframe['DOCENTE_ID'] = final_urls_dataframe['DOCENTE_ID'].fillna(-1)
    # Convert to integer and then to string
    url_lecturers = 'https://www.unive.it/data/persone/'
    final_urls_dataframe['URL_DOCENTE'] = url_lecturers + final_urls_dataframe[
        'DOCENTE_ID'].astype(int).astype(str)
    return final_urls_dataframe

def unive_teaching_urls(final_urls_dataframe):
    final_urls_dataframe["URLS_INSEGNAMENTO"] = 'https://www.unive.it/data/insegnamento/' + final_urls_dataframe['AF_ID'].astype(str)
    return final_urls_dataframe

def semesters(final_urls_dataframe):


    for index, semester in final_urls_dataframe['CYCLE'].items():
        if semester in ['II Semestre', "3° Periodo", "4° Periodo"]:
            new_semester = 'Spring Semester (Feb-June)'
            final_urls_dataframe.at[index, 'CYCLE'] = new_semester
        elif semester == 'Annuale':
            new_semester = 'Annual'
            final_urls_dataframe.at[index, 'CYCLE'] = new_semester
        else:
            new_semester = 'Fall Semester (Sep-Jen)'
            final_urls_dataframe.at[index, 'CYCLE'] = new_semester

    return final_urls_dataframe

if __name__ == "__main__":
    final_urls_dataframe = df_creating()
