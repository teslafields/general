from concurrent.futures import Future


class InitFuture:
    def __init__(self):
        self.future = dict.fromkeys(
            ['insert_qrcode_reader', 'ping', 'insert_ipwall', 'stop_emergency', 'delete_ipwall', 'update_cpu',
             'keep_the_door_opened', 'get_relays_status', 'insert_user', 'delete_set_rf', 'delete_all_ipwalls',
             'delete_all_users', 'delete_all_guests', 'delete_qrcode_reader', 'delete_guest', 'delete_all_qrcode_readers', 'insert_set_rf',
             'delete_all_set_rf', 'vacuum_db', 'open_the_door', 'start_emergency', 'delete_user', 'get_sensors_status',
             'close_the_door', 'set_datetime', 'send_relays_status', 'ativo', 'error', 'stop_emergency',
             'emergency_started', 'emergency_stoped', 'sensor_status_changed', 'vacuum_done', 'ipwall_online',
             'update_cpu_started', 'update_ipwall_result', 'update_ipwall', 'ipwall_started', 'reset_ipwall',
             'insert_guest', 'insert_qrcode_reader'])
        for key in self.future.keys():
            self.future[key] = Future()

    def get(self):
        return self.future
