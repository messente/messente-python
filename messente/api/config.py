# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
from messente.api.error import ConfigurationError
from messente.logging import DEFAULT_LOG_FORMAT
from messente.logging import log

from six.moves import configparser

configuration = configparser.SafeConfigParser()

configuration.add_section("api")
configuration.add_section("sms")
configuration.add_section("credit")


configuration.set("api", "test", "ASD")
configuration.set(
    "api",
    "urls",
    "https://api2.messente.com https://api3.messente.com"
)

configuration.set(
    "api", "username", os.getenv("MESSENTE_API_USERNAME", "")
)
configuration.set(
    "api", "password", os.getenv("MESSENTE_API_PASSWORD", "")
)
configuration.set("api", "log_stdout", "false")
configuration.set("api", "log_debug", "false")
configuration.set("api", "log_file", "")
configuration.set(
    "api", "log_format", DEFAULT_LOG_FORMAT.replace("%", "%%")
)


def load(path):
    global configuration
    log.debug("Loading configuration file: %s", path)
    path = os.path.expanduser(path)
    if not os.path.exists(path):
        raise ConfigurationError(
            "Invalid configuration file '%s'" % path
        )

    configuration.read(path)
