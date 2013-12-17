from datetime import datetime, timedelta, time
from dateutil.parser import parse
import urllib
import json


def fetch_rooms():
    """Save the list of rooms and their IDs in the database."""
    response = urllib.urlopen('http://emptps-lsh.ens-lyon.fr/php/ajax/SalGrid.php?rows=200')
    data = json.load(response)
    rooms = [(int(row['id']), row['cell'][0], row['cell'][1]) for row in data['rows']]
    with open('rooms.json', 'wb') as f:
        json.dump(rooms, f)


def occupancy_intervals(room_id, date_start, date_last=None):
    """Returns the list of intervals at which the room is occupied"""
    ONEDAY = timedelta(days=1)

    if not date_last:
        date_last = date_start
    date_last = date_last + ONEDAY
    date_start_str = date_start.strftime('%Y-%m-%d')
    date_last_str = date_last.strftime('%Y-%m-%d')

    url = 'http://emptps-lsh.ens-lyon.fr/php/ajax/OccList.php?start=' + date_start_str + '&end=' + date_last_str + '&sel=Sal%3A+' + str(room_id)
    response = urllib.urlopen(url)
    data = json.load(response)

    return [(parse(cell['start']).replace(tzinfo=None), parse(cell['end']).replace(tzinfo=None)) for cell in data]


def get_clashing_booking(room_id, start_time, stop_time):
    """Checks if a room in Descartes is free for the specified time interval, by
    returning a list of booking clashing with it. Arguments are datetime
    objects. The time interval is allowed to span multiple days."""

    last_day = datetime.combine(stop_time.date(), time.max)
    intervals = occupancy_intervals(room_id, start_time, last_day)

    return filter(lambda (t1, t2): start_time < t2 and t1 < stop_time, intervals)


if __name__ == '__main__':
    print("Fetching the list of rooms...")
    fetch_rooms()
