import messente
import os
import logging
import time

sms_data = {
    "to": os.environ["TEST_RECIPIENT"],
    "text": "test",
    "time_to_send": int(time.time()) + 10,
}

api = messente.Messente(log_stdout=False)
api.sms.log.setLevel(logging.CRITICAL)

(ok, errors) = api.sms.validate(sms_data)

if ok:
    response = api.sms.send(sms_data)
    sms_id = response.get_sms_id()
    print("Sent:", sms_id)
    response = api.sms.cancel(sms_id)
    print("Cancel:", response.get_result())


try:
    # when trying to send invalid message, an exception is raised
    response = api.sms.send({})
except messente.api.error.InvalidMessageError as e:
    print("Error:", e)

# validation can be turned off in the call to send()
response = api.sms.send({}, validate=False)
print("No validation:", response.get_result())
print("No validation, error message:", response.get_full_error_msg())
