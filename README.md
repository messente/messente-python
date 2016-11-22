# messente-python

Python API supporting Messente.com services.

Modules:
- credits
- sms


## Configuration parameters

Configuration parameters can passed as:
- keyword arguments, when instantiating api module, e.g.

```
import messente
api = messente.Messente(
    username="me",
    password="xxx",
	api_url="https://xxx",
	ini_path="config.ini"
)

```
or they can be read from *.ini configuration file pointed by "ini_path" keyword argument.

Some parameters can be passed as environment variables:
- MESSENTE_API_URL (defaults to https://api2.messente.com)
- MESSENTE_API_USERNAME
- MESSENTE_API_PASSWORD
