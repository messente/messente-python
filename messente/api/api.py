from __future__ import absolute_import

import os
import requests

from messente.logging import Logger
from messente.api import config


class API(Logger):
    def __init__(self, config_section, **kwargs):
        self._config_section = config_section
        for section in ["default", self._config_section]:
            if not config.configuration.has_section(section):
                config.configuration.add_section(section)

        if kwargs.get("ini_path", ""):
            config.load(kwargs.pop("ini_path"))

        self._config_getters = {
            str: config.configuration.get,
            int: config.configuration.getint,
            bool: config.configuration.getboolean,
        }

        super().__init__(
            stdout=self.get_bool_option("log_stdout", False),
            debug=self.get_bool_option("log_debug", False),
            log_format=self.get_option("log_format", None),
            log_file=self.get_option("log_file"),
        )
        overrides = {
            "api_url": "MESSENTE_API_URL",
            "username": "MESSENTE_API_USERNAME",
            "password": "MESSENTE_API_PASSWORD",
        }

        for item in overrides:
            value = kwargs.pop(item, os.getenv(overrides[item], ""))
            if value:
                self.set_option(item, value)

        self.log.info("Initialized")

    def call_api(self, endpoint, method="GET", **data):
        fmt = "{api_url}/{endpoint}"
        url_params = dict(
            api_url=self.get_option("api_url"),
            endpoint=endpoint,
        )
        url = fmt.format(**url_params)
        data.update(dict(
            username=self.get_option("username"),
            password="[redacted]",
        ))

        self.log.info("%s: %s", method, url)
        self.log.debug("%s", data)

        data.update(dict(password=self.get_option("password")))

        try:
            r = None
            method = method.upper()
            if method == "GET":
                r = requests.get(url, params=data, allow_redirects=True)
            elif method == "POST":
                r = requests.post(url, params=data, allow_redirects=True)
            return r
        except Exception as e:
            self.log.exception(e)

    def set_option(self, option, value):
        config.configuration[self._config_section][option] = value

    def get_option(self, option, default=None, **kwargs):
        data_type = kwargs.pop("data_type", str)
        default_value = (default or data_type())
        fallback_section = kwargs.pop("fallback_section", "default")
        section = self._config_section
        if not config.configuration.has_option(self._config_section, option):
            section = fallback_section
        getter = self._config_getters[data_type]
        return getter(section, option, fallback=default_value)

    def get_str_option(self, *args, **kwargs):
        return self.get_option(*args, **kwargs)

    def get_int_option(self, *args, **kwargs):
        return self.get_option(*args, data_type=int, **kwargs)

    def get_bool_option(self, *args, **kwargs):
        return self.get_option(*args, data_type=bool, **kwargs)

    def log_response(self, r):
        if not r.is_replied():
            self.log.critical("No response")
        elif not r.is_ok():
            self.log.error(r.get_full_error_msg())
        else:
            self.log.debug(r.get_raw_text())
