# import unittest
import responses
from messente.api import credit
from test import utils


api = credit.CreditsAPI(
    user="test",
    password="test",
    api_url=utils.TEST_URL
)


@responses.activate
def test_invalid_credentials():
    responses.add_callback(
        responses.GET, utils.ANY_URL,
        callback=utils.mock_response(200, "ERROR 101"),
    )

    r = api.get_balance()
    assert r.status == "ERROR"
    assert r.error_code == 101


@responses.activate
def test_get_balance():
    value = "OK 123.45678"
    responses.add_callback(
        responses.GET, utils.ANY_URL,
        callback=utils.mock_response(200, value),
    )

    r = api.get_balance()

    assert isinstance(r, credit.Response)
    assert isinstance(r, credit.CreditsResponse)

    assert r.error_code is None
    assert r.error_msg == ""
    assert r.status == "OK"
    assert r.get_raw_text() == value


@responses.activate
def test_server_failure():
    value = "FAILED 209"
    responses.add_callback(
        responses.GET, utils.ANY_URL,
        callback=utils.mock_response(200, value),
    )

    r = api.get_balance()

    assert isinstance(r, credit.Response)
    assert isinstance(r, credit.CreditsResponse)

    assert r.error_code == 209
    assert r.status == "FAILED"
    assert r.error_msg
    assert r.get_raw_text() == value
