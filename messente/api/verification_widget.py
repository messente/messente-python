from __future__ import absolute_import

import hashlib
from messente.api import api


class VerificationWidgetAPI(api.API):
    """Documentation: http://messente.com/documentation/verification-widget"""

    def __init__(self, **kwargs):
        super().__init__("verification-widget", **kwargs)

    def calculate_signature(self, data):
        plain = "".join(map(lambda k: (k) + str(data[k]), sorted(data)))
        return hashlib.md5(plain.encode("utf8")).hexdigest()

    def verify_signature(self, signature, data):
        return (signature == self.calculate_signature(data))

    def _validate(self, data, **kwargs):
        errors = {}
        url = data.get("callback_url", None)
        if not url:
            self.set_error_required(errors, "callback_url")
        elif not isinstance(url, str):
            self.set_error(errors, "callback_url")

        version = data.get("version", None)
        if version is None or not str(version).isnumeric():
            self.set_error(errors, "version")

        return (not len(errors), errors)
