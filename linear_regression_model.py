"""
linear regression
"""

import pandas as pd
import plotly.express as px
from data_cleanup import *


# DATAFRAME FOR CONTAINERS FROM SHANGHAI TO TORONTO
west_dwell = pd.read_csv('data/supply_chain_data.csv')

# filters rows for Containers, end-to-end Shanghai-Toronto via West Coast ports
keep_for_value(west_dwell, {'Performance indicators': 'Containers, end-to-end Shanghai-Toronto via West Coast ports'})

# removes columns not needed
remove_columns(west_dwell, [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14])

# converts all the dates to the datetime format
dates_to_datetime(west_dwell, 'REF_DATE')

# removes rows with dates before the pandemic
remove_dates_before(west_dwell, 'REF_DATE', datetime.date(2020, 2, 1))

# renames the column
west_dwell.rename(columns={'VALUE': 'End-to-End Duration Shanghai-Toronto via West Coast ports in Days'}, inplace=True)


# DATAFRAME FOR DEATHS CAUSED BY COVID
covid_data = pd.read_csv('data/WHO-COVID-19-global-data.csv')

# filters rows for Canadian data only
keep_for_value(covid_data, {'Country': 'Canada'})

# converts all the dates to the datetime format
dates_to_datetime(covid_data, 'Date_reported')

# renames the column
covid_data.rename(columns={'Date_reported': 'REF_DATE', 'Cumulative_cases': 'COVID-19 cases'}, inplace=True)

# removes columns not needed
remove_columns(covid_data, [1, 2, 3, 4, 6, 7])

# for loop to keep data of only the first day of each month
for index in covid_data.index:
    if covid_data['REF_DATE'][index].day != 1:
        covid_data.drop(index, inplace=True)

# removes dates after november 2020 to be consistent with supply_chain_data.csv
remove_dates_after(covid_data, 'REF_DATE', datetime.date(2020, 11, 1))

# merging the supply chain data frame with the covid dataframe
df1 = pd.merge(west_dwell, covid_data, on='REF_DATE')

# Scatter Plot with Linear Regression line to show trend between transportation times and covid cases
fig1 = px.scatter(df1, y="End-to-End Duration Shanghai-Toronto via West Coast ports in Days", x="COVID-19 cases", trendline='ols')
fig1.show()
