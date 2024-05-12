import pandas as pd
from .df_creating import df_creating

def df_dropdown():
    final_urls_dataframe = df_creating()

    df_drop = drop_columns(final_urls_dataframe)

    years = academic_year(df_drop)

    semester = semesters(years)

    dropdown_df = semester
    return dropdown_df


def drop_columns(df):
    """
    This function takes a DataFrame as input and returns a new DataFrame with only the specified columns.

    Parameters:
    df (pandas.DataFrame): The input DataFrame containing all columns.

    Returns:
    pandas.DataFrame: A new DataFrame containing only the specified columns.

    Note:
    The specified columns are: "TEACHING", "CYCLE", "PARTITION", "SITE", "CREDITS", "DEGREE_TYPE", 'LECTURE_DAY'.
    The original DataFrame is not modified. A copy of the selected columns is returned.
    """

    columns_to_keep = [
        "TEACHING", "CYCLE", "SITE",
        "CREDITS", "DEGREE_TYPE", 'LECTURE_DAY'
    ]

    df_drop = df.loc[:, columns_to_keep].copy()

    return df_drop


def academic_year(df):
    """
    This function takes a DataFrame as input and modifies the 'LECTURE_DAY' column to represent the academic year.
    The academic year is determined based on the month of the lecture day. If the month is between September and December,
    the academic year is represented as the current year divided by the next year. Otherwise, it is represented as the previous
    year divided by the current year.

    Parameters:
    df (pandas.DataFrame): The input DataFrame containing the 'LECTURE_DAY' column.

    Returns:
    pandas.DataFrame: The modified DataFrame with the 'LECTURE_DAY' column representing the academic year.
    """

    for index, day in df['LECTURE_DAY'].items():
        day_split = day.split('-')
        day_split = [int(day) for day in day_split]
        if day_split[1] >= 9 and day_split[1] <= 12:
            new_year = day_split[0]+1
            final_new_year = str(day_split[0]) + '/' + str(new_year)
            df.at[index, 'LECTURE_DAY'] = final_new_year
        else:
            old_year = day_split[0]-1
            final_new_year = str(old_year) + '/' + str(day_split[0])
            df.at[index, 'LECTURE_DAY'] = final_new_year

    df.rename(columns={'LECTURE_DAY': 'ACADEMIC_YEAR'}, inplace=True)

    return df


def semesters(df):
    df = df.loc[df['CYCLE'] != 'Precorsi'].copy()

    df = df.fillna('')

    for index, semester in df['CYCLE'].items():
        if semester in ['II Semestre', "3° Periodo", "4° Periodo"]:
            new_semester = 'Spring Semester (Feb-June)'
            df.at[index, 'CYCLE'] = new_semester
        elif semester == 'Annuale':
            new_semester = 'Annual'
            df.at[index, 'CYCLE'] = new_semester
        else:
            new_semester = 'Fall Semester (Sep-Jen)'
            df.at[index, 'CYCLE'] = new_semester

    return df


if __name__ == "__main__":
    final_urls_dataframe = df_dropdown() 

