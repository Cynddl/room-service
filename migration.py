# -*- coding: utf-8 -*-

import pandas

from room_service import *

# Drop tables
Room.drop_table()
auth.User.drop_table()

# Create tables
auth.User.create_table()
Room.create_table()

auth.User.create_table(fail_silently=True)  # make sure table created.
admin = auth.User(username='admin', email='', admin=True, active=True)
admin.set_password('admin')
admin.save()


df = pandas.read_csv('bdd-salles.csv')

for _, row in df.iterrows():
    room = Room()
    room.type = row['type']
    room.name = row['Nom de salle']
    room.site = row['site'].lower()
    room.capacity = row['capacité exacte']
    if pandas.notnull(row['vidéoprojecteur']):
        room.projector = row['vidéoprojecteur']
    if pandas.notnull(row['Enceinte']):
        room.speaker = row['Enceinte']
    if pandas.notnull(row['Caméra']):
        room.camera = row['Caméra']
    if pandas.notnull(row['OS']):
        room.os = row['OS']

    if pandas.notnull(row['API']):
        room.api = row['API']
    if pandas.notnull(row['area_code']):
        room.area_code = row['area_code']
    if pandas.notnull(row['room_code']):
        room.room_code = row['room_code']

    room.save()
