#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import logging
import os
import ujson

from quart import Quart, request

# Own modules
from db import create_game, get_game_code, get_game_history
from utils import make_json_response, get_sha
from mastermind import play_guess

# Quart config
app = Quart(__name__)
app.config['JSON_AS_ASCII'] = False  # jsonify utf-8
app.secret_key = 'poqtygsbaslkyab7823b,jkfgasduog'
app.config['CURRENT_SESSION'] = ''
app.debug = True

# Logger config
logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')
logger = logging.getLogger('APP')


@app.route('/game/new', methods=['GET'])
async def game_new():
    """
    """
    game_id = await create_game(get_sha())
    return make_json_response(code=0, body={'game_id': game_id})


@app.route('/game/play', methods=['POST'])
async def game_play():
    """
    """
    params = await request.get_json()
    logger.debug("Received input /game/play: %s" % (params))

    game_id = params.get('game_id')
    guess = params.get('guess')
    
    code = await get_game_code(game_id)
    if code is None:
        return make_json_response(code=1, msg='game_id not valid')

    result = play_guess(code, guess)
    logger.debug("Received input /game/history: %s" % (params))
    return make_json_response(code=0, body=result)


@app.route('/game/history', methods=['GET'])
async def game_history():
    """
    """
    params = await request.get_json()
    logger.debug("Received input /game/history: %s" % (params))
    
    game_id = params.get('game_id')

    history = await get_game_history(game_id)
    if history is None:
        return make_json_response(code=1, msg='game_id not valid')

    logger.debug("Received input /game/history: %s" % (params))
    return make_json_response(code=0, body=history)


# APP start for debug
if __name__ == '__main__':
    app.run('0.0.0.0', 8080)