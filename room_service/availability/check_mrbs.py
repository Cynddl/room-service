import requests
import re
from datetime import timedelta, datetime, time


_MRBS_SKELETON = 'http://glaive-03-domu-lamp.ens-lyon.fr/ENT/{}/day.php'
_MRBS_ARGS = '?year={}&month={}&day={}&area={}&room={}&debug_flag=1'


def parse_url(api_path, area, room, date):
    """Returns the list of hours at which the given room is occupied."""

    skeleton = _MRBS_SKELETON.format(api_path)
    args = _MRBS_ARGS.format(date.year, date.month, date.day, area, room)
    f = requests.get(skeleton + args, timeout=1, verify=False)
    filtered = filter(lambda s: s.startswith('d['), f.text.split('\n'))
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
    return [datetime.combine(date.date(), time(int(h[0:-2]), int(h[-2:len(h)]))) for h in hours]


def occupancy_intervals(api_path, area, room, date):
    """Returns the list of intervals at which the room is occupied"""
    # Length of a single time slot.
    TIMESLOT = timedelta(minutes=30)
    raw_data = parse_url(api_path, area, room, date)
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


def get_clashing_booking(api_path, area, room, start_time, stop_time):
    """Checks if a room in Monod is free for the specified time interval, by
    returning a list of booking clashing with it. Arguments are datetime
    objects. The time interval is allowed to span multiple days."""
    ONEDAY = timedelta(1)
    intervals = list()
    day = start_time
    last_day = datetime.combine(stop_time.date(), time.max)
    while day < last_day:
        intervals.extend(occupancy_intervals(api_path, area, room, day))
        day += ONEDAY
    clashing = filter(lambda (t1, t2): start_time < t2 and t1 < stop_time, intervals)
    return clashing


if __name__ == '__main__':
    # Demo
    room, area = 1, 1
    start = datetime(2013, 12, 16, 13, 50)
    stop = datetime(2013, 12, 17, 10, 30)
    print("Querying room {} in area {} from {} to {}...".format(room, area, start, stop))
    clashing = get_clashing_booking('mrbs-enseignement', area, room, start, stop)
    for booking in clashing:
        print("Room already booked from {} to {}".format(booking[0], booking[1]))
    if clashing:
        print("Sorry, the room is not available.")
    else:
        print("The room is free!")
