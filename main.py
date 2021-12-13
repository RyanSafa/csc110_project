"""
Enter text here
"""
import pandas
from data_cleanup import remove_columns, filter_for_value
from categorize_products import *
import matplotlib

food_data = pandas.read_csv('data/food_data.csv')
remove_columns(food_data, [1, 2, 4, 5, 6, 7, 8, 9, 11, 12, 14])
filter_for_value(food_data, {3: 't'})
foods = organize_foods(food_data)
foods_lst = determine_category(foods)
avg_inflation_list = get_average_inflation(foods_lst)
df = create_inflation_datafram(foods[0].date_list, avg_inflation_list)

df.plot.line(x="DATE")
