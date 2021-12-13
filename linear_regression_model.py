"""
linear regression
"""
from data_cleanup import *


def clean_up_end_to_end_df(data: DataFrame) -> None:
    """
    Cleans up the supply chain dataframe to get data about transportation time of containers
    from Shanghai to Toronto via West Coast Ports
    """
    # filters rows for Containers, end-to-end Shanghai-Toronto via West Coast ports
    keep_for_value(data, {'Performance indicators': 'Containers, end-to-end Shanghai-Toronto via West Coast ports'})

    # removes columns not needed
    remove_columns(data, [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14])

    # converts all the dates to the datetime format
    dates_to_datetime(data, 'REF_DATE')

    # removes rows with dates before the pandemic
    remove_dates_before(data, 'REF_DATE', datetime.date(2020, 2, 1))

    # renames the column
    data.rename(columns={'VALUE': 'End-to-End Duration Shanghai-Toronto via West Coast ports in Days'}, inplace=True)


def clean_covid_for_cases_df(data: DataFrame) -> None:
    """
    Clean up the covid dataframe to only have dates and cumulative count of covid cases.
    """
    # filters rows for Canadian data only
    keep_for_value(data, {'Country': 'Canada'})

    # converts all the dates to the datetime format
    dates_to_datetime(data, 'Date_reported')

    # renames the column
    data.rename(columns={'Date_reported': 'REF_DATE', 'Cumulative_cases': 'COVID-19 cases'}, inplace=True)

    # removes columns not needed
    remove_columns(data, [1, 2, 3, 4, 6, 7])

    # for loop to keep data of only the first day of each month
    for index in data.index:
        if data['REF_DATE'][index].day != 1:
            data.drop(index, inplace=True)
