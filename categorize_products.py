"""
Enter text here
"""
import copy

import pandas
from pandas import DataFrame
import datetime
from data_cleanup import dates_to_datetime

# CONSTANTS
MEAT = ['steak', 'rib', 'beef', 'chops', 'roast', 'bacon',
        'wiener', 'salmon', 'chicken']
DAIRY = ['milk', 'butter', 'egg', 'cheese']
FRUIT = ['apple', 'banana', 'grapefruit', 'orange',
         'tomato', 'fruit']
VEGETABLE = ['cabbage', 'celery', 'mushroom', 'carrot',
             'onion', 'potato', 'bean']
MISCELLANEOUS_FOOD = ['soda', 'coffee', 'flour',
                      'ketchup', 'sugar', 'oil', 'soup', 'baby',
                      'tear', 'drink', 'macaroni', 'flakes']
HYGIENE = ['laundry', 'towels', 'tissue', 'shampoo',
           'deodorant', 'toothpaste']


class FoodItem:
    """
    enter text
    """
    product: str
    date_list: list
    value_list: list

    def __init__(self, product: str, date_list: list, value_list: list) -> None:
        self.product = product
        self.date_list = date_list
        self.value_list = value_list

    def __str__(self) -> str:
        return 'product: ' + self.product

    def __repr__(self) -> str:
        return 'product: ' + self.product

    def calc_inflation(self):
        monthly_inflation_list = []
        BASE_PRICE = self.value_list[0]
        for i in range(1, len(self.value_list)):
            monthly_inflation = ((self.value_list[i] - BASE_PRICE) / BASE_PRICE) * 100
            monthly_inflation_list.append(monthly_inflation)
        return monthly_inflation_list


class Foods:
    """
    Enter text here
    """
    category: str
    food_list: list[FoodItem]

    def __init__(self, category: str, food_list: list[FoodItem]) -> None:
        self.category = category
        self.food_list = food_list

    def calc_average_inflation(self) -> list[float]:
        inflations = []
        avg_inflation = []
        for food in self.food_list:
            inflation_list = food.calc_inflation()
            inflations.append(inflation_list)

        for i in range(len(inflations) - 1, 0, -1):
            if len(inflations[i]) != 320:
                inflations.pop(i)

        for i in range(len(inflations[0])):
            avg = 0
            for j in range(len(inflations)):
                avg += inflations[j][i]
            avg = avg / len(inflations[0]) * 100
            avg_inflation.append(avg)

        return avg_inflation


def organize_foods(food_data: DataFrame) -> list[FoodItem]:
    """
    Enter text here
    """
    foods = []
    dates_to_datetime(food_data, 'REF_DATE')
    unique_foods = food_data[food_data.columns[1]].drop_duplicates()
    date_list = food_data[food_data.columns[0]].drop_duplicates().tolist()

    for _, row in unique_foods.iteritems():
        new_data = food_data[food_data['Products'] == row]
        value_list = new_data[new_data.columns[2]].tolist()
        foods.append(FoodItem(row, date_list, value_list))
    return foods


def determine_category(foods_list: list[FoodItem]) -> list[Foods]:
    """
    Determine which category row belongs to.
    """
    amount_of_categories = 7
    product_list = [[] for _ in range(amount_of_categories)]

    for food in foods_list:
        if any(f in food.product.lower() for f in MEAT):
            product_list[0].append(food)
        elif any(f in food.product.lower() for f in DAIRY):
            product_list[1].append(food)
        elif any(f in food.product.lower() for f in FRUIT):
            product_list[2].append(food)
        elif any(f in food.product.lower() for f in VEGETABLE):
            product_list[3].append(food)
        elif any(f in food.product.lower() for f in MISCELLANEOUS_FOOD):
            product_list[4].append(food)
        elif any(f in food.product.lower() for f in HYGIENE):
            product_list[5].append(food)
        else:
            product_list[6].append(food)

    meat_products = Foods('MEATS', product_list[0])
    dairy_products = Foods('DAIRY', product_list[1])
    fruit_products = Foods('FRUITS', product_list[2])
    veg_products = Foods('VEGETABLES', product_list[3])
    misc_products = Foods('MISCELLANEOUS FOOD', product_list[4])
    hygiene_products = Foods('HYGIENE', product_list[5])
    other_products = Foods('OTHER', product_list[6])

    return [meat_products, dairy_products, fruit_products,
                veg_products, misc_products, hygiene_products,
                other_products]


def get_average_inflation(foods_lst: list[Foods]) -> list[list[float]]:
        """
        ENTER TEXT HERE
        """
        avg_inflation_list = []

        for f in foods_lst:
            avg_inflation_list.append(f.calc_average_inflation())

        return avg_inflation_list


def create_inflation_datafram(date_list: list[datetime.date], infl_avg_list: list[list[float]]) -> DataFrame:
        d = {'DATE': date_list[:len(date_list)-1], 'MEAT_AVG_INFL': infl_avg_list[0],
              'DAIRY_AVG_INFL': infl_avg_list[1], 'FRUIT_AVG_INFL': infl_avg_list[2],
              'VEG_AVG_INFL': infl_avg_list[3], 'MISC_AVG_INFL': infl_avg_list[4],
              'HYGEINE_AVG_INFL': infl_avg_list[5], 'OTHER_AVG_INFL': infl_avg_list[6]}
        print(len(date_list[:len(date_list)-1]), len(infl_avg_list[0]))
        return pandas.DataFrame(data=d)

