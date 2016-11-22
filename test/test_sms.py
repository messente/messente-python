import unittest

from messente import sms


class test_sms_api(unittest.TestCase):
    def test_init(self):
        sms_api = sms.SmsAPI(
            user="test",
            password="test",
            url="https://api2.messente.com"
        )
        # print(sms_api.get_url())
