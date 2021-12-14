"""
Secondary file for CSC110 Project

Copyright and Usage Information
===============================

This file is Copyright (c) 2020 Ryan Safaeian, Akshat aneja,
Jyotiraditya Gupta, and Manav Manoj Malviya
"""
import datetime
from pandas import DataFrame

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
    A class representing a food item, which has a product name,
    and a value_list, which represents the price of the FoodItem
    from January 1995 to September 2021

    Representational Invariant:
     - len(self.value_list) > 1
    """
    product: str
    value_list: list[float]

    def __init__(self, product: str, value_list: list) -> None:
        self.product = product
        self.value_list = value_list

    def __str__(self) -> str:
        return 'product: ' + self.product

    def calc_inflation(self) -> list[float]:
        """
        Return a list containing the rate of inflation
        over a one one month period for a FoodItem
        using the a FoodItem's value_list.

        >>> food_item = FoodItem('steak', [1.0,2.25])
        >>> inflation_list = food_item.calc_inflation()
        >>> inflation_list == [125.0]
        True
        """
        monthly_inflation_list = []

        # The base price that we will be using to assess the inflation
        # rate is the FoodItem's price in January 1995, which is the
        # first index of self._value_list.

        base_price = self.value_list[0]

        for i in range(1, len(self.value_list)):
            # inflation rate formula

            monthly_inflation = ((self.value_list[i] - base_price) / base_price) * 100
            monthly_inflation_list.append(monthly_inflation)

        return monthly_inflation_list


class Foods:
    """
    A class which represents foodItems, called food_list,
    and a category.
    """
    category: str
    food_list: list[FoodItem]

    def __init__(self, category: str, food_list: list[FoodItem]) -> None:
        self.category = category
        self.food_list = food_list

    def calc_average_inflation(self) -> list[float]:
        """
        Returns a list of floats which represents the
        average inflation rate of each month for each FoodItem
        in foods_list.
        """
        food_item_inflation = []
        avg_inflation = []

        # get all the inflation rates for each FoodItem
        # in self.food_list

        for food in self.food_list:
            inflation_list = food.calc_inflation()
            food_item_inflation.append(inflation_list)

        # this for loop removes a list in food_item_inflation
        # given that it's length is not 320, which means that
        # the FoodItem has been added to the data file after
        # January 1st 1995. So, we cannot include it
        # in our analysis, since we are looking to track
        # inflation rates from January 1st 1995.

        for i in range(len(food_item_inflation) - 1, 0, -1):
            if len(food_item_inflation[i]) != 320:
                food_item_inflation.pop(i)

        # calculate the average inflation rate for each
        # FoodItem for every month.

        for i in range(len(food_item_inflation[0])):
            avg = 0
            for x in food_item_inflation:
                avg += x[i]
            avg = avg / len(food_item_inflation[0]) * 100
            avg_inflation.append(avg)

        return avg_inflation


def create_food_items(food_data: DataFrame) -> list[FoodItem]:
    """
    Return a list of FoodItems from the food_data DataFrame
    """
    foods = []
    unique_foods = food_data[food_data.columns[1]].drop_duplicates()

    for _, row in unique_foods.iteritems():
        new_data = food_data[food_data['Products'] == row]
        value_list = new_data[new_data.columns[2]].tolist()
        foods.append(FoodItem(row, value_list))
    return foods


def determine_category(foods_list: list[FoodItem]) -> list[Foods]:
    """
    Return a list of foods from foods_list.

    Precondition:
      - len(foods_list) != []
    """
    # create an empty list with 7 sublists
    amount_of_categories = 7
    product_list = [[] for _ in range(amount_of_categories)]

    # determine which category each FoodItem belongs to
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
        given a list of foods, return a list containing lists of
        average inflation for each Food.

    Preconditions:
      - len(foods_list) != []
    """
    avg_inflation_list = []

    for f in foods_lst:
        avg_inflation_list.append(f.calc_average_inflation())

    return avg_inflation_list


def create_inflation_dataframe(date_list: list[datetime.date],
                               infl_avg_list: list[list[float]]) -> DataFrame:
    """
    Create a new DataFrame, given date_list, which represents the dates
    from January 1995 to September 2021 and infl_avg_list, which represents
    the a list that contains a list containg floats, which represent
    the inflation for a  Foods object.

    Preconditions:
      - len(infl_avg_list) == 7
      - all(len(sublist) == len(date_list) for sublist in infl_avg_list)
    """
    d = {'DATE': date_list, 'MEAT_AVG_INFL': infl_avg_list[0],
         'DAIRY_AVG_INFL': infl_avg_list[1], 'FRUIT_AVG_INFL': infl_avg_list[2],
         'VEG_AVG_INFL': infl_avg_list[3], 'MISC_AVG_INFL': infl_avg_list[4],
         'HYGEINE_AVG_INFL': infl_avg_list[5], 'OTHER_AVG_INFL': infl_avg_list[6]}
    return DataFrame(data=d)


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
