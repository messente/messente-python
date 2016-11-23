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
    "ERROR 108": " ".join(["Number is in blacklist."]),
    "ERROR 111": " ".join([
        "Sender parameter 'from' is invalid.",
        "You have not activated this sender name on Messente.com.",
    ]),
    "FAILED 102": " ".join([
        "No delivery report yet, try again in 5 seconds"
    ]),
})


class SmsResponse(Response):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_error_map(self):
        return error_map


class SmsAPI(api.API):
    """Documentation: http://messente.com/documentation/sending-sms"""

    def __init__(self, **kwargs):
        super().__init__(config_section="sms", **kwargs)

    def send(self, validate=True, **kwargs):
        if validate:
            (ok, errors) = self.validate(kwargs)
            if not ok:
                for field in errors:
                    self.log.error("%s: %s", field, errors[field])
                raise InvalidMessageError("Message is invalid")

        r = SmsResponse(self.call_api("send_sms", **kwargs))

        if not r.is_replied():
            self.log.critical("No response")
        elif not r.is_ok():
            self.log.error(r.get_full_error_msg())
        else:
            self.log.info(r.get_raw_text())
        return r

    def send_safe(self, **kwargs):
        """Prevents raising exception on failed validation"""
        try:
            self.send(**kwargs)
        except InvalidMessageError:
            pass
        return None

    def validate(self, data):
        errors = {}
        if "to" not in data:
            errors["to"] = "Required: 'to'"

        content = data.get("text", "")
        if not content:
            errors["text"] = "Required: 'text'/'content'"

        time_to_send = data.get("time_to_send")
        if time_to_send:
            is_positive_int = str(data["time_to_send"]).isdigit()
            if not is_positive_int or not utils.ge_epoch(time_to_send):
                errors["time_to_send"] = "Invalid 'time_to_send'"

        if "validity" in data and not str(data["validity"]).isdigit():
            errors["validity"] = "Invalid 'validity'"

        autoconvert = data.get("autoconvert")
        if autoconvert and autoconvert not in ["on", "off", "full"]:
            errors["autoconvert"] = "Invalid 'autoconvert'"

        udh = data.get("udh")
        if udh and udh not in ["MS", "UE"]:
            errors["udh"] = "Invalid 'udh'"

        mclass = data.get("mclass")
        if mclass and mclass not in [0, 1, 2, 3]:
            errors["mclass"] = "Invalid 'mclass'"

        text_store = data.get("text-store")
        if text_store and text_store not in ["plaintext", "sha256", "nostore"]:
            errors["text-store"] = "Invalid 'text-store'"

        return (not len(errors), errors)
