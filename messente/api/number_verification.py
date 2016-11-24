from __future__ import absolute_import


from messente.api import config
from messente.api import api
from messente.api.response import Response
from messente.api.error import ApiError
from messente.api.error import ERROR_CODES
from messente.api import utils


error_map = ERROR_CODES.copy()

error_map.update({
    "ERROR 111": " ".join([
        "Sender parameter 'from' is invalid."
        "You have not activated this sender name from Messente.com"
    ]),
    "ERROR 109": "PIN code field is missing in the template value."
})


class NumberVerificationResponse(Response):
    _VERIFIED_STATUS = "VERIFIED"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_error_map(self):
        return error_map

    def _parse(self):
        if self.raw_response.text.strip() == self._VERIFIED_STATUS:
            self.status = self._VERIFIED_STATUS
        else:
            super()._parse()

    def is_ok(self):
        return (
            self.is_replied() and
            self.status in ["OK", self._VERIFIED_STATUS]
        )

    def get_result(self):
        return self.status_text

    def is_already_verified(self):
        return (self.status == self._VERIFIED_STATUS)


class NumberVerificationAPI(api.API):
    """https://messente.com/documentation/tools/verification-api"""

    def __init__(self, **kwargs):
        super().__init__("number-verification", **kwargs)

    def verify_start(self, data, **kwargs):
        if kwargs.get("validate", True):
            self.validate(data)
        r = NumberVerificationResponse(
            self.call_api(
                "verify/start",
                **data
            ),
        )
        self.log_response(r)
        return r

    def _validate(self, data):
        errors = {}

        if not data.get("to", ""):
            self.set_error_required(errors, "to")

        template = data.get("template", None)
        if template is not None and "<PIN>" not in str(template):
            self.set_error(errors, "template")

        max_tries = data.get("max_tries", None)
        if max_tries is not None:
            if not str(data["max_tries"]).isdigit() or max_tries < 1:
                self.set_error(errors, "max_tries")

        retry_delay = data.get("retry_delay", None)
        if retry_delay is not None and not str(retry_delay).isdigit():
                self.set_error(errors, "retry_delay")

        validity = data.get("validity", None)
        if validity is not None:
            is_positive_int = str(data["validity"]).isdigit()
            if not is_positive_int or validity > 1800:
                self.set_error(errors, "validity")

        return (not len(errors), errors)
