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

    def _get_error_map(self):
        return error_map

    def get_result(self):
        return self.status_text


class DeliveryAPI(api.API):
    """
    Documentation:
    http://messente.com/documentation/sms-messaging/delivery-report
    """

    def __init__(self, **kwargs):
        super().__init__("delivery", **kwargs)

    def get_dlr_response(self, sms_id):
        r = DeliveryResponse(
            self.call_api("get_dlr_response", sms_unique_id=sms_id)
        )
        self.log_response(r)
        return r

    def get_report(self, sms_id):
        return self.get_dlr_response(sms_id)
