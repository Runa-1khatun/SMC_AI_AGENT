from datetime import datetime


def get_session():

    hour = datetime.utcnow().hour

    if 0 <= hour < 7:
        return "ASIAN"

    elif 7 <= hour < 13:
        return "LONDON"

    elif 13 <= hour < 17:
        return "NEWYORK"

    elif 17 <= hour < 21:
        return "OVERLAP"

    return "CLOSED"