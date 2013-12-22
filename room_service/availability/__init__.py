from check_mrbs import get_clashing_booking as mrbs_clash
from check_emptps import get_clashing_booking as emptps_clash


def get_clashing_booking(room, start_time, stop_time):
    if room.api == 'mrbs' or room.api == 'mrbs-enseignement':
        return mrbs_clash(room.api, room.area_code, room.room_code, start_time, stop_time)
    elif room.api == 'emptps':
        return emptps_clash(room.room_code, start_time, stop_time)
    else:
        return []


def check_availability(room, start_time, stop_time):
    return get_clashing_booking(room, start_time, stop_time) == []
