# -*- coding: utf-8 -*-

import messente

api = messente.Messente()

response = api.credit.get_balance()
if response.is_ok():
    print("Account balance:", response.get_result())
else:
    print(response.get_full_error_msg())
