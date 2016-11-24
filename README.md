# messente-python

Python API supporting Messente.com services.
See: http://messente.com/documentation

Modules:
- sms (SmsAPI)
- delivery (DeliveryAPI)
- credit (CreditsAPI)
- pricing (PricingAPI)
- number_verification / pin codes (NumberVerificationAPI) 


## Examples

You can find sample scripts in the 'examples' directory.

### SmsAPI

#### Basic example

```python
	import messente

	api = messente.Messente(username="user", password="password")
	api.sms.send(dict(to="+XXXxxxxxxxxx", text="test"))

```

#### Advanced example

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


### NumberVerificationAPI

Sending ping code to a number:

```python
    api = messente.Messente()
    response = api.number_verification.send_pin(dict(
        to=to,
        max_tries=3,
        retry_delay=30,  # seconds
        validity=(5 * 60),  # seconds
        template="Your pin code is: <PIN>"
    ))
    print("Verification ID:", response.get_verification_id())
```

Once the verification_id is obtained, use it together with the PIN code
to obtain verification status.

Verifying PIN code:

```python
	api = messente.Messente()
    response = api.number_verification.verify_pin(dict(
        pin=pin,
        verification_id=verification_id
	))
		
    print("Result:", response.get_result())
    print("VERIFIED:\t", response.is_verified())
    print("EXPIRED:\t", response.is_expired())
    print("THROTTLED:\t", response.is_throttled())
    print("INVALID:\t", response.is_invalid())		
```


## Configuration parameters

Configuration parameters can passed via:
- keyword arguments in constructor
- configuration file (*.ini)

Authentication parameters can also be set in environment instead:
- **MESSENTE_API_USERNAME**
- **MESSENTE_API_PASSWORD**



## Running unittests tests

To run all the unit tests, simply execute:
```nosetests -v```
