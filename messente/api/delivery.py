from __future__ import absolute_import

from messente.api import config
from messente.api import api
from messente.api.response import Response
from messente.api.error import ERROR_CODES


error_map = ERROR_CODES.copy()
error_map.update({
    "FAILED 102": " ".join([
        "No delivery report yet, try again in 5 seconds"
    ]),
})


class DeliveryResponse(Response):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_delivery_status(self):
        if self.is_ok():
            return self.get_raw_text().split(" ")[1]
        return None


class DeliveryAPI(api.API):
    """Documentation: http://messente.com/documentation/delivery-report"""

    def __init__(self, **kwargs):
        super().__init__(config_section="delivery", **kwargs)

    def get_dlr_response(self, sms_id):
        r = DeliveryResponse(
            self.call_api("get_dlr_response", sms_unique_id=sms_id)
        )
        if not r.is_replied():
            self.log.critical("No response")
        elif not r.is_ok():
            self.log.error(r.get_full_error_msg())
        else:
            self.log.debug(r.get_raw_text())
        return r

    def get_report(self, sms_id):
        return self.get_dlr_response(sms_id)
