#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import aiomysql
import os


DB_USER = os.environ["DB_USER"]
DB_PSWD = os.environ["DB_PSWD"]
DB_HOST = os.environ["DB_HOST"]
DB_NAME = os.environ["DB_NAME"]


# DB POOL INIT
# ============
pool = None

async def init_mysql():
    global pool
    pool = await aiomysql.create_pool(host=DB_HOST, port=3306,
                                      user=DB_USER, password=DB_PSWD,
                                      db=DB_NAME, loop=loop)

loop = asyncio.get_event_loop()
loop.run_until_complete(init_mysql())


# MySQL Decorators
# ================
def mysql_connect(*args, **kwargs):
    # default `mysql_connect` paramaters
    params = {'use_dict': False, 'database': DB_NAME}

    def real_decorator(f):
        async def wrapper(*args, **kwargs):
            async with pool.acquire() as conn:
                await conn.select_db(params['database'])
                cur_type = aiomysql.DictCursor if params['use_dict'] else aiomysql.Cursor
                async with conn.cursor(cursor=cur_type) as cursor:
                    args = (cursor,) + args
                    val = await f(*args, **kwargs)
                    await conn.commit()
                    return val

        wrapper.__name__ = f.__name__
        return wrapper

    # Decorator with optional arguments:
    # (https://stackoverflow.com/a/3931903)
    if len(args) == 1 and callable(args[0]):
        # No arguments, this is the decorator
        # Set default values for the arguments
        return real_decorator(args[0])
    else:
        for k, v in kwargs.items():
            params[k] = v
        return real_decorator



# DB OPERATIONS
# =============
@mysql_connect()
async def create_game(cursor, game_id, code):
    """
    """
    return None


@mysql_connect()
async def get_game_code(cursor, game_id):
    """
    """
    return None


@mysql_connect()
async def get_game_history(cursor, game_id):
    """
    """
    return None
