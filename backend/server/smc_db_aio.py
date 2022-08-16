# curd actions related to newsmerpdb
# TODO convert to aiomysql
from typing import cast
import aiomysql
from dataclasses import dataclass
from enum import Enum
import os
import json
import datetime

from aiomysql.connection import asyncio

SMC_DB_PASSWD = os.getenv('SMC_DB_PASSWD')

if SMC_DB_PASSWD is None:
    raise LookupError("SMC_DB_PASSWD env not set")

class Meal(Enum):
    BREAKFAST = 1
    LUNCH = 2
    SNACKS = 3
    DINNER = 4


pool = None
async def get_pool():
    global pool
    if pool is not None:
        return pool

    print("Creating Pool to SMC db")
    pool = await aiomysql.create_pool(
            user='canteenadmin',
            password=SMC_DB_PASSWD,
            host='10.0.0.139',
            db='django',
            ssl=False)
    return cast(aiomysql.Pool, pool)

async def close_pool():
    pool = await get_pool()
    pool.close()
    print("Closing SMC db")
    await pool.wait_closed()


@dataclass
class FoodItem:
    product_id: int
    name: str
    meal: int # Follows enum Meal
    special: bool


# {'id': 253, 'attimeof_id': 3, 'product_id': 253, 'image':
        # 'Amul Butter .jpg', 'pname': 'Amul Butter ',
        # 'r_uprice': 5.0, 'nr_uprice': 5.0, 'available':
        # 'Yes', 'special': 'No'}]

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

async def get_menu() -> list[FoodItem]:
    # TODO implement caching
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(MENU_QUERY)
            raw_menu_list = await cursor.fetchall()

    menu_items: list[FoodItem] = []
    for raw_item in raw_menu_list:
        item = FoodItem(
            product_id=raw_item['id'],
            name=raw_item['pname'],
            meal=raw_item['attimeof_id'],
            special= True if raw_item['special'] == 'Yes' else False)
        menu_items.append(item)

    return menu_items


USER_DETAILS_QUERY = """
select
  uid,
  balance
from
  canteen_users
where
  email = %s;
"""

async def get_user_details(email: str):
    # TODO implement caching
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            cursor: aiomysql.Cursor
            await cursor.execute(USER_DETAILS_QUERY, (email,))
            data = await cursor.fetchone()
    return data['uid'], data['balance']

USER_PAST_ORDERS = """
select
  r.food,
  u.presentbalance,
  u.datetime
from
  canteen_userdetails as u
  join canteen_regularuserusage as r on r.userdetails_ptr_id = u.id
where
  uid = %s
order by
  datetime desc
"""

async def get_past_orders(uid: str):
    MEAL_COUNT = 20
    # TODO implement caching
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            cursor: aiomysql.Cursor
            await cursor.execute(USER_PAST_ORDERS, (uid,))
            data = await cursor.fetchmany(MEAL_COUNT)

    meal_list = []
    for meal in data:
        meal_datetime = meal['datetime'].isoformat()
        meal_items = json.dumps(meal['food'])
        balance = meal['presentbalance']
        meal_obj = {
                "balance": balance,
                "datetime": meal_datetime,
                "items": meal_items,
                }
        meal_list.append(meal_obj)

    return meal_list


async def main():
    data = await get_past_orders('18MS082')
    print(data)
    await close_pool()

if __name__ == '__main__':
    asyncio.run(main())
