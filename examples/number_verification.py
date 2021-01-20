# -*- coding: utf-8 -*-

from messente.api.sms import Messente
import sys

api = Messente(username="api_user", password="api_password")

if len(sys.argv) == 2:
    to = sys.argv[1]
    print("# Sending pin to:", to)
    response = api.number_verification.send_pin(dict(
        to=to,
        max_tries=1,
        retry_delay=30,  # seconds
        validity=(5 * 60),  # seconds
        template="Example: your pin code is: <PIN>"
    ))
    print("Verification ID:", response.get_verification_id())
elif len(sys.argv) == 3:
    verification_id = sys.argv[1]
    pin = sys.argv[2]
    print("# Verifying pin")
    response = api.number_verification.verify_pin(dict(
        pin=pin,
        verification_id=verification_id
    ))

    print("Result:", response.get_result())
    print("VERIFIED:\t", response.is_verified())
    print("EXPIRED:\t", response.is_expired())
    print("THROTTLED:\t", response.is_throttled())
    print("INVALID:\t", response.is_invalid())
else:
    print("Usage:")
    print("1. Sending pin code")
    print(sys.argv[0], "+XXXxxxxx")
    print("")
    print("2. Verifying pin code")
    print(sys.argv[0], "VERIFICATION_ID PIN")
