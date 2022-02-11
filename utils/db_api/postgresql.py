import contextlib
from typing import Optional, AsyncIterator

import asyncpg

from data import config


class Database:

    def __init__(self):
        self._pool: Optional[asyncpg.Pool] = None

    async def get_all_orders(self):
        sql = "SELECT order_info FROM orders"
        sql_output = await self.execute(sql, fetch=True)
        sql = "DELETE FROM orders"
        await self.execute(sql, execute=True)
        return sql_output

    async def new_order(self, customer_id, order_info):
        sql = "INSERT INTO orders (customer_id, order_info) VALUES ($1,$2);"
        return await self.execute(sql, customer_id, order_info, execute=True)

    async def delete_item(self, item_id):
        sql = "DELETE FROM items WHERE id = $1"
        return await self.execute(sql, item_id, execute=True)

    async def update_item_info(self, what_update, new_value, item_id):
        if what_update == 'item_name':
            sql = "UPDATE items SET item_name = $1 WHERE id = $2;"
        elif what_update == 'price':
            sql = "UPDATE items SET price = $1 WHERE id = $2;"
        elif what_update == 'description':
            sql = "UPDATE items SET description = $1 WHERE id = $2;"
        else:
            sql = "UPDATE items SET photo_link = $1 WHERE id = $2;"

        return await  self.execute(sql, new_value, item_id, execute=True)

    async def show_sort_items(self):
        sql = "SELECT * FROM items ORDER BY item_name LIMIT 20 "
        return await self.execute(sql, fetch=True)

    async def get_item_by_id(self, id):
        sql = "SELECT * FROM items WHERE id=$1"
        return await self.execute(sql, id, fetchrow=True)

    async def show_items(self, text):
        text = f'%{text}%'
        sql = "SELECT * FROM items WHERE item_name ILIKE $1;"
        return await self.execute(sql, text, fetch=True)

    async def add_new_item(self, item_name, price, description, photo_link):
        sql = "INSERT INTO items (item_name, price, description, photo_link) VALUES ($1,$2,$3,$4)"
        return await self.execute(sql, item_name, price, description, photo_link, execute=True)

    async def add_new_question(self, user_id, question):
        sql = "INSERT INTO support(user_id,question) VALUES ($1,$2)"
        return await self.execute(sql, user_id, question, execute=True)

    async def get_questions(self):
        sql = "SELECT (id, user_id, question) FROM support"
        return await self.execute(sql, fetch=True)

    async def delete_question_from_database(self, id):
        sql = "DELETE FROM support WHERE id=$1"
        return await self.execute(sql, id, execute=True)

    async def get_question(self, pk):
        sql = "SELECT (question) FROM support WHERE id=$1"
        return await self.execute(sql, pk, fetchrow=True)

    async def get_all_users_ids(self):
        sql = "SELECT user_id FROM users"
        return await self.execute(sql, fetch=True)

    async def get_balance(self, user_id):
        sql = 'SELECT balance FROM users WHERE user_id = $1;'
        return await self.execute(sql, user_id, fetchrow=True)

    async def check_user_or_register_referral(self, invite_code):
        sql = 'SELECT referred FROM referral WHERE referred=$1;'
        return await self.execute(sql, invite_code, fetchrow=True)

    async def register_user(self, referral_id, referred_id):
        sql = 'INSERT INTO referral (referral,referred) VALUES ($1,$2);'
        await self.execute(sql, referral_id, referred_id, execute=True)
        sql = 'INSERT INTO users (user_id, balance) VALUES ($1,$2)'
        await self.execute(sql, referred_id, 0, execute=True)

    async def add_10_dollars(self, user_id):
        sql = 'SELECT balance FROM users WHERE user_id =$1;'
        sql_output = await self.execute(sql, user_id, fetchrow=True)

        if sql_output is None:
            sql = 'INSERT INTO users (user_id, balance) VALUES ($1,$2)'
            await self.execute(sql, user_id, 10, execute=True)
        else:
            balance = sql_output[0]
            new_balance = balance + 10
            sql = 'UPDATE users SET balance = $1 WHERE user_id=$2;'
            await self.execute(sql, new_balance, user_id, execute=True)

    async def new_description(self, description):
        sql = "INSERT INTO cash (val) VALUES ($1)"
        await self.execute(sql, description, execute=True)
        sql = "SELECT id FROM cash WHERE val = $1"
        return await self.execute(sql, description, fetchval=True)

    async def get_cashed_description(self, id):
        sql = "SELECT val FROM cash WHERE id = $1"
        sql_output = await self.execute(sql, id, fetchval=True)
        sql = "DELETE FROM cash WHERE id= $1"
        await self.execute(sql, id, execute=True)
        return sql_output

    async def create_table_cash(self):
        sql = """
                CREATE TABLE IF NOT EXISTS cash (
                id SERIAL PRIMARY KEY,
                val TEXT NOT NULL
                );
                """
        await self.execute(sql, execute=True)

    async def create_table_referral(self):
        sql = """
                CREATE TABLE IF NOT EXISTS referral (
                id SERIAL PRIMARY KEY,
                referral BIGINT NOT NULL ,
                referred INT NOT NULL
                );
                """

        await self.execute(sql, execute=True)

    async def create_table_orders(self):
        sql = """
                        CREATE TABLE IF NOT EXISTS orders (
                        id SERIAL PRIMARY KEY,
                        customer_id BIGINT NOT NULL ,
                        order_info TEXT NOT NULL
                        
                        );
                        """
        await self.execute(sql, execute=True)

    async def create_table_items(self):
        sql = """
                CREATE TABLE IF NOT EXISTS items (
                id SERIAL PRIMARY KEY,
                item_name VARCHAR(255) NOT NULL ,
                price INT NOT NULL,
                description TEXT NOT NULL,
                photo_link VARCHAR(255) NOT NULL
                );
                """

        await self.execute(sql, execute=True)

    async def create_table_support(self):
        sql = """
                CREATE TABLE IF NOT EXISTS support (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL ,
                question VARCHAR(255) NOT NULL
                );
                """

        await self.execute(sql, execute=True)

    async def create_table_users(self):
        sql = """
                CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL ,
                balance BIGINT DEFAULT 0
                );
                """

        await self.execute(sql, execute=True)

    async def create_table_help(self):
        sql = """
                    CREATE TABLE IF NOT EXISTS help (
                    id SERIAL PRIMARY KEY,
                    customer_id BIGINT NOT NULL UNIQUE,
                    question VARCHAR(255) NOT NULL
                    );
                    """

        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self._transaction() as connection:  # type: asyncpg.Connection
            if fetch:
                result = await connection.fetch(command, *args)
            elif fetchval:
                result = await connection.fetchval(command, *args)
            elif fetchrow:
                result = await connection.fetchrow(command, *args)
            elif execute:
                result = await connection.execute(command, *args)
        return result

    # Это можно просто скопировать для корректной работы с соединениями
    @contextlib.asynccontextmanager
    async def _transaction(self) -> AsyncIterator[asyncpg.Connection]:
        if self._pool is None:
            self._pool = await asyncpg.create_pool(
                user=config.DB_USER,
                password=config.DB_PASS,
                host=config.DB_HOST,
                database=config.DB_NAME,
            )
        async with self._pool.acquire() as conn:  # type: asyncpg.Connection
            async with conn.transaction():
                yield conn

    async def close(self) -> None:
        if self._pool is None:
            return None

        await self._pool.close()
