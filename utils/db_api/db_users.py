from typing import Union

import asyncpg
from asyncpg import Pool, Connection

from data.config import DB_USER, DB_PASS, IP, DB_NAME


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=DB_USER,
            password=DB_PASS,
            host=IP,
            database=DB_NAME
        )
        return self.pool
    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval : bool = False,
                      fetchrow: bool = False,
                      execute: bool = False):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result
    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS USERS(
        telegram_id int NOT NULL,
        fullname varchar(255) NULL,
        PRIMARY KEY(telegram_id)
        );
        """
        await self.execute(sql, execute=True)
    async def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return await self.execute(sql, fetch=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += ' AND '.join(
            [f'{item} = ${num}' for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def select_user(self, **kwargs):
        sql = """
        SELECT * FROM Users WHERE 
        """
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def add_user(self, telegram_id: int, fullname: str):
        sql = """
        INSERT INTO Users (telegram_id, fullname) VALUES($1, $2)
        """
        return await self.execute(sql, telegram_id, fullname, execute=True)

    async def update_fullname(self, fullname, telegram_id):
        sql = """
        UPDATE Users SET fullname=$1 WHERE telegram_id=$2"""
        return await self.execute(sql, fullname, telegram_id, execute=True)

    async def delete_users(self):
        sql = """
        DELETE FROM Users WHERE TRUE"""
        await self.execute(sql, execute=True)

    async def drop_table(self):
        sql = """
        DROP TABLE Users
        """
        await self.execute(sql, execute=True)