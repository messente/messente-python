import responses

from test import utils

from messente.api import credit
from messente.api import Response
from messente.api.error import ConfigurationError


api = credit.CreditsAPI(
    user="test",
    password="test",
    api_url=utils.TEST_URL
)


def test_invalid_config_path():
    raised = False
    try:
        credit.CreditsAPI(
            user="test",
            password="test",
            api_url=utils.TEST_URL,
            ini_path="non-existent-and-thus-invalid.ini"
        )
    except ConfigurationError:
        raised = True

    assert raised


@responses.activate
def test_invalid_credentials():
    responses.add_callback(
        responses.GET, utils.ANY_URL,
        callback=utils.mock_response(200, "ERROR 101"),
    )

    r = api.get_balance()
    assert r.status == "ERROR"
    assert r.error_code == 101
    assert r.error_msg


@responses.activate
def test_get_balance():
    value = 123.45678
    text = "OK %s" % value
    responses.add_callback(
        responses.GET, utils.ANY_URL,
        callback=utils.mock_response(200, text),
    )

    r = api.get_balance()

    assert isinstance(r, Response)
    assert isinstance(r, credit.CreditsResponse)

    assert r.error_code is None
    assert r.error_msg == ""
    assert r.status == "OK"
    assert r.get_raw_text() == text
    assert r.get_balance_value() == str(value)


@responses.activate
def test_server_failure():
    value = "FAILED 209"
    responses.add_callback(
        responses.GET, utils.ANY_URL,
        callback=utils.mock_response(200, value),
    )

    r = api.get_balance()

    assert r.error_code == 209
    assert r.status == "FAILED"
    assert r.error_msg
    assert r.get_raw_text() == value
