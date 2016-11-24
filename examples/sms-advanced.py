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
logging.disable(logging.ERROR)
api.sms.log.setLevel(logging.CRITICAL)

(ok, errors) = api.sms.validate(sms_data)

if ok:
    print("# Sending")
    response = api.sms.send(sms_data)
    sms_id = response.get_sms_id()
    print("Sent:", sms_id)

    print("# Delivery")
    response = api.delivery.get_dlr_response(sms_id)
    print("Delivery:", response.get_result())
    print("Delivery error message:", response.get_full_error_msg())

    print("# Cancellation")
    response = api.sms.cancel(sms_id)
    print("Cancel:", response.get_result())


print("# Validation")
try:
    # when trying to send invalid message, an exception is raised
    response = api.sms.send({})
except messente.api.error.InvalidMessageError as e:
    print("Validation Error:", e)

print("# Disabled validation")
# validation can be turned off in the call to send()
response = api.sms.send({}, validate=False)
print("No validation:", response.get_result())
print("No validation, error message:", response.get_full_error_msg())
