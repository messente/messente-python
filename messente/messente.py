from __future__ import absolute_import
import os

from . import api


class Messente(object):
    def __init__(self, **kwargs):
        if "ini_path" in kwargs:
            api.config.load(kwargs.pop("ini_path"))
        self.sms = api.sms.SmsAPI()
        self.credit = api.credit.CreditsAPI()
