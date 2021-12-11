"""
Enter text here
"""
import pandas
from data_cleanup import remove_columns, filter_for_value
import categorize_products

food_data = pandas.read_csv('data/food_data.csv')
remove_columns(food_data, [1, 2, 4, 5, 6, 7, 8, 9, 11, 12, 14])
filter_for_value(food_data, {3: 't'})
my_set = (categorize_products.categorize_foods(food_data))
