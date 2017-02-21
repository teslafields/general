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
from Read import ReadTag

# Object to read the tag
tag = ReadTag()

INDEX = 'index.html'

pages = {
    'index': 'index.html',
    'jjclass': 'jjclass.html',
    'gym': 'gym.html'
    }

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    print('route /')
    return render_template(INDEX, pages=pages)


if __name__ == "__main__":
    try:
        Thread(target=tag.read_loop).start()
        app.run(host='localhost', port=5000)
    except KeyboardInterrupt:
        raise SystemExit
