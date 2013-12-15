from flask import Flask, render_template
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
    site = TextField(choices=[('Monod', 'Monod'), ('Descartes', 'Descartes')])
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

if __name__ == '__main__':
    auth.User.create_table(fail_silently=True)
    Room.create_table(fail_silently=True)
    app.run()
