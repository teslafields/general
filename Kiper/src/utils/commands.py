valid = {"valid_from": "2016-09-09 16:40:00", "valid_until": "2016-10-02 16:40:00", "access_counter": 1}

IPWALL = dict(ipwall_id=3, ipwall_name="Porta 1", ip="10.15.15.113", disable_emergency=False, access_type="walker",
              control_doors={"door1": True, "door2": False}, button_enable=False, door1_dependency=None,
              door2_dependency=None, days_of_week=None)
              # door1_dependency=[{'ipwall_id': 2, 'door_id': 2}, {'ipwall_id': 2, 'door_id': 2},
              #                   {'ipwall_id': 4, 'door_id': 2}, {'ipwall_id': 5, 'door_id': 1},
              #                   {'ipwall_id': 6, 'door_id': 1}, {'ipwall_id': 7, 'door_id': 1}], door2_dependency=None,
              #days_of_week={"sunday": "00:00-05:10", "friday": "15:00-21:30", "monday": "04:13-20:35"})

car = dict(ipwall_id=12, ipwall_name="Porta 1", ip="10.15.15.112", disable_emergency=False, access_type="walker",
           control_doors={"door1": True, "door2": False}, button_enable=True, door1_dependency=None,
           door2_dependency=None,
           days_of_week={"sunday": "00:00-05:10", "friday": "15:00-21:30", "monday": "04:13-20:35"})

SETRF = {'set_rf_id': 1,
         'set_rf': {'button1': {"ipwall_id": 1, "door_id": 1}, 'button2': {"ipwall_id": 1, "door_id": 2},
                    'button3': {"ipwall_id": 1, "door_id": 1}, 'button4': {"ipwall_id": -1, "door_id": 1}}}

USER = dict(user_id=19, ipwall_access_tag=[3], set_rf_id=1, counter_rf=132, tag_id=68595732715, rf_id=3059812612,
            blocked=False, opening_time=8, secret="MU4WCNJSGQ2GGLJYMNSDELJUGQ2GILLCGQ4TELJUMYZGCMLEMNSWCYTFG4",
            restrict_access=True, days_of_week={"sunday": "00:00-05:10", "friday": "15:00-21:30"}, administrator=False)

QRCODE = dict(qrcode_reader_id=1, qrcode_reader_ip="10.15.15.54",
              relation=[{"cam_id": 0, "ipwall_id": 3, "wiegand_id": 0}])

GUEST = {'guest_id': 1, 'ipwall_access_list': [3], 'valid': valid, 'code': "av23h6"}

UPDATE_CPU = {'restore': True, 'http_server_ip': "10.5.0.13", 'http_server_port': 8888, 'file_path': "/updates/",
              'update_to_version': "1.5.0", 'update_file': "last-version.update_web"}

UPDATE_IPWALL = {"ipwall_id": 3, "http_server_ip": "10.5.0.13", "http_server_port": 8888,
                 "file_path": "/updates/ipax283h16-M3-K.bin", "file_name": "ipax283h16-M3-K.bin", "file_size": 459256}
