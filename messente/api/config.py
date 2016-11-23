from __future__ import absolute_import

import os
from messente.api.error import ConfigurationError
from messente.logging import DEFAULT_LOG_FORMAT
from messente.logging import log

try:
    import configparser
except ImportError:
    import ConfigParser as configparser


configuration = configparser.SafeConfigParser()

configuration["default"] = dict(
    api_url=os.getenv(
        "MESSENTE_API_URL",
        "https://api21.messente.com"
    ),
    username=os.getenv("MESSENTE_API_USERNAME", ""),
    password=os.getenv("MESSENTE_API_PASSWORD", ""),
    log_stdout=False,
    log_debug=False,
    log_format=DEFAULT_LOG_FORMAT.replace("%", "%%"),
)

configuration.add_section("sms")
configuration.add_section("credit")


def load(path):
    global configuration
    log.debug("Loading configuration file: %s", path)
    path = os.path.expanduser(path)
    if not os.path.exists(path):
        raise ConfigurationError(
            "Invalid configuration file '%s'" % path
        )

    configuration.read(path)
