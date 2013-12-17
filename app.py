from flask import Flask, render_template, json, request
from flask_peewee.db import Database
from flask_peewee.auth import Auth
from flask_peewee.admin import Admin, ModelAdmin
from peewee import *

from flask.ext.assets import Environment, Bundle


# configure our database
DATABASE = {
    'name': 'database.db',
    'engine': 'peewee.SqliteDatabase',
}
DEBUG = True
SECRET_KEY = 'bleubleu'


# Lancement de l'application
app = Flask(__name__)
app.config.from_object(__name__)
db = Database(app)
auth = Auth(app, db)


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

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.site)


class RoomAdmin(ModelAdmin):
    columns = ('name', 'capacity', 'site')


# Admin interface #
admin = Admin(app, auth)

admin.register(Room, RoomAdmin)
auth.register_admin(admin)
admin.setup()

# Assets
assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('main.scss', filters='pyscss', output='main.css')
assets.register('scss_all', scss)


@app.route('/')
def index(name=None):
    return render_template('index.html', name=name)


@app.route('/search', methods=['POST'])
def search():
    # date = request.form.get('date_raw')
    # time_first = request.form.get('time_first')
    # time_last = request.form.get('time_last')
    roomCapacity = request.form.get('roomCapacity')
    roomType = request.form.get('roomType')
    site = request.form.get('site')
    equipement = request.form.getlist('equipement')
    print equipement

    if roomCapacity == '<20':
        capacity_filter = Room.capacity < 20
    elif roomCapacity == '20-50':
        capacity_filter = (Room.capacity >= 20) & (Room.capacity <= 50)
    elif roomCapacity == '50-100':
        capacity_filter = (Room.capacity >= 50) & (Room.capacity <= 100)
    elif roomCapacity == '>100':
        capacity_filter = Room.capacity > 100
    else:
        capacity_filter = True

    equipement_filter = True
    if 'projector' in equipement:
        equipement_filter &= Room.projector >= 1
    if 'camera' in equipement:
        equipement_filter &= Room.camera >= 1
    if 'speaker' in equipement:
        equipement_filter &= Room.speaker >= 1

    type_filter = Room.type == roomType

    rooms = Room.select().where((Room.site == site) & capacity_filter & type_filter & equipement_filter)
    return json.dumps({'status': 'success', 'rooms': len(list(rooms))})

if __name__ == '__main__':
    auth.User.create_table(fail_silently=True)
    Room.create_table(fail_silently=True)
    app.run()
