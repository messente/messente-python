import responses
import json

from test import utils

from messente.api import pricing
from messente.api import Response


fake_response = json.dumps({
    "country": "EE",
    "name": "Estonia",
    "prefix": "372",
    "networks": [
        {"mccmnc": "24803", "name": "Tele2", "price": "0.00000"},
        {"mccmnc": "24802", "name": "Elisa", "price": "0.00000"},
        {"mccmnc": "24801", "name": "EMT", "price": "0.00000"}
    ]
})


@responses.activate
def test_get_coutry_prices():
    responses.add_callback(
        responses.GET, utils.TEST_ANY_URL,
        callback=utils.mock_response(200, fake_response),
    )

    api = pricing.PricingAPI(api_url=utils.TEST_URL)
    r = api.get_country_prices("EE")
    assert isinstance(r, Response)
    assert isinstance(r, pricing.PricingResponse)
    assert r.is_ok()
    assert (json.loads(r.get_result()).get("networks")[1]["name"] == "Elisa")

    r = api.get_country_prices("EE", format="xml")
    # only test if ok - only json is mocked
    assert r.is_ok()


@responses.activate
def test_get_pricelist():
    responses.add_callback(
        responses.GET, utils.TEST_ANY_URL,
        callback=utils.mock_response(200, fake_response, headers={
            "Content-type": "text/csv;charset=UTF-8"
        }),
    )

    api = pricing.PricingAPI(api_url=utils.TEST_URL)
    r = api.get_pricelist()
    assert isinstance(r, Response)
    assert isinstance(r, pricing.PricingResponse)
    assert r.is_ok()
    assert len(r.get_result())

    r = api.get_country_prices("EE", format="xml")
    # only test if ok - only json is mocked
    assert r.is_ok()
