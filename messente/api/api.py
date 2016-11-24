from __future__ import absolute_import

import os
import requests

from messente.logging import Logger
from messente.api import config
from messente.api.error import ConfigurationError
from messente.api.error import InvalidMessageError


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

        params = dict(
            log_stdout=bool,
            log_debug=bool,
            log_format=str,
            log_file=str,
        )

        for p in params:
            params[p] = kwargs.pop(p, self.get_option(p, data_type=params[p]))

        super().__init__(**params)

        env_overrides = {
            "username": "MESSENTE_API_USERNAME",
            "password": "MESSENTE_API_PASSWORD",
        }

        for option in env_overrides:
            value = kwargs.pop(option, os.getenv(env_overrides[option], ""))
            if value:
                config.configuration[self._config_section][option] = value
        self.api_urls = []
        self.set_urls(kwargs.pop("urls", None))
        self.log.info("Initialized")

    def set_urls(self, urls=None):
        if not urls:
            urls = self.get_option("urls", "")
        if not urls:
            raise Exception()
        if type(urls) not in [list, tuple]:
            urls = urls.split(" ")
        self.api_urls = [url.strip() for url in urls]

    def call_api(self, endpoint, method="GET", **data):
        if not self.api_urls:
            raise ConfigurationError("No urls configured")
        # first succesful url makes the function return
        for url in self.api_urls:
            url = "{url}/{endpoint}".format(url=url, endpoint=endpoint)
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
        self.log.error("No more urls to try. Giving up.")
        return None

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

    def validate(self, data, **kwargs):
        (ok, errors) = self._validate(data, **kwargs)
        if not ok:
            for field in errors:
                self.log.error("%s: %s", field, errors[field])
                raise InvalidMessageError("Message is invalid")

    def _validate(self, data, **kwargs):
        return (True, {})

    def set_error(self, errors, field, msg=None):
        errors[field] = (msg or "Invalid '%s'" % field)

    def set_error_required(self, errors, field, msg=None):
        errors[field] = (msg or "Required '%s'" % field)
