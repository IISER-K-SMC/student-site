# curd actions related to newsmerpdb
# TODO convert to aiomysql
import asyncio

from dataclasses import dataclass
from enum import Enum
from typing import Optional

import mysql.connector
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from contextlib import contextmanager
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



@contextmanager
def get_connection():
    con = mysql.connector.connect(
            user='canteenadmin',
            password=SMC_DB_PASSWD,
            host='10.0.0.139',
            database='django',
            ssl_disabled=True)
    try:
        yield con
    finally:
        con.close()


# {'id': 253, 'attimeof_id': 3, 'product_id': 253, 'image':
        # 'Amul Butter .jpg', 'pname': 'Amul Butter ',
        # 'r_uprice': 5.0, 'nr_uprice': 5.0, 'available':
        # 'Yes', 'special': 'No'}]

async def get_menu() -> list[FoodItem]:
    # TODO implement caching
    try:
        raw_menu_list = await asyncio.wait_for(
                    asyncio.get_event_loop().run_in_executor(None,_get_menu),
                    1
                )
    except asyncio.TimeoutError:
        global con
        con = None
        return []
        

    menu_items: list[FoodItem] = []
    for raw_item in raw_menu_list:
        item = FoodItem(
            product_id=raw_item['id'],
            name=raw_item['pname'],
            meal=raw_item['attimeof_id'],
            special= True if raw_item['special'] == 'Yes' else False)
        menu_items.append(item)

    return menu_items


async def get_pname(product_id: int) -> str:
    if product_id == 0:
        return "Overall"
    product_name = await asyncio.get_event_loop().run_in_executor(None,_get_pname, product_id)
    if product_name:
        return product_name 
    return "Failed to get Name"

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
    with get_connection() as con:
        cursor: MySQLCursor = con.cursor(dictionary=True)
        try:
            with cursor:
                cursor.execute(MENU_QUERY)
                return cursor.fetchall()
        except:
            # If error then reopen connection from next time
            con = None
            return []


def _get_pname(product_id: int) -> Optional[str]:
    with get_connection() as con:
        cursor: MySQLCursor = con.cursor()
        try:
            with cursor:
                cursor.execute("""
                        SELECT
                          pname
                        FROM
                          canteen_product
                        WHERE
                          id = %s
                        LIMIT 1
                        """, (product_id,))
                db_data = cursor.fetchone()
                if db_data:
                    return db_data[0]
                else:
                    return None
        except:
            return None
