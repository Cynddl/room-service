import urllib
import re
import datetime
from datetime import timedelta


def parse_monod(area, room, date):
    """Returns the list of hours at which the given room is occupied."""
    skeleton = 'https://glaive-03-domu-lamp.ens-lyon.fr/ENT/mrbs-enseignement/day.php?'
    args = 'year=%i&month=%i&day=%i&area=%i&room=%i&debug_flag=1' % (date.year, date.month, date.day, area, room)

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
    # The format is weird: "HHMM". Convert it to a datetime object.
    return [datetime.datetime.combine(date.date(), datetime.time(int(h[0:-2]), int(h[-2:len(h)]))) for h in hours]


def occupancy_intervals(area, room, date):
    """Returns the list of intervals at which the room is occupied"""
    # Length of a single time slot.
    TIMESLOT = timedelta(minutes=30)
    raw_data = parse_monod(area, room, date)
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


def is_room_free(area, room, start_time, stop_time):
    """Checks if a room in Monod is free for the specified time
    interval. Arguments are datetime objects. The time interval is allowed
    to span multiple days."""
    ONEDAY = datetime.timedelta(1)
    intervals = list()
    day = start_time
    while day < stop_time:
        intervals.extend(occupancy_intervals(area, room, day))
        day += ONEDAY
    clashing = filter(lambda (t1, t2): start_time < t2 and t1 < stop_time, intervals)
    return (not clashing)
