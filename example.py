import messente

api = messente.Messente(
#    username="username",
#    password="pass",
    ini_path="config.ini",
)

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

# send_safe returns None if message is invalid
# response = api.sms.send_safe(**sms_data)
