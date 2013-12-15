import urllib
import re
import datetime
from datetime import timedelta


class Time(datetime.datetime):
    """Extends the datetime.datetime class to look like datetime.time, but
    with support for substraction and all the nice stuff."""
    def __new__(cls, hour=0, minute=0, second=0, microsecond=0, tzinfo=None):
        return super(Time, cls).__new__(cls, 2000, 1, 1, hour, minute, second, microsecond, tzinfo)


def parse_monod(year, month, day, area, room):
    """Returns the list of hours at which the given room is occupied."""
    skeleton = 'https://glaive-03-domu-lamp.ens-lyon.fr/ENT/mrbs-enseignement/day.php?'
    args = 'year=%i&month=%i&day=%i&area=%i&room=%i&debug_flag=1' % (year, month, day, area, room)

    f = urllib.urlopen(skeleton + args)
    raw = f.readlines()
    filtered = filter(lambda s: s.startswith('d['), raw)
    data = list()
    for l in filtered:
        m = re.match("d\[(\d+)\]\[(\d+)\]\[(\d+)\]", l)
        if m:
            groups = m.groups()
            if len(groups) == 3:
                data.append(groups)
    # Each item in data is a triple (room, day, hour). We only need the hour.
    hours = [d[2] for d in data if int(d[0]) == room]
    # The format is weird: "HHMM". Convert it to a (hours, minutes) tuple.
    return [Time(int(h[0:-2]), int(h[-2:len(h)])) for h in hours]


def occupancy_intervals(year, month, day, area, room):
    """Returns the list of intervals at which the room is occupied"""
    # Length of a single time slot.
    TIMESLOT = timedelta(minutes=30)
    raw_data = parse_monod(year, month, day, area, room)
    if not raw_data:
        return []
    intervals = list()
    current_start = raw_data[0]
    for (t1, t2) in zip(raw_data[:-1], raw_data[1:]):
        if t2 - t1 != TIMESLOT:
            intervals.append((current_start, t1 + TIMESLOT))
            current_start = t2
    intervals.append((current_start, t2 + TIMESLOT))
    return intervals


def is_room_free(year, month, day, area, room,
                 start_hour, start_min,
                 stop_hour, stop_min):
    intervals = occupancy_intervals(year, month, day, area, room)
    start = Time(start_hour, start_min)
    stop = Time(stop_hour, stop_min)
    clashing = filter(lambda (t1, t2): start < t2 and t1 < stop, intervals)
    return (not clashing)
