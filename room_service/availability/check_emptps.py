from datetime import datetime, timedelta, time
from dateutil.parser import parse
import requests

_EMPTPS_URL = 'http://emptps-lsh.ens-lyon.fr/php/ajax/OccList.php'
_EMPTPS_ARGS = '?start={}&end={}&sel=Sal%3A+{}'


def occupancy_intervals(room_id, date_start, date_last=None):
    """Returns the list of intervals at which the room is occupied."""
    ONEDAY = timedelta(days=1)

    if not date_last:
        date_last = date_start
    date_last = date_last + ONEDAY
    date_start_str = date_start.strftime('%Y-%m-%d')
    date_last_str = date_last.strftime('%Y-%m-%d')

    url = _EMPTPS_URL + _EMPTPS_ARGS.format(date_start_str, date_last_str, room_id)
    response = requests.get(url)
    data = response.json()

    return [(parse(cell['start']).replace(tzinfo=None), parse(cell['end']).replace(tzinfo=None)) for cell in data]


def get_clashing_booking(room_id, start_time, stop_time):
    """Checks if a room in Descartes is free for the specified time interval, by
    returning a list of booking clashing with it. Arguments are datetime
    objects. The time interval is allowed to span multiple days."""

    last_day = datetime.combine(stop_time.date(), time.max)
    intervals = occupancy_intervals(room_id, start_time, last_day)

    return filter(lambda (t1, t2): start_time < t2 and t1 < stop_time, intervals)
