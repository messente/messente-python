from __future__ import absolute_import

import os
import sys
import logging

from messente.api.error import ConfigurationError


DEFAULT_LOG_FORMAT = "%(asctime)-15s %(levelname)-7s %(name)-32s %(message)s"
log = logging.getLogger("messente")


class Logger(object):
    def __init__(self, name=None, **kwargs):
        self.log = log.getChild((name or self.__class__.__name__))

        if kwargs.pop("log_debug", False):
            self.log.setLevel(logging.DEBUG)
        else:
            self.log.setLevel(logging.INFO)

        formatter = logging.Formatter(
            kwargs.pop("log_format", DEFAULT_LOG_FORMAT)
        )

        handlers = []
        if kwargs.pop("log_stdout", False):
            handlers.append(logging.StreamHandler(stream=sys.stdout))

        log_file = kwargs.pop("log_file")
        if log_file:
            d = os.path.dirname(log_file)
            if not os.path.isdir(d):
                os.makedirs(d)
            handlers.append(logging.FileHandler(log_file))

        for hndl in handlers:
            hndl.setFormatter(formatter)
            self.log.addHandler(hndl)
