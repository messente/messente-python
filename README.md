# messente-python

Python API supporting Messente.com services.

Modules:
- sms (SmsAPI)
- credit (CreditsAPI)
- number_verification (NumberVerificationAPI)
- pricing (PricingAPI)


## Configuration parameters

Configuration parameters can passed via:
- keyword arguments in constructor
- configuration file (*.ini)

Authentication parameters can be set in environment as:
*MESSENTE_API_USERNAME* and *MESSENTE_API_PASSWORD*

## Examples



### SmsAPI

The most basic and straightforward code to send a sms is

```python
import messente

api = messente.Messente(username="user", password="password")
api.sms.send(dict(to="+XXXxxxxxxxxx", text="test"))

```

A little more advanced example including validation, error handling
and cancelling a message can be demonstrated as:

```python
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

```


### CreditsAPI

```python
import messente

api = messente.Messente(username="me", password="xxxxx")
response = api.credit.get_balance()
if response.is_ok():
    print("Account balance:", response.get_result())
else:
    print(response.get_full_error_msg())

```

### PricingAPI

```python
import messente
import tempfile
import json

api = messente.Messente()

# Fetch prices for country
response = api.pricing.get_country_prices("ee")
if response.is_ok():
    print(json.loads(response.get_result()))

# Fetch full pricelist
response = api.pricing.get_pricelist()
if response.is_ok():
    print(response.get_result())

# Save pricelist to a file
(_, filename) = tempfile.mkstemp()
response = api.pricing.get_pricelist(filename)
if response.is_ok():
    print("Pricelist saved in:", filename)
```
