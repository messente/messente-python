import responses

from test import utils

from messente.api import sms
from messente.api.error import ConfigurationError


api = sms.SmsAPI(
    user="test",
    password="test",
    api_url=utils.TEST_URL,
)

sms_data = {
    "to": "+372123456789",
    "text": "test"
}


def test_invalid_config_path():
    raised = False
    try:
        sms.SmsAPI(
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

    r = api.send(sms_data, validate=False)
    assert isinstance(r, sms.Response)
    assert isinstance(r, sms.SmsResponse)
    assert r.status == "ERROR"
    assert r.error_code == 101
    assert r.error_msg


# @responses.activate
# def test_send():
#     sms_id = "sms-001"
#     text = "OK %s" % sms_id
#     responses.add_callback(
#         responses.GET, utils.ANY_URL,
#         callback=utils.mock_response(200, text),
#     )

#     r = api.get_balance()

#     assert isinstance(r, sms.Response)
#     assert isinstance(r, sms.SmsResponse)

#     assert r.error_code is None
#     assert r.error_msg == ""
#     assert r.status == "OK"
#     assert r.get_raw_text() == text
#     assert r.get_sms_id() == sms_id
