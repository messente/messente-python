from __future__ import absolute_import

from messente.api.error import ERROR_CODES


class Response(object):
    def __init__(self, response):
        self.raw_response = response
        self.error_code = None
        self.error_msg = ""
        self.status = ""
        self.parse()

    def parse(self):
        if self.raw_response is None:
            return

        parts = self.raw_response.text.split(" ")
        if parts:
            self.status = parts[0].upper()
            if self.status in ["ERROR", "FAILED"]:
                self.error_code = int(parts[1])
                k = self.status + " " + str(self.error_code)
                self.error_msg = self._get_error_map().get(k , "Unknown error")

    def is_replied(self):
        return (self.raw_response is not None)

    def is_ok(self):
        return (self.is_replied() and self.status == "OK")

    def is_error(self):
        return (
            self.status == "ERROR" or
            self.error_code is not None
        )

    def get_full_error_msg(self):
        return "{status} {error_code}: {error_msg}".format(**self.__dict__)

    def get_raw_text(self):
        return self.raw_response.text

    def _get_error_map(self):
        return ERROR_CODES
