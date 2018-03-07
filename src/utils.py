#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import hashlib
import time
import random


from quart import jsonify


def make_json_response(body=None, code=0, msg='ok'):
    return jsonify(code=code, msg=msg, body=body)


def get_sha():
    """
    """
    hash = hashlib.sha1()
    rand_num = str(random.randint(0, 12345))
    hash.update((str(time.time())+rand_num).encode('utf-8'))
    return hash.hexdigest()[:40]
