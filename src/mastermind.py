#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import random

from aiocache import cached, RedisCache
from aiocache.serializers import PickleSerializer


# Mastermind config
COLORS = ['RED', 'GREEN', 'BLUE', 'YELLOW', 'PURPLE']
CODE_LENGTH = 4

@cached(cache=RedisCache, serializer=PickleSerializer(), port=6379, endpoint='redis')
async def play_guess(code, guess):
    """
    """
    black_pegs = 0
    white_pegs = 0
    guess_whites = []
    code_whites = []

    for i in range(0, len(code)):
        if guess[i] == code[i]:
            black_pegs += 1
        else:
            guess_whites += [guess[i]]
            code_whites += [code[i]]

    for i in range(0, len(code_whites)):
        if guess_whites[i] in code_whites:
            white_pegs += 1
            
    return {'black_pegs': black_pegs, 'white_pegs': white_pegs}


def get_random_code():
    """
    """
    return random.sample(COLORS, CODE_LENGTH)


def validate_guess(code, guess):
    """
    """
    if len(guess) != len(code):
        return False
    elif not isinstance(guess, list):
        return False
    else:
        return True
