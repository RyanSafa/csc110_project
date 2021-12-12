"""
Enter text here
"""
from pandas import DataFrame, to_datetime
import datetime


def remove_columns(data: DataFrame, column_indices: list[int]) -> None:
    """
    Drop/remove columns in the DatFrame, data, based on the column(s)
    index given in column_indices.
    """
    column_indices.sort(reverse=True)

    for index in column_indices:
        data.drop(data.columns[index], inplace=True, axis=1)


def filter_for_value(data: DataFrame, column_to_value: dict[int, any]) -> None:
    """
    Filter rows in data based on their index for a given value,
    found in column_to_value.
    """

    for index, value in column_to_value.items():
        data.drop(data.loc[data[data.columns[index]] == value].index, inplace=True)


def keep_for_value(data: DataFrame, column_to_value: dict[str, any]) -> None:
    """
    Keep rows in data based on their index for a given value,
    found in column_to_value.
    """

    for index, value in column_to_value.items():
        data.drop(data.loc[data[index] != value].index, inplace=True)


def dates_to_datetime(data: DataFrame, column: str) -> None:
    """
    Change the date from whatever format it is in to datetime.
    """
    for index in data.index:
        data.loc[index, column] = to_datetime(data.loc[index, column])
