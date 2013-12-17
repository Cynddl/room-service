# -*- coding: utf-8 -*-

import pandas

from app import *


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
    if not pandas.isnull(row['vidéoprojecteur']):
        room.projector = row['vidéoprojecteur']
    if not pandas.isnull(row['Enceinte']):
        room.speaker = row['Enceinte']
    if not pandas.isnull(row['Caméra']):
        room.camera = row['Caméra']
    if not pandas.isnull(row['linux/windows']):
        room.os = row['linux/windows']

    room.save()
