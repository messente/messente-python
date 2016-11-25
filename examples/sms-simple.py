# -*- coding: utf-8 -*-

import messente

api = messente.Messente(username="user", password="password")
api.sms.send(dict(to="+XXXxxxxxxxxx", text="test"))
