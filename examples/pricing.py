# -*- coding: utf-8 -*-

import messente
import tempfile
import json

api = messente.Messente()

# Fetch prices for country
response = api.pricing.get_country_prices("ee")
if response.is_ok():
    print(json.loads(response.get_result()))

# Fetch whole pricelist
response = api.pricing.get_pricelist()
if response.is_ok():
    print(response.get_result())

# Save whole pricelist in a file
(_, filename) = tempfile.mkstemp()
response = api.pricing.get_pricelist(filename)
if response.is_ok():
    print("Pricelist saved in:", filename)
