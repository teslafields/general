#! /usr/bin/python

__author__ = "maickel"
__date__ = "$30/05/2016 09:20:34$"

import time
from flask import Flask, request, render_template, redirect, url_for, json, jsonify
from views.forms import *
from threading import Thread
from kiperserver import KiperServer
from model.db_manager import *
import peewee
import subprocess
import os, sys
from utils.script_test_ssh import download_log

server = None
sv_ip = None
port = 5000

INDEX = 'index.html'
CENTER = 'center.html'

REQUEST = 'request.html'
LOGS = 'logs.html'
BEHAVE = 'behave.html'

INSERT_IPWALL = 'insert_ipwall.html'
DELETE_IPWALL = 'delete_ipwall.html'
DELETE_ALL_IPWALLS = 'delete_all_ipwalls.html'

INSERT_SET_RF = 'insert_set_rf.html'
DELETE_SET_RF = 'delete_set_rf.html'
DELETE_ALL_SET_RF = 'delete_all_set_rf.html'

INSERT_USER = 'insert_user.html'
DELETE_USER = 'delete_user.html'
DELETE_ALL_USERS = 'delete_all_users.html'

INSERT_QRCODE_READER = 'insert_qrcode_reader.html'
DELETE_QRCODE_READER = 'delete_qrcode_reader.html'
DELETE_ALL_QRCODE_READERS = 'delete_all_qrcode_readers.html'

INSERT_GUEST = 'insert_guest.html'
DELETE_GUEST = 'delete_guest.html'
DELETE_ALL_GUESTS = 'delete_all_guests.html'

INSERT_REQUEST = 'insert_request.html'

try:
    LIST_IPWALL = DbManager.get_ipwall_list()
    LIST_RF = DbManager.get_set_rf_list()
    LIST_USER = DbManager.get_user_list()
    LIST_QRCODE_READER = DbManager.get_qrcode_list()
    LIST_GUEST = DbManager.get_guest_list()
    LIST_REQUEST = []
except peewee.OperationalError:
    LIST_IPWALL = []
    LIST_RF = []
    LIST_USER = []
    LIST_QRCODE_READER = []
    LIST_GUEST = []
    LIST_REQUEST = []
    print("DB not created yet!")

pages = {
    'index': 'index.html',

    'ipwall': 'ipwall.html',
    'insert_ipwall': INSERT_IPWALL,
    'delete_ipwall': DELETE_IPWALL,
    'delete_all_ipwalls': DELETE_ALL_IPWALLS,

    'set_rf': 'set_rf.html',
    'insert_set_rf': INSERT_SET_RF,
    'delete_set_rf': DELETE_SET_RF,
    'delete_all_set_rf': DELETE_ALL_SET_RF,

    'user': 'user.html',
    'insert_user': INSERT_USER,
    'delete_user': DELETE_USER,
    'delete_all_users': DELETE_ALL_USERS,

    'qrcode_reader': 'qrcode_reader.html',
    'insert_qrcode_reader': INSERT_QRCODE_READER,
    'delete_qrcode_reader': DELETE_QRCODE_READER,
    'delete_all_qrcode_readers': DELETE_ALL_QRCODE_READERS,

    'guest': 'guest.html',
    'insert_guest': INSERT_GUEST,
    'delete_guest': DELETE_GUEST,
    'delete_all_guests': DELETE_ALL_GUESTS,

    'request': REQUEST,
    'insert_request': 'insert_request.html',
    'behave': BEHAVE,
    'logs': LOGS
}

control = {
    'ipwall': LIST_IPWALL,
    'set_rf': LIST_RF,
    'user': LIST_USER,
    'qrcode_reader': LIST_QRCODE_READER,
    'guest': LIST_GUEST,
    'request': LIST_REQUEST
}

app = Flask(__name__, static_folder='static')

# def waitTimeout(addr="10.15.15.102"):
#     ativo = True
#     while ativo:
#         stdout, stderr = subprocess.Popen('netstat -patun | grep "'+addr+'"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
#         if len(stdout) == 0:
#             ativo = False
#         time.sleep(0.5)

def flush(version):
    global server
    if server:
        if version == '1.4.2':
            server.handler.delete_all_users()
            server.handler.delete_all_set_rf()
            server.handler.delete_all_ipwalls()
        else:
            server.handler.delete_all_guests()
            server.handler.delete_all_qrcode_readers()
            server.handler.delete_all_users()
            server.handler.delete_all_set_rf()
            server.handler.delete_all_ipwalls()
    else:
        pass


@app.route('/')
def index():
    print('route /')
    return render_template(INDEX, pages=pages, control=control)

@app.route('/itsalive', methods=['GET'])
def itsalive():
    global server
    if server:
        if server.handler.future['ativo'].done():
            return jsonify(result={'connection': True})
    return jsonify(result={'connection': False})

def get_list_ipwall():
    global LIST_IPWALL
    decorated = [(dict_['ipwall_id'], dict_) for dict_ in LIST_IPWALL]
    decorated.sort()
    LIST_IPWALL = [dict_ for (key, dict_) in decorated]
    return LIST_IPWALL


def get_list_rf():
    global LIST_RF
    decorated = [(dict_['set_rf_id'], dict_) for dict_ in LIST_RF]
    decorated.sort()
    LIST_RF = [dict_ for (key, dict_) in decorated]
    return LIST_RF


def get_list_user():
    global LIST_USER
    decorated = [(dict_['user_id'], dict_) for dict_ in LIST_USER]
    decorated.sort()
    LIST_USER = [dict_ for (key, dict_) in decorated]
    return LIST_USER


def get_list_qrcode_reader():
    global LIST_QRCODE_READER
    decorated = [(dict_['qrcode_reader_id'], dict_) for dict_ in LIST_QRCODE_READER]
    decorated.sort()
    LIST_QRCODE_READER = [dict_ for (key, dict_) in decorated]
    return LIST_QRCODE_READER


def get_list_guest():
    global LIST_GUEST
    decorated = [(dict_['guest_id'], dict_) for dict_ in LIST_GUEST]
    decorated.sort()
    LIST_GUEST = [dict_ for (key, dict_) in decorated]
    return LIST_GUEST


def get_list_request():
    global LIST_REQUEST
    decorated = [(dict_['request_id'], dict_) for dict_ in LIST_REQUEST]
    try:
        decorated.sort()
    except TypeError:
        pass
    LIST_REQUEST = [dict_ for (key, dict_) in decorated]
    return LIST_REQUEST


@app.route('/connection', methods=['POST'])
def connection():
    json_request = request.get_json(force=True)
    global server
    global sv_ip
    if json_request['check'] is True:
        if not server:
            server = KiperServer(host=sv_ip, protocol=float(json_request['protocol']))
    else:
        try:
            server.shutdown()
            server = None
            #waitTimeout()
        except AttributeError:
            pass
    return jsonify(result={'msg': 'success'})


@app.route('/get_ipwalls', methods=['GET'])
def get_ipwall():
    return jsonify(result=DbManager.get_ipwall_list())


@app.route('/get_rfs', methods=['GET'])
def get_rfs():
    return jsonify(result=DbManager.get_set_rf_list())


@app.route('/get_users', methods=['GET'])
def get_users():
    return jsonify(result=DbManager.get_user_list())


@app.route('/get_qrcode_readers', methods=['GET'])
def get_qrcode_readers():
    return jsonify(result=DbManager.get_qrcode_list())


@app.route('/get_guests', methods=['GET'])
def get_guests():
    return jsonify(result=DbManager.get_guest_list())


@app.route('/get_requests', methods=['GET'])
def get_requests():
    return jsonify(result=get_list_request())


@app.route('/get_ipwall/<string:id>', methods=['GET'])
def get_ipwall_id(id):
    for ipwall in LIST_IPWALL:
        if ipwall['ipwall_id'] == int(id):
            return jsonify(result=ipwall)


@app.route('/get_behave', methods=['GET'])
def get_behave():
    global server
    server.shutdown()
    # waitTimeout()
    lis_stdout = []
    stdout, stderr = subprocess.Popen('cd ' + os.getcwd() + '/features; behave -i kiper_commands.feature --tags=ping', stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE, shell=True).communicate()  # -o '+str(os.getpid())+'.behave.log
    print('************************* BEHAVE STDOUT *************************')
    for s in stdout.decode().split('\n'):
        lis_stdout.append(s)
        print('||\t' + s)
    print('*****************************************************************')
    # waitTimeout()
    server = KiperServer()
    return jsonify(result=lis_stdout)


# *** INSERT ***
@app.route('/insert_ipwall', methods=['POST'])
def insert_ipwall():
    json_ipwall = request.get_json(force=True)
    index = None
    for value in LIST_IPWALL:
        if json_ipwall['ipwall_id'] in str(value['ipwall_id']):
            index = value
    if index:
        LIST_IPWALL.remove(index)
    form = FormInsertIpwall()
    form.set(json_ipwall)
    LIST_IPWALL.append(form.get())
    if server:
        server.handler.insert_ipwall(form.get())
    return jsonify(result={'msg': 'success'})


@app.route('/insert_set_rf', methods=['POST'])
def insert_set_rf():
    json_rf = request.get_json(force=True)
    index = None
    for value in LIST_RF:
        if json_rf['set_rf_id'] in str(value['set_rf_id']):
            index = value
    if index:
        LIST_RF.remove(index)
    form = FormInsertSetRf()
    form.set(json_rf)
    LIST_RF.append(form.get())
    if server:
        server.handler.insert_set_rf(form.get())
    return jsonify(result={'msg': 'success'})


@app.route('/insert_user', methods=['POST'])
def insert_user():
    json_user = request.get_json(force=True)
    index = None
    for value in LIST_USER:
        if json_user['user_id'] in str(value['user_id']):
            index = value
    if index:
        LIST_USER.remove(index)
    form = FormInsertUser()
    form.set(json_user)
    LIST_USER.append(form.get())
    if server:
        server.handler.insert_user(form.get())
    return jsonify(result={'msg': 'success'})


@app.route('/insert_qrcode_reader', methods=['POST'])
def insert_qrcode_reader():
    json_qrcode_reader = request.get_json(force=True)
    index = None
    for value in LIST_QRCODE_READER:
        if json_qrcode_reader['qrcode_reader_id'] in str(value['qrcode_reader_id']):
            index = value
    if index:
        LIST_QRCODE_READER.remove(index)
    form = FormInsertQrcodeReader()
    form.set(json_qrcode_reader)
    LIST_QRCODE_READER.append(form.get())
    if server:
        server.handler.insert_qrcode_reader(form.get())
    return jsonify(result={'msg': 'success'})


@app.route('/insert_guest', methods=['POST'])
def insert_guest():
    json_guest = request.get_json(force=True)
    index = None
    for value in LIST_GUEST:
        if json_guest['guest_id'] in str(value['guest_id']):
            index = value
    if index:
        LIST_GUEST.remove(index)
    form = FormInsertGuest()
    form.set(json_guest)
    LIST_GUEST.append(form.get())
    if server:
        server.handler.insert_guest(form.get())
    return jsonify(result={'msg': 'success'})

@app.route('/insert_request', methods=['POST'])
def insert_request():
    json_request = request.get_json(force=True)
    LIST_REQUEST.append(json_request)
    if json_request['request_id'] == 1:
        if server:
            server.handler.ping()
    elif json_request['request_id'] == 2:
        if server:
            server.handler.set_datetime(None, None)
    elif json_request['request_id'] == 3:
        if server:
            server.handler.vacuum()
    elif json_request['request_id'] == 4:
        if server:
            server.handler.start_emergency()
    elif json_request['request_id'] == 5:
        if server:
            server.handler.stop_emergency()
    elif json_request['request_id'] == 6:
        try:
            port = int(json_request['http_server_port'])
        except ValueError:
            port = None
        update = {'restore': json_request['check_restore'], 'http_server_ip': json_request['http_server_ip'],
                  'http_server_port': port,
                  'file_path': json_request['file_path'],
                  'update_to_version': json_request['update_to_version'],
                  'update_file': json_request['update_file']}
        if server:
            if update['restore']:
                flush(server.handler.cpu_version)
            server.handler.update_cpu(update)
    elif json_request['request_id'] == 7:
        if server:
            server.handler.get_sensors_status({'ipwall_id': int(json_request['select_ipwall_id_1'])})
    elif json_request['request_id'] == 8:
        if server:
            server.handler.get_relays_status({'ipwall_id': int(json_request['select_ipwall_id_1'])})
    elif json_request['request_id'] == 9:
        if server:
            server.handler.open_the_door({'ipwall_id': int(json_request['select_ipwall_id_2']),
                                          'door_id': int(json_request['door_id'])})
    elif json_request['request_id'] == 9:
        if server:
            server.handler.open_the_door({'ipwall_id': int(json_request['select_ipwall_id_2']),
                                          'door_id': int(json_request['door_id'])})
    elif json_request['request_id'] == 10:
        if server:
            server.handler.keep_the_door_opened({'ipwall_id': int(json_request['select_ipwall_id_2']),
                                                 'door_id': int(json_request['door_id'])})
    elif json_request['request_id'] == 11:
        if server:
            server.handler.close_the_door({'ipwall_id': int(json_request['select_ipwall_id_2']),
                                           'door_id': int(json_request['door_id'])})
    elif json_request['request_id'] == 12:
        if server:
            server.handler.reset_ipwall({'ipwall_id': int(json_request['select_ipwall_id_1'])})
    elif json_request['request_id'] == 13:
        print(json_request)
        try:
            ipwallid = int(json_request['ipwall_id'])
            port = int(json_request['http_server_port'])
            update = {'ipwall_id': ipwallid, 'http_server_ip': json_request['http_server_ip'],
                      'http_server_port': port, 'file_path': json_request['file_path'],
                      'file_name': json_request['file_name'], 'file_size': int(json_request['file_size'])}
            if server:
                server.handler.update_ipwall(update)
        except ValueError:
            return jsonify(result={'msg': 'fail'})
    elif json_request['request_id'] == 15:
        r = download_log(json_request['file_name'], 'khomp')
        print(r)
    elif json_request['request_id'] == 16:
        if server:
            flush(server.handler.cpu_version)
    elif json_request['request_id'] == 17:
        if server:
            server.handler.log_type({"new_log_type": json_request['type']})

    return jsonify(result={'msg': 'success'})


# *** EDIT ***

@app.route('/edit_ipwall/<string:id>', methods=['GET'])
def edit_ipwall(id):
    for value in LIST_IPWALL:
        if id in str(value['ipwall_id']):
            return jsonify(value)


@app.route('/edit_rf/<string:id>', methods=['GET'])
def edit_rf(id):
    for value in LIST_RF:
        if id in str(value['set_rf_id']):
            return jsonify(value)


@app.route('/edit_user/<string:id>', methods=['GET'])
def edit_user(id):
    for value in LIST_USER:
        if id in str(value['user_id']):
            return jsonify(value)


@app.route('/edit_qrcode_reader/<string:id>', methods=['GET'])
def edit_qrcode_reader(id):
    for value in LIST_QRCODE_READER:
        if id in str(value['qrcode_reader_id']):
            return jsonify(value)


@app.route('/edit_guest/<string:id>', methods=['GET'])
def edit_guest(id):
    for value in LIST_GUEST:
        if id in str(value['guest_id']):
            return jsonify(value)


# *** DELETE ***

@app.route('/delete_ipwall/<string:id>', methods=['POST'])
def delete_ipwall(id):
    if request.method == 'POST':
        index = None
        for value in LIST_IPWALL:
            if id in str(value['ipwall_id']):
                index = value
        if index:
            LIST_IPWALL.remove(index)
        db_return = None
        if server:
            server.handler.delete_ipwall({'ipwall_id': int(id)})
            while server.handler.db_return is None:
                time.sleep(0.5)
            db_return = server.handler.db_return
    return jsonify(result=db_return)


@app.route('/delete_set_rf/<string:id>', methods=['POST'])
def delete_set_rf(id):
    if request.method == 'POST':
        index = None
        for value in LIST_RF:
            if id in str(value['set_rf_id']):
                index = value
        if index:
            LIST_RF.remove(index)
        db_return = None
        if server:
            server.handler.delete_set_rf({'set_rf_id': int(id)})
            while server.handler.db_return is None:
                time.sleep(0.5)
            db_return = server.handler.db_return
    return jsonify(result=db_return)


@app.route('/delete_user/<string:id>', methods=['POST'])
def delete_user(id):
    if request.method == 'POST':
        index = None
        for value in LIST_USER:
            if id in str(value['user_id']):
                index = value
        if index:
            LIST_USER.remove(index)
        if server:
            server.handler.delete_user({'user_id': int(id)})
    return jsonify(result=get_list_user())


@app.route('/delete_qrcode_reader/<string:id>', methods=['POST'])
def delete_qrcode_reader(id):
    if request.method == 'POST':
        index = None
        for value in LIST_QRCODE_READER:
            if id in str(value['qrcode_reader_id']):
                index = value
        if index:
            LIST_QRCODE_READER.remove(index)
        if server:
            server.handler.delete_qrcode_reader({'qrcode_reader_id': int(id)})
    return jsonify(result=get_list_qrcode_reader())


@app.route('/delete_guest/<string:id>', methods=['POST'])
def delete_guest(id):
    if request.method == 'POST':
        index = None
        for value in LIST_GUEST:
            if id in str(value['guest_id']):
                index = value
        if index:
            LIST_GUEST.remove(index)
        if server:
            server.handler.delete_guest({'guest_id': int(id)})
    return jsonify(result=get_list_guest())


# *** DELETE ALL ***

@app.route('/delete_all_ipwalls', methods=['POST'])
def delete_all_ipwalls():
    global LIST_IPWALL
    if request.method == 'POST':
        LIST_IPWALL = []
        if server:
            server.handler.delete_all_ipwalls()
    return jsonify(result=get_list_ipwall())


@app.route('/delete_all_set_rf', methods=['POST'])
def delete_all_set_rf():
    global LIST_RF
    if request.method == 'POST':
        LIST_RF = []
        if server:
            server.handler.delete_all_set_rf()
    return jsonify(result=get_list_rf())


@app.route('/delete_all_users', methods=['POST'])
def delete_all_users():
    global LIST_USER
    if request.method == 'POST':
        LIST_USER = []
        if server:
            server.handler.delete_all_users()
    return jsonify(result=get_list_user())


@app.route('/delete_all_qrcode_readers', methods=['POST'])
def delete_all_qrcode_readers():
    global LIST_QRCODE_READER
    if request.method == 'POST':
        LIST_QRCODE_READER = []
        if server:
            server.handler.delete_all_qrcode_readers()
    return jsonify(result=get_list_qrcode_reader())


@app.route('/delete_all_guests', methods=['POST'])
def delete_all_guest():
    global LIST_GUEST
    if request.method == 'POST':
        LIST_GUEST = []
        if server:
            server.handler.delete_all_guests()
    return jsonify(result=get_list_guest())

app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    result = {
        'up': 'tico',
        'down': 'teco'
    }
    return json.jsonify(result=a + b)


if __name__ == "__main__":
    try:
        sv_ip = sys.argv[1]
    except IndexError:
        sv_ip = '10.5.0.13'
    try:
        # while True:
        #    time.sleep(0.1)
        app.run(host=sv_ip, port=port, debug=False)
        #Thread(target=app.run, kwargs={'host': sv_ip, 'debug': False}).start()
    except KeyboardInterrupt:
        if server:
            server.shutdown()
        raise SystemExit
