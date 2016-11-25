# -*- coding: utf-8 -*-

from __future__ import absolute_import

from messente.api import config
from messente.api import api
from messente.api.response import Response


class CreditResponse(Response):
    def __init__(self, *args, **kwargs):
        Response.__init__(self, *args, **kwargs)

    def get_result(self):
        if self.is_ok():
            return self.get_raw_text().split(" ")[1]
        return None


class CreditAPI(api.API):
    """
    Documentation:
    http://messente.com/documentation/tools/credits-api
    """

    def __init__(self, **kwargs):
        api.API.__init__(self, "credit", **kwargs)

    def get_balance(self):
        r = CreditResponse(self.call_api("get_balance"))
        self.log_response(r)
        return r
