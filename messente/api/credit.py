from __future__ import absolute_import

from messente.api import config
from messente.api import api
from messente.api.response import Response


class CreditResponse(Response):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_balance_value(self):
        if self.is_ok():
            return self.get_raw_text().split(" ")[1]
        return None


class CreditAPI(api.API):
    """Documentation: http://messente.com/documentation/credits-api"""

    def __init__(self, **kwargs):
        super().__init__("credit", **kwargs)

    def get_balance(self):
        r = CreditResponse(self.call_api("get_balance"))
        self.log_response(r)
        return r
