from __future__ import absolute_import
import os

from messente import api


class Messente(object):
    def __init__(self, **kwargs):
        if kwargs.get("ini_path", ""):
            api.config.load(kwargs.pop("ini_path"))
        # modules
        self.sms = api.sms.SmsAPI(**kwargs)
        self.credit = api.credit.CreditAPI(**kwargs)
        self.delivery = api.delivery.DeliveryAPI(**kwargs)
        self.pricing = api.pricing.PricingAPI(**kwargs)
        self.number_verification = (
            api.number_verification.NumberVerificationAPI(**kwargs)
        )
        self.verification_widget = (
            api.verification_widget.VerificationWidgetAPI(**kwargs)
        )
