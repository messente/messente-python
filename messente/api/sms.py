from __future__ import absolute_import

from messente.api import config
from messente.api import api
from messente.api import utils
from messente.api.response import Response
from messente.api.error import InvalidMessageError
from messente.api.error import ERROR_CODES


error_map = ERROR_CODES.copy()
error_map.update({
    "ERROR 103": " ".join([
        "Invalid IP address.",
        "The IP address you made the request from,",
        "is not in the API whitelist settings.",
    ]),
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


class SmsResponse(Response):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_error_map(self):
        return error_map

    def get_sms_id(self):
        if self.is_ok():
            return self.get_raw_text().split(" ")[1]
        return None


class SmsAPI(api.API):
    """Documentation: http://messente.com/documentation/sending-sms"""

    def __init__(self, **kwargs):
        super().__init__(config_section="sms", **kwargs)

    def send(self, data, **kwargs):
        if kwargs.get("validate", True):
            (ok, errors) = self.validate(data)
            if not ok:
                for field in errors:
                    self.log.error("%s: %s", field, errors[field])
                    raise InvalidMessageError("Message is invalid")

        r = SmsResponse(self.call_api("send_sms", **data))

        if not r.is_replied():
            self.log.critical("No response")
        elif not r.is_ok():
            self.log.error(r.get_full_error_msg())
        else:
            self.log.debug(r.get_raw_text())
        return r

    def validate(self, data):
        errors = {}
        to = data.get("to", "")
        if not to:
            errors["to"] = "Required: 'to'"

        text = data.get("text", "")
        if not text:
            errors["text"] = "Required: 'text'"

        time_to_send = data.get("time_to_send", None)
        if time_to_send is not None:
            is_int = utils.is_int(time_to_send)
            if not is_int or not utils.ge_epoch(int(time_to_send)):
                errors["time_to_send"] = "Invalid 'time_to_send'"

        validity = data.get("validity", None)
        if validity is not None and not str(data["validity"]).isdigit():
            errors["validity"] = "Invalid 'validity'"

        autoconvert = data.get("autoconvert", None)
        if autoconvert is not None and autoconvert not in ["on", "off", "full"]:
            errors["autoconvert"] = "Invalid 'autoconvert'"

        udh = data.get("udh", None)
        if udh is not None and udh not in ["MS", "UE"]:
            errors["udh"] = "Invalid 'udh'"

        mclass = data.get("mclass", None)
        if mclass is not None and mclass not in [0, 1, 2, 3]:
            errors["mclass"] = "Invalid 'mclass'"

        text_store = data.get("text-store", None)
        isset = text_store is not None
        if isset and text_store not in ["plaintext", "sha256", "nostore"]:
            errors["text-store"] = "Invalid 'text-store'"

        return (not len(errors), errors)
