import sys

sys.path.append('..')
from behave import *
import time
from kipercommands import IPWALL, SETRF, USER, GUEST, QRCODE, UPDATE_CPU, UPDATE_IPWALL
from concurrent.futures import wait
import re

timeout = 10


@given('um comando server->cpu "{cmd}"')
def step_impl(context, cmd):
    wait(fs=[context.server.handler.future['set_datetime']], timeout=timeout)
    time.sleep(2)
    if 'ping' in context.tags:
        context.server.handler.ping()

    elif 'get_relays_status' in context.tags:
        id = [int(i) for i in re.findall(r'\d+', cmd)]
        context.server.handler.get_relays_status({'ipwall_id': id.pop()})

    elif 'start_emergency' in context.tags:
        context.server.handler.start_emergency()

    elif 'stop_emergency' in context.tags:
        context.server.handler.stop_emergency()

    elif 'open_the_door' in context.tags:
        id = [int(i) for i in re.findall(r'\d+', cmd)]
        context.server.handler.open_the_door({'ipwall_id': id[0], 'door_id': id[1]})

    elif 'keep_the_door_opened' in context.tags:
        id = [int(i) for i in re.findall(r'\d+', cmd)]
        context.server.handler.keep_the_door_opened({'ipwall_id': id[0], 'door_id': id[1]})

    elif 'close_the_door' in context.tags:
        id = [int(i) for i in re.findall(r'\d+', cmd)]
        context.server.handler.close_the_door({'ipwall_id': id[0], 'door_id': id[1]})

    elif 'update_cpu' in context.tags:
        context.server.handler.update_cpu(UPDATE_CPU)

    elif 'update_ipwall' in context.tags:
        context.server.handler.update_ipwall(UPDATE_IPWALL)

    elif 'reset_ipwall' in context.tags:
        id = [int(i) for i in re.findall(r'\d+', cmd)]
        context.server.handler.reset_ipwall({'ipwall_id': id.pop()})

    elif 'vacuum_db' in context.tags:
        context.server.handler.vacuum()

    elif 'insert_ipwall' in context.tags:
        context.server.handler.insert_ipwall(IPWALL)

    elif 'insert_set_rf' in context.tags:
        context.server.handler.insert_set_rf(SETRF)

    elif 'insert_user' in context.tags:
        context.server.handler.insert_user(USER)

    elif 'insert_qrcode_reader' in context.tags:
        context.server.handler.insert_qrcode_reader(QRCODE)

    elif 'insert_guest' in context.tags:
        context.server.handler.insert_guest(GUEST)

    elif 'delete_ipwall' in context.tags:
        context.server.handler.delete_ipwall({'ipwall_id': IPWALL['ipwall_id']})

    elif 'delete_set_rf' in context.tags:
        context.server.handler.delete_set_rf({'set_rf_id': SETRF['set_rf_id']})

    elif 'delete_user' in context.tags:
        context.server.handler.delete_user({'user_id': USER['user_id']})

    elif 'delete_qrcode_reader' in context.tags:
        context.server.handler.delete_qrcode_reader({'qrcode_reader_id': QRCODE['qrcode_reader_id']})

    elif 'delete_guest' in context.tags:
        context.server.handler.delete_guest({'guest_id': GUEST['guest_id']})

    elif 'delete_all_ipwalls' in context.tags:
        context.server.handler.delete_all_ipwalls()

    elif 'delete_all_set_rf' in context.tags:
        context.server.handler.delete_all_set_rf()

    elif 'delete_all_users' in context.tags:
        context.server.handler.delete_all_users()

    elif 'delete_all_qrcode_readers' in context.tags:
        context.server.handler.delete_all_qrcode_readers()

    elif 'delete_all_guests' in context.tags:
        context.server.handler.delete_all_guests()

    assert True == True


@when('recebe o ack do comando')
def step_impl(context):
    if 'get_relays_status' in context.tags:
        wait(fs=[context.server.handler.future['get_relays_status']], timeout=timeout)
        assert context.server.handler.future['get_relays_status'].done() == True

    elif 'start_emergency' in context.tags:
        wait(fs=[context.server.handler.future['start_emergency']], timeout=timeout)
        assert context.server.handler.future['start_emergency'].done() == True

    elif 'stop_emergency' in context.tags:
        wait(fs=[context.server.handler.future['stop_emergency']], timeout=timeout)
        assert context.server.handler.future['stop_emergency'].done() == True

    elif 'open_the_door' in context.tags:
        wait(fs=[context.server.handler.future['open_the_door']], timeout=timeout)
        assert context.server.handler.future['open_the_door'].done() == True

    elif 'keep_the_door_opened' in context.tags:
        wait(fs=[context.server.handler.future['keep_the_door_opened']], timeout=timeout)
        assert context.server.handler.future['keep_the_door_opened'].done() == True

    elif 'close_the_door' in context.tags:
        wait(fs=[context.server.handler.future['close_the_door']], timeout=timeout)
        assert context.server.handler.future['close_the_door'].done() == True

    elif 'vacuum_db' in context.tags:
        wait(fs=[context.server.handler.future['vacuum_db']], timeout=timeout)
        assert context.server.handler.future['vacuum_db'].done() == True

    elif 'update_ipwall' in context.tags:
        wait(fs=[context.server.handler.future['update_ipwall']], timeout=timeout)
        assert context.server.handler.future['update_ipwall'].done() == True

    elif 'reset_ipwall' in context.tags:
        wait(fs=[context.server.handler.future['reset_ipwall']], timeout=timeout)
        assert context.server.handler.future['reset_ipwall'].done() == True

    elif 'update_cpu' in context.tags:
        wait(fs=[context.server.handler.future['update_cpu']], timeout=timeout)
        assert context.server.handler.future['update_cpu'].done() == True


@then('recebe resposta cpu->server {cmd}')
def step_impl(context, cmd):
    if 'get_relays_status' in context.tags:
        wait(fs=[context.server.handler.future['send_relays_status']], timeout=timeout)
        assert context.server.handler.future['send_relays_status'].done() == True

    elif 'start_emergency' in context.tags:
        wait(fs=[context.server.handler.future['emergency_started']], timeout=timeout)
        assert context.server.handler.future['emergency_started'].done() == True

    elif 'stop_emergency' in context.tags:
        wait(fs=[context.server.handler.future['emergency_stoped']], timeout=timeout)
        assert context.server.handler.future['emergency_stoped'].done() == True

    elif 'open_the_door' in context.tags:
        wait(fs=[context.server.handler.future['sensor_status_changed']], timeout=timeout + 4)
        assert context.server.handler.future['sensor_status_changed'].done() == True

    elif 'keep_the_door_opened' in context.tags:
        wait(fs=[context.server.handler.future['sensor_status_changed']], timeout=2 * timeout + 4)
        assert context.server.handler.future['sensor_status_changed'].done() == True

    elif 'close_the_door' in context.tags:
        wait(fs=[context.server.handler.future['sensor_status_changed']], timeout=2 * timeout + 4)
        assert context.server.handler.future['sensor_status_changed'].done() == True

    elif 'vacuum_db' in context.tags:
        wait(fs=[context.server.handler.future['vacuum_done']], timeout=timeout)
        assert context.server.handler.future['vacuum_done'].done() == True

    elif 'update_ipwall' in context.tags:
        wait(fs=[context.server.handler.future['update_ipwall_result']], timeout=60)
        assert context.server.handler.future['update_ipwall_result'].done() == True

    elif 'reset_ipwall' in context.tags:
        wait(fs=[context.server.handler.future['ipwall_started']], timeout=60)
        assert context.server.handler.future['ipwall_started'].done() == True

    elif 'update_cpu' in context.tags:
        wait(fs=[context.server.handler.future['update_cpu_started']], timeout=60)
        assert context.server.handler.future['update_cpu_started'].done() == True

@then('recebe {string}')
def step_impl(context, string):
    if 'ping' in context.tags:
        wait(fs=[context.server.handler.future['ping']], timeout=2 * timeout)
        assert context.server.handler.future['ping'].done() == True

    elif 'insert_ipwall' in context.tags:
        wait(fs=[context.server.handler.future['insert_ipwall'], context.server.handler.future['ipwall_online']], timeout=2 * timeout)
        assert context.server.handler.future['ipwall_online'].done() ==  True

    elif 'insert_set_rf' in context.tags:
        wait(fs=[context.server.handler.future['insert_set_rf']], timeout=2 * timeout)
        assert context.server.handler.future['insert_set_rf'].done() == True

    elif 'insert_user' in context.tags:
        wait(fs=[context.server.handler.future['insert_user']], timeout=2 * timeout)
        assert context.server.handler.future['insert_user'].done() == True

    elif 'insert_qrcode_reader' in context.tags:
        wait(fs=[context.server.handler.future['insert_qrcode_reader']], timeout=2 * timeout)
        assert context.server.handler.future['insert_qrcode_reader'].done() == True

    elif 'insert_guest' in context.tags:
        wait(fs=[context.server.handler.future['insert_guest']], timeout=2 * timeout)
        assert context.server.handler.future['insert_guest'].done() == True

    elif 'delete_ipwall' in context.tags:
        wait(fs=[context.server.handler.future['ipwall_online']], timeout=2 * timeout)
        wait(fs=[context.server.handler.future['delete_ipwall']], timeout=2 * timeout)
        assert context.server.handler.future['delete_ipwall'].done() == True

    elif 'delete_set_rf' in context.tags:
        wait(fs=[context.server.handler.future['delete_set_rf']], timeout=2 * timeout)
        assert context.server.handler.future['delete_set_rf'].done() == True

    elif 'delete_user' in context.tags:
        wait(fs=[context.server.handler.future['delete_user']], timeout=2 * timeout)
        assert context.server.handler.future['delete_user'].done() == True

    elif 'delete_qrcode_reader' in context.tags:
        wait(fs=[context.server.handler.future['delete_qrcode_reader']], timeout=2 * timeout)
        assert context.server.handler.future['delete_qrcode_reader'].done() == True

    elif 'delete_guest' in context.tags:
        wait(fs=[context.server.handler.future['delete_guest']], timeout=2 * timeout)
        assert context.server.handler.future['delete_guest'].done() == True

    elif 'delete_all_ipwalls' in context.tags:
        wait(fs=[context.server.handler.future['delete_all_ipwalls']], timeout=2 * timeout)
        assert context.server.handler.future['delete_all_ipwalls'].done() == True

    elif 'delete_all_set_rf' in context.tags:
        wait(fs=[context.server.handler.future['delete_all_set_rf']], timeout=2 * timeout)
        assert context.server.handler.future['delete_all_set_rf'].done() == True

    elif 'delete_all_users' in context.tags:
        wait(fs=[context.server.handler.future['delete_all_users']], timeout=2 * timeout)
        assert context.server.handler.future['delete_all_users'].done() == True

    elif 'delete_all_qrcode_readers' in context.tags:
        wait(fs=[context.server.handler.future['delete_all_qrcode_readers']], timeout=2 * timeout)
        assert context.server.handler.future['delete_all_qrcode_readers'].done() == True
