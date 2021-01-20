# -*- coding: utf-8 -*-

from messente.api.sms import Messente

api = Messente(username="user", password="password")
api.sms.send(dict(to="+XXXxxxxxxxxx", text="test"))
