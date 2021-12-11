"""
Enter text here
"""
from pandas import DataFrame
from data_cleanup import remove_columns
#CONSTANTS
MEAT = ['steak', 'rib', 'beef', 'chops', 'roast', 'bacon',
        'wiener', 'salmon', 'chicken']
DAIRY = ['milk', 'butter', 'egg', 'cheese']
FRUITS = ['apple', 'banana', 'grapefruit', 'orange',
          'tomato', 'fruit']
VEGETABLES = ['cabbage', 'celery', 'mushroom', 'carrot',
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

    def __init__(self, product: str, category: str, date_list: list, value_list: list) -> None:
        self.product = product
        self.category = category
        self.date_list = date_list
        self.value_list = value_list

    def __str__(self) -> str:
        return 'name: ' + self.produxcgt


def categorize_foods(food_data: DataFrame) -> list[FoodItem]:
    """
    Enter text here
    """
    unique_foods = food_data[food_data.columns[1]].drop_duplicates()
    foods = []
    for _, row in unique_foods.iteritems():
        product = row
        new_data = food_data[food_data['Products'] == row]
        date_list = new_data[new_data.columns[0]].tolist()
        value_list = new_data[new_data.columns[2]].tolist()

    return foods


