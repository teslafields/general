import model.kiper_tables as db
from playhouse.shortcuts import model_to_dict
import peewee

class DbManager:
    def __init__(self, future):
        self.future = future

    def insert(self, cmd, logger):
        if 'params' in cmd:
            params = cmd['params']

        if cmd['cmd'] == 'insert_ipwall':

            i = db.Ipwall(ipwall_id=params['ipwall_id'], name=params['ipwall_name'], ip=params['ip'],
                          disable_emergency=params['disable_emergency'], button_enable=params['button_enable'],
                          control_door1=params['control_doors']['door1'],
                          control_door2=params['control_doors']['door2'],
                          access_type=db.AccessType.select().where(
                              db.AccessType.access_type == params['access_type']).get())
            i.save() or i.save(force_insert=True)
            if params['days_of_week']:
                for key in params['days_of_week'].keys():
                    period = params['days_of_week'][key]
                    begin = period[:5] + ':00'
                    end = period[6:] + ':59'
                    ref = db.RestrictAccess(day_of_week_id=db.DayOfWeek.select().where(db.DayOfWeek.name == key).get(),
                                            start_time=begin, end_time=end)
                    ref.save()
                    db.IpwallRestrictAccess(ipwall_id=i, restrict_access_id=ref).save()
            if params['door1_dependency']:
                for x in params['door1_dependency']:
                    db.IpwallDoorDependency(
                        ipwall_id=i,
                        door_id=1,
                        door_dependency=db.Door.select().where(db.Door.door == x['door_id']).get(),
                        ipwall_dependency=x['ipwall_id']).save()
            if params['door2_dependency']:
                for x in params['door2_dependency']:
                    db.IpwallDoorDependency(
                        ipwall_id=i,
                        door_id=2,
                        door_dependency=db.Door.select().where(db.Door.door == x['door_id']).get(),
                        ipwall_dependency=x['ipwall_id']).save()
            self.future['insert_ipwall'].set_result(True)
            logger.info("***IPWALL INSERIDO***")

        elif cmd['cmd'] == 'insert_set_rf':

            setrf = db.SetRf(set_rf=params['set_rf_id'], name='set_rf')
            setrf.save() or setrf.save(force_insert=True)
            db.Button(set_rf_id=setrf,
                      ipwall_id=db.Ipwall.select().where(
                          db.Ipwall.ipwall_id == params['set_rf']['button1']['ipwall_id']).get(),
                      door_id=db.Door.select().where(
                          db.Door.door == params['set_rf']['button1']['door_id']).get()).save()
            db.Button(set_rf_id=setrf,
                      ipwall_id=db.Ipwall.select().where(
                          db.Ipwall.ipwall_id == params['set_rf']['button2']['ipwall_id']).get(),
                      door_id=db.Door.select().where(
                          db.Door.door == params['set_rf']['button2']['door_id']).get()).save()
            db.Button(set_rf_id=setrf,
                      ipwall_id=db.Ipwall.select().where(
                          db.Ipwall.ipwall_id == params['set_rf']['button3']['ipwall_id']).get(),
                      door_id=db.Door.select().where(
                          db.Door.door == params['set_rf']['button3']['door_id']).get()).save()

            db.Button(set_rf_id=setrf,
                      ipwall_id=db.Ipwall.select().where(
                            db.Ipwall.ipwall_id == params['set_rf']['button4']['ipwall_id']).get(),
                      door_id=db.Door.select().where(
                            db.Door.door == params['set_rf']['button4']['door_id']).get()).save()
            self.future['insert_set_rf'].set_result(True)
            logger.info("***SET RF INSERIDO***")

        elif cmd['cmd'] == 'insert_user':
            if params['set_rf_id']:
                try:
                    setrf = db.SetRf.select().where(db.SetRf.set_rf == params['set_rf_id']).get()
                except db.SetRf.DoesNotExist:
                    logger.info("SetRf Does Not Exist")
                    return
            else:
                setrf = None
            ui = None
            u = db.User(user_id=params['user_id'], rf_id=db.Rf.select().where(db.Rf.rf == params['rf_id']).get(),
                        tag_id=db.Tag.select().where(db.Tag.tag == params['tag_id']).get(), set_rf_id=setrf,
                        counter_rf=params['counter_rf'], opening_time=params['opening_time'],
                        blocked=params['blocked'],
                        administrator=params['administrator'], secret=params['secret'])
            if params['ipwall_access_tag']:
                try:
                    ipwalls = []
                    for id in params['ipwall_access_tag']:
                        ipwalls.append(db.Ipwall.select().where(db.Ipwall.ipwall_id == id).get())
                    for ref in ipwalls:
                        ui = db.UserIpwall(user_id=u, ipwall_id=ref)
                except db.Ipwall.DoesNotExist:
                    logger.info('Ipwall Does Not Exist')
                    return
            u.save() or u.save(force_insert=True)
            if ui:
                ui.save()
            if params['restrict_access']:
                for key in params['days_of_week'].keys():
                    period = params['days_of_week'][key]
                    begin = period[:5] + ':00'
                    end = period[6:] + ':59'
                    ref = db.RestrictAccess(day_of_week_id=db.DayOfWeek.select().where(db.DayOfWeek.name == key).get(),
                                            start_time=begin, end_time=end)
                    ref.save()
                    db.UserRestrictAccess(user_id=u, restrict_access_id=ref).save()
            self.future['insert_user'].set_result(True)
            logger.info("***USER INSERIDO***")

        elif cmd['cmd'] == 'insert_qrcode_reader':
            relation = params['relation'][0]
            q = db.Qrcode(ip=params['qrcode_reader_ip'], qrcode_id=params['qrcode_reader_id'],
                          cam_id=relation['cam_id'], wiegand_id=relation['wiegand_id'])
            q.save() or q.save(force_insert=True)
            i = db.Ipwall.select().where(db.Ipwall.ipwall_id == relation['ipwall_id']).get()
            db.QrcodeIpwall(ipwall_id=i, qrcode_id=q).save()
            self.future['insert_qrcode_reader'].set_result(True)
            logger.info("***QRCODE INSERIDO***")
        elif cmd['cmd'] == 'insert_guest':
            valid = params['valid']
            g = db.Guest(guest_id=params['guest_id'], valid_from=valid['valid_from'], valid_until=valid['valid_until'],
                         access_counter=valid['access_counter'], code=params['code'])
            g.save() or g.save(force_insert=True)
            for x in params['ipwall_access_list']:
                db.GuestIpwall(guest_id=g, ipwall_id=db.Ipwall.select().where(db.Ipwall.ipwall_id == x).get()).save()
            self.future['insert_guest'].set_result(True)
            logger.info("***GUEST INSERIDO***")
        elif cmd['cmd'] == 'delete_ipwall':
            restrict_id = []
            for x in db.IpwallRestrictAccess.select().where(
                            db.IpwallRestrictAccess.ipwall_id == db.Ipwall.select().where(
                                db.Ipwall.ipwall_id == params['ipwall_id']).get().ipwall_id):
                restrict_id.append(x.restrict_access_id.id)
            try:
                db.Ipwall.delete().where(db.Ipwall.ipwall_id == params['ipwall_id']).execute()
            except peewee.IntegrityError:
                return -1
            for x in restrict_id:
                db.RestrictAccess.delete().where(db.RestrictAccess.id == x).execute()
            self.future['delete_ipwall'].set_result(True)
            logger.info("---IPWALL DELETED---")
        elif cmd['cmd'] == 'delete_set_rf':
            try:
                q = db.SetRf.delete().where(db.SetRf.set_rf == params['set_rf_id'])
                q.execute()
            except peewee.IntegrityError:
                return -1
            self.future['delete_set_rf'].set_result(True)
            logger.info("---SET RF DELETED---")
        elif cmd['cmd'] == 'delete_user':
            restrict_id = []
            for x in db.UserRestrictAccess.select().where(db.UserRestrictAccess.user_id == db.User.select().where(
                            db.User.user_id == params['user_id']).get().user_id):
                restrict_id.append(x.restrict_access_id.id)
            db.User.delete().where(db.User.user_id == params['user_id']).execute()
            for x in restrict_id:
                db.RestrictAccess.delete().where(db.RestrictAccess.id == x).execute()
            self.future['delete_user'].set_result(True)
            logger.info("---USER DELETED---")
        elif cmd['cmd'] == 'delete_qrcode_reader':
            db.Qrcode.delete().where(db.Qrcode.qrcode_id == params['qrcode_reader_id']).execute()
            self.future['delete_qrcode_reader'].set_result(True)
            logger.info("---QRCODE DELETED---")
        elif cmd['cmd'] == 'delete_guest':
            db.Guest.delete().where(db.Guest.guest_id == params['guest_id']).execute()
            self.future['delete_guest'].set_result(True)
            logger.info("---GUEST DELETED---")
        elif cmd['cmd'] == 'delete_all_ipwalls':
            db.Ipwall.delete().execute()
            self.future['delete_all_ipwalls'].set_result(True)
            logger.info("--*ALL IPWALLS DELETED*--")
        elif cmd['cmd'] == 'delete_all_set_rf':
            db.SetRf.delete().execute()
            self.future['delete_all_set_rf'].set_result(True)
            logger.info("--*ALL SET RF DELETED*--")
        elif cmd['cmd'] == 'delete_all_users':
            db.User.delete().execute()
            self.future['delete_all_users'].set_result(True)
            logger.info("--*ALL USERS DELETED*--")
        elif cmd['cmd'] == 'delete_all_qrcode_readers':
            db.Qrcode.delete().execute()
            self.future['delete_all_qrcode_readers'].set_result(True)
            logger.info("--*ALL QRCODES DELETED*--")
        elif cmd['cmd'] == 'delete_all_guests':
            db.Guest.delete().execute()
            self.future['delete_all_guests'].set_result(True)
            logger.info("--*ALL GUESTS DELETED*--")
        return 0

    def get_ipwall_list():
        list = []
        for k in db.Ipwall.select():
            beta = model_to_dict(k)
            beta.update({'access_type': beta['access_type']['access_type']})
            beta.update({'ipwall_name': beta['name']})
            beta.update({'control_doors': {'door1': beta['control_door1'], 'door2': beta['control_door2']}})
            del beta['control_door1']
            del beta['control_door2']
            del beta['name']
            ref_list = []
            dep1 = []
            dep2 = []
            for x in db.IpwallDoorDependency.select().where(db.IpwallDoorDependency.ipwall_id == k):
                ref_list.append(x)
            if ref_list:
                for x in ref_list:
                    if x.door_id == 1:
                        dep1.append({'ipwall_id': x.ipwall_dependency, 'door_id': x.door_dependency.id})
                    else:
                        dep2.append({'ipwall_id': x.ipwall_dependency, 'door_id': x.door_dependency.id})
                beta.update({'door1_dependency': dep1})
                beta.update({'door2_dependency': dep2})
            else:
                beta.update({'door1_dependency': None})
                beta.update({'door2_dependency': None})
            days = {}
            for y in db.IpwallRestrictAccess.select().where(db.IpwallRestrictAccess.ipwall_id == k):
                restrict = db.RestrictAccess.select().where(db.RestrictAccess.id == y.restrict_access_id).get()
                days.update({restrict.day_of_week_id.name: str(restrict.start_time)[:5]+'-'+str(restrict.end_time)[:5]})
            beta.update({'days_of_week': days})
            list.append(beta)
        # print('\nGET ipwall_list: ', list)
        return list

    def get_set_rf_list():
        list = []
        for k in db.SetRf.select():
            dictbutton = {}
            for button in db.Button.select().where(db.Button.set_rf_id == k):
                button_table = model_to_dict(button)
                if button_table['id'] % 4 == 0:
                    dictbutton.update({'button4': {'ipwall_id': button_table['ipwall_id']['ipwall_id'],
                                                   'door_id': button_table['door_id']['door']}})
                elif button_table['id'] % 4 == 3:
                    dictbutton.update({'button3': {'ipwall_id': button_table['ipwall_id']['ipwall_id'],
                                                   'door_id': button_table['door_id']['door']}})
                elif button_table['id'] % 4 == 2:
                    dictbutton.update({'button2': {'ipwall_id': button_table['ipwall_id']['ipwall_id'],
                                                   'door_id': button_table['door_id']['door']}})
                elif button_table['id'] % 4 == 1:
                    dictbutton.update({'button1': {'ipwall_id': button_table['ipwall_id']['ipwall_id'],
                                                   'door_id': button_table['door_id']['door']}})
            cmd = model_to_dict(k)
            setrf = {'set_rf_id': cmd['set_rf'], 'set_rf': dictbutton}
            list.append(setrf)
        # print('\nGET set_rf_list: ', list)
        return list

    def get_user_list():
        list = []
        for k in db.User.select():
            yota = []
            for y in db.UserIpwall.select().where(db.UserIpwall.user_id == k):
                yota.append(model_to_dict(y)['ipwall_id']['ipwall_id'])
            x = model_to_dict(k)
            x.update({'tag_id': x['tag_id']['tag']})
            try:
                if x['set_rf_id']['set_rf']:
                    x.update({'set_rf_id': x['set_rf_id']['set_rf']})
                x.update({'rf_id': x['rf_id']['rf']})
            except KeyError:
                pass
            x.update({'ipwall_access_tag': yota})
            list.append(x)
        # print('\nGET user_list: ', list)
        return list

    def get_qrcode_list():
        list = []
        gama = []
        for k in db.Qrcode.select():
            for y in db.QrcodeIpwall.select().where(db.QrcodeIpwall.qrcode_id == k):
                gama.append({'cam_id': model_to_dict(y)['qrcode_id']['cam_id'],
                             'ipwall_id': model_to_dict(y)['ipwall_id']['ipwall_id'],
                             'wiegand_id': model_to_dict(y)['qrcode_id']['wiegand_id']})
            qrcode = {}
            qrcode.update({'qrcode_reader_id': model_to_dict(k)['qrcode_id']})
            qrcode.update({'qrcode_reader_ip': model_to_dict(k)['ip']})
            qrcode.update({'relation': gama})
            list.append(qrcode)
        # print('\nGET qrcode_list: ', list)
        return list

    def get_guest_list():
        list = []
        alpha = {}
        for k in db.Guest.select():
            omega = []
            for y in db.GuestIpwall.select().where(db.GuestIpwall.guest_id == k):
                omega.append(model_to_dict(y)['ipwall_id']['ipwall_id'])
            alpha['guest_id'] = model_to_dict(k)['guest_id']
            alpha['code'] = model_to_dict(k)['code']
            alpha['ipwall_access_list'] = omega
            alpha['valid'] = {'valid_from': str(model_to_dict(k)['valid_from']),
                              'valid_until': str(model_to_dict(k)['valid_until']),
                              'access_counter': model_to_dict(k)['access_counter']}
            list.append(alpha)
        # print('\nGET guest_list: ', list)
        return list
