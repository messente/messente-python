from __future__ import absolute_import

from messente.api import config
from messente.api import api
from messente.api.response import Response


class CreditsAPI(api.API):
    """Documentation: http://messente.com/documentation/credits-api"""

    def __init__(self, **kwargs):
        super().__init__(config_section="credits", **kwargs)

    def get_balance(self, **kwargs):
        r = Response(self.call_api(**kwargs))
        if not r.is_replied():
            self.log.critical("No response")
        elif not r.is_ok():
            self.log.error(r.get_full_error_msg())
        else:
            self.log.info(r.get_raw_text())
        return r.get_raw_text().split(" ")[1]
