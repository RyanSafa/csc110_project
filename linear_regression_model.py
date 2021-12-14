"""
Secondary file for CSC110 Project

Copyright and Usage Information
===============================

This file is Copyright (c) 2020 Ryan Safaeian, Akshat aneja,
Jyotiraditya Gupta, and Manav Manoj Malviya
"""
import datetime
from pandas import DataFrame
from data_cleanup import remove_columns, keep_for_value, \
    dates_to_datetime, remove_dates_before


def clean_up_end_to_end_df(data: DataFrame) -> None:
    """
    Cleans up the supply chain dataframe to get data about transportation time of containers
    from Shanghai to Toronto via West Coast Ports
    """
    # filters rows for Containers, end-to-end Shanghai-Toronto via West Coast ports
    keep_for_value(data, {'Performance indicators':
                          'Containers, end-to-end Shanghai-Toronto via West Coast ports'})

    # removes columns not needed
    remove_columns(data, [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14])

    # converts all the dates to the datetime format
    dates_to_datetime(data, 'REF_DATE')

    # removes rows with dates before the pandemic
    remove_dates_before(data, 'REF_DATE', datetime.date(2020, 2, 1))

    # renames the column
    data.rename(columns={'VALUE': 'End-to-End Duration Shanghai-Toronto '
                                  'via West Coast ports in Days'}, inplace=True)


def clean_covid_for_cases_df(data: DataFrame) -> None:
    """
    Clean up the covid dataframe to only have dates and cumulative count of covid cases.
    """
    # filters rows for Canadian data only
    keep_for_value(data, {'Country': 'Canada'})

    # converts all the dates to the datetime format
    dates_to_datetime(data, 'Date_reported')

    # renames the column
    data.rename(columns={'Date_reported': 'REF_DATE',
                         'Cumulative_cases': 'COVID-19 cases'}, inplace=True)

    # removes columns not needed
    remove_columns(data, [1, 2, 3, 4, 6, 7])

    # for loop to keep data of only the first day of each month
    for index in data.index:
        if data['REF_DATE'][index].day != 1:
            data.drop(index, inplace=True)


if __name__ == '__main__':
    import python_ta.contracts

    python_ta.check_all(config={
        'extra-imports': ['data_cleanup', 'pandas', 'datetime'],
        # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
