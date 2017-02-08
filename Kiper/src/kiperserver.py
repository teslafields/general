__author__ = "maickel"
__date__ = "$27/04/2016 12:46:48$"

__all__ = ['KiperHandler', 'KiperServer']

psswd = 'KhompS057989Y2015B20R00T02RootPassword'
import socket, select, ssl, asyncore, json
import json.decoder as decoder
from datetime import datetime
from uuid import uuid1
from threading import Thread, Timer
import logging
from logging.handlers import RotatingFileHandler
import os
import defer
import http.server
import socketserver
import time
from utils.future import InitFuture
from model.db_manager import DbManager
import model.kiper_tables as db
from concurrent.futures import Future
# https://pythonhosted.org/defer/defer.html
# https://docs.python.org/3.4/library/asyncore.html

''' GLOBAL DEFINITIONS '''
timeout = 5 #timeout for ack answering

CERTFILE = os.getcwd()+'/rootCA.pem'
KEYFILE = os.getcwd()+'/rootCA.key'


''' LOGGER CONFIGURATION '''
if os.name == 'nt':
    LOG_DIR = '\\khomp\\logs\\'
else:
    LOG_DIR = '/var/log/khomp/'
afile = '{}kiper.log'.format(LOG_DIR)

maxBytes = 1000000
backupCount = 10

my_logger = logging.getLogger('KiperMessage')
my_logger.setLevel(logging.INFO)
rotator = RotatingFileHandler(afile, 'a', maxBytes, backupCount)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
rotator.setFormatter(formatter)
my_logger.addHandler(rotator)


''' HTTP SERVER '''
class HttpServer:
    def __init__(self, address='10.5.0.13', port=8888):
        Handler = http.server.SimpleHTTPRequestHandler
        self.httpd = socketserver.TCPServer((address, port), Handler)
        my_logger.info("kiperserver: Serving HTTP at port: {}".format(port))


''' KIPER HANDLER '''
class KiperHandler(asyncore.dispatcher_with_send):
    def __init__(self, conn, protocol, timezone=-2):
        asyncore.dispatcher_with_send.__init__(self, conn)
        self.socket = ssl.wrap_socket(conn, do_handshake_on_connect=False, server_side=True, certfile=CERTFILE,
                                      keyfile=KEYFILE)
        self.stack = {}
        self.queue_commands = {}
        self.queue_events = {}
        self.future = InitFuture().get()
        self.terminator = '\n'
        self.timezone = timezone #timezone for set_datetime
        self.protocol = protocol
        self.cpu_version = None
        self.db_return = None
        self.address = self.socket.getpeername()
        while True:
            try:
                self.socket.do_handshake()
                break
            except ssl.SSLWantReadError:
                select.select([self.socket], [], [])
            except ssl.SSLWantWriteError:
                select.select([], [self.socket], [])
            except ssl.SSLZeroReturnError:
                select.select([], [], [self.socket])
            else:
                raise

    def readable(self):
        if isinstance(self.socket, ssl.SSLSocket):
            while self.socket.pending() > 0:
                self.handle_read_event()
        return True

    def handle_read(self):
        buffer = ''
        while True:
            try:
                buffer += self.recv(256).decode()
            except ssl.SSLWantReadError:
                break
            except decoder.JSONDecodeError:
                break

        if buffer:
            for json_data in buffer.splitlines():
                my_logger.info("SV <-- %s", str(json_data + '\n'))
                self.handle_request(json.loads(json_data))

    def handle_request(self, data):
        # Recebemos de handle_head o dado em JSON. Capturamos o comando(data['cmd']) do pacote
        # e chamamos o metodo responsavel pelo tratamento.
        # Ex: data['cmd'] retorna 'get_datetime'. A funcao 'handler_get_datetime' sera chamada.

        handler = getattr(self, '{}_{}'.format('handler', data['cmd']))
        handler(data)

    def id_generator(self):
        # Gera uma ID unica com base no hostname da maquina, endereco do hardware e um numero randomico de 14-bit
        return uuid1().int

    def now(self):
        # Retorna o horario atual no formato YYYY-MM-DD HH:MM:SS
        return datetime.now().strftime('%Y-%m-%d %X')

    def set_datetime(self, bla, ble):
        print(bla, ble)
        deferred = defer.Deferred()
        cmd = {
            'cmd': 'set_datetime',
            'id': self.id_generator(),
            'datetime': self.now(),
            'params': {
                'new_datetime': self.now(),
                'server_protocol_version': self.protocol,
                'timezone': self.timezone
            },
        }
        deferred.add_callback(self.callback)
        self.sender(cmd)
        self.stack[cmd['id']] = cmd
        self.queue_commands[cmd['id']] = [deferred, None]
        return deferred

    def sender(self, cmd):
        # Aqui fazemos a magica de transformar o comando que inicialmente nao recebido como dicionario em JSON.
        # Apos converter o dicionario para JSON adicionamos o terminador do protocolo('\n').
        # O envio pelo socket deve ser feito como Bytes, o encode() se encarrega em codificar a string para Bytes.
        # Valor inicial de cmd:             {campo: valor, campo: valor}
        cmd = json.dumps(cmd)  # Valor em JSON:                    '{campo: valor, campo: valor}'
        cmd += self.terminator  # Valor em JSON com delimitador:    '{campo: valor, campo: valor}\n'
        cmd = cmd.encode(encoding='ascii') # Valor em Bytes:                   b'{campo: valor, campo: valor}\n'
        self.send(cmd)
        my_logger.info("SV --> %s", str(cmd))

    def send_ack(self, id):
        cmd = {
            'cmd': 'ack',
            'id': id,
        }
        self.sender(cmd)

    def handler_ack(self, data):
        deferred = self.queue_commands.get(data['id'])
        if deferred[1]:
            deferred[1].cancel()
        if deferred[0]:
            try:
                if data.get('error'):
                    deferred[0].errback(data)
                    self.future['error'].set_result(True)
                else:
                    deferred[0].callback(data['id'])
            except:
                my_logger.info('Not expected receive two packets', data)

    def no_ack(self, id):
        try:
            self.stack.pop(id)
            my_logger.warning('Ack do comando id %s nao recebido', str(id))
        except KeyError:
            pass

    def callback(self, id):
        try:
            cmd = self.stack.pop(id)
        except KeyError:
            return
        if cmd['cmd'] == 'set_datetime':
            self.future['set_datetime'].set_result(True)
        elif cmd['cmd'] == 'ping':
            self.future['ping'].set_result(True)
        elif cmd['cmd'] == 'get_relays_status':
            self.future['get_relays_status'].set_result(True)
        elif cmd['cmd'] == 'start_emergency':
            self.future['start_emergency'].set_result(True)
        elif cmd['cmd'] == 'stop_emergency':
            self.future['stop_emergency'].set_result(True)
        elif cmd['cmd'] == 'open_the_door':
            self.future['open_the_door'].set_result(True)
        elif cmd['cmd'] == 'keep_the_door_opened':
            self.future['keep_the_door_opened'].set_result(True)
        elif cmd['cmd'] == 'close_the_door':
            self.future['close_the_door'].set_result(True)
        elif cmd['cmd'] == 'vacuum_db':
            self.future['vacuum_db'].set_result(True)
        elif cmd['cmd'] == 'update_cpu':
            self.future['update_cpu'].set_result(True)
        elif cmd['cmd'] == 'update_ipwall':
            self.future['update_ipwall'].set_result(True)
        elif cmd['cmd'] == 'reset_ipwall':
            self.future['reset_ipwall'].set_result(True)
        else:
            self.db_return = DbManager(self.future).insert(cmd, my_logger)

    def errback(self, id):
        pass

    def ping(self):
        deferred = defer.Deferred()
        cmd = {
            'cmd': 'ping',
            'id': self.id_generator(),
            'datetime': self.now()
        }
        deferred.add_callback(self.callback)
        self.sender(cmd)
        t = Timer(timeout, self.no_ack, [cmd['id']])
        t.start()
        self.queue_commands[cmd['id']] = [deferred, t]
        self.stack[cmd['id']] = cmd
        return deferred

    """ ************************Requisições SERVER -> CPU (IPWALL, RF, USER, GUEST E QRCODE)************************ """

    def insert_ipwall(self, kwargs):
        deferred = defer.Deferred()
        cmd = {
            'cmd': 'insert_ipwall',
            'id': self.id_generator(),
            'datetime': self.now(),
        }
        if kwargs:
            cmd.update({'params': kwargs})
        deferred.add_callback(self.callback)
        self.future['ipwall_online'] = Future()
        self.sender(cmd)
        t = Timer(timeout, self.no_ack, [cmd['id']])
        t.start()
        self.queue_commands[cmd['id']] = [deferred, t]
        self.stack[cmd['id']] = cmd
        return deferred

    def insert_set_rf(self, kwargs):
        deferred = defer.Deferred()
        cmd = {
            'cmd': 'insert_set_rf',
            'id': self.id_generator(),
            'datetime': self.now(),
        }
        if kwargs:
            cmd.update({'params': kwargs})
        deferred.add_callback(self.callback)
        self.sender(cmd)
        t = Timer(timeout, self.no_ack, [cmd['id']])
        t.start()
        self.queue_commands[cmd['id']] = [deferred, t]
        self.stack[cmd['id']] = cmd
        return deferred

    def insert_user(self, kwargs):
        deferred = defer.Deferred()
        cmd = {
            'cmd': 'insert_user',
            'id': self.id_generator(),
            'datetime': self.now(),
        }
        if kwargs:
            cmd.update({'params': kwargs})
        deferred.add_callback(self.callback)
        self.sender(cmd)
        t = Timer(timeout, self.no_ack, [cmd['id']])
        t.start()
        self.queue_commands[cmd['id']] = [deferred, t]
        self.stack[cmd['id']] = cmd
        return deferred

    def insert_guest(self, kwargs):
        deferred = defer.Deferred()
        cmd = {
            'cmd': 'insert_guest',
            'id': self.id_generator(),
            'datetime': self.now()
        }
        if kwargs:
            cmd.update({'params': kwargs})
        deferred.add_callback(self.callback)
        self.sender(cmd)
        t = Timer(timeout, self.no_ack, [cmd['id']])
        t.start()
        self.queue_commands[cmd['id']] = [deferred, t]
        self.stack[cmd['id']] = cmd
        return deferred

    def insert_qrcode_reader(self, kwargs):
        deferred = defer.Deferred()
        cmd = {
            'cmd': 'insert_qrcode_reader',
            'id': self.id_generator(),
            'datetime': self.now(),
        }
        if kwargs:
            cmd.update({'params': kwargs})
        deferred.add_callback(self.callback)
        self.sender(cmd)
        t = Timer(timeout, self.no_ack, [cmd['id']])
        t.start()
        self.queue_commands[cmd['id']] = [deferred, t]
        self.stack[cmd['id']] = cmd
        return deferred

    def delete_ipwall(self, kwargs):
        deferred = defer.Deferred()
        cmd = {
            'cmd': 'delete_ipwall',
            'id': self.id_generator(),
            'datetime': self.now(),
        }
        if kwargs:
            cmd.update({'params': kwargs})
        deferred.add_callback(self.callback)
        self.sender(cmd)
        t = Timer(timeout, self.no_ack, [cmd['id']])
        t.start()
        self.queue_commands[cmd['id']] = [deferred, t]
        self.stack[cmd['id']] = cmd
        return deferred

    def delete_set_rf(self, kwargs):
        deferred = defer.Deferred()
        cmd = {
            'cmd': 'delete_set_rf',
            'id': self.id_generator(),
            'datetime': self.now(),
        }
        if kwargs:
            cmd.update({'params': kwargs})
        deferred.add_callback(self.callback)
        self.sender(cmd)
        t = Timer(timeout, self.no_ack, [cmd['id']])
        t.start()
        self.queue_commands[cmd['id']] = [deferred, t]
        self.stack[cmd['id']] = cmd
        return deferred

    def delete_user(self, kwargs):
        deferred = defer.Deferred()
        cmd = {
            'cmd': 'delete_user',
            'id': self.id_generator(),
            'datetime': self.now(),
        }
        if kwargs:
            cmd.update({'params': kwargs})
        deferred.add_callback(self.callback)
        self.sender(cmd)
        t = Timer(timeout, self.no_ack, [cmd['id']])
        t.start()
        self.queue_commands[cmd['id']] = [deferred, t]
        self.stack[cmd['id']] = cmd
        return deferred

    def delete_qrcode_reader(self, kwargs):
        deferred = defer.Deferred()
        cmd = {
            'cmd': 'delete_qrcode_reader',
            'id': self.id_generator(),
            'datetime': self.now(),
        }
        if kwargs:
            cmd.update({'params': kwargs})
        deferred.add_callback(self.callback)
        self.sender(cmd)
        t = Timer(timeout, self.no_ack, [cmd['id']])
        t.start()
        self.queue_commands[cmd['id']] = [deferred, t]
        self.stack[cmd['id']] = cmd
        return deferred

    def delete_guest(self, kwargs):
        deferred = defer.Deferred()
        cmd = {
            'cmd': 'delete_guest',
            'id': self.id_generator(),
            'datetime': self.now(),
        }
        if kwargs:
            cmd.update({'params': kwargs})
        deferred.add_callback(self.callback)
        self.sender(cmd)
        t = Timer(timeout, self.no_ack, [cmd['id']])
        t.start()
        self.queue_commands[cmd['id']] = [deferred, t]
        self.stack[cmd['id']] = cmd
        return deferred

    def delete_all_ipwalls(self):
        deferred = defer.Deferred()
        cmd = {
            'cmd': 'delete_all_ipwalls',
            'id': self.id_generator(),
            'datetime': self.now(),
        }
        deferred.add_callback(self.callback)
        self.sender(cmd)
        t = Timer(timeout, self.no_ack, [cmd['id']])
        t.start()
        self.queue_commands[cmd['id']] = [deferred, t]
        self.stack[cmd['id']] = cmd
        return deferred

    def delete_all_set_rf(self):
        deferred = defer.Deferred()
        cmd = {
            'cmd': 'delete_all_set_rf',
            'id': self.id_generator(),
            'datetime': self.now(),
        }
        deferred.add_callback(self.callback)
        self.sender(cmd)
        t = Timer(timeout, self.no_ack, [cmd['id']])
        t.start()
        self.queue_commands[cmd['id']] = [deferred, t]
        self.stack[cmd['id']] = cmd
        return deferred

    def delete_all_users(self):
        deferred = defer.Deferred()
        cmd = {
            'cmd': 'delete_all_users',
            'id': self.id_generator(),
            'datetime': self.now(),
        }
        deferred.add_callback(self.callback)
        self.sender(cmd)
        t = Timer(timeout, self.no_ack, [cmd['id']])
        t.start()
        self.queue_commands[cmd['id']] = [deferred, t]
        self.stack[cmd['id']] = cmd
        return deferred

    def delete_all_qrcode_readers(self):
        deferred = defer.Deferred()
        cmd = {
            'cmd': 'delete_all_qrcode_readers',
            'id': self.id_generator(),
            'datetime': self.now(),
        }
        deferred.add_callback(self.callback)
        self.sender(cmd)
        t = Timer(timeout, self.no_ack, [cmd['id']])
        t.start()
        self.queue_commands[cmd['id']] = [deferred, t]
        self.stack[cmd['id']] = cmd
        return deferred

    def delete_all_guests(self):
        deferred = defer.Deferred()
        cmd = {
            'cmd': 'delete_all_guests',
            'id': self.id_generator(),
            'datetime': self.now(),
        }
        deferred.add_callback(self.callback)
        self.sender(cmd)
        t = Timer(timeout, self.no_ack, [cmd['id']])
        t.start()
        self.queue_commands[cmd['id']] = [deferred, t]
        self.stack[cmd['id']] = cmd
        return deferred

    """ *************************************Requisições SERVER -> CPU (Gerais)************************************* """

    def update_cpu(self, kwargs):
        deferred = defer.Deferred()
        cmd = {
            'cmd': 'update_cpu',
            'id': self.id_generator(),
            'datetime': self.now()
        }
        if kwargs:
            cmd.update({'params': kwargs})
        deferred.add_callback(self.callback)
        self.sender(cmd)
        t = Timer(timeout, self.no_ack, [cmd['id']])
        t.start()
        self.queue_commands[cmd['id']] = [deferred, t]
        self.stack[cmd['id']] = cmd
        return deferred

    def update_ipwall(self, kwargs):
        deferred = defer.Deferred()
        cmd = {
            'cmd': 'update_ipwall',
            'id': self.id_generator(),
            'datetime': self.now()
        }
        if kwargs:
            cmd.update({'params': kwargs})
        deferred.add_callback(self.callback)
        self.sender(cmd)
        t = Timer(timeout, self.no_ack, [cmd['id']])
        t.start()
        self.queue_commands[cmd['id']] = [deferred, t]
        self.stack[cmd['id']] = cmd
        return deferred

    def start_emergency(self):
        deferred = defer.Deferred()
        cmd = {
            'cmd': 'start_emergency',
            'id': self.id_generator(),
            'datetime': self.now()
        }
        deferred.add_callback(self.callback)
        self.sender(cmd)
        t = Timer(timeout, self.no_ack, [cmd['id']])
        t.start()
        self.queue_commands[cmd['id']] = [deferred, t]
        self.stack[cmd['id']] = cmd
        return deferred

    def stop_emergency(self):
        deferred = defer.Deferred()
        cmd = {
            'cmd': 'stop_emergency',
            'id': self.id_generator(),
            'datetime': self.now()
        }
        deferred.add_callback(self.callback)
        self.sender(cmd)
        t = Timer(timeout, self.no_ack, [cmd['id']])
        t.start()
        self.queue_commands[cmd['id']] = [deferred, t]
        self.stack[cmd['id']] = cmd
        return deferred

    def get_sensors_status(self, ipwall):
        deferred = defer.Deferred()
        cmd = {
            'cmd': 'get_sensors_status',
            'id': self.id_generator(),
            'datetime': self.now()
        }
        if ipwall:
            cmd.update({'params': ipwall})
        deferred.add_callback(self.callback)
        self.sender(cmd)
        t = Timer(timeout, self.no_ack, [cmd['id']])
        t.start()
        self.queue_commands[cmd['id']] = [deferred, t]
        self.stack[cmd['id']] = cmd
        return deferred

    def get_relays_status(self, ipwall):
        deferred = defer.Deferred()
        cmd = {
            'cmd': 'get_relays_status',
            'id': self.id_generator(),
            'datetime': self.now()
        }
        if ipwall:
            cmd.update({'params': ipwall})
        deferred.add_callback(self.callback)
        self.sender(cmd)
        t = Timer(timeout, self.no_ack, [cmd['id']])
        t.start()
        self.queue_commands[cmd['id']] = [deferred, t]
        self.stack[cmd['id']] = cmd
        return deferred

    def open_the_door(self, kwargs):
        deferred = defer.Deferred()
        cmd = {
            'cmd': 'open_the_door',
            'id': self.id_generator(),
            'datetime': self.now(),
        }
        if kwargs:
            cmd.update({'params': kwargs})
        self.future['sensor_status_changed'] = Future()
        deferred.add_callback(self.callback)
        self.sender(cmd)
        t = Timer(timeout, self.no_ack, [cmd['id']])
        t.start()
        self.queue_commands[cmd['id']] = [deferred, t]
        self.stack[cmd['id']] = cmd
        return deferred

    def keep_the_door_opened(self, kwargs):
        deferred = defer.Deferred()
        cmd = {
            'cmd': 'keep_the_door_opened',
            'id': self.id_generator(),
            'datetime': self.now(),
        }
        if kwargs:
            cmd.update({'params': kwargs})
        self.future['sensor_status_changed'] = Future()
        deferred.add_callback(self.callback)
        self.sender(cmd)
        t = Timer(timeout, self.no_ack, [cmd['id']])
        t.start()
        self.queue_commands[cmd['id']] = [deferred, t]
        self.stack[cmd['id']] = cmd
        return deferred

    def close_the_door(self, kwargs):
        deferred = defer.Deferred()
        cmd = {
            'cmd': 'close_the_door',
            'id': self.id_generator(),
            'datetime': self.now(),
        }
        if kwargs:
            cmd.update({'params': kwargs})
        self.future['sensor_status_changed'] = Future()
        deferred.add_callback(self.callback)
        self.sender(cmd)
        t = Timer(timeout, self.no_ack, [cmd['id']])
        t.start()
        self.queue_commands[cmd['id']] = [deferred, t]
        self.stack[cmd['id']] = cmd
        return deferred

    def log_type(self, kwargs):
        deferred = defer.Deferred()
        cmd = {
            'cmd': 'change_log_type',
            'id': self.id_generator(),
            'datetime': self.now(),
        }
        if kwargs:
            cmd.update({'params': kwargs})
        deferred.add_callback(self.callback)
        self.sender(cmd)
        t = Timer(timeout, self.no_ack, [cmd['id']])
        t.start()
        self.queue_commands[cmd['id']] = [deferred, t]
        self.stack[cmd['id']] = cmd
        return deferred

    def vacuum(self):
        deferred = defer.Deferred()
        cmd = {
            'cmd': 'vacuum_db',
            'id': self.id_generator(),
            'datetime': self.now()
        }
        deferred.add_callback(self.callback)
        self.sender(cmd)
        t = Timer(timeout, self.no_ack, [cmd['id']])
        t.start()
        self.queue_commands[cmd['id']] = [deferred, t]
        self.stack[cmd['id']] = cmd
        return deferred

    def reset_ipwall(self, ipwall):
        deferred = defer.Deferred()
        cmd = {
            'cmd': 'reset_ipwall',
            'id': self.id_generator(),
            'datetime': self.now()
        }
        if ipwall:
            cmd.update({'params': ipwall})
        deferred.add_callback(self.callback)
        self.sender(cmd)
        t = Timer(timeout, self.no_ack, [cmd['id']])
        t.start()
        self.queue_commands[cmd['id']] = [deferred, t]
        self.stack[cmd['id']] = cmd
        return deferred

    """ ****************************************** Handlers ******************************************************** """

    def handler_received_message_without_newline(self, data):
        self.send_ack(data['id'])

    def handler_usb_update_cpu_started(self, data):
        self.send_ack(data['id'])

    def handler_get_datetime(self, data):
        # get_datetime - comando que solicita ao Server para setar o horario correto na CPU.
        # Comando esperado: set_datetime
        self.cpu_version = data['params']['cpu_version']
        self.send_ack(data['id'])
        self.set_datetime(self.now(), self.protocol)

    def handler_cpu_started(self, data):
        self.send_ack(data['id'])

    def handler_interlock_in_action(self, data):
        self.send_ack(data['id'])

    def handler_send_offline_event_list(self, data):
        self.send_ack(data['id'])

    def handler_ping(self, data):
        self.send_ack(data['id'])

    def handler_update_cpu_started(self, data):
        # comando  que  informa  que  o  update  sera  iniciado.  O  update  ira  reinicializar  a  CPU.
        self.send_ack(data['id'])
        self.future['update_cpu_started'].set_result(True)

    def handler_protocol_version_error(self, data):
        # comando que informa que existe incompatibilidade maior que do Server.
        # Nesse caso a CPU so aceitara ser atualizada.
        self.send_ack(data['id'])

    def handler_send_energy_status(self, data):
        self.send_ack(data['id'])

    def handler_send_sensors_status(self, data):
        self.send_ack(data['id'])

    def handler_send_access_code_tag(self, data):
        self.send_ack(data['id'])
        callback = self.queue_events.get(data['cmd'])
        if callback:
            callback(data)

    def handler_update_ipwall_result(self, data):
        self.send_ack(data['id'])
        self.future['update_ipwall_result'].set_result(True)

    def handler_ipwall_online(self, data):
        self.send_ack(data['id'])
        callback = self.queue_events.get(data['cmd'])
        self.future['ipwall_online'].set_result(True)
        if callback:
            callback(data)

    def handler_ipwall_started(self, data):
        self.send_ack(data['id'])
        self.future['ipwall_started'].set_result(True)

    def handler_new_ipwall(self, data):
        self.send_ack(data['id'])

    def handler_ipwall_offline(self, data):
        self.send_ack(data['id'])

    def handler_ipwall_restarting(self, data):
        self.send_ack(data['id'])

    def handler_update_cpu_started(self, data):
        self.send_ack(data['id'])

    def handler_qrcode_reader_online(self, data):
        self.send_ack(data['id'])

    def handler_qrcode_reader_offline(self, data):
        self.send_ack(data['id'])

    def handler_walker_panic(self, data):
        self.send_ack(data['id'])

    def handler_sensor_status_changed(self, data):
        self.send_ack(data['id'])
        callback = self.queue_events.get(data['cmd'])
        self.future['sensor_status_changed'].set_result(True)
        if callback: callback(data)

    def handler_send_relays_status(self, data):
        self.send_ack(data['id'])
        self.future['send_relays_status'].set_result(True)

    def handler_emergency_started(self, data):
        self.send_ack(data['id'])
        self.future['emergency_started'].set_result(True)

    def handler_emergency_stopped(self, data):
        self.send_ack(data['id'])
        self.future['emergency_stoped'].set_result(True)

    def handler_ipwall_not_exists(self, data):
        self.send_ack(data['id'])

    def handler_sluice_problem(self, data):
        self.send_ack(data['id'])

    def handler_command_refused(self, data):
        self.send_ack(data['id'])

    def handler_send_access_code_rf(self, data):
        self.send_ack(data['id'])

    def handler_cpu_door_opened(self, data):
        self.send_ack(data['id'])

    def handler_cpu_door_closed(self, data):
        self.send_ack(data['id'])

    def handler_button_open_the_door_activated(self, data):
        self.send_ack(data['id'])

    def handler_sip_registration_lost(self, data):
        self.send_ack(data['id'])

    def handler_sip_call(self, data):
        self.send_ack(data['id'])

    def handler_wrong_ipwall_registration(self, data):
        self.send_ack(data['id'])

    def handler_vacuum_done(self, data):
        self.send_ack(data['id'])
        self.future['vacuum_done'].set_result(True)

    def handler_error_log_updated(self, data):
        self.send_ack(data['id'])

    def notify_me(self, event, callback):
        self.queue_events[event] = callback

    def handle_close(self):
        global timeout
        if timeout == 5:
            my_logger.info("Connection from {}:{} was closed ".format(*self.address))
            timeout += 1

    def handler_network_configuration_cpu_changed(self, data):
        self.send_ack(data['id'])

    def handler_send_access_qrcode(self, data):
        self.send_ack(data['id'])

    def handler_sip_wrong_password(self, data):
        self.send_ack(data['id'])

    def handler_ipwall_break_in(self, data):
        self.send_ack(data['id'])

    def handler_qrcode_reader_break_in(self, data):
        self.send_ack(data['id'])

    def handler_qrcode_reader_version(self, data):
        self.send_ack(data['id'])

    def handler_can_enable(self, data):
        self.send_ack(data['id'])

class KiperServer(asyncore.dispatcher):
    def __init__(self, host='10.5.0.13', port=8000, protocol=1.2):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        try:
            self.bind((host, port))
            self.listen(1)
            self.handler = None
            self.http = HttpServer()
            self.sock = None
            self.protocol = protocol
            self.server_forever()
            timeo = 60
            while (not self.handler) and timeo:
                my_logger.info("kiperserver: waiting...")
                time.sleep(0.5)
                timeo -= 1
            db.create_tables(my_logger)
        except OSError:
            my_logger.warning("ADDRESS IN USE! Wait for a few seconds and try again")

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            self.sock = sock
            my_logger.info("New connection from {}:{}".format(*addr))
            self.handler = KiperHandler(sock, self.protocol)
            self.handler.future['ativo'].set_result(True)
            my_logger.info('kiperserver: Connected to CPU')
            Thread(target=self.http.httpd.serve_forever).start()

    def server_forever(self):
        my_logger.info("server_forever")
        Thread(target=asyncore.loop, kwargs={'use_poll': True}).start()
        my_logger.info('server_forever_out')

    def shutdown(self):
        self.http.httpd.shutdown()
        self.http.httpd.server_close()
        self.handle_close()
        self.handler.close()
        my_logger.info("kiperserver: server DOWN")


if __name__ == '__main__':
    server = KiperServer()
