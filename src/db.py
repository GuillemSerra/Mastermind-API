#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import aiomysql
import os
import ujson

from aiocache import cached, RedisCache
from aiocache.serializers import PickleSerializer


DB_USER = os.environ["DB_USER"]
DB_PSWD = os.environ["DB_PSWD"]
DB_HOST = os.environ["DB_HOST"]
DB_NAME = os.environ["DB_NAME"]
MAX_HISTORY_GUESSES = 12

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
    await cursor.execute("INSERT INTO games (id, code) VALUES (%s, %s)",
                         (game_id, '&'.join(code)))
    return cursor.rowcount > 0


@cached(ttl=300, cache=RedisCache, serializer=PickleSerializer(), port=6379, endpoint='redis')
@mysql_connect(use_dict=True)
async def get_game_code(cursor, game_id):
    """
    """
    await cursor.execute("SELECT code FROM games WHERE id = %s",
                         (game_id,))

    result = await cursor.fetchone()
    return result if result is None else result['code'].split('&')


@mysql_connect()
async def insert_game_guess(cursor, game_id, guess, result):
    """
    """
    await cursor.execute("INSERT INTO history (game_id, guess, result) VALUES (%s, %s, %s)",
                         (game_id, '&'.join(guess), ujson.dumps(result)))
    return cursor.rowcount > 0


@mysql_connect()
async def get_game_history(cursor, game_id):
    """
    """
    await cursor.execute("SELECT guess, result FROM history WHERE game_id = %s ORDER BY id DESC LIMIT %s",
                         (game_id, MAX_HISTORY_GUESSES))

    return [{'guess': row[0].split('&'), 'result': ujson.loads(row[1])}
            for row in await cursor.fetchall()]
