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
from flask_cors import CORS, cross_origin
from flask_basicauth import BasicAuth


INDEX = 'index.html'
# LIST_TEMP = {'temperature': deque([], maxlen=100), 'datetime': deque([], maxlen=100)}
LIST_TEMP = {'exercicio': [], 'title': None, 'id': []}
musculo = ['Triceps', 'Biceps', 'Abs', 'Peito', 'Costas', 'Perna']

cont = 0
pages = {
    'index': 'index.html',
    }

app = Flask(__name__, static_folder='static')
app.config['BASIC_AUTH_USERNAME'] = 'benhurzi@gmail.com'
app.config['BASIC_AUTH_PASSWORD'] = 'fitlabcore'

basic_auth = BasicAuth(app)

CORS(app)

@app.route('/')
def index():
    print('route /')
    return render_template(INDEX)

@app.route('/exercicio', methods=['GET'])
@basic_auth.required
def get_temp():
    global musculo
    lis = LIST_TEMP.copy()
    lis['exercicio'] = musculo
    lis['title'] = 'Musculo'
    for i in range(0, len(musculo)):
        lis['id'] = i
    global cont
    cont += 1
    # lis['temp'] = [[date, temp]]
    return jsonify(result=lis)

if __name__ == "__main__":
    try:
        app.run(host='localhost', port=5010)
    except KeyboardInterrupt:
        raise SystemExit
