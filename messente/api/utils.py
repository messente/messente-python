import time
import os

from messente.logging import log


def is_int(value):
    try:
        int(value)
    except (ValueError, TypeError):
        return False
    return True


def ge_epoch(value):
    return (value >= int(time.time()))


def write_file(path, contents, **kwargs):
    d = os.path.dirname(path)
    try:
        if not os.path.isdir(d):
            os.makedirs(d)
        with open(path, "w") as f:
            f.write(contents)
        return True
    except OSError as e:
        log.exception(e)
    return False
