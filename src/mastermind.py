#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio


# Mastermind config
COLORS = ['RED', 'GREEN', 'BLUE', 'YELLOW']
CODE_LENGTH = 4


def play_guess(code, guess):
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
    return ['RED', 'GREEN', 'BLUE', 'YELLOW']
