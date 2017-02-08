import peewee
from playhouse.shortcuts import model_to_dict 

database = peewee.SqliteDatabase('teste.db', pragmas=(('foreign_keys', 'on'),))


class BaseModel(peewee.Model):
    class Meta:
        database = database


class Artist(BaseModel):
    name = peewee.CharField()
    a_id = peewee.IntegerField(primary_key=True, unique=True)


class Radio(BaseModel):
    name =  peewee.CharField()


class ArtistRadio(BaseModel):
    artist = peewee.ForeignKeyField(Artist, on_delete="CASCADE")
    radio = peewee.ForeignKeyField(Radio)


def create():
    if not Artist.table_exists():
        Artist.create_table()
        print("artist table created")
    if not Radio.table_exists():
        Radio.create_table()
    if not ArtistRadio.table_exists():
        ArtistRadio.create_table()

def main():
    create()
    a1 = Artist(name='Raul', a_id=19)
    a1.save()
    a2 = Artist(name='Cazuza', a_id=20)
    a2.save()
    
    r1 = Radio(name='supernova')
    r1.save()
    r2 = Radio(name='franciscana')
    r2.save()

    for radios in Radio.select():
        ArtistRadio(radio=radios).save()

    print(Artist.select().where(Artist.a_id == 19).get())
    print(Artist.select().where(Artist.a_id == 19).get().id)
    print('FOR:')
    for x in Artist.select().where(Artist.a_id == 19):
        print(x.id)

    input()
    id_artist = 1
    radio_id = []
    for x in ArtistRadio.select().where(ArtistRadio.artist == id_artist):
        print('ArtistRadio ', model_to_dict(x))
        radio_id.append(x.radio.id)
    Artist.delete().where(Artist == id_artist).execute()
    for x in radio_id:
        Radio.delete().where(Radio == x).execute()

if __name__ == '__main__':
    main()
