import messente

api = messente.Messente(ini_path="config.ini")
print(api.credit.get_balance())

sms_data = dict(
    # to="+372xxxxxxxx",
    text="api test utf8 zażółć gęślą jaźń",
)

# validation example
(ok, errors) = api.sms.validate(sms_data)

# sending message (may raise InvalidMessageError)
response = api.sms.send(sms_data)
print(response.get_full_error_msg())
print(response.get_raw_text())
