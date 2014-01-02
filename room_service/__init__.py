from flask import Flask
from flask_peewee.db import Database
from flask_peewee.auth import Auth
from flask_peewee.admin import Admin

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


from room_service.models import Room, RoomAdmin
import room_service.views


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
