from flask import render_template, json, request
from room_service import app
from room_service.models import Room

from datetime import datetime

from room_service.availability import check_availability


@app.route('/')
def index(name=None):
    return render_template('index.html', name=name)


@app.route('/search', methods=['POST'])
def search():
    date = request.form.get('date_raw')
    time_first = request.form.get('time_first')
    time_last = request.form.get('time_last')
    date_first = datetime.strptime(date + ' ' + time_first, "%Y-%m-%d %H:%M")
    date_last = datetime.strptime(date + ' ' + time_last, "%Y-%m-%d %H:%M")

    roomCapacity = request.form.get('roomCapacity')
    roomType = request.form.get('roomType')
    site = request.form.get('site')
    equipement = request.form.getlist('equipement')

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

    rooms_list = [(r.id, r.name, check_availability(r, date_first, date_last)) for r in rooms]
    rooms_list = sorted(rooms_list, key=lambda r_tuple: r_tuple[2], reverse=True)

    return json.dumps({'status': 'success', 'rooms': rooms_list})
