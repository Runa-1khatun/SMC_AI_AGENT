from datetime import datetime


def get_killzone():

    hour = datetime.utcnow().hour
    minute = datetime.utcnow().minute

    current = hour + (minute / 60)

    # London Kill Zone
    if 7 <= current < 10:
        return "LONDON"

    # New York Kill Zone
    elif 13 <= current < 16:
        return "NEWYORK"

    # London + New York Overlap
    elif 13 <= current < 15:
        return "OVERLAP"

    return "NONE"