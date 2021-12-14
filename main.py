"""
Main file for CSC110 Project

Copyright and Usage Information
===============================

This file is Copyright (c) 2020 Ryan Safaeian, Akshat aneja,
Jyotiraditya Gupta, and Manav Manoj Malviya
"""
import datetime
import matplotlib.pyplot as mpl
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

from categorize_products import create_food_items, \
    create_inflation_dataframe, determine_category, \
    get_average_inflation
from data_cleanup import dates_to_datetime, filter_for_value, \
    remove_columns, remove_dates_after
from linear_regression_model import clean_covid_for_cases_df, clean_up_end_to_end_df

food_data = pd.read_csv('data/food_data.csv')

# data clean up
remove_columns(food_data, [1, 2, 4, 5, 6, 7, 8, 9, 11, 12, 14])
filter_for_value(food_data, {3: 't'})
dates_to_datetime(food_data, 'REF_DATE')


foods = create_food_items(food_data)
foods_lst = determine_category(foods)
avg_inflation_list = get_average_inflation(foods_lst)
date_list = food_data[food_data.columns[0]].drop_duplicates().tolist()
df = create_inflation_dataframe(date_list[:len(date_list) - 1], avg_inflation_list)

# create a line plot with 'DATE' as the x-axis and
# the y-axis as the inflation for each category of
# products

df.plot.line(x="DATE")
plt.ylabel('Inflation')
mpl.show()

e2e_data = pd.read_csv('data/supply_chain_data.csv')
clean_up_end_to_end_df(e2e_data)
covid_data = pd.read_csv('data/WHO-COVID-19-global-data.csv')
clean_covid_for_cases_df(covid_data)

# removes dates in covid_data to be consistent with e2e_data
remove_dates_after(covid_data, 'REF_DATE', datetime.date(2020, 11, 1))

# merging the supply chain data frame with the covid dataframe
df1 = pd.merge(e2e_data, covid_data, on='REF_DATE')

# Scatter Plot with Linear Regression line to show trend between transportation times and covid cases
fig1 = px.scatter(df1, y="End-to-End Duration Shanghai-Toronto via West Coast ports in Days", x="COVID-19 cases",
                  trendline='ols')
fig1.show()
