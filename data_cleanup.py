"""
Secondary file for CSC110 Project

Copyright and Usage Information
===============================

This file is Copyright (c) 2020 Ryan Safaeian, Akshat aneja,
Jyotiraditya Gupta, and Manav Manoj Malviya
"""
import datetime
from pandas import DataFrame, to_datetime


def remove_columns(data: DataFrame, column_indices: list[int]) -> None:
    """
    Drop/remove columns in the DatFrame, data, based on the column(s)
    index given in column_indices.

    Preconditions:
      - all(num < len(data.columns) for num in column_indices)
    """

    column_indices.sort(reverse=True)

    for index in column_indices:
        data.drop(data.columns[index], inplace=True, axis=1)


def filter_for_value(data: DataFrame, column_to_value: dict[int, any]) -> None:
    """
    Filter rows in data based on their index for a given value,
    found in column_to_value.

    Preconditions:
     - all(num < len(data.columns) for num in column_to_value)
    """

    for index, value in column_to_value.items():
        data.drop(data.loc[data[data.columns[index]] == value].index, inplace=True)


def keep_for_value(data: DataFrame, column_to_value: dict[str, any]) -> None:
    """
    Keep rows in data based on their index for a given value,
    found in column_to_value.

    Preconditions:
     - all(name in data.columns for name in column_to_value)
    """

    for index, value in column_to_value.items():
        data.drop(data.loc[data[index] != value].index, inplace=True)


def dates_to_datetime(data: DataFrame, column: str) -> None:
    """
    Change the date from whatever format it is in to datetime.

     Preconditions:
     - column in data.columns
    """
    for index in data.index:
        data.loc[index, column] = to_datetime(data.loc[index, column])


def remove_dates_before(data: DataFrame, column: str, date: datetime) -> None:
    """
    Remove all rows with dates in column before date.

    Preconditions:
    - all(isinstance(date, datetime.date) for date in data[column].tolist())
    - column in data.columns
    """
    data.drop(data.loc[data[column] < date].index, inplace=True)


def remove_dates_after(data: DataFrame, column: str, date: datetime) -> None:
    """
    Remove all rows with dates in column after date.

    Preconditions:
    - all(isinstance(date, datetime.date) for date in data[column].tolist())
    - column in data.columns
    """
    data.drop(data.loc[data[column] > date].index, inplace=True)


if __name__ == '__main__':
    import python_ta.contracts

    python_ta.check_all(config={
        'extra-imports': ['pandas', 'datetime'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
