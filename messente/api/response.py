from __future__ import absolute_import

from messente.api.error import ERROR_CODES


class Response(object):
    def __init__(self, response):
        self.raw_response = response
        self.error_code = None
        self.error_msg = ""
        self.http_status_code = None
        self.status = ""
        self.parse()

    def parse(self):
        if self.raw_response is None:
            return

        self.http_status_code = int(self.raw_response.status_code)
        if self.http_status_code not in [200]:
            return

        is_simple = (
            self.raw_response.text.startswith("OK ") or
            self.raw_response.text.startswith("ERROR ") or
            self.raw_response.text.startswith("FAILED ")
        )

        if is_simple:
            parts = self.raw_response.text.split(" ")
            if parts:
                self.status = parts[0]
                if self.status in ["ERROR", "FAILED"]:
                    self.error_code = int(parts[1])
                    k = self.status + " " + str(self.error_code)
                    self.error_msg = self._get_error_map().get(k , "")
        else:
            self.status = "OK"

    def is_replied(self):
        return (self.http_status_code in [200])

    def is_ok(self):
        return (self.is_replied() and self.status == "OK")

    def is_error(self):
        return (
            self.status in ["ERROR", "FAILED"] or
            self.error_code is not None
        )

    def get_full_error_msg(self):
        return "{status} {error_code}: {error_msg}".format(**self.__dict__)

    def get_raw_text(self):
        return self.raw_response.text

    def get_result(self):
        return self.get_raw_text()

    def _get_error_map(self):
        return ERROR_CODES
