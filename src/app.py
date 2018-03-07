#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import logging
import os
import ujson
import traceback

from quart import Quart, request

# App modules
from db import create_game, get_game_code, insert_game_guess, get_game_history
from utils import make_json_response, get_sha
from mastermind import play_guess, get_random_code, validate_guess

# Quart config
app = Quart(__name__)
app.config['JSON_AS_ASCII'] = False  # jsonify utf-8
app.secret_key = 'poqtygsbaslkyab7823b,jkfgasduog'
app.config['CURRENT_SESSION'] = ''


# Logger config
logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')
logger = logging.getLogger('APP')


@app.route('/game/new', methods=['GET'])
async def game_new():
    """
    """
    game_id = get_sha()
    code = get_random_code()

    logger.debug("New game /game/new: %s || %s" % (game_id, code))
    valid_game = await create_game(game_id, code)
    if not valid_game:
        return make_json_response(code=1, msg='Something went wrong')
    else:
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
    logger.debug("Code for %s: %s" % (game_id, code))
    if code is None:
        return make_json_response(code=1, msg='game_id not valid')

    if not validate_guess(code, guess):
        return make_json_response(code=1, msg='guess not valid')

    try:
        result = await play_guess(code, guess)
        logger.debug("Game: %s, Guess: %s, Result: %s" % (game_id, guess, result))
    except Exception as e:
        logging.error(traceback.format_exc())
        return make_json_response(code=1, msg='guess not valid')
    
    await insert_game_guess(game_id, guess, result)
    
    return make_json_response(code=0, body=result)


@app.route('/game/history', methods=['GET'])
async def game_history():
    """
    """
    params = await request.get_json()
    logger.debug("Received input /game/history: %s" % (params))
    
    game_id = params.get('game_id')

    history = await get_game_history(game_id)

    return make_json_response(code=0, body=history)


# APP start for debug
if __name__ == '__main__':
    app.run('0.0.0.0', 8080)
