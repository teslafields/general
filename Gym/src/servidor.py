#! /usr/bin/python

__author__ = "benhur"
__date__ = "$12/12/2016 09:20:34$"

import time
from flask import Flask, request, render_template, redirect, url_for, json, jsonify
from threading import Thread
import json
import subprocess
import os, sys
import random
from datetime import datetime
from collections import deque

INDEX = 'index.html'
LIST_TEMP = {'temperature': deque([], maxlen=100), 'datetime': deque([], maxlen=100)}
temperature = 0.0
cont = 0
pages = {
    'index': 'index.html',
    'student': 'student.html',
    'teacher': 'teacher.html',
    'gym': 'gym.html'
    }

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    print('route /')
    return render_template(INDEX, pages=pages)

# @app.route('/temperature', methods=['GET'])
# def get_temp():
#     print('route /temperature')
#     x = random.uniform(1,10)
#     global temperature
#     temperature = temperature + x
#     if temperature > 80:
#         temperature = 0.0
#     LIST_TEMP['temperature'].append([cont, temperature])
#     LIST_TEMP['datetime'].append(cont)
#     lis = LIST_TEMP.copy()
#     lis['temperature'] = list(LIST_TEMP['temperature'])
#     lis['datetime'] = list(LIST_TEMP['datetime'])
#     global cont
#     cont += 1
#     return jsonify(result=lis)

if __name__ == "__main__":
    try:
        app.run(host='10.5.0.13', port=5010)
    except KeyboardInterrupt:
        raise SystemExit
