from __future__ import absolute_import
import os

from messente import api


class Messente(object):
    def __init__(self, **kwargs):
        if kwargs.get("ini_path", ""):
            api.config.load(kwargs.pop("ini_path"))
        # modules
        self.sms = api.sms.SmsAPI()
        self.credit = api.credit.CreditsAPI()
        self.delivery = api.delivery.DeliveryAPI()
