import peewee

database = peewee.SqliteDatabase('kiper.db', pragmas=(('foreign_keys', 'on'),))

days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


class BaseModel(peewee.Model):
    class Meta:
        database = database


class AccessType(BaseModel):
    access_type = peewee.CharField()


class Door(BaseModel):
    door = peewee.IntegerField()


class Rf(BaseModel):
    rf = peewee.BigIntegerField()


class Tag(BaseModel):
    tag = peewee.BigIntegerField()


class SetRf(BaseModel):
    set_rf = peewee.BigIntegerField(unique=True, primary_key=True)
    name = peewee.CharField()


class Qrcode(BaseModel):
    ip = peewee.CharField()
    qrcode_id = peewee.IntegerField(unique=True, primary_key=True)
    cam_id = peewee.IntegerField()
    wiegand_id = peewee.IntegerField()


class DayOfWeek(BaseModel):
    name = peewee.CharField()


class Guest(BaseModel):
    guest_id = peewee.IntegerField(unique=True, primary_key=True)
    valid_from = peewee.DateTimeField()
    valid_until = peewee.DateTimeField()
    code = peewee.CharField()
    access_counter = peewee.IntegerField()


class RestrictAccess(BaseModel):
    start_time = peewee.TimeField()
    end_time = peewee.TimeField()
    day_of_week_id = peewee.ForeignKeyField(DayOfWeek)


class User(BaseModel):
    user_id = peewee.IntegerField(unique=True, primary_key=True)
    set_rf_id = peewee.ForeignKeyField(SetRf, null=True)
    rf_id = peewee.ForeignKeyField(Rf, null=True)
    tag_id = peewee.ForeignKeyField(Tag, null=True)
    counter_rf = peewee.IntegerField(null=True)
    opening_time = peewee.IntegerField(null=True)
    blocked = peewee.BooleanField()
    administrator = peewee.BooleanField()
    secret = peewee.CharField(null=True)


class Ipwall(BaseModel):
    ipwall_id = peewee.IntegerField(unique=True, primary_key=True)
    access_type = peewee.ForeignKeyField(AccessType)
    name = peewee.CharField(null=True)
    ip = peewee.CharField(null=True)
    control_door1 = peewee.BooleanField(null=True)
    control_door2 = peewee.BooleanField(null=True)
    button_enable = peewee.BooleanField(null=True)
    disable_emergency = peewee.BooleanField(null=True)


class IpwallDoorDependency(BaseModel):
    ipwall_id = peewee.ForeignKeyField(Ipwall, on_delete='CASCADE')
    door_id = peewee.IntegerField()
    ipwall_dependency = peewee.IntegerField()
    door_dependency = peewee.ForeignKeyField(Door)


class IpwallRestrictAccess(BaseModel):
    ipwall_id = peewee.ForeignKeyField(Ipwall, on_delete='CASCADE')
    restrict_access_id = peewee.ForeignKeyField(RestrictAccess)


class UserIpwall(BaseModel):
    user_id = peewee.ForeignKeyField(User, on_delete='CASCADE')
    ipwall_id = peewee.ForeignKeyField(Ipwall, on_delete='CASCADE')


class Button(BaseModel):
    set_rf_id = peewee.ForeignKeyField(SetRf, on_delete='CASCADE')
    door_id = peewee.ForeignKeyField(Door)
    ipwall_id = peewee.ForeignKeyField(Ipwall, on_delete='CASCADE')


class QrcodeIpwall(BaseModel):
    qrcode_id = peewee.ForeignKeyField(Qrcode, on_delete='CASCADE')
    ipwall_id = peewee.ForeignKeyField(Ipwall, on_delete='CASCADE')


class GuestIpwall(BaseModel):
    guest_id = peewee.ForeignKeyField(Guest, on_delete='CASCADE')
    ipwall_id = peewee.ForeignKeyField(Ipwall, on_delete='CASCADE')


class UserRestrictAccess(BaseModel):
    user_id = peewee.ForeignKeyField(User, on_delete='CASCADE')
    restrict_access_id = peewee.ForeignKeyField(RestrictAccess)


def create_tables(logger):
    if not AccessType.table_exists():
        AccessType.create_table()
        AccessType(access_type='walker').save()
        AccessType(access_type='car').save()
        logger.info('DB: Table AccessType created')
    if not Ipwall.table_exists():
        Ipwall.create_table()
        i = Ipwall(ipwall_id=-1, access_type=AccessType.select().where(AccessType.access_type=='car').get())
        i.save() or i.save(force_insert=True)
        logger.info('DB: Table IPwall created')
    if not Door.table_exists():
        Door.create_table()
        Door(door=1).save()
        Door(door=2).save()
        logger.info('DB: Table Door created')
    if not Rf.table_exists():
        Rf.create_table()
        Rf(rf=769261826).save()
        Rf(rf=3059812612).save()
        Rf(rf=11599937).save()
        Rf(rf=1111111111).save()
        Rf(rf=6777777777).save()
        Rf(rf=1233).save()
        Rf(rf=43561).save()
        logger.info('DB: Table Rf created')
    if not Tag.table_exists():
        Tag.create_table()
        Tag(tag=68843220756).save()
        Tag(tag=68843220856).save()
        Tag(tag=68595732715).save()
        Tag(tag=68595732615).save()
        Tag(tag=22222222222).save()
        Tag(tag=33333333333).save()
        Tag(tag=44444444444).save()
        Tag(tag=55555555555).save()
        logger.info('DB: Table Tag created')
    if not SetRf.table_exists():
        SetRf.create_table()
        logger.info('DB: Table SetRf created')
    if not Qrcode.table_exists():
        Qrcode.create_table()
        logger.info('DB: Table Qrcode created')
    if not DayOfWeek.table_exists():
        DayOfWeek.create_table()
        for key in days:
            DayOfWeek(name=key).save()
        logger.info('DB: Table DayOfWeek created')
    if not Guest.table_exists():
        Guest.create_table()
        logger.info('DB: Table Guest created')
    if not RestrictAccess.table_exists():
        RestrictAccess.create_table()
        logger.info('DB: Table RestrictAccess created')
    if not User.table_exists():
        User.create_table()
        logger.info('DB: Table User created')
    if not Ipwall.table_exists():
        Ipwall.create_table()
        logger.info('DB: Table Ipwall created')
    if not IpwallDoorDependency.table_exists():
        IpwallDoorDependency.create_table()
        logger.info('DB: Table IpwallDoorDependency created')
    if not IpwallRestrictAccess.table_exists():
        IpwallRestrictAccess.create_table()
        logger.info('DB: Table IpwallRestrictAccess created')
    if not Button.table_exists():
        Button.create_table()
        logger.info('DB: Table Button created')
    if not UserIpwall.table_exists():
        UserIpwall.create_table()
        logger.info('DB: Table UserIpwall created')
    if not QrcodeIpwall.table_exists():
        QrcodeIpwall.create_table()
        logger.info('DB: Table QrcodeIpwall created')
    if not GuestIpwall.table_exists():
        GuestIpwall.create_table()
        logger.info('DB: Table GuestIpwall created')
    if not UserRestrictAccess.table_exists():
        UserRestrictAccess.create_table()
        logger.info('DB: Table UserRestrictAccess created')
