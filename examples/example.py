#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import random

COLORS = ['RED', 'GREEN', 'BLUE', 'YELLOW', 'PURPLE']
CODE_LENGTH = 4

# CREATE GAME
# ===========
url = "http://localhost:8080/game/new"
payload = {}
headers = {'content-type': 'application/json'}

print("\nCREATE NEW GAME: %s" % (url,))

response = requests.request("GET", url, data=json.dumps(payload), headers=headers)

print("RESPONSE: %s\n\n" % (response.text,))


# PLAY GAME
# =========
game_id = json.loads(response.text)['body']['game_id']
url = "http://localhost:8080/game/play"
headers = {'content-type': 'application/json'}

print("PLAY GAME: %s, ID: %s" % (url, game_id))

for i in range(0,5):
    guess = random.sample(COLORS, CODE_LENGTH)
    print("GUESS: %s" % (guess,))
    
    payload = {"game_id": game_id, "guess": guess}
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

    print("RESULT: %s\n" % (response.text,))


# GET HISTORY
# ===========
url = "http://localhost:8080/game/history"
payload = {'game_id': game_id}
headers = {'content-type': 'application/json'}

print("\nGET GAME HISTORY: %s, ID: %s" % (url, game_id))

response = requests.request("GET", url, data=json.dumps(payload), headers=headers)

print("RESULT: %s\n" % (response.text,))
