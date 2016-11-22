import time


def is_int(value):
    try:
        int(value)
    except ValueError:
        return False
    return True


def ge_epoch(value):
    return (value >= int(time.time()))
