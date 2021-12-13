"""
linear regression
"""

import pandas as pd
import datetime
import plotly.express as px
from data_cleanup import keep_for_value, remove_columns, dates_to_datetime, remove_dates_before, remove_dates_after


# FIRST DATAFRAME FOR CONTAINERS FROM SHANGHAI TO TORONTO
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


# SECOND DATAFRAME FOR CONTAINERS PORT DWELL TIMES AT EAST COAST PORTS
east_dwell = pd.read_csv('data/supply_chain_data.csv')
# filters rows for Containers, port dwell time East Coast ports
keep_for_value(east_dwell, {'Performance indicators': 'Containers, port dwell time East Coast ports'})

# removes columns not needed
remove_columns(east_dwell, [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14])

# converts all the dates to the datetime format
dates_to_datetime(east_dwell, 'REF_DATE')

# removes rows with dates before the pandemic
remove_dates_before(east_dwell, 'REF_DATE', datetime.date(2020, 2, 1))

# renames the column
east_dwell.rename(columns={'VALUE': 'Port Dwell Time at East Coast Ports in Days'}, inplace=True)


# DATAFRAME FOR DEATHS CAUSED BY COVID
covid_data = pd.read_csv('data/WHO-COVID-19-global-data.csv')

# filters rows for Canadian data only
keep_for_value(covid_data, {'Country': 'Canada'})

# converts all the dates to the datetime format
dates_to_datetime(covid_data, 'Date_reported')

# renames the column
covid_data.rename(columns={'Date_reported': 'REF_DATE', 'Cumulative_deaths': 'Deaths due to COVID-19'}, inplace=True)

# removes columns not needed
remove_columns(covid_data, [1, 2, 3, 4, 5, 6])

# for loop to keep data of only the first day of each month
for index in covid_data.index:
    if covid_data['REF_DATE'][index].day != 1:
        covid_data.drop(index, inplace=True)

# removes dates after july to be consistent with supply_chain_data.csv
remove_dates_after(covid_data, 'REF_DATE', datetime.date(2021, 7, 1))

# merging both the supply chain data frames with the covid dataframe
df1 = pd.merge(west_dwell, covid_data, on='REF_DATE')
df2 = pd.merge(east_dwell, covid_data, on='REF_DATE')

# Scatter Plots with Linear Regression lines to show trends between duration and covid deaths.
fig1 = px.scatter(df1, y="End-to-End Duration Shanghai-Toronto via West Coast ports in Days", x="Deaths due to COVID-19", trendline='ols')
fig1.show()
fig2 = px.scatter(df2, y="Port Dwell Time at East Coast Ports in Days", x="Deaths due to COVID-19", trendline='ols')
fig2.show()
