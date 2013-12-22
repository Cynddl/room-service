from flask_peewee.admin import ModelAdmin
from peewee import *
from room_service import db


# Models #
class Room(db.Model):
    name = CharField()
    capacity = IntegerField()
    site = TextField(choices=[('monod', 'Monod'), ('descartes', 'Descartes')])
    type = CharField()

    os = CharField(null=True)
    camera = IntegerField(null=True)
    projector = IntegerField(null=True)
    speaker = IntegerField(null=True)

    api = CharField(null=True)
    room_code = IntegerField(null=True)
    area_code = IntegerField(null=True)

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.site)


class RoomAdmin(ModelAdmin):
    columns = ('name', 'capacity', 'site')
