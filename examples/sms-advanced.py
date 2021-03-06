# -*- coding: utf-8 -*-

from messente.api.sms import Messente
from messente.api.sms.api.error import InvalidMessageError

import sys
import time

# process input parameters
if len(sys.argv) < 3:
    print("Usage: %s PHONE_NO TEXT [DELAY]" % sys.argv[0])
    sys.exit(1)

delay = 0
if len(sys.argv) == 4:
    delay = int(sys.argv[3])

sms_data = {
    "to": sys.argv[1],
    "text": sys.argv[2],
}

if delay:
    sms_data.update({"time_to_send": int(time.time()) + delay})

# process sms
api = Messente()

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


# Validation examples
print("# Validation")
try:
    # when trying to send invalid message, an exception is raised
    response = api.sms.send({})
except InvalidMessageError as e:
    print("Validation Error:", e)

print("# Disabled validation")
# validation can be turned off in the call to send()
response = api.sms.send({}, validate=False)
print("No validation:", response.get_result())
print("No validation, error message:", response.get_full_error_msg())
