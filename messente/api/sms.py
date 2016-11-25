from __future__ import absolute_import

from messente.api import config
from messente.api import api
from messente.api import utils
from messente.api.response import Response
from messente.api.error import InvalidMessageError
from messente.api.error import ERROR_CODES


sms_error_map = ERROR_CODES.copy()
sms_error_map.update({
    "ERROR 104": " ".join([
        "Destination country for this number was not found."
    ]),
    "ERROR 105": " ".join([
        "No such country or area code or invalid phone number format."
    ]),
    "ERROR 106": " ".join(["Destination country is not supported."]),
    "ERROR 107": " ".join(["Not enough credit on account."]),
    "ERROR 108": " ".join(["Number is blacklisted."]),
    "ERROR 111": " ".join([
        "Sender parameter 'from' is invalid.",
        "You have not activated this sender name on Messente.com.",
    ]),
})

cancel_sms_error_map = ERROR_CODES.copy()
cancel_sms_error_map.update({
    "ERROR 107": "Could not find message with provided message ID."
})


class SmsResponse(Response):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_error_map(self):
        return sms_error_map

    def get_sms_id(self):
        if self.is_ok():
            return self.get_raw_text().split(" ")[1]
        return None


class CancelSmsResponse(Response):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_error_map(self):
        return cancel_sms_error_map


class SmsAPI(api.API):
    """
    Documentation:
    http://messente.com/documentation/sending-sms
    """

    def __init__(self, **kwargs):
        super().__init__("sms", **kwargs)

    def send(self, data, **kwargs):
        if kwargs.pop("validate", True):
            self.validate(data, fatal=True)

        r = SmsResponse(self.call_api("send_sms", **data))
        self.log_response(r)
        return r

    def cancel(self, sms_id):
        r = CancelSmsResponse(self.call_api("cancel_sms", sms_unique_id=sms_id))
        self.log_response(r)
        return r

    def _validate(self, data, **kwargs):
        errors = {}

        if not data.get("to", ""):
            self.set_error_required(errors, "to")

        if not data.get("text", ""):
            self.set_error_required(errors, "text")

        time_to_send = data.get("time_to_send", None)
        if time_to_send is not None:
            is_int = utils.is_int(time_to_send)
            if not is_int or not utils.ge_epoch(int(time_to_send)):
                self.set_error(errors, "time_to_send")

        validity = data.get("validity", None)
        if validity is not None and not str(validity).isdigit():
            self.set_error(errors, "validity")

        autoconvert = data.get("autoconvert", None)
        if autoconvert is not None and autoconvert not in ["on", "off", "full"]:
            self.set_error(errors, "autoconvert")

        udh = data.get("udh", None)
        if udh is not None and udh not in ["MS", "UE"]:
            self.set_error(errors, "udh")

        mclass = data.get("mclass", None)
        if mclass is not None and mclass not in [0, 1, 2, 3]:
            self.set_error(errors, "mclass")

        text_store = data.get("text-store", None)
        isset = text_store is not None
        if isset and text_store not in ["plaintext", "sha256", "nostore"]:
            self.set_error(errors, "text-store")

        return (not len(errors), errors)
