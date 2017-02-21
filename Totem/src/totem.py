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


ip = ['192.168.1.101', '10.100.10.191']

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

@app.route('/jiu-jitsu-class')
def jiu_jitsu_class():
    return render_template(pages['jjclass'])


if __name__ == "__main__":
    try:
        Thread(target=app.run, kwargs={'host':ip[1], 'port':5000}).start()
        t=Thread(target=tag.read_loop).start()
        t.join()
        print("saiu da Thread")
        if tag.RESULT['ok']:
            jiu_jitsu_class()
    except KeyboardInterrupt
