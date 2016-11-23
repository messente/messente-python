import responses

from test import utils

from messente.api import sms
from messente.api import Response
from messente.api.error import ConfigurationError
from messente.api.error import InvalidMessageError


api = sms.SmsAPI(
    user="test",
    password="test",
    api_url=utils.TEST_URL,
)


def mk_sms_data(data=None):
    sms_data = {
        "to": "+372123456789",
        "text": "test"
    }
    sms_data.update(data or {})
    return sms_data


@responses.activate
def test_invalid_credentials():
    responses.add_callback(
        responses.GET, utils.ANY_URL,
        callback=utils.mock_response(200, "ERROR 101"),
    )

    r = api.send(mk_sms_data(), validate=False)
    assert isinstance(r, Response)
    assert isinstance(r, sms.SmsResponse)
    assert r.status == "ERROR"
    assert r.error_code == 101
    assert r.error_msg


@responses.activate
def test_send():
    sms_id = "sms-001"
    text = "OK %s" % sms_id
    responses.add_callback(
        responses.GET, utils.ANY_URL,
        callback=utils.mock_response(200, text),
    )

    r = api.send(mk_sms_data())

    assert r.error_code is None
    assert r.error_msg == ""
    assert r.status == "OK"
    assert r.get_raw_text() == text
    assert r.get_sms_id() == sms_id


def test_send_invalid():
    raised = False
    try:
        r = api.send({})
    except InvalidMessageError:
        raised = True
    assert raised


@responses.activate
def test_send_no_validate():
    sms_id = "sms-001"
    text = "OK %s" % sms_id
    responses.add_callback(
        responses.GET, utils.ANY_URL,
        callback=utils.mock_response(200, text),
    )

    r = api.send({}, validate=False)
    # OK if no exception was raised
    assert True

