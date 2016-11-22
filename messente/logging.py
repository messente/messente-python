from __future__ import absolute_import

import os
import sys
import logging

from messente.api.error import ConfigurationError


DEFAULT_LOG_FORMAT = "%(asctime)-15s %(levelname)-7s %(name)-24s %(message)s"
DEFAULT_FORMATTER = logging.Formatter(DEFAULT_LOG_FORMAT)
ROOT_LOGGER = logging.getLogger("messente")


class Logger(object):
    def __init__(self, name=None, **kwargs):
        self.log = ROOT_LOGGER.getChild((name or self.__class__.__name__))

        if kwargs.pop("debug", False):
            self.log.setLevel(logging.DEBUG)

        formatter = DEFAULT_FORMATTER
        if "log_format" in kwargs:
            formatter = logging.Formatter(
                kwargs.pop("log_format", DEFAULT_LOG_FORMAT)
            )

        handlers = []
        if kwargs.pop("stdout", False):
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
