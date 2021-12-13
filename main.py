"""
Enter text here
"""
import pandas as pd
import plotly.express as px
from data_cleanup import remove_columns, filter_for_value
from categorize_products import *
from linear_regression_model import *
import matplotlib

food_data = pandas.read_csv('data/food_data.csv')
remove_columns(food_data, [1, 2, 4, 5, 6, 7, 8, 9, 11, 12, 14])
filter_for_value(food_data, {3: 't'})
foods = organize_foods(food_data)
foods_lst = determine_category(foods)
avg_inflation_list = get_average_inflation(foods_lst)
df = create_inflation_datafram(foods[0].date_list, avg_inflation_list)

df.plot.line(x="DATE")

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
