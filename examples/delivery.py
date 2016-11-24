import messente

api = messente.Messente(username="api_user", password="api_password")
response = api.sms.send(dict(to="+XXXxxxxxxxxx", text="test"))
sms_id = response.get_sms_id()
response = api.delivery.get_dlr_response(sms_id)
print(response.get_result())
