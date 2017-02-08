#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "maickel"
__date__ = "$01/06/2016 10:02:34$"

import re

REGEX_DOOR_DEPENDECY1 = '(?<=1-)\w+'
REGEX_DOOR_DEPENDECY2 = '(?<=2-)\w+'


# *** IP WALL ***


class FormInsertIpwall(object):
    def __init__(self):
        self.form = self.get_model()

    def set(self, form):
        #form = dict(form.items())
        self.form['ipwall_id'] = int(form['ipwall_id'])
        self.form['ipwall_name'] = form['ipwall_name']
        self.form['ip'] = form['ip']

        self.form['disable_emergency'] = form['check_disable_emergency']
        self.form['button_enable'] = form['check_button_enable']

        if 'check_door_dependency1' in form:
            if form['check_door_dependency1']:
                door_dependency = []
                for key, value in form.items():
                    if value:
                        if 'ipwall-1' in key:
                            result = re.search(REGEX_DOOR_DEPENDECY1, key)
                            door_id = 'doorid-1-{0}'.format(result.group(0))
                            dependency = {'ipwall_id': int(value), 'door_id': int(form[door_id])}
                            door_dependency.append(dependency)
                print('door ', door_dependency)
                self.form['door1_dependency'] = door_dependency
        else:
            self.form['door1_dependency'] = None

        if 'check_door_dependency2' in form:
            if form['check_door_dependency2']:
                door_dependency = []
                for key, value in form.items():
                    if value:
                        if 'ipwall-2' in key:
                            result = re.search(REGEX_DOOR_DEPENDECY2, key)
                            door_id = 'doorid-2-{0}'.format(result.group(0))
                            dependency = {'ipwall_id': int(value), 'door_id': int(form[door_id])}
                            door_dependency.append(dependency)
                print('door ', door_dependency)
                self.form['door2_dependency'] = door_dependency
        else:
            self.form['door2_dependency'] = None
        self.form['access_type'] = form['access_type']
        control_door = {'door1': False, 'door2': False}
        control_door['door1'] = form['check_door1']
        control_door['door2'] = form['check_door2']
        self.form['control_doors'] = control_door.copy()
        if form['select_ipwall_days_of_week-0'] != 'null':
            self.form.update({'days_of_week': {}})
            for value in form:
                if 'select_ipwall_days_of_week' in value:
                    id = value.split('-')[1]
                    day = form[value]
                    start_time = 'ipwall_start_time-{0}'.format(id)
                    end_time = 'ipwall_end_time-{0}'.format(id)
                    self.form['days_of_week'][form[value]] = '{0}-{1}'.format(form[start_time], form[end_time])

    def get(self):
        return self.form

    def get_model(self):
        model = {
            'ipwall_id': None,
            'ipwall_name': None,
            'ip': None,
            'days_of_week': None,
            'access_profile_id': None,
            'disable_emergency': None,
            'access_type': None,
            'control_doors': {
                'door1': False,
                'door2': False
            },
            'button_enable': False,
            'door1_dependency': None,
            'door2_dependency': None

        }
        return model.copy()


# *** SET RF ***


class FormInsertSetRf(object):
    def __init__(self):
        self.form = self.get_model()

    def set(self, form):
        form = dict(form.items())
        self.form['set_rf_id'] = int(form['set_rf_id'])

        if 'ipwall_id_1' in form:
            print(form['ipwall_id_1'])
            self.form['set_rf']['button1']['ipwall_id'] = int(form['ipwall_id_1'])
            self.form['set_rf']['button1']['door_id'] = int(form['door_id_1'])
        if 'ipwall_id_2' in form:
            self.form['set_rf']['button2']['ipwall_id'] = int(form['ipwall_id_2'])
            self.form['set_rf']['button2']['door_id'] = int(form['door_id_2'])
        if 'ipwall_id_3' in form:
            try:
                self.form['set_rf']['button3']['ipwall_id'] = int(form['ipwall_id_3'])
            except ValueError:
                self.form['set_rf']['button3']['ipwall_id'] = None
            self.form['set_rf']['button3']['door_id'] = int(form['door_id_3'])
        if 'ipwall_id_4' in form:
            self.form['set_rf']['button4']['ipwall_id'] = int(form['ipwall_id_4'])
            self.form['set_rf']['button4']['door_id'] = int(form['door_id_4'])

    def get(self):
        return self.form.copy()

    def get_model(self):
        button = {
            'ipwall_id': None,
            'door_id': None
        }
        model = {
            'set_rf_id': None,
            'set_rf': {
                'button1': button.copy(),
                'button2': button.copy(),
                'button3': button.copy(),
                'button4': button.copy()
            }
        }
        return model.copy()


# *** USER ***

class FormInsertUser(object):
    def __init__(self):
        self.form = self.get_model()

    def set(self, form):
        form = dict(form.items())
        self.form['user_id'] = int(form['user_id'])
        try:
            self.form['set_rf_id'] = int(form['select_set_rf_id'])
        except TypeError:
            self.form['set_rf_id'] = None
        except ValueError:
            self.form['set_rf_id'] = None
        try:
            x = form['tag_id']
            self.form['tag_id'] = int(x)
        except ValueError:
            self.form['tag_id'] = None
        try:
            y = form['rf_id']
            self.form['rf_id'] = int(y)
        except ValueError:
            self.form['rf_id'] = None
        self.form['counter_rf'] = int(form['counter_rf'])
        self.form['blocked'] = form['check_blocked']
        self.form['administrator'] = form['check_administrator']
        self.form['secret'] = form['secret']
        self.form['opening_time'] = int(form['opening_time'])

        if 'check_restrict_access' in form:
            self.form['restrict_access'] = form['check_restrict_access']
            self.form['days_of_week'] = {}
        for value in form:
            if 'ipwall_id' in value:
                if form[value]:
                    self.form['ipwall_access_tag'].append(int(value.split('-')[1]))
            if 'select_days_of_week' in value:
                if form[value] != 'null':
                    id = value.split('-')[1]
                    day = form[value]
                    start_time = 'start_time-{0}'.format(id)
                    end_time = 'end_time-{0}'.format(id)
                    self.form['days_of_week'][form[value]] = '{0}-{1}'.format(form[start_time], form[end_time])

    def get(self):
        return self.form.copy()

    def get_model(self):
        model = {
            'user_id': None,
            'ipwall_access_tag': [],
            'set_rf_id': None,
            'counter_rf': None,
            'tag_id': None,
            'rf_id': None,
            'blocked': False,
            'administrator': False,
            'opening_time': None,
            'secret': None,
            'restrict_access': False,
            'days_of_week': None
        }
        return model.copy()


class FormInsertGuest(object):
    def __init__(self):
        self.form = self.get_model()

    def set(self, form):
        access_list = []
        self.form['guest_id'] = int(form['guest_id'])
        for x in form:
            if 'check_ipwall_id_guest' in x:
                id = x.split('+')[1]
                access_list.append(int(id))
        self.form['ipwall_access_list'] = access_list
        self.form['code'] = form['code']
        vfrom = form['valid_from'][:10] + ' ' + form['valid_from'][11:] + ':00'
        vuntil = form['valid_until'][:10] + ' ' + form['valid_until'][11:] + ':59'
        self.form['valid'] = {'valid_from': vfrom, 'valid_until': vuntil,
                              'access_counter': int(form['access_counter'])}

    def get(self):
        return self.form.copy()

    def get_model(self):
        model = {
            'guest_id': None,
            'ipwall_access_list': None,
            'valid': None,
            'code': None
        }
        return model.copy()


class FormInsertQrcodeReader(object):
    def __init__(self):
        self.form = self.get_model()

    def set(self, form):
        self.form['qrcode_reader_ip'] = form['qrcode_reader_ip']
        self.form['qrcode_reader_id'] = int(form['qrcode_reader_id'])
        if 'relation_cam_id-0' in form:
            self.form['relation'] = []
        for value in form:
            if 'relation_cam_id-' in value:
                id = value.split('-')[1]
                cam = int(form[value])
                try:
                    wiegand = int(form['relation_cam_id-{}'.format(id)])
                except ValueError:
                    wiegand = None
                try:
                    ipwall = int(form['relation_ipwall_id-{}'.format(id)])
                except ValueError:
                    ipwall = 0
                self.form['relation'].append({'cam_id': cam, 'wiegand_id': wiegand, 'ipwall_id': ipwall})

    def get(self):
        return self.form.copy()

    def get_model(self):
        model = {
            'qrcode_reader_id': None,
            'qrcode_reader_ip': None,
            'relation': None
        }
        return model.copy()

# *** REQUEST ***

class FormInsertRequest(object):
    def __init__(self):
        self.form = self.get_model()

    def set(self, form):
        form = dict(form.items())
        self.form['request_id'] = int(form['request_id'])
        self.form['radio_change_log_type'] = form['radio_change_log_type']
        self.form['update_to_version'] = form['update_to_version']
        self.form['check_restore'] = form['check_restore']
        self.form['http_server_ip'] = form['counter_rfhttp_server_ip']
        self.form['http_server_port'] = form['counter_rfhttp_server_port']
        self.form['file_path'] = form['file_path']
        self.form['update_file'] = form['update_file']
        self.form['ipwall_id'] = form['ipwall_id']
        self.form['door_id'] = form['door_id']

        print(self.form)

    def get(self):
        return self.form.copy()

    def get_model(self):
        model = {
            'request_id': None,
            'radio_change_log_type': None,
            'update_to_version': None,
            'check_restore': None,
            'http_server_ip': None,
            'http_server_port': None,
            'file_path': False,
            'update_file': None,
            'ipwall_id': None,
            'door_id': None
        }
        return model.copy()
