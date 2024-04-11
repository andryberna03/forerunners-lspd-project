import requests
import pandas as pd

# Define the main function of the module that calls all other functions
def df_creating():
    # Define the URLs from which to retrieve data
    urls = {
        "degrees":  "http://apps.unive.it/sitows/didattica/corsi",
        "teachings": "http://apps.unive.it/sitows/didattica/insegnamenti",
        "degrees_teachings": "http://apps.unive.it/sitows/didattica/corsiinsegnamenti",
        "lecturers": "http://apps.unive.it/sitows/didattica/docenti",
        "teachings_lecturers": "http://apps.unive.it/sitows/didattica/insegnamentidocenti",
        "lectures": "http://apps.unive.it/sitows/didattica/lezioni",
        "classrooms": "http://apps.unive.it/sitows/didattica/aule",
        "locations": "http://apps.unive.it/sitows/didattica/sedi",
    }

    # Use the defined function to get dataframes for each URL
    urls_dataframes = get_data(urls)

    # Use the function to preprocess the data in the dataframes
    preprocessed_urls_dataframes = preprocess_data(urls_dataframes)

    # Use the function to merge the preprocessed dataframes
    merged_urls_dataframe = merge_data(preprocessed_urls_dataframes)

    #
    final_urls_dataframe = reorder_and_convert(merged_urls_dataframe)

    return final_urls_dataframe



# Retrieve JSON data from a URL and convert it to a Pandas DataFrame
def get_data(urls):
    """
    Retrieve data from the URL, convert it to a Pandas DataFrame,
    modify the URLs dictionary in place, and assign it to a new variable.

    Args:
        urls (dict[str: str]): Dictionary containing URLs to retrieve data from.

    Returns:
        (dict[str: pd.DataFrame]): Dictionary with retrieved data as Pandas DataFrames.
    """
    # Loop through each URL in the URLs dictionary
    for url in urls.keys():
        # Retrieve data from the URL
        url_response = requests.get(urls[url])
        # Convert the response into a JSON object and store it in a list
        url_data = url_response.json()
        # Convert the JSON object into a Pandas DataFrame
        url_df = pd.DataFrame(url_data)
        # Replace in place URLs whitin dictionary
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
    urls_dataframes (dict[str, pd.DataFrame]): A dictionary containing DataFrames to preprocess.

    Returns:
    dict[str, pd.DataFrame]: The preprocessed DataFrames.
    """
    # Convert specified columns to uppercase
    urls_dataframes["lecturers"]['NOME'] = urls_dataframes["lecturers"]['NOME'].str.upper()
    urls_dataframes["lecturers"]['COGNOME'] = urls_dataframes["lecturers"]['COGNOME'].str.upper()

    # Rename specific columns
    urls_dataframes["teachings"].rename(columns={"NOME": "TEACHING", "SEDE": "SITE"}, inplace=True)
    urls_dataframes["lecturers"].rename(columns={"NOME": "LECTURER_NAME"}, inplace=True)
    urls_dataframes["classrooms"].rename(columns={"NOME": "CLASSROOM_NAME"}, inplace=True)
    urls_dataframes["locations"].rename(columns={"NOME": "LOCATION_NAME"}, inplace=True)

    preprocessed_urls_dataframes = urls_dataframes

    return preprocessed_urls_dataframes


# Merge all dataframes in one using dictionary with dataframes
def merge_data(urls_dataframes):
    """
    Merges multiple DataFrames from the provided dictionary using various columns and methods.

    Args:
    urls_dataframes (dict[str, pd.DataFrame]): A dictionary containing DataFrames to merge.

    Returns:
    pd.DataFrame: The merged DataFrame.
    """
    # Merge insegnamenti_df and corsi_insegnamenti_df on the common column 'AF_ID' and use intersection of keys from both frames
    merged_df = pd.merge(urls_dataframes["teachings"], urls_dataframes["degrees_teachings"], on='AF_ID', how='inner')

    # Drop duplicate rows based on the combination of columns 'AR_ID' and 'AF_ID'
    merged_df = merged_df.drop_duplicates(subset=['AR_ID', "AF_ID"])

    # Merge merged_df and corsi_df on the columns [CDS_COD,"PDS_COD] and use intersection of keys from both frames
    merged_df = pd.merge(merged_df, urls_dataframes["degrees"], on=["CDS_COD", "PDS_COD"], how='inner')

    # Merge merged_df and lezioni_df on the columns 'AR_ID' and use intersection of keys from both frames
    merged_df = pd.merge(merged_df, urls_dataframes["lectures"], on="AR_ID", how='inner')

    # Drops duplicate rows based on the 'IMPEGNO_ID' column
    merged_df = merged_df.drop_duplicates(subset=['IMPEGNO_ID'])

    # Merge the DataFrame with aule_df DataFrame on the column 'AULA_ID' and use intersection of keys from both frames
    merged_df = pd.merge(merged_df, urls_dataframes["classrooms"], on="AULA_ID", how='inner')

    # Merge the DataFrame with aule_df DataFrame on the column 'SEDE_ID' and use intersection of keys from both frames
    final_urls_df = pd.merge(merged_df, urls_dataframes["locations"], on="SEDE_ID", how='inner')

    # Dropping unnecessary columns such as 'CDS_COD' and 'PDS_COD'
    final_urls_df = final_urls_df.drop(['CDS_COD', 'PDS_COD', "PDS_DES", "AR_ID", "IMPEGNO_ID", "AULA_ID", "SEDE_ID"], axis=1)

    return final_urls_df

def reorder_and_convert(merged_urls_dataframe):
    """
    Reorders the columns of the DataFrame according to the provided order and converts the 'DOCENTI' column values to uppercase.

    Args:
    df (pd.DataFrame): The DataFrame to process.
    new_column_order (list[str]): The new order of columns.

    Returns:
    pd.DataFrame: The processed DataFrame.
    """
    # Defining the new order of columns
    new_column_order = ['AF_ID', 'GIORNO', 'INIZIO', 'FINE',
                        'NOME_INSEGNAMENTO', 'CICLO', 'ANNO_CORSO', 'DOCENTI',
                        'CODICE', 'PARTIZIONE', 'LUOGO', 'SETTORE', 'CREDITI',
                        'PESO', 'PESO_TOTALE', 'TIPO_CORSO_COD',
                        'TIPO_CORSO_DES', 'CDS_DES', 'TIPO_ATTIVITA', 'NOTE',
                        'NOME_AULA', 'POSTI', 'NOME_SEDE', 'INDIRIZZO', 'COORDINATE']

    # Setting the new order of the columns
    merged_urls_dataframe = merged_urls_dataframe.reindex(columns=new_column_order)

    # Converts the 'DOCENTI' column values to uppercase
    merged_urls_dataframe['DOCENTI'] = merged_urls_dataframe['DOCENTI'].str.upper()

    final_urls_dataframe = merged_urls_dataframe

    return final_urls_dataframe

if __name__ == "__main__":
    final_urls_dataframe = df_creating()