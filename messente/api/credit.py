from __future__ import absolute_import

from messente.api import config
from messente.api import api
from messente.api.response import Response


class CreditsResponse(Response):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_balance_value(self):
        if self.is_ok():
            self.get_raw_text().split(" ")[1]


class CreditsAPI(api.API):
    """Documentation: http://messente.com/documentation/credits-api"""

    def __init__(self, **kwargs):
        super().__init__(config_section="credits", **kwargs)

    def get_balance(self, **kwargs):
        r = CreditsResponse(self.call_api("get_balance", **kwargs))
        if not r.is_replied():
            self.log.critical("No response")
        elif not r.is_ok():
            self.log.error(r.get_full_error_msg())
        else:
            self.log.info(r.get_raw_text())
        return r
