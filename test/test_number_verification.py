import responses

from test import utils

from messente.api import number_verification
from messente.api import Response
from messente.api.error import ConfigurationError


api = number_verification.NumberVerificationAPI(
    user="test",
    password="test",
    urls=utils.TEST_URL
)


@responses.activate
def test_invalid_credentials():
    responses.add_callback(
        responses.GET, utils.TEST_ANY_URL,
        callback=utils.mock_response(200, "ERROR 101"),
    )

    r = api.verify_start({}, validate=False)
    assert r.status == "ERROR"
    assert r.error_code == 101
    assert r.error_msg


@responses.activate
def test_verify_start():
    value = "abcdef"
    text = "OK %s" % value
    responses.add_callback(
        responses.GET, utils.TEST_ANY_URL,
        callback=utils.mock_response(200, text),
    )

    r = api.verify_start(dict(to="+37212345678"))

    assert isinstance(r, Response)
    assert isinstance(r, number_verification.NumberVerificationResponse)

    assert r.error_code is None
    assert r.error_msg == ""
    assert r.status == "OK"
    assert r.get_raw_text() == text
    assert r.get_result() == str(value)


@responses.activate
def test_server_failure():
    text = "FAILED 209"
    responses.add_callback(
        responses.GET, utils.TEST_ANY_URL,
        callback=utils.mock_response(200, text),
    )

    r = api.verify_start(dict(to="+37212345678"))

    assert isinstance(r, Response)
    assert isinstance(r, number_verification.NumberVerificationResponse)

    assert r.error_code is 209
    assert r.error_msg
    assert r.status == "FAILED"
    assert r.get_raw_text() == text
    assert r.get_result() == ""

