from __future__ import absolute_import

import os
from messente.api.error import ConfigurationError
from messente.logging import DEFAULT_LOG_FORMAT

try:
    import configparser
except ImportError:
    import ConfigParser as configparser


configuration = configparser.SafeConfigParser()

configuration["default"] = dict(
    api_url=os.getenv(
        "MESSENTE_API_URL",
        "https://api2.messente.com"
    ),
    username=os.getenv("MESSENTE_API_USERNAME", ""),
    password=os.getenv("MESSENTE_API_PASSWORD", ""),
    endpoint="",
    log_stdout=False,
    log_debug=False,
    log_format=DEFAULT_LOG_FORMAT.replace("%", "%%"),
)

configuration["sms"] = dict(
    api_url="https://api2.messente.com",
    endpoint="send_sms"
)


def load(path):
    global configuration
    path = os.path.expanduser(path)
    if not os.path.exists(path):
        raise ConfigurationError(
            "Invalid configuration file '%s'" % path
        )

    configuration.read(path)
