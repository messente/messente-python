from __future__ import absolute_import
import json

from messente.api import config
from messente.api import api
from messente.api.response import Response
from messente.api.error import ApiError
from messente.api.error import ERROR_CODES


error_map = ERROR_CODES.copy()
error_map.update({
    "ERROR 104": "Country was not found.",
    "ERROR 105": "This country is not supported",
    "ERROR 106": "Invalid format provided. Only json or xml is allowed."
})


class PricingResponse(Response):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_error_map(self):
        return error_map

    def get_result(self):
        if self.is_ok():
            content_type = self.raw_response.headers.get("Content-type", "")
            if "text/csv" in content_type or "xml" in content_type:
                return self.get_raw_text()
            elif "json" in content_type:
                return json.loads(self.get_raw_text())
        return None


class PricingAPI(api.API):
    """https://messente.com/documentation/tools/pricing-api"""

    def __init__(self, **kwargs):
        super().__init__("pricing", **kwargs)

    def get_country_prices(self, country_code, **kwargs):
        response_format = kwargs.pop("format", "json")
        if response_format not in ["json", "xml"]:
            raise ApiError(
                "Invalid response_format requested: %s" % response_format
            )
        r = PricingResponse(
            self.call_api(
                "prices",
                country=country_code,
                format=response_format,
            )
        )
        self.log_response(r)
        return r

    def get_pricelist(self):
        r = PricingResponse(self.call_api("pricelist"))
        self.log_response(r)
        return r
