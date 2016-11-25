import time
import os
import re

from messente.logging import log


PHONE_REPLACE_RE = re.compile("(\+|-|_|\.|\s)*")


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


def adapt_phone_number(phone):
    return PHONE_REPLACE_RE.sub("", (phone or "").strip())


def is_phone_number_valid(phone):
    s = str(phone)
    return (s.isdigit() and 9 < len(s) < 16)
