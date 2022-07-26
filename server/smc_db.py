# curd actions related to newsmerpdb
import asyncio
from dataclasses import dataclass
from enum import Enum

import mysql.connector
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor
import os

SMC_DB_PASSWD = os.getenv('SMC_DB_PASSWD')
if SMC_DB_PASSWD is None:
    raise LookupError("SMC_DB_PASSWD env not set")

class Meal(Enum):
    BREAKFAST = 1
    LUNCH = 2
    SNACKS = 3
    DINNER = 4

@dataclass
class FoodItem:
    product_id: int
    name: str
    meal: int # Follows enum Meal
    special: bool


con = None
def get_connection() -> MySQLConnection:
    global con
    if con is None:
        print("Making DB connection")
        con = mysql.connector.connect(
                user='canteenadmin',
                password=SMC_DB_PASSWD,
                host='10.0.0.139',
                database='django',
                ssl_disabled=True)
    return con

# {'id': 253, 'attimeof_id': 3, 'product_id': 253, 'image':
        # 'Amul Butter .jpg', 'pname': 'Amul Butter ',
        # 'r_uprice': 5.0, 'nr_uprice': 5.0, 'available':
        # 'Yes', 'special': 'No'}]

async def get_menu() -> list[FoodItem]:
    # TODO implement caching
    raw_menu_list = await asyncio.get_event_loop().run_in_executor(None,_get_menu)

    menu_items: list[FoodItem] = []
    for raw_item in raw_menu_list:
        item = FoodItem(
            product_id=raw_item['id'],
            name=raw_item['pname'],
            meal=raw_item['attimeof_id'],
            special= True if raw_item['special'] == 'Yes' else False)
        menu_items.append(item)

    return menu_items

MENU_QUERY = """
SELECT
  *
FROM
  canteen_attimeof_food
  JOIN canteen_product ON canteen_attimeof_food.product_id = canteen_product.id
WHERE
  canteen_product.available = 'Yes'
ORDER BY
  canteen_attimeof_food.attimeof_id,
  canteen_product.id;
"""

def _get_menu() -> list[dict]:
    con = get_connection()
    cursor: MySQLCursor = con.cursor(dictionary=True)
    try:
        with cursor:
            cursor.execute(MENU_QUERY)
            return cursor.fetchall()
    except:
        # If error then reopen connection from next time
        con = None
        return []


def close_connection() -> None:
    global con
    if con is not None:
        con.close()
